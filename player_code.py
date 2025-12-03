import pygame
import entities_code
import tile_occupants_code
from random import randint

class Player:
    def __init__(self, starting_pos: list[int, int], tile_width: list[int, int], name: str, enemy=False):
        self.name = name
        self.score = 0
        self.bonuses = {}
        self.inventory = {}
        self.tools = {}
        self.number_of_entities_ever = 1
        self.is_enemy = enemy
        self.level = 1.0
        
        type = randint(0, 4)
        mushrooms = ["toadstool", "oyster", "psilocybe", "portobello", "morel"]
        self.entities = {"0": entities_code.MushroomTemplate(mushrooms[type], starting_pos, tile_width, self.name, self, enemy=self.is_enemy), }
        
    def set_focus_for_all_entities(self, new_focus="", new_target_id=""):
        for entity in self.entities.values():
            entity.set_focus_and_target(new_focus=new_focus, new_target_id=new_target_id)
        
    def spawn_entity(self, type_of_mushroom: str, tile_width: list[int ,int], starting_pos: list[int, int]):
        if len(self.entities) < 20:
            self.entities[str(self.number_of_entities_ever)] = entities_code.MushroomTemplate(type_of_mushroom, starting_pos, tile_width, self.name, self, enemy=self.is_enemy)
            self.number_of_entities_ever += 1
        
    def tick_entities(self, tile_spread, enemy_self, selected_tiles, surface, offset, viewscale):
        for entity in self.entities.values():
            entity.move(tile_spread, self, enemy_self, selected_tiles, surface, offset, viewscale)
    
    def check_entity_healths(self, tile_spread, enemy_self, selected_tiles, surface, offset, viewscale, gamescreen):
        to_be_deleted = []
        for name, entity in self.entities.items():
            if entity.health <= 0:
                occupant_id = str(entity.type) + "_corpse"
                tile_spread[entity.position[1]][entity.position[0]].add_occupants([tile_occupants_code.OccupantTemplate(occupant_id, tile_spread[entity.position[1]][entity.position[0]])])
                if entity.position in selected_tiles:
                    tile_spread[entity.position[1]][entity.position[0]].blit(surface, offset, viewscale, tile_spread, selected=True)
                    
                else:
                    tile_spread[entity.position[1]][entity.position[0]].blit(surface, offset, viewscale, tile_spread)
                
                tile_spread[entity.position[1]][entity.position[0]].entity_occupied = False
                tile_spread[entity.position[1]][entity.position[0]].enemy_occupied = False
                
                if name == gamescreen.selected_entity and self.is_enemy == False:
                    gamescreen.deselect_selection_button_command(deselect_entity = True)
                    
                to_be_deleted.append(name)
                
            elif entity.health <= (entity.max_health * .2) and (entity.can_be_scared == True) and randint(0, 4) == 0:
                entity.set_focus_and_target(new_focus="home")
                
                
        for name in to_be_deleted:
            if gamescreen.selected_entity == name and self.is_enemy == False:
                gamescreen.selected_entity = ""
                
            del self.entities[name]

            if self.is_enemy == False:
                try:
                    del gamescreen.menu.buttons[name]
                
                except KeyError:
                    pass
                
            
    def blit(self, surface, offset, tile_dimensions: list[int, int], offset_offset = [0, 0]):
        for entity in self.entities.values():
            entity.blit(surface, offset, tile_dimensions, offset_offset=offset_offset)
            