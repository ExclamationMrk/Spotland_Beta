import pygame
import tool_code
import tile_code
import tile_occupants_code
from time import sleep
from random import randint

def initialisation_function(self, type, starting_tile_width, playerself):
    if type == "toadstool":
        self.strength = 2
        if randint(0, 1) == 1:
            self.can_be_scared = False
        self.name = "Toadstool Mycelian"
        self.image = "images\entities\mushrooms\mycelian_toadstool_profile.png"
        self.loaded_image = pygame.image.load(self.image)
        
    elif type == "oyster":
        self.strength = 2
        self.health *= .8
        self.sight_range *= 1.5
        self.tool_use_cooldown = 5
        self.name = "Oyster Mycelian"
        self.image = "images\entities\mushrooms\mycelian_oyster_profile.png"
        self.loaded_image = pygame.image.load(self.image)
        
    elif type == "psilocybe":
        self.health *= .6
        self.tool_use_cooldown = 5
        self.can_be_scared = False
        self.name = "Psilocybe Mycelian"
        self.image = "images\entities\mushrooms\mycelian_psilocybe_profile.png"
        self.loaded_image = pygame.image.load(self.image)
    
    elif type == "portobello":
        self.strength = 4
        self.movement_cooldown = 4
        self.tool_use_cooldown = 7
        self.can_be_scared = False
        self.health *= 2
        self.name = "Portobello Mycelian"
        self.image = "images\entities\mushrooms\mycelian_portobello_profile.png"
        self.loaded_image = pygame.image.load(self.image)
        
    elif type == "morel":
        self.health *= .5
        self.movement_cooldown = 1
        self.tool_use_cooldown = 3
        self.name = "Morel Mycelian"
        self.image = "images\entities\mushrooms\mycelian_morel_profile.png"
        self.loaded_image = pygame.image.load(self.image)
        
    else:
        self.name = "Toadstool Mycelian"
        self.image = "images\entities\mushrooms\mycelian_toadstool_profile.png"
        self.loaded_image = pygame.image.load(self.image)

    self.health += round((self.health * .1) * playerself.level, 1)
    self.strength += round((self.strength *.1) * playerself.level, 1)
    self.max_health = round(self.health, 1)

