import pygame
from random import randint
import tile_code
import generation_code
import player_code
import entities_code
from menu_code import Menu, MainMenu
from time import sleep
from math import trunc as mathtrunc

def little_loading_function(dimensions):
    impact_font = pygame.font.SysFont('Impact', int(dimensions[1] / 10))
    text = impact_font.render("Loading...", True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = (dimensions[0] / 2, dimensions[1] / 2)
    
    return [text, [rect.x, rect.y]]

class GameFrame:
    def __init__(self, window_dimensions: list[int, int]):
        self.gamescreen = pygame.display.set_mode(window_dimensions, pygame.RESIZABLE)
        pygame.display.set_caption("Spotland")
        
        main_menu = MainMenu(window_dimensions, self.gamescreen)
        rules = main_menu.run(self.gamescreen)
        if rules == "quit":
            exit
            
        else:
            generation_settings = rules
            
            print(generation_settings)
        
            self.gamescreen.fill((0, 0, 0))
            loading = little_loading_function(self.gamescreen.get_size())
            self.gamescreen.blit(loading[0], loading[1])
            pygame.display.update()
            sleep(1)
            
            self.generation = generation_code.Generation(generation_settings["world_dimensions"], generation_settings["tile_dimensions"], generation_settings["water_rules"], generation_settings["desert_rules"], generation_settings["hilly_rules"], generation_settings["river_rules"])
            self.world_name = generation_settings["world_name"]
            self.viewpoint_offset = [window_dimensions[0] * .2, 200]
            self.offset_offset = [0, 0]
            self.viewscale = 1.0
            self.viewscale_exponent = 0
            self.viewscale_change_sleep = 0
            self.pause_state = 0
            self.mousedown = False
            
            starting_pos = [randint(0, self.generation.dimensions[0] - 1), randint(0, self.generation.dimensions[1] - 1)]
            
            self.player = player_code.Player(starting_pos, self.generation.tile_dimensions, "Dylan")
            
            starting_pos2 = [randint(0, self.generation.dimensions[0] - 1), randint(0, self.generation.dimensions[1] - 1)]
            
            self.player_2 = player_code.Player(starting_pos2, self.generation.tile_dimensions, "Not Dylan", enemy=True)
            self.player_2.entities["0"].focus = "inverse_attacking"
            
            self.menu = Menu(self.gamescreen.get_size(), self.player)
            
            self.selection = []
            self.selected_entity = ""

    def select(self, selecting_command = ""):
        mouse_pos = pygame.mouse.get_pos()
                    
        selected_tile_location = [int((mouse_pos[0] - self.viewpoint_offset[0]) / (self.generation.tile_dimensions[0] * self.viewscale)), int((mouse_pos[1] - self.viewpoint_offset[1]) / (self.generation.tile_dimensions[1] * self.viewscale))]
        
        try:
            if selecting_command == "shift":
                pass
            
            elif selecting_command == "ctrl":
                pass  
            
            elif selecting_command == "deselect":
                for old_tile in self.selection:
                    self.generation.tile_spread[old_tile[1]][old_tile[0]].blit(self.gamescreen, (self.viewpoint_offset[0] + self.offset_offset[0], self.viewpoint_offset[1] + self.offset_offset[1]), self.viewscale, self.generation.tile_spread,)
                    
                self.selection = []
                
                self.menu.grab_selected_tile_info(self, initial=True)
            
            else:
                for old_tile in self.selection:
                    self.generation.tile_spread[old_tile[1]][old_tile[0]].blit(self.gamescreen, (self.viewpoint_offset[0] + self.offset_offset[0], self.viewpoint_offset[1] + self.offset_offset[1]), self.viewscale, self.generation.tile_spread,)
                        
                self.selection = []
                    
                self.generation.tile_spread[selected_tile_location[1]][selected_tile_location[0]].blit(self.gamescreen, (self.viewpoint_offset[0] + self.offset_offset[0], self.viewpoint_offset[1] + self.offset_offset[1]), self.viewscale, self.generation.tile_spread, selected=True)
                self.selection.append(selected_tile_location)
                
                self.menu.grab_selected_tile_info(self, initial=True)
                
                for key, entity in self.player.entities.items():
                    if entity.position in self.selection:
                        self.deselect_selection_button_command(deselect_entity=True)
                        
                        self.selected_entity = key
                        self.menu.grab_selected_entity_info(self, self.gamescreen, initial=True)
                
        except KeyError:
            pass

    def update_random_tile(self):
        random_tile = self.generation.pull_random()
        
        if self.selection != []:
            if random_tile in self.selection:
                self.generation.tile_spread[random_tile[1]][random_tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                
            else:
                self.generation.tile_spread[random_tile[1]][random_tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
            
        else:
            self.generation.tile_spread[random_tile[1]][random_tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
        
        position_and_dimension_data = ((self.viewpoint_offset[0] + (self.generation.tile_spread[random_tile[1]][random_tile[0]].location[0] * self.generation.tile_spread[random_tile[1]][random_tile[0]].dimensions[0] * self.viewscale),
                                            self.viewpoint_offset[1] + (self.generation.tile_spread[random_tile[1]][random_tile[0]].location[1] * self.generation.tile_spread[random_tile[1]][random_tile[0]].dimensions[1] * self.viewscale)),
                                            (self.generation.tile_spread[random_tile[1]][random_tile[0]].dimensions[0] * self.viewscale, self.generation.tile_spread[random_tile[1]][random_tile[0]].dimensions[1] * self.viewscale))
        
        self.generation.tile_spread[random_tile[1]][random_tile[0]].update_occupants(self.gamescreen, position_and_dimension_data, self)
            
    def deselect_selection_button_command(self, deselect_tile = False, deselect_entity = False):
        if deselect_tile:
            self.select(selecting_command="deselect")
            
        if deselect_entity:
            self.selected_entity = ""
            self.menu.grab_selected_entity_info(self, self.gamescreen, initial=True)
            
    def update_clicked(self, mouse_button_action = None):
        if mouse_button_action == None:
            pass
        
        elif mouse_button_action == "down":
            self.taken_mouse_pos = pygame.mouse.get_pos()
            self.mousedown = True
            
        elif mouse_button_action == "up":
            self.mousedown = False
            self.viewpoint_offset[0] += self.offset_offset[0]
            self.viewpoint_offset[1] += self.offset_offset[1]
            self.offset_offset = [0, 0]
            
            self.blit()
            
        if self.mousedown:
            mouse_pos = pygame.mouse.get_pos()
            self.offset_offset = [mouse_pos[0] - self.taken_mouse_pos[0], mouse_pos[1] - self.taken_mouse_pos[1]]
            self.blit()
            
    def updateview(self, call: str,):
        if self.viewscale_change_sleep <= 0:
            if call == "n":
                self.viewpoint_offset[1] += (self.generation.tile_dimensions[1] * self.viewscale)
                
            elif call == "s":
                self.viewpoint_offset[1] -= (self.generation.tile_dimensions[1] * self.viewscale)
                
            elif call == "w":
                self.viewpoint_offset[0] -= (self.generation.tile_dimensions[0] * self.viewscale)
                
            elif call == "e":
                self.viewpoint_offset[0] += (self.generation.tile_dimensions[0] * self.viewscale)
                
            elif call == "r":
                self.viewscale = 1.0
                self.viewscale_exponent = 1
                
                gamescreen_size = self.gamescreen.get_size()
                tile_spread_size_w_h = [self.generation.dimensions[0] * self.generation.tile_dimensions[0], self.generation.dimensions[1] * self.generation.tile_dimensions[1]]
                
                new_offset_w_h = [(gamescreen_size[0] - tile_spread_size_w_h[0]) / 2, (gamescreen_size[1] - tile_spread_size_w_h[1]) / 2]
                
                self.viewpoint_offset = new_offset_w_h
            
            elif call == "+" and self.viewscale_exponent < 5:
                mouse_pos = pygame.mouse.get_pos()
                
                mouse_pos_in_relation_to_tile_spread_tl_x_y = [mouse_pos[0] - self.viewpoint_offset[0], mouse_pos[1] - self.viewpoint_offset[1]]
                tile_with_mouse_inside = [(mouse_pos_in_relation_to_tile_spread_tl_x_y[0] / (self.generation.tile_dimensions[0] * self.viewscale)), (mouse_pos_in_relation_to_tile_spread_tl_x_y[1] / (self.generation.tile_dimensions[1] * self.viewscale))]
                old_xy_of_tile_with_mouse_inside = [tile_with_mouse_inside[0] * (self.generation.tile_dimensions[0] * self.viewscale), tile_with_mouse_inside[1] * (self.generation.tile_dimensions[1] * self.viewscale)]
                
                self.viewscale_exponent += 1
                self.viewscale = float(2 ** self.viewscale_exponent)
                
                position_on_tile_spread_that_player_was_on = [tile_with_mouse_inside[0] * self.generation.tile_dimensions[0] * self.viewscale, tile_with_mouse_inside[1] * self.generation.tile_dimensions[1] * self.viewscale]
                
                self.viewpoint_offset[0] -= (position_on_tile_spread_that_player_was_on[0] - old_xy_of_tile_with_mouse_inside[0])
                self.viewpoint_offset[1] -= (position_on_tile_spread_that_player_was_on[1] - old_xy_of_tile_with_mouse_inside[1])
                
            elif call == "-" and self.viewscale_exponent > 0:
                mouse_pos = pygame.mouse.get_pos()
                
                mouse_pos_in_relation_to_tile_spread_tl_x_y = [mouse_pos[0] - self.viewpoint_offset[0], mouse_pos[1] - self.viewpoint_offset[1]]
                tile_with_mouse_inside = [(mouse_pos_in_relation_to_tile_spread_tl_x_y[0] / (self.generation.tile_dimensions[0] * self.viewscale)), (mouse_pos_in_relation_to_tile_spread_tl_x_y[1] / (self.generation.tile_dimensions[1] * self.viewscale))]
                old_xy_of_tile_with_mouse_inside = [tile_with_mouse_inside[0] * (self.generation.tile_dimensions[0] * self.viewscale), tile_with_mouse_inside[1] * (self.generation.tile_dimensions[1] * self.viewscale)]
                
                self.viewscale_exponent -= 1
                self.viewscale = float(2 ** self.viewscale_exponent)
                
                position_on_tile_spread_that_player_was_on = [tile_with_mouse_inside[0] * self.generation.tile_dimensions[0] * self.viewscale, tile_with_mouse_inside[1] * self.generation.tile_dimensions[1] * self.viewscale]
                
                self.viewpoint_offset[0] -= (position_on_tile_spread_that_player_was_on[0] - old_xy_of_tile_with_mouse_inside[0])
                self.viewpoint_offset[1] -= (position_on_tile_spread_that_player_was_on[1] - old_xy_of_tile_with_mouse_inside[1])
                
            self.viewscale_change_sleep = 3
            
        tile_width = [self.generation.tile_dimensions[0] * self.viewscale, self.generation.tile_dimensions[1] * self.viewscale]
        self.blit()
        
            
    def tick(self):
        self.update_random_tile()
        self.player.check_entity_healths(self.generation.tile_spread, self.player_2, self.selection, self.gamescreen, self.viewpoint_offset, self.viewscale, self)
        self.player_2.check_entity_healths(self.generation.tile_spread, self.player, self.selection, self.gamescreen, self.viewpoint_offset, self.viewscale, self)
        self.viewscale_change_sleep -= 1
        
        self.menu.grab_selected_tile_info(self)
        self.menu.grab_selected_entity_info(self, self.gamescreen)
        self.blit_overlay()
        
            
    def tick_entities(self):
        for entity in self.player_2.entities.values():
            
            if self.selection != []:
                if entity.position in self.selection:
                    self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                    
                else:
                    self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
                if self.generation.tile_spread[entity.position[1]][entity.position[0]].neighbors["s"] != None:
                    tile_pos_to_be_blitted = []
                    tile_iterant = 1
                    
                    try:
                        while len(self.generation.tile_spread[entity.position[1] + tile_iterant][entity.position[0]].tile_occupants) > 0:
                            tile_pos_to_be_blitted.append([entity.position[0], entity.position[1] + tile_iterant])
                            
                            tile_iterant += 1

                    except KeyError:
                        pass
                        
                    for tile in tile_pos_to_be_blitted:
                        try:
                            if tile in self.selection:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                                
                            else:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                                
                        except IndexError:
                            self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
            else:
                self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                if self.generation.tile_spread[entity.position[1]][entity.position[0]].neighbors["s"] != None:
                    tile_iterant = 1
                    tile_pos_to_be_blitted = []
                    
                    try:
                        while len(self.generation.tile_spread[entity.position[1] + tile_iterant][entity.position[0]].tile_occupants) > 0:
                            tile_pos_to_be_blitted.append([entity.position[0], entity.position[1] + tile_iterant])
                            
                            tile_iterant += 1

                    except KeyError:
                        pass
                        
                    for tile in tile_pos_to_be_blitted:
                        try:
                            if tile in self.selection:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                                
                            else:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                                
                        except IndexError:
                            self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
        self.player_2.tick_entities(self.generation.tile_spread, self.player, self.selection, self.gamescreen, self.viewpoint_offset, self.viewscale)
        self.player_2.blit(self.gamescreen, self.viewpoint_offset, [self.generation.tile_dimensions[0] * self.viewscale, self.generation.tile_dimensions[1] * self.viewscale], offset_offset=self.offset_offset)
        
        for entity in self.player.entities.values():
            
            if self.selection != []:
                if entity.position in self.selection:
                    self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                    
                else:
                    self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
                if self.generation.tile_spread[entity.position[1]][entity.position[0]].neighbors["s"] != None:
                    tile_pos_to_be_blitted = []
                    tile_iterant = 1
                    
                    try:
                        while len(self.generation.tile_spread[entity.position[1] + tile_iterant][entity.position[0]].tile_occupants) > 0:
                            tile_pos_to_be_blitted.append([entity.position[0], entity.position[1] + tile_iterant])
                            
                            tile_iterant += 1

                    except KeyError:
                        pass
                        
                    for tile in tile_pos_to_be_blitted:
                        try:
                            if tile in self.selection:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                                
                            else:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                                
                        except IndexError:
                            self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
            else:
                self.generation.tile_spread[entity.position[1]][entity.position[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                if self.generation.tile_spread[entity.position[1]][entity.position[0]].neighbors["s"] != None:
                    tile_iterant = 1
                    tile_pos_to_be_blitted = []
                    
                    try:
                        while len(self.generation.tile_spread[entity.position[1] + tile_iterant][entity.position[0]].tile_occupants) > 0:
                            tile_pos_to_be_blitted.append([entity.position[0], entity.position[1] + tile_iterant])
                            
                            tile_iterant += 1

                    except KeyError:
                        pass
                        
                    for tile in tile_pos_to_be_blitted:
                        try:
                            if tile in self.selection:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread, selected=True)
                                
                            else:
                                self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                                
                        except IndexError:
                            self.generation.tile_spread[tile[1]][tile[0]].blit(self.gamescreen, self.viewpoint_offset, self.viewscale, self.generation.tile_spread,)
                    
        self.player.tick_entities(self.generation.tile_spread, self.player_2, self.selection, self.gamescreen, self.viewpoint_offset, self.viewscale)
        self.player.blit(self.gamescreen, self.viewpoint_offset, [self.generation.tile_dimensions[0] * self.viewscale, self.generation.tile_dimensions[1] * self.viewscale], offset_offset=self.offset_offset)
        
        if self.selected_entity != "":
            self.player.entities[self.selected_entity].name = self.menu.textboxes["Selected Entity's Name"].data
                        
    def blit(self):
        self.gamescreen.fill((0, 0, 0))
        
        if self.pause_state == 0:
            for row, set in self.generation.tile_spread.items():
                for column, tile in set.items():
                    if tile.location in self.selection:
                        tile.blit(self.gamescreen, (self.viewpoint_offset[0] + self.offset_offset[0], self.viewpoint_offset[1] + self.offset_offset[1]), self.viewscale, self.generation.tile_spread, True)
                        
                    else:
                        tile.blit(self.gamescreen, (self.viewpoint_offset[0] + self.offset_offset[0], self.viewpoint_offset[1] + self.offset_offset[1]), self.viewscale, self.generation.tile_spread, False)
                        
            self.player.blit(self.gamescreen, self.viewpoint_offset, [self.generation.tile_dimensions[0] * self.viewscale, self.generation.tile_dimensions[1] * self.viewscale])
            self.player_2.blit(self.gamescreen, self.viewpoint_offset, [self.generation.tile_dimensions[0] * self.viewscale, self.generation.tile_dimensions[1] * self.viewscale])

        self.menu.resize(self.gamescreen, self)
        self.blit_overlay()
        
    def blit_overlay(self):
        self.menu.blit(self.gamescreen, self)
                