class MushroomTemplate:
    def __init__(self, mushroom_type: str, starting_pos: list[int, int], starting_tile_width: list[int, int], owner: str, playerself, enemy=False):
        self.is_enemy = enemy
        self.health = randint(9, 11)
        self.max_health = self.health
        self.position = starting_pos
        self.can_be_scared = True
        self.home = starting_pos
        self.strength = 1.0
        self.mode = "active"
        self.image = ""
        self.loaded_image = ""
        self.loaded_boat_image = pygame.image.load("images\entities\mushrooms\mycelian_ship.png")
        self.focus = "gathering"
        self.target_id = ""
        self.target_position = [0, 0]
        self.tool_pos_offset = [0, 0]
        self.current_path = []
        self.is_moving = True
        self.is_floating = False
        self.sight_range = 4
        self.movement_cooldown = 2
        self.movement_cooldown_subtractor = 1
        self.movement_cooldown_timer = 0
        self.tool = tool_code.ToolTemplate("stone_pickaxe")
        self.tool_use_cooldown = 4
        self.tool_use_cooldown_subtractor = 1
        self.tool_use_cooldown_timer = 0
        self.name = ""
        self.in_water = False
        self.type = mushroom_type
        self.owner = owner
        self.selected = False
        self.level = playerself.level
        
        initialisation_function(self=self, type=mushroom_type, starting_tile_width=starting_tile_width, playerself=playerself)
        
    def set_home(self, home_pos: list[int, int]):
        self.home = home_pos
        
    def damage(self, attacker_entity_self, ):
        if attacker_entity_self.tool.attacking == False:
            self.health -= round((attacker_entity_self.strength * attacker_entity_self.tool.damage) / 2, 1)
            
        else:
            self.health -= round(attacker_entity_self.strength * attacker_entity_self.tool.damage, 1)
        
    def use_tool(self, target_tile, surface, offset: list[int, int], viewscale: float, tile_spread, selected=False):
        resources = self.tool.func(self=self.tool, parentself=self, tile_spread=tile_spread, target_tile=target_tile.location)
        
        if "attacking" not in self.focus:
            if resources[1] == True:
                if selected:
                    target_tile.blit(surface, offset, viewscale, tile_spread, selected=True)
                    
                else:
                    target_tile.blit(surface, offset, viewscale, tile_spread,)
            
        return resources
    
    def resize(self, tile_width: list[int, int]):
        self.loaded_image = pygame.transform.scale(self.loaded_image, (tile_width[0], tile_width[1]))
        
    def blit(self, surface, offset: list[int, int], tile_dimensions: list[int, int], offset_offset = [0, 0]):
        if self.in_water:
            loaded_image_rect = pygame.transform.scale(self.loaded_image, tile_dimensions).get_rect()
            loaded_ship_image = pygame.transform.scale(self.loaded_boat_image, (loaded_image_rect.width, loaded_image_rect.height))
            surface.blit(loaded_ship_image, ((self.position[0] * tile_dimensions[0]) + (offset[0] + offset_offset[0]), (self.position[1] * tile_dimensions[1]) + (offset[1] + offset_offset[1])))
            
        else:
            surface.blit(pygame.transform.scale(self.loaded_image, tile_dimensions), ((self.position[0] * tile_dimensions[0]) + (offset[0] + offset_offset[0]), (self.position[1] * tile_dimensions[1]) + (offset[1] + offset_offset[1])))

            if self.tool.image != "":
                loaded_tool_image = pygame.transform.scale((self.tool.image), (tile_dimensions[0] / 2, tile_dimensions[1] / 2))
                surface.blit(loaded_tool_image, (((self.position[0] + self.tool_pos_offset[0]) * tile_dimensions[0]) + (offset[0] + offset_offset[0]), ((self.position[1] + self.tool_pos_offset[1]) * tile_dimensions[1]) + (offset[1] + offset_offset[1])))
            
    def get_walkable_tiles(self, tile_spread, position):
        neighbors = tile_spread[position[1]][position[0]].neighbors
        valid_directions = {}
        
        for direction, pos in neighbors.items():
            if pos != None:
                test = True
                for occupant in tile_spread[pos[1]][pos[0]].tile_occupants:
                    if occupant.walkable or self.is_floating:
                        pass
                    
                    else:
                        test = False
                        
                if test and tile_spread[pos[1]][pos[0]].entity_occupied == False:
                    valid_directions[direction] = pos
                    
        return valid_directions
        
    def set_focus_and_target(self, new_focus="", new_target_id=""):        
        if self.focus == "selected":
            self.current_path = []
            
        elif self.focus == "":
            pass
        
        elif new_focus != self.focus:
            self.current_path = []
            
        else:
            pass
        
        if new_focus == "":
            pass
        
        else:
            self.focus = new_focus
            
        if new_target_id == "":
            pass
        
        else:
            self.target_id = new_target_id
                
    def get_tiles_within_view(self, tile_spread):
        distance_looked = 0
        tiles_within_view = [self.position]
        while distance_looked < self.sight_range:
            new_tiles = []
            for tile in tiles_within_view:
                if distance_looked >= self.sight_range:
                    break
                
                neighbors = list(tile_spread[tile[1]][tile[0]].neighbors.values())
                for neighbor in neighbors:
                    if neighbor != None and neighbor not in tiles_within_view and neighbor not in new_tiles:
                        new_tiles.append(neighbor)
                        
            for tile in new_tiles:
                tiles_within_view.append(tile)
                
            distance_looked += 1
        
        return tiles_within_view
    
    def get_target_tile_occupant_within_range(self, tile_spread):
        if self.focus == "targeted":
            tiles_with_target = []
            tiles_in_view = self.get_tiles_within_view(tile_spread)
            for tile in tiles_in_view:
                for occupant in tile_spread[tile[1]][tile[0]].tile_occupants:
                    if occupant.occupant_id == self.target_id:
                        tiles_with_target.append(tile)
                            
            return tiles_with_target
        
        elif self.focus == "gathering":
            tiles_with_target = []
            tiles_in_view = self.get_tiles_within_view(tile_spread)
            for tile in tiles_in_view:
                for occupant in tile_spread[tile[1]][tile[0]].tile_occupants:
                    if (occupant.tool_needed == self.tool.type or occupant.tool_needed == None) and occupant.natural == True:
                        tiles_with_target.append(tile)
                            
            return tiles_with_target
        
        elif self.focus == "attacking":
            tiles_with_target = []
            tiles_in_view = self.get_tiles_within_view(tile_spread)
            for tile in tiles_in_view:
                if tile_spread[tile[1]][tile[0]].enemy_occupied:
                    tiles_with_target.append(tile)
                            
            return tiles_with_target
        
        elif self.focus == "inverse_attacking":
            tiles_with_target = []
            tiles_in_view = self.get_tiles_within_view(tile_spread)
            for tile in tiles_in_view:
                if tile_spread[tile[1]][tile[0]].enemy_occupied == False and tile_spread[tile[1]][tile[0]].entity_occupied:
                    tiles_with_target.append(tile)
                            
            return tiles_with_target
        
        elif self.focus == "trailing":
            tiles_with_target = []
            tiles_in_view = self.get_tiles_within_view(tile_spread)
            for tile in tiles_in_view:
                if tile_spread[tile[1]][tile[0]].enemy_occupied == False and tile_spread[tile[1]][tile[0]].entity_occupied:
                    tiles_with_target.append(tile)
                            
            return tiles_with_target
            
        elif self.focus == "stay":
            return [self.position]
            
        else:
            return [self.position]
             
    def get_pathfinding_costs(self, tile_position):
        return [(abs(self.position[0] - tile_position[0]) + abs(self.position[0] - tile_position[0])), (abs(tile_position[0] - self.target_position[0]) + abs(tile_position[0] - self.target_position[0]))]
        
    def set_target_position_on_focus(self, selected_tiles, playerself, enemyself, tile_spread):
        if self.focus == "selected":
            if selected_tiles == []:
                pass
                
            else:
                if self.focus == "selected":
                    if self.target_position == selected_tiles[0]:
                        pass
                    
                    else:
                        self.target_position = selected_tiles[0]
                        self.current_path = self.pathfinding(tile_spread)
                        
        elif self.focus == "gathering":
            good_tiles = self.get_target_tile_occupant_within_range(tile_spread)
            if good_tiles != []:
                self.target_position = good_tiles[0]
            
            else:
                tiles_in_view = self.get_tiles_within_view(tile_spread)
                self.target_position = tiles_in_view[randint(0, len(tiles_in_view) - 1)]
            
        elif self.focus == "home":
            self.target_position = self.home
            
        elif self.focus == "attacking":
            good_tiles = self.get_target_tile_occupant_within_range(tile_spread)
            if good_tiles != []:
                self.target_position = good_tiles[0]
            
            else:
                tiles_in_view = self.get_tiles_within_view(tile_spread)
                self.target_position = tiles_in_view[randint(0, len(tiles_in_view) - 1)]
                
        elif self.focus == "inverse_attacking":
            good_tiles = self.get_target_tile_occupant_within_range(tile_spread)
            if good_tiles != []:
                self.target_position = good_tiles[0]
            
            else:
                tiles_in_view = self.get_tiles_within_view(tile_spread)
                self.target_position = tiles_in_view[randint(0, len(tiles_in_view) - 1)]
                
        elif self.focus == "stay":
            self.target_position = self.position
        
    def pathfinding(self, tile_spread):
        succeeded = False
        if self.position != self.target_position and len(list(self.get_walkable_tiles(tile_spread, self.position).values())) > 0 and self.target_position not in list(tile_spread[self.position[1]][self.position[0]].neighbors.values()):
            open_tiles = []
            closed_tiles = []
            self.current_path = [] 
            used_positions = []
            
            open_tiles.append({"cost": sum(self.get_pathfinding_costs(self.position)), "position": self.position, "from": None})
            used_positions.append(self.position)
            
            target_position = self.target_position
            while True:
                best_tile = None
                best_tile_index = 0
                for num, tile in enumerate(open_tiles):
                    if best_tile == None:
                        best_tile = tile
                        best_tile_index = num
                        
                    else:
                        if tile["cost"] < best_tile["cost"]:
                            best_tile = tile
                            best_tile_index = num
                            
                if best_tile == None:
                    new_target = None
                    neighbors = list(tile_spread[target_position[1]][target_position[0]].neighbors.values())
                    while new_target == None:
                        new_target = neighbors.pop(randint(0, len(neighbors) - 1))
                        
                    target_position = new_target
                    open_tiles = []
                    closed_tiles = []
                    self.current_path = []
                    used_positions = []
            
                    open_tiles.append({"cost": sum(self.get_pathfinding_costs(self.position)), "position": self.position, "from": None})
                    used_positions.append(self.position)
                    
                    continue
                
                else:
                    closed_tiles.append(open_tiles.pop(best_tile_index))
                    
                    if best_tile["position"] == target_position:
                        succeeded = True
                        break
                    
                    possible_tiles = list(self.get_walkable_tiles(tile_spread, best_tile["position"]).values())
                    for tile in possible_tiles:
                        if tile not in used_positions:
                            cost = sum(self.get_pathfinding_costs(tile))
                            
                            open_tiles.append({"cost": cost, "position": tile, "from": best_tile["position"]})
                            used_positions.append(tile)
                      
        solved_path = []
        
        if succeeded and len(list(self.get_walkable_tiles(tile_spread, self.position).values())) > 0:
            tile_and_origin = {}
            tiles = []
            origins = []
            for tile in closed_tiles:
                x = str(tile["position"][0]) + "x"
                y = str(tile["position"][1]) + "y"
                xy = x + y
                
                tile_and_origin[xy] = tile["from"]
                
            selected_tile = target_position
            
            while self.position not in solved_path:
                solved_path.append(selected_tile)
                
                x = str(selected_tile[0]) + "x"
                y = str(selected_tile[1]) + "y"
                xy = x + y
                
                selected_tile = tile_and_origin[xy]
            
        return solved_path
                  
    def move(self, tile_spread, player_self, enemy_self, selected_tiles, surface, offset, viewscale):
        self.set_target_position_on_focus(selected_tiles, player_self, enemy_self, tile_spread)
        
        if tile_spread[self.position[1]][self.position[0]].type == "w":
            self.in_water = True
            
        else:
            self.in_water = False
        
        if self.is_moving:
            if self.movement_cooldown_timer <= 0:
                if self.focus != "stay" and self.current_path == []:
                    self.current_path = self.pathfinding(tile_spread)
                
                if self.current_path != []:
                    new_position = self.current_path.pop(-1)
                    open_tiles = self.get_walkable_tiles(tile_spread, self.position)
                    if new_position in list(open_tiles.values()) or new_position == self.position:
                        tile_spread[self.position[1]][self.position[0]].enemy_occupied = False
                        tile_spread[self.position[1]][self.position[0]].entity_occupied = False
                        self.position = new_position                 
                        if self.is_enemy:
                            tile_spread[self.position[1]][self.position[0]].enemy_occupied = True
                        tile_spread[self.position[1]][self.position[0]].entity_occupied = True
                        
                    else:
                        self.current_path = self.pathfinding(tile_spread)
                
                self.movement_cooldown_timer = self.movement_cooldown
                
            else:
                if self.movement_cooldown_timer >= 0:
                    self.movement_cooldown_timer -= self.movement_cooldown_subtractor
                    
        if self.mode == "active":
            if self.tool_use_cooldown_timer <= 0:
                if "attacking" not in self.focus and self.focus != "trailing":
                    neighbors = list(tile_spread[self.position[1]][self.position[0]].neighbors.values())
                    neighbors.append(self.position)
                    if self.focus != "stay" and self.target_position != None and self.target_position in neighbors:
                        if self.target_position in selected_tiles:
                            resources = self.use_tool(tile_spread[self.target_position[1]][self.target_position[0]], surface, offset, viewscale, tile_spread, selected=True)
                        
                        else:
                            resources = self.use_tool(tile_spread[self.target_position[1]][self.target_position[0]], surface, offset, viewscale, tile_spread)
                            
                        if resources[1] == True:
                            for resource in resources[0]:
                                try:
                                    player_self.inventory[resource] += 1
                                    
                                except KeyError:
                                    player_self.inventory[resource] = 1
                        
                    else:
                        pass
                    
                else:
                    neighbors = list(tile_spread[self.position[1]][self.position[0]].neighbors.values())
                    neighbors.append(self.position)
                    if self.focus != "stay" and self.target_position != None and self.target_position in neighbors:
                        if self.target_position in selected_tiles:
                            tiles_pos_hit = self.use_tool(tile_spread[self.target_position[1]][self.target_position[0]], surface, offset, viewscale, tile_spread, selected=True)
                        
                        else:
                            tiles_pos_hit = self.use_tool(tile_spread[self.target_position[1]][self.target_position[0]], surface, offset, viewscale, tile_spread)
                            
                        for entity in enemy_self.entities.values():
                            if entity.position in tiles_pos_hit:
                                entity.damage(self)
                    
                self.tool_use_cooldown_timer = self.tool_use_cooldown
                
            else:
                if self.tool_use_cooldown_timer >= 0:
                    self.tool_use_cooldown_timer -= self.tool_use_cooldown_subtractor