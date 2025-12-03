import pygame
from random import randint


class Menu:
    def __init__(self, initial_window_size: list[int, int], playerself):
        self.mouse_in_menu = [False, ""]
        self.bg_panels = {
                        "middle": MenuPanel([.5, .8], initial_window_size, [1.01, 3.3], 0, radius=5), 
                        "left": MenuPanel([.105, .8], initial_window_size, [5.5, 4], 0, radius=5), 
                        "right": MenuPanel([.39, .8], initial_window_size, [2.75, 4], 0, radius=5),
                        }
        self.buttons = {
                        "focus_selection_stay_button": Button([.434, .715], initial_window_size, [16, 16], "", "focus_selection_stay_button", "stay", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_stay.png", has_hover_textbox=True, hover_textbox_text=["Stay Put"]),
                        "focus_selection_home_button": Button([.485, .715], initial_window_size, [16, 16], "", "focus_selection_home_button", "home", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_home.png", has_hover_textbox=True, hover_textbox_text=["Go Home"]),
                        "focus_selection_selected_button": Button([.536, .715], initial_window_size, [16, 16], "", "focus_selection_selected_button", "selected", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_selected.png", has_hover_textbox=True, hover_textbox_text=["Go To Selected"]),
                        "focus_selection_gathering_button": Button([.434, .77], initial_window_size, [16, 16], "", "focus_selection_gathering_button", "gathering", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_gathering.png", has_hover_textbox=True, hover_textbox_text=["Gather With Tool"]),
                        "focus_selection_trailing_button": Button([.485, .77], initial_window_size, [16, 16], "", "focus_selection_trailing_button", "trailing", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_trailing.png", has_hover_textbox=True, hover_textbox_text=["Trail A Friendly"]),
                        "focus_selection_attacking_button": Button([.536, .77], initial_window_size, [16, 16], "", "focus_selection_attacking_button", "attacking", 0, radius=10, has_image=True, image_path="images\menu_icons/focus_icon_attacking.png", has_hover_textbox=True, hover_textbox_text=["Attack A Foe"]),
                        "deselection_entity_button": Button([.24, .9], initial_window_size, [15, 16], "X", "deselection_entity_button", "deselect_entity", 0, radius=10, has_hover_textbox=True, hover_textbox_text=["Deselect Entity"]),
                        "deselection_tile_button": Button([.046, .9], initial_window_size, [15, 16], "X", "deselection_tile_button", "deselect_tile", 0, radius=10, has_hover_textbox=True, hover_textbox_text=["Deselect Tile"]),

                        }
        self.textboxes = {
                        "Selected Entity's Name": TextBox([.34, .9], initial_window_size, [7, 15], "Selected Entity's Name", 0, radius=10)
                        }
        self.texts = {
                        "selected_entity_focus": TextObject("Focus:", 15, [.5, .825], 0, "twcen", [30, 30, 30], initial_window_size, color_change_limit=60),
                        "selected_entity_level": TextObject("Level:", 15, [.5, .845], 0, "twcen", [30, 30, 30], initial_window_size, color_change_limit=60),
                        "selected_entity_health": TextObject("0/0", 15, [.5, .865], 0, "twcen", [30, 30, 30], initial_window_size, color_change_limit=60),
                        "selected_entity_strength": TextObject("Strength:", 15, [.5, .885], 0, "twcen", [30, 30, 30], initial_window_size, color_change_limit=60),
                        
                        "selected_entity_tool": TextObject("Tool:", 15, [.7, .91], 0, "twcen", [30, 30, 30], initial_window_size, color_change_limit=60),

                        }
        self.grids = {

                        }   
        self.button_grids = {
            
                            }
        self.images = {
                        "selected_entity_image": ImageObject("images/menu_icons/unselected_entity_icon.png", [0.31, 0.78], [.15, .15], initial_window_size, 0, is_square = True, has_hover_textbox=True, hover_textbox_text=["Current Mycelian Image:", "None"])
                        }
        self.rects = {
                        "selected_tile_rect": MenuRect([.105, .72], [.05, .05], initial_window_size, 0, False, True, [255, 255, 255], [100, 100, 100], is_square=True, has_hover_textbox=True, hover_textbox_text=["No Tile Selected"])
                        }
        
        accepted_hover_objects_1 = []
        accepted_hover_objects_1.extend(list(self.buttons.keys()))
        accepted_hover_objects_1.extend(list(self.images.keys()))
        accepted_hover_objects_1.extend(list(self.rects.keys()))
        print(accepted_hover_objects_1)
        
        self.hover_textboxes = {
                            "hover_textbox_1": HoverTextBox(.015, "Testing", initial_window_size, accepted_hover_objects_1)
                            }

        self.function = "menu"
        self.menulevel = 0
        self.running = True
        self.in_text_box = None
        self.info_panel = {"bg rect": "", "name rect": "", "input rect": ""}
        
        for grid_name, grid in self.grids.items():
            grid.export_grid_textboxes(self.textboxes)
            
    def check_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_over_menus = []
            
        for panel_name, panel_obj in self.bg_panels.items():
            if panel_obj.panel_rect.collidepoint(mouse_pos) and panel_obj.level == self.menulevel:
                mouse_over_menus.append(panel_name)
                
        for button in self.buttons.values():
            if button.button_rect.collidepoint(mouse_pos) and button.level == self.menulevel:
                mouse_over_menus.append(button.name)
                
        for textbox in self.textboxes.values():
            if textbox.rect.collidepoint(mouse_pos) and textbox.level == self.menulevel:
                mouse_over_menus.append(textbox.name)
                
        for rect_name, rect_obj in self.rects.items():
            if rect_obj.level == self.menulevel and rect_obj.rect.collidepoint(mouse_pos):
                mouse_over_menus.append(rect_name)

        for img_name, img_obj in self.images.items():
            img_rect = img_obj.loaded_image.get_rect()
            img_rect.center = img_obj.position
            if img_obj.level == self.menulevel and img_rect.collidepoint(mouse_pos):
                mouse_over_menus.append(img_name)
                
        if mouse_over_menus:
            return [True, mouse_over_menus[-1]]
        
        else:
            return [False, ""]
        
    def unselect(self):
        self.in_text_box = None
        for name, textbox in self.textboxes.items():
            if name == self.mouse_in_menu[1]:
                pass
            
            else:               
                textbox.actively_typing = False
            
    def resize(self, surface, gameframeself):
        for button in self.buttons.values():
            button.resize_and_reposition(surface.get_size())
                        
        for textbox in self.textboxes.values():
            textbox.resize_and_reposition(surface.get_size())
                        
        for text in self.texts.values():
            text.rerender(surface.get_size())
            
        for panel in self.bg_panels.values():
            panel.resize_and_reposition(surface.get_size())
            
        for image in self.images.values():
            image.resize_and_reposition(surface.get_size())
            
        for rect in self.rects.values():
            rect.resize_and_reposition(surface.get_size())
            
        for hover_textbox in self.hover_textboxes.values():
            hover_textbox.blit(gameframeself)
            
    def clicked(self, surface, playerself, gameframeself):
        try:
            if self.buttons[self.mouse_in_menu[1]].level == self.menulevel:
                self.buttons[self.mouse_in_menu[1]].blit(surface, clicked=True)
                
                if "focus_selection" in self.buttons[self.mouse_in_menu[1]].name and gameframeself.selected_entity != "":
                    gameframeself.player.entities[gameframeself.selected_entity].set_focus_and_target(new_focus=self.buttons[self.mouse_in_menu[1]].function)
                    
                elif "deselect" in self.buttons[self.mouse_in_menu[1]].function:
                    if "entity" in self.buttons[self.mouse_in_menu[1]].function:
                        gameframeself.deselect_selection_button_command(deselect_tile = False, deselect_entity = True)
                        
                    elif "tile" in self.buttons[self.mouse_in_menu[1]].function:
                        gameframeself.deselect_selection_button_command(deselect_tile = True, deselect_entity = False)
                        
                    elif "both" in self.buttons[self.mouse_in_menu[1]].function:
                        gameframeself.deselect_selection_button_command(self=gameframeself, deselect_tile = True, deselect_entity = True)
                        
                    else:
                        pass
                
        except:
            try:
                if self.textboxes[self.mouse_in_menu[1]].level == self.menulevel:
                    self.unselect()
                    if self.textboxes[self.mouse_in_menu[1]].actively_typing:
                        self.textboxes[self.mouse_in_menu[1]].actively_typing = False
                        print("flipped False")
                        
                    else:
                        self.textboxes[self.mouse_in_menu[1]].actively_typing = True
                        self.in_text_box = True
                        print("flipped true")
                        
            except:
                pass
           
    def grab_selected_tile_info(self, gameframeself, initial=False):
        if initial:
            if gameframeself.selection == []:
                self.rects["selected_tile_rect"].resize_and_reposition(gameframeself.gamescreen.get_size(), new_fill=False, new_fill_color=None, new_stroke=True, new_stroke_color=[100, 100, 100], new_hover_textbox_text=["No Tile Selected"])
                
            else:
                new_color = gameframeself.generation.tile_spread[gameframeself.selection[0][1]][gameframeself.selection[0][0]].color
                
                tile_location = gameframeself.generation.tile_spread[gameframeself.selection[0][1]][gameframeself.selection[0][0]].location
                
                tile_location = "pos " + str(tuple(tile_location))
                
                tile_type = gameframeself.generation.tile_spread[gameframeself.selection[0][1]][gameframeself.selection[0][0]].type
                
                if tile_type == "b":
                    tile_type = "blank tile"
                
                elif tile_type == "w":
                    tile_type = "water tile"
                    
                elif tile_type == "d":
                    tile_type = "desert tile"
                
                elif tile_type == "g":
                    tile_type = "grassland tile"
                                        
                elif tile_type == "h":
                    tile_type = "hillyland tile"
                                    
                else:
                    tile_type = "unknown tile... how??"
                    
                concatenated_string = [tile_location, tile_type]
                                    
                self.rects["selected_tile_rect"].resize_and_reposition(gameframeself.gamescreen.get_size(), new_fill=True, new_fill_color=new_color, new_stroke=False, new_stroke_color=None, new_hover_textbox_text=concatenated_string)
                
        else:
            if gameframeself.selection == []:
                pass
            
            else:
                tile_location = gameframeself.generation.tile_spread[gameframeself.selection[0][1]][gameframeself.selection[0][0]].location
                
                tile_location = "pos " + str(tuple(tile_location))
                
                tile_type = gameframeself.generation.tile_spread[gameframeself.selection[0][1]][gameframeself.selection[0][0]].type
                
                if tile_type == "b":
                    tile_type = "blank tile"
                
                elif tile_type == "w":
                    tile_type = "water tile"
                    
                elif tile_type == "d":
                    tile_type = "desert tile"
                
                elif tile_type == "g":
                    tile_type = "grassland tile"
                                        
                elif tile_type == "h":
                    tile_type = "hillyland tile"
                                    
                else:
                    tile_type = "unknown tile... how??"
                    
                concatenated_string = [tile_location, tile_type]
                                    
                self.rects["selected_tile_rect"].resize_and_reposition(gameframeself.gamescreen.get_size(), new_hover_textbox_text=concatenated_string)
                           
    def grab_selected_entity_info(self, gameframeself, surface, initial=False):
        if initial:
            if gameframeself.selected_entity == "":
                self.texts["selected_entity_focus"].rerender(surface.get_size(), newtext="Focus:")
                self.texts["selected_entity_level"].rerender(surface.get_size(), newtext="Level:")
                self.texts["selected_entity_health"].rerender(surface.get_size(), newtext="0/0")
                self.texts["selected_entity_strength"].rerender(surface.get_size(), newtext="Strength:")
                
                self.texts["selected_entity_tool"].rerender(surface.get_size(), newtext="Tool:")
                
                self.images["selected_entity_image"].resize_and_reposition(surface.get_size(), new_image_path=r"images/menu_icons/unselected_entity_icon.png")
                
                self.textboxes["Selected Entity's Name"].data = ""
                self.textboxes["Selected Entity's Name"].rerender_textbox(surface.get_size())
                
            else:
                focus_text = "Focus: " + str(gameframeself.player.entities[gameframeself.selected_entity].focus)
                level_text = "Level: " + str(gameframeself.player.entities[gameframeself.selected_entity].level)
                health_text = str(round(gameframeself.player.entities[gameframeself.selected_entity].health, 5)) + "/" + str(gameframeself.player.entities[gameframeself.selected_entity].max_health)
                strength_text = "Strength: " + str(gameframeself.player.entities[gameframeself.selected_entity].strength)
                
                tool_text = "Tool: " + gameframeself.player.entities[gameframeself.selected_entity].tool.name
                
                image_path = gameframeself.player.entities[gameframeself.selected_entity].image
                
                self.texts["selected_entity_focus"].rerender(surface.get_size(), newtext=focus_text)
                self.texts["selected_entity_level"].rerender(surface.get_size(), newtext=level_text)
                self.texts["selected_entity_health"].rerender(surface.get_size(), newtext=health_text)
                self.texts["selected_entity_strength"].rerender(surface.get_size(), newtext=strength_text)
                
                self.texts["selected_entity_tool"].rerender(surface.get_size(), newtext=tool_text)
                
                self.images["selected_entity_image"].resize_and_reposition(surface.get_size(), new_image_path=image_path)
                
                self.textboxes["Selected Entity's Name"].data = gameframeself.player.entities[gameframeself.selected_entity].name
                self.textboxes["Selected Entity's Name"].rerender_textbox(surface.get_size())
                
        else:
            if gameframeself.selected_entity == "":
                pass
                
            else:
                focus_text = "Focus: " + str(gameframeself.player.entities[gameframeself.selected_entity].focus)
                level_text = "Level: " + str(gameframeself.player.entities[gameframeself.selected_entity].level)
                health_text = str(round(gameframeself.player.entities[gameframeself.selected_entity].health, 5)) + "/" + str(gameframeself.player.entities[gameframeself.selected_entity].max_health)
                strength_text = "Strength: " + str(gameframeself.player.entities[gameframeself.selected_entity].strength)
                
                tool_text = "Tool: " + gameframeself.player.entities[gameframeself.selected_entity].tool.name
                
                self.texts["selected_entity_focus"].rerender(surface.get_size(), newtext=focus_text)
                self.texts["selected_entity_level"].rerender(surface.get_size(), newtext=level_text)
                self.texts["selected_entity_health"].rerender(surface.get_size(), newtext=health_text)
                self.texts["selected_entity_strength"].rerender(surface.get_size(), newtext=strength_text)
                
                self.texts["selected_entity_tool"].rerender(surface.get_size(), newtext=tool_text)
           
    def blit_selected_entity_info(self, gameframeself, surface):
        pass
            
    def blit(self, surface, gameframeself):
        self.mouse_in_menu = self.check_collision()
        
        for panel_name, panel_obj in self.bg_panels.items():
            if panel_obj.level == self.menulevel:
                if panel_name == self.mouse_in_menu[1]:
                    panel_obj.blit(surface, hover=True)
                    
                else:
                    panel_obj.blit(surface)
                    
        for button_command, button_obj in self.buttons.items():
            if button_obj.level == self.menulevel:
                if button_command == self.mouse_in_menu[1]:
                    button_obj.blit(surface, hover=True)
                        
                else:
                    button_obj.blit(surface)
        
        in_a_textbox_flag = False
        for textbox_name, textbox_obj in self.textboxes.items():
            if textbox_obj.level == self.menulevel:
                if textbox_name == self.mouse_in_menu[1]:
                    in_a_textbox_flag = True
                    textbox_obj.blit(surface, self.info_panel, hover=True)
                    
                else:
                    textbox_obj.blit(surface, self.info_panel)
                    
        for text_name, text_obj in self.texts.items():
            if text_obj.level == self.menulevel:
                text_obj.blit(surface)
                
        for rect_name, menurect_obj in self.rects.items():
            if menurect_obj.level == self.menulevel:
                menurect_obj.blit(gameframeself)
                
        for image_name, image_obj in self.images.items():
            if image_obj.level == self.menulevel:
                image_obj.blit(surface)
                
        for hover_name, hover_obj in self.hover_textboxes.items():
            hover_obj.blit(gameframeself)

        self.blit_selected_entity_info(gameframeself, surface)
                
        if self.info_panel["bg rect"] == "":
            pass
        
        else:
            if in_a_textbox_flag:
                pygame.draw.rect(surface, (100, 100, 100), self.info_panel["bg rect"], border_radius=10)
                surface.blit(self.info_panel["name rect"][0], self.info_panel["name rect"][1])
                surface.blit(self.info_panel["input rect"][0], self.info_panel["input rect"][1])
    
        
class MainMenu:
    def __init__(self, initial_window_width: list[int, int], surface):
        self.rules = {"world_dimensions": [30, 20], "tile_dimensions": [10, 10], "water_rules": [1000], "desert_rules": [1000], "hilly_rules": [1000], "river_rules": [["x", 1], ["y", 2], ["x", 3], ["y", 4], ["x", 5], ["y", 4]], "world_name": "test"}
        self.mouse_in_menu = [False, ""]
        self.buttons = {"CNS Start Button": Button([.5, .2], initial_window_width, [1.9, 8], "Start Spot Creation", "CNS Start Button", "CNS Start Button", 0, radius=10),
                        "Tips": Button([.5, .4], initial_window_width, [2, 8], "Need some Tips?", "Tips", "Tips", 0, radius=10),
                        "Credits": Button([.5, .6], initial_window_width, [2, 8], "Credits", "Credits", "Credits", 0, radius=10),
                        "Exit": Button([.5, .8], initial_window_width, [2, 8], "Get me outta here!", "Exit", "Exit", 0, radius=10),
                        "Home1": Button([.18, .18], initial_window_width, [4, 12], "Home Menu", "Home1", "Home1", 1, radius=10),
                        "Create New Spot": Button([.5, .92], initial_window_width, [3, 13], "Create New Spot", "Create New Spot", "Create New Spot", 1, radius=10)
                        }
        self.textboxes = {"world width": TextBox([.6, .2], initial_window_width, [6, 12], "world width", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=2),
                        "world height": TextBox([.8, .2], initial_window_width, [6, 12], "world height", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=2),
                        "tile width": TextBox([.6, .3], initial_window_width, [6, 12], "tile width", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=2),
                        "tile height": TextBox([.8, .3], initial_window_width, [6, 12], "tile height", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=2),
                        
                        "water amount": TextBox([.15, .53], initial_window_width, [8, 14], "water amount", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=1),
                        "desert amount": TextBox([.15, .63], initial_window_width, [8, 14], "desert amount", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=1),
                        "hilly amount": TextBox([.15, .73], initial_window_width, [8, 14], "hilly amount", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=1),
                        "river amount": TextBox([.75, .53], initial_window_width, [8, 14], "river amount", 1, radius=10, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], length_limit=1),
                        
                        "world name": TextBox([.42, .83], initial_window_width, [2, 10], "world name", 1, radius=10, length_limit=20)
                        }
        self.texts = {"title1": TextObject("World and Tile Settings", 60, [.61, .1], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "world size": TextObject("World Size:", 34, [.42, .2], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "width label": TextObject("Width", 27, [.6, .14], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "height label": TextObject("Height", 27, [.8, .14], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "x1": TextObject("X", 34, [.7, .2], 1, "comic sans", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "tile size": TextObject("Tile Size:", 34, [.42, .3], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "x2": TextObject("X", 34, [.7, .3], 1, "comic sans", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "title2": TextObject("World Attribute Settings", 60, [.5, .43], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "amount label": TextObject("Amount", 27, [.15, .46], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "river amount": TextObject("River Amount", 27, [.75, .475], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "lake amount": TextObject("Lake Spots", 20, [.15, .485], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "hilly amount": TextObject("Hilly Spots", 20, [.15, .685], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    "desert amount": TextObject("Desert Spots", 20, [.15, .585], 1, "twcen", [255, 255, 255], initial_window_width, color_change_limit=100),
                    }
        self.grids = {"water_gen_attempts": QuickGrid(initial_window_width, [.35, .53], [5, 2], 0, [.225, .07], 1, "water_gen_attempts", charlimit=5, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]),
                    "desert_gen_attempts": QuickGrid(initial_window_width, [.35, .63], [5, 2], 0, [.225, .07], 1, "desert_gen_attempts", charlimit=5, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]),
                    "hilly_gen_attempts": QuickGrid(initial_window_width, [.35, .73], [5, 2], 0, [.225, .07], 1, "hilly_gen_attempts", charlimit=5, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]),
                    "river_gen_direction": QuickGrid(initial_window_width, [.705, .7], [1, 9], 0, [.09, .25], 1, "river_gen_direction", charlimit=1, accepted_chars=["x", "y"]),
                    "river_gen_width": QuickGrid(initial_window_width, [.795, .7], [1, 9], 0, [.09, .25], 1, "river_gen_width", charlimit=1, accepted_chars=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]),
                    }        
        self.info_panel = {"bg rect": "", "name rect": "", "input rect": ""}
        
        for grid_name, grid in self.grids.items():
            grid.export_grid_textboxes(self.textboxes)
        
        self.function = "menu"
        self.bg = MainMenuBackground(surface)
        self.menulevel = 0
        self.running = True
        self.in_text_box = None
        self.saved_data = {}
        for key, value in self.textboxes.items():
            self.saved_data[key] = value.data
        
    def check_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_over_menus = []
            
        for button in self.buttons.values():
            if button.button_rect.collidepoint(mouse_pos) and button.level == self.menulevel:
                mouse_over_menus.append(button.name)
                
        for textbox in self.textboxes.values():
            if textbox.rect.collidepoint(mouse_pos) and textbox.level == self.menulevel:
                mouse_over_menus.append(textbox.name)
                
        if mouse_over_menus:
            return [True, mouse_over_menus[-1]]
        
        else:
            return [False, ""]
        
    def unselect(self):
        for name, textbox in self.textboxes.items():
            if name == self.mouse_in_menu[1]:
                pass
            
            else:               
                textbox.actively_typing = False
            
    def create_new_spot(self):
        world_wh = [30, 20]
        tile_wh = [20, 20]
        river_rules = []
        water_rules = []
        hilly_rules = []
        desert_rules = []
        
        river_direction = []
        river_width = []
        
        for textbox_name, textbox in self.textboxes.items():
            if "world" in textbox_name:
                if "width" in textbox_name and self.textboxes["world width"].data != "" and self.textboxes["world width"].data != "0":
                    world_wh[0] = (int(self.textboxes["world width"].data))
                    
                if "height" in textbox_name and self.textboxes["world height"].data != "" and self.textboxes["world height"].data != "0":
                    world_wh[1] = (int(self.textboxes["world height"].data))
                    
            if "tile" in textbox_name:
                if "width" in textbox_name and self.textboxes["tile width"].data != "" and self.textboxes["tile width"].data != 0:
                    tile_wh[0] = (int(self.textboxes["tile width"].data))
                    
                if "height" in textbox_name and self.textboxes["tile height"].data != "" and self.textboxes["tile height"].data != 0:
                    tile_wh[1] = (int(self.textboxes["tile height"].data))
            
            if "river" in textbox_name:
                if "direction" in textbox_name:
                    if textbox.data != "":
                        river_direction.append(textbox.data)
                        
                    else:
                        direction = bool(randint(0, 1))
                        if direction:
                            river_direction.append("y")
                            
                        else:
                            river_direction.append("x")
                    
                if "width" in textbox_name:
                    if textbox.data != "":
                        river_width.append(int(textbox.data))
                        
                    else:
                        river_width.append(1)
                    
            if "hilly" in textbox_name:
                if "gen" in textbox_name:
                    if textbox.data != "":
                        hilly_rules.append(int(textbox.data))
                        
                    else:
                        hilly_rules.append(0)
                    
            if "desert" in textbox_name:
                if "gen" in textbox_name:
                    if textbox.data != "":
                        desert_rules.append(int(textbox.data))
                        
                    else:
                        desert_rules.append(0)
                    
            if "water" in textbox_name:
                if "gen" in textbox_name:
                    if textbox.data != "":
                        water_rules.append(int(textbox.data))
                        
                    else:
                        water_rules.append(0)
            
        for num, direction in enumerate(river_direction):
            river_rules.append([direction, river_width[num]])
            
        if self.textboxes["water amount"].data == "":
            water_rules.append(0)
            
        if self.textboxes["hilly amount"].data == "":
            hilly_rules.append(0)
            
        if self.textboxes["desert amount"].data == "":
            desert_rules.append(0)
            
        if self.textboxes["river amount"].data == "":
            river_rules.append(["y", 3])
            
        self.rules["world_dimensions"] = world_wh
        self.rules["tile_dimensions"] = tile_wh
        self.rules["water_rules"] = water_rules
        self.rules["desert_rules"] = desert_rules
        self.rules["hilly_rules"] = hilly_rules
        self.rules["river_rules"] = river_rules
        
        if self.textboxes["world name"].data == "":
            self.rules["world_name"] = "Untitled Spot"
            
        if self.textboxes["world name"].data:
            self.rules["world_name"] = str(self.textboxes["world name"].data)
        
        self.running = False
            
    def clicked(self, surface):
        try:
            if self.buttons[self.mouse_in_menu[1]].level == self.menulevel:
                self.buttons[self.mouse_in_menu[1]].blit(surface, clicked=True)
                if self.mouse_in_menu[1] == "CNS Start Button":
                    self.menulevel = 1
                    
                elif self.mouse_in_menu[1] == "Tips":
                    print("tips")
                    
                elif self.mouse_in_menu[1] == "Credits":
                    print("credits")
                    
                elif self.mouse_in_menu[1] == "Exit":
                    self.running = False
                    self.rules = "quit"
                    
                elif self.mouse_in_menu[1] == "Home1":
                    self.menulevel = 0
                    try:
                        self.unselect()
                        
                    except KeyError:
                        pass
                    
                elif self.mouse_in_menu[1] == "Create New Spot":
                    self.create_new_spot()
                    
        except:
            try:
                if self.textboxes[self.mouse_in_menu[1]].level == self.menulevel:
                    self.unselect()
                    if self.textboxes[self.mouse_in_menu[1]].actively_typing:
                        self.textboxes[self.mouse_in_menu[1]].actively_typing = False
                        print("flipped False")
                        
                    else:
                        self.textboxes[self.mouse_in_menu[1]].actively_typing = True
                        print("flipped true")
                        
            except:
                pass
    
    def return_generation_settings(self):
        return self.rules
    
    def blit(self, surface):
        surface.fill((0, 0, 0))
        self.bg.blit(surface)
        
        self.mouse_in_menu = self.check_collision()
        
        for button_command, button_obj in self.buttons.items():
            if button_obj.level == self.menulevel:
                if button_command == self.mouse_in_menu[1]:
                    button_obj.blit(surface, hover=True)
                        
                else:
                    button_obj.blit(surface)
        
        in_a_textbox_flag = False      
        for textbox_name, textbox_obj in self.textboxes.items():
            if textbox_obj.level == self.menulevel:
                if textbox_name == self.mouse_in_menu[1]:
                    textbox_obj.blit(surface, self.info_panel, hover=True)
                    in_a_textbox_flag = True
                    
                else:
                    textbox_obj.blit(surface, self.info_panel)
                    
        for text_name, text_obj in self.texts.items():
            if text_obj.level == self.menulevel:
                text_obj.blit(surface)
                
        if self.info_panel["bg rect"] == "":
            pass
        
        else:
            if in_a_textbox_flag:
                pygame.draw.rect(surface, (100, 100, 100), self.info_panel["bg rect"], border_radius=10)
                surface.blit(self.info_panel["name rect"][0], self.info_panel["name rect"][1])
                surface.blit(self.info_panel["input rect"][0], self.info_panel["input rect"][1])
          
    def textbox_read(self):
        for key, value in self.textboxes.items():
            self.saved_data[key] = value.data
          
    def textbox_reading_for_grid_resize(self, surface):
        try:
            if self.saved_data["water amount"] != self.textboxes["water amount"].data:
                if self.textboxes["water amount"].data == "":
                    self.grids["water_gen_attempts"].reinit(surface.get_size(), self.grids["water_gen_attempts"].grid_size, 0, self.grids["water_gen_attempts"].grid_wh_ratio, self.textboxes)

                else:
                    self.grids["water_gen_attempts"].reinit(surface.get_size(), self.grids["water_gen_attempts"].grid_size, int(self.textboxes["water amount"].data), self.grids["water_gen_attempts"].grid_wh_ratio, self.textboxes)
                
        except:
            pass
        
        try:
            if self.saved_data["desert amount"] != self.textboxes["desert amount"].data:
                if self.textboxes["desert amount"].data == "":
                    self.grids["desert_gen_attempts"].reinit(surface.get_size(), self.grids["desert_gen_attempts"].grid_size, 0, self.grids["desert_gen_attempts"].grid_wh_ratio, self.textboxes)

                else:
                    self.grids["desert_gen_attempts"].reinit(surface.get_size(), self.grids["desert_gen_attempts"].grid_size, int(self.textboxes["desert amount"].data), self.grids["desert_gen_attempts"].grid_wh_ratio, self.textboxes)
                
        except:
            pass
        
        try:
            if self.saved_data["hilly amount"] != self.textboxes["hilly amount"].data:
                if self.textboxes["hilly amount"].data == "":
                    self.grids["hilly_gen_attempts"].reinit(surface.get_size(), self.grids["hilly_gen_attempts"].grid_size, 0, self.grids["hilly_gen_attempts"].grid_wh_ratio, self.textboxes)

                else:
                    self.grids["hilly_gen_attempts"].reinit(surface.get_size(), self.grids["hilly_gen_attempts"].grid_size, int(self.textboxes["hilly amount"].data), self.grids["hilly_gen_attempts"].grid_wh_ratio, self.textboxes)
               
        except:
            pass
        
        try:
            if self.saved_data["river amount"] != self.textboxes["river amount"].data:
                if self.textboxes["river amount"].data == "":
                    self.grids["river_gen_direction"].reinit(surface.get_size(), self.grids["river_gen_direction"].grid_size, 0, self.grids["river_gen_direction"].grid_wh_ratio, self.textboxes)
                    self.grids["river_gen_width"].reinit(surface.get_size(), self.grids["river_gen_width"].grid_size, 0, self.grids["river_gen_width"].grid_wh_ratio, self.textboxes)
                    
                else:
                    self.grids["river_gen_direction"].reinit(surface.get_size(), self.grids["river_gen_direction"].grid_size, int(self.textboxes["river amount"].data), self.grids["river_gen_direction"].grid_wh_ratio, self.textboxes)
                    self.grids["river_gen_width"].reinit(surface.get_size(), self.grids["river_gen_width"].grid_size, int(self.textboxes["river amount"].data), self.grids["river_gen_width"].grid_wh_ratio, self.textboxes)
         
        except:
            pass
        self.textbox_read()
                
    def run(self, surface):
        clock = pygame.time.Clock()
        menu_tick_event = pygame.USEREVENT + 1
        
        pygame.time.set_timer(menu_tick_event, 60)
        
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == menu_tick_event:
                    self.bg.update_floaters(surface)
                    self.blit(surface)
                    
                if event.type ==  pygame.MOUSEBUTTONDOWN:
                    self.clicked(surface)
                    
                if event.type == pygame.QUIT:
                    self.running = False
                    self.rules = "quit"
                
                if event.type == pygame.WINDOWRESIZED:
                    for button in self.buttons.values():
                        button.resize_and_reposition(surface.get_size())
                        
                    for textbox in self.textboxes.values():
                        textbox.resize_and_reposition(surface.get_size())
                        
                    for text in self.texts.values():
                        text.rerender(surface.get_size())
                        
                if event.type == pygame.KEYDOWN:
                    for textbox in self.textboxes.values():
                        if textbox.actively_typing:
                            textbox.add_chars(pygame.key.name(event.key), surface.get_size())
                                
                        else:
                            pass
                        
                    self.textbox_reading_for_grid_resize(surface)
                    
            clock.tick(60)
            pygame.display.flip()
            
        return self.return_generation_settings()
    
    
class Button:
    def __init__(self, position_ratio: list[float, float], initial_window_size: list[int, int], width_height_ratio: list[int, int], text: str, name: str, function: str, level: int, radius=0, has_image=False, image_path="", has_hover_textbox=False, hover_textbox_text=[""]):
        pygame.font.init()
        self.position_ratio_w_h = position_ratio
        self.position = [initial_window_size[0] * position_ratio[0], initial_window_size[1] * position_ratio[1]]
        self.button_rect = pygame.Rect([self.position[0] - (initial_window_size[0] / width_height_ratio[0] / 2), self.position[1] - (initial_window_size[1] / width_height_ratio[1] / 2)], [initial_window_size[0] / width_height_ratio[0], initial_window_size[1] / width_height_ratio[1]])
        self.width_height_ratio = width_height_ratio
        self.text = text
        self.name = name
        self.function = function
        self.clicked_countdown = 0
        self.level = level
        self.radius = radius
        self.has_image = has_image
        self.has_hover_textbox = has_hover_textbox
        self.hover_textbox_text = hover_textbox_text
        
        if self.has_image:
            self.image_path = image_path
            
            loaded_image = pygame.image.load(self.image_path)
            scale_ratio = (self.button_rect.height * .8) / loaded_image.get_height()
            
            self.loaded_image = pygame.transform.scale(loaded_image, [loaded_image.get_width() * scale_ratio, loaded_image.get_height() * scale_ratio])
        
    def resize_and_reposition(self, window_size: list[int, int], new_hover_text = None):
        self.button_rect.width = window_size[0] / self.width_height_ratio[0]
        self.button_rect.height = window_size[1] / self.width_height_ratio[1]
        
        self.button_rect.center = (window_size[0] * self.position_ratio_w_h[0], window_size[1] * self.position_ratio_w_h[1])
        
        if self.has_image:
            loaded_image = pygame.image.load(self.image_path)
            scale_ratio = (self.button_rect.height * .8) / loaded_image.get_height()
                
            self.loaded_image = pygame.transform.scale(loaded_image, [loaded_image.get_width() * scale_ratio, loaded_image.get_height() * scale_ratio])
        
    def blit(self, surface, hover=False, clicked=False):
        if self.radius == 0:
            if hover and self.clicked_countdown == 0:
                pygame.draw.rect(surface, (150, 150, 165), self.button_rect)
                
            else:
                pygame.draw.rect(surface, (200 - (self.clicked_countdown), 200 - (self.clicked_countdown), 220 - (self.clicked_countdown * 1.1)), self.button_rect)
                
            pygame.draw.rect(surface, (100, 100, 110), self.button_rect, width=5)
                
        else:
            if hover and self.clicked_countdown == 0:
                pygame.draw.rect(surface, (150, 150, 165), self.button_rect, border_radius=self.radius)
                
            else:
                pygame.draw.rect(surface, (200 - (self.clicked_countdown), 200 - (self.clicked_countdown), 220 - (self.clicked_countdown * 1.1)), self.button_rect, border_radius=self.radius)
            
            pygame.draw.rect(surface, (100, 100, 110), self.button_rect, width=5, border_radius=self.radius)
            
        
        if self.has_image:
            transformed_image_rect = self.loaded_image.get_rect()
            transformed_image_rect.center = self.button_rect.center
            
            surface.blit(self.loaded_image, (transformed_image_rect.x, transformed_image_rect.y))
                
        else:
            text_rect = pygame.font.SysFont("twcen", int(self.button_rect.height / 1.9), True, False).render(self.text, False, (0, 0, 0)).get_rect()
            if self.button_rect.width < text_rect.width:
                rendered_text = pygame.font.SysFont("twcen", int(self.button_rect.height / 1.9), True, False).render(self.text, False, (0, 0, 0))
                rendered_text = pygame.transform.scale(rendered_text, (self.button_rect.width, text_rect.height))
                
            else:
                rendered_text = pygame.font.SysFont("twcen", int(self.button_rect.height / 1.9), True, False).render(self.text, False, (0, 0, 0))
            
            text_rect = rendered_text.get_rect()
            text_rect.center = self.button_rect.center
            
            surface.blit(rendered_text, (text_rect.x, text_rect.y))
        
        if clicked:
            self.clicked_countdown = 15
            
        else:
            pass
            
        if self.clicked_countdown > 0:
            self.clicked_countdown -= 1
            
            
class TextBox:
    def __init__(self,  position_ratio: list[float, float], initial_window_size: list[int, int], width_height_ratio: list[int, int], name: str, level: int, radius = 0, accepted_chars = True, length_limit = 0):
        self.actively_typing = False
        self.width_height_ratio = width_height_ratio
        self.position_ratio_w_h = position_ratio
        self.position = [position_ratio[0] * initial_window_size[0], position_ratio[1] * initial_window_size[1]]
        self.rect = pygame.Rect(0, 0, initial_window_size[0] / self.width_height_ratio[0], initial_window_size[1] / self.width_height_ratio[1])
        self.level = level
        self.length_limit = length_limit
        self.data = ""
        self.data_text_rendered = pygame.font.SysFont("arial", int(initial_window_size[1] / self.width_height_ratio[1] * .7), True, False).render(str(self.data), False, (0, 0, 0))
        if accepted_chars == True:
            self.accepted_chars = "all"
            
        else:
            self.accepted_chars = accepted_chars
            
        self.name = name
        self.radius = radius
        
        self.rect.center = self.position
        
    def resize_and_reposition(self, window_size: list[int, int]):
        self.rect.width = window_size[0] / self.width_height_ratio[0]
        self.rect.height = window_size[1] / self.width_height_ratio[1]
        self.rerender_textbox(window_size)
        
        self.position = [window_size[0] * self.position_ratio_w_h[0], window_size[1] * self.position_ratio_w_h[1]]
        
        self.rect.center = self.position
        
    def rerender_textbox(self, window_size: list[int, int]):
        self.data_text_rendered = pygame.font.SysFont("arial", int(window_size[1] / self.width_height_ratio[1] * .7), True, False).render(str(self.data), False, (0, 0, 0))
        
        text_rect = self.data_text_rendered.get_rect()
        if text_rect.width > self.rect.width:
            self.data_text_rendered = pygame.transform.scale(self.data_text_rendered, (self.rect.width, int(window_size[1] / self.width_height_ratio[1] * .7)))
        
    def add_chars(self, char, window_size):
        caps_dict = {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N",
                             "o": "O", "p": "P", "q": "Q", "r": "R", "s": "S", "t": "T", "u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "1": "!", "2": "@",
                             "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")", "`": "~", "-": "_", "=": "+", "[": "{", "]": "}", "\\": "|",
                             ";": ":", "'": '"', ",": "<", ".": ">", "/": "?"}
        
        if len(char) > 1:
            if self.length_limit == 0 or len(self.data) < self.length_limit:
                if char == "space" and ((" " in self.accepted_chars) or (self.accepted_chars == "all")):
                    self.data += " "
                        
            if char == "backspace":
                self.data = self.data[:-1]
                            
            elif char == "return":
                self.actively_typing = False
                        
            elif char == "shift":
                pass
                
            self.rerender_textbox(window_size)
                                
        elif self.length_limit == 0 or len(self.data) < self.length_limit:
            if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                char = caps_dict[char]
                
                if char in self.accepted_chars or self.accepted_chars == "all":
                    self.data += char
                    
                else:
                    pass
                
            else:
                if char in self.accepted_chars or self.accepted_chars == "all":
                    self.data += char
                    
            self.rerender_textbox(window_size)
            
    def mini_info_window(self, surface, info_dict):
        window_size = surface.get_size()
        mouse_pos = pygame.mouse.get_pos()
        
        font = pygame.font.SysFont("arial", int(window_size[1] / 60), True, False)
        
        name_text = "Textbox Name: " + self.name
        name_text_render = font.render(name_text, False, (255, 255, 255))
        
        if self.accepted_chars != "all":
            valid_input_text = "Valid Keys: "
            for char in self.accepted_chars:
                valid_input_text += "'" + char + "' "
                
            valid_input_text.rstrip()
            
        else:
            valid_input_text = "Valid Keys: all"
            
        valid_input_text_render = font.render(valid_input_text, False, (255, 255, 255))
        
        
        name_rect = name_text_render.get_rect()
        valid_input_rect = valid_input_text_render.get_rect()
        
        if name_rect.width > valid_input_rect.width:
            info_rect = pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, name_rect.width * 1.1, name_rect.height * 2.2)
                
        else:
            info_rect = pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, valid_input_rect.width * 1.1, name_rect.height * 2.2)
        
        center = (info_rect.centerx, info_rect.centery)
        
        valid_input_rect.midtop = center
        name_rect.midbottom = center  
        
        info_dict["bg rect"] = info_rect
        info_dict["name rect"] = [valid_input_text_render, (valid_input_rect.x, valid_input_rect.y)]
        info_dict["input rect"] = [name_text_render, (name_rect.x, name_rect.y)]
            
    def blit(self, surface, info_dict, hover=False):
        if self.actively_typing:
            pygame.draw.rect(surface, (150, 150, 165), self.rect, border_radius=self.radius)
            
        else:
            if hover:
                pygame.draw.rect(surface, (150, 150, 165), self.rect, border_radius=self.radius)
                
            else:
                pygame.draw.rect(surface, (200, 200, 220), self.rect, border_radius=self.radius)
                
        pygame.draw.rect(surface, (100, 100, 110), self.rect, width=5, border_radius=self.radius)
        
        if hover:
            self.mini_info_window(surface, info_dict)
                
        text_rect = self.data_text_rendered.get_rect()
        text_rect.center = self.rect.center
                
        surface.blit(self.data_text_rendered, (text_rect.x, text_rect.y))
            
        
class MainMenuBackground:
    def __init__(self, surface):
        self.floaters = []
        self.spawn_floater(surface)
        
    def update_floaters(self, surface):
        for number, floater in enumerate(self.floaters):
            test = floater.update(surface)
            if test:
                pass
            
            else:
                del self.floaters[number]
                
        if len(self.floaters) < 1:
            self.spawn_floater(surface)
            
    def spawn_floater(self, surface):
        h_w = randint(50, 200)
        surface_center = [surface.get_size()[0] / 2, surface.get_size()[1] / 2]
        position = [surface_center[0] - (h_w / 2), surface_center[1] - (h_w / 2)]
        
        pos_neg = [-1, 1]
        x_velo = (randint(300, 900) / 100) * pos_neg[randint(0, 1)]
        y_velo = (randint(300, 900) / 100) * pos_neg[randint(0, 1)]
        self.floaters.append(MMBGFloater(randint(0, 5), position, [h_w, h_w], [(x_velo), (y_velo)], randint(500, 1000)))
    def blit(self, surface):
        for floater in self.floaters:
            floater.blit(surface)


class MMBGFloater:
    def __init__(self, image: int, position: list[float, float], width_height: list[int, int], velocities_x_y: list[float, float], opacity_iterations: int):
        image_dict = {0: 'images/entities/mushrooms/mycelian_toadstool_profile.png', 1: 'images/entities/mushrooms/mycelian_oyster_profile.png',
                           2: 'images/entities/mushrooms/mycelian_psilocybe_profile.png', 3: 'images/entities/mushrooms/mycelian_portobello_profile.png',
                           4: 'images/entities/mushrooms/mycelian_morel_profile.png', 5: 'images/entities/mushrooms/mycelian_miku_profile.png'}
        
        self.current_image = image_dict[image]
        self.loaded_image = pygame.transform.scale(pygame.image.load(self.current_image), width_height)
        self.position = position
        self.size_width_height = width_height
        self.velocity_x_y = [(velocities_x_y[0]), (velocities_x_y[1])]
        self.opacity_iterations_left = opacity_iterations
        self.alpha = 255
        
    def update(self, surface):
        edges = {"sides": [pygame.Rect(1, 1, 1, surface.get_size()[1]), pygame.Rect(surface.get_size()[0], 1, surface.get_size()[0], surface.get_size()[1])],
                 "top_bottom": [pygame.Rect(1, 1, surface.get_size()[0], 1), pygame.Rect(1, surface.get_size()[1], surface.get_size()[0], surface.get_size()[1])]}
        
        image_rect = self.loaded_image.get_rect()
        image_rect.topleft = self.position
        
        pygame.draw.rect(surface, (0, 0, 0), image_rect)
        
        if image_rect.collidepoint(pygame.mouse.get_pos()):
            if self.velocity_x_y[0] >= 0:
                self.velocity_x_y[0] += .02
                
            else:
                self.velocity_x_y[0] -= .02
                
            if self.velocity_x_y[1] >= 0:
                self.velocity_x_y[1] += .02
                
            else:
                self.velocity_x_y[1] -= .02
                
            if randint(0, 9) == 0:
                self.velocity_x_y[0] *= -1
                
            if randint(0, 9) == 0:
                self.velocity_x_y[1] *= -1
        
        for rect in edges["sides"]:
            if image_rect.colliderect(rect):
                self.velocity_x_y[0] *= -1
                
            else:
                pass
            
        for rect in edges["top_bottom"]:
            if image_rect.colliderect(rect):
                self.velocity_x_y[1] *= -1
                
            else:
                pass
            
        self.position[0] += (self.velocity_x_y[0])
        self.position[1] += (self.velocity_x_y[1])
        
        if self.opacity_iterations_left > 0:
            self.opacity_iterations_left -= 1
            
            return True
            
        else:
            self.alpha -= 1
            
            if self.alpha <= 0:
                return False
            
            else:
                self.loaded_image.set_alpha(self.alpha)
                
                return True
            
        
    def blit(self, surface):
        surface.blit(self.loaded_image, self.position)
        
        
class TextObject:
    def __init__(self, text: str, font_size: int, position_ratio: list[float, float], level: int, font: str, color: list[int, int ,int], initial_window_size: list[int, int], bold=False, italic=False, color_change_limit=50):
        self.text = text
        self.font_size_ratio = font_size / initial_window_size[1]
        self.position_ratio = position_ratio
        self.position = [initial_window_size[0] * position_ratio[0], initial_window_size[1] * position_ratio[1]]
        self.level = level
        self.font = font
        self.bold = bold
        self.italic = italic
        self.initial_color = tuple(color)
        self.color_decrease = True
        self.color_change_limit = color_change_limit
        self.color = color
        self.rendered_text = pygame.sysfont.SysFont(self.font, font_size, self.bold, self.italic).render(self.text, False, self.color)
        
    def blit(self, surface):
        if 0 not in self.color:
            if self.color_decrease:
                if (self.color[0] > (self.initial_color[0] - self.color_change_limit)) and (self.color[1] > (self.initial_color[1] - self.color_change_limit)) and (self.color[2] > (self.initial_color[2] - self.color_change_limit)):
                    self.color[0] -= 1
                    self.color[1] -= 1
                    self.color[2] -= 1
                    
                else:
                    self.color_decrease = False
                    
            else:
                if (self.color[0] < self.initial_color[0]) and (self.color[1] < self.initial_color[1]) and (self.color[2] < self.initial_color[2]):
                    self.color[0] += 1
                    self.color[1] += 1
                    self.color[2] += 1
                    
                elif (self.color[0] == self.initial_color[0]) and (self.color[1] == self.initial_color[1]) and (self.color[2] == self.initial_color[2]):
                    self.color_decrease = True
                    
                else:
                    pass
                
        else:
            self.color[0] += 1
            self.color[1] += 1
            self.color[2] += 1
            self.color_decrease = False
        
        self.rerender(surface.get_size())
            
        rect = self.rendered_text.get_rect()
        rect.center = self.position
        surface.blit(self.rendered_text,(rect.x, rect.y))
    
    def rerender(self, window_size: list[int, int], newtext=""):
        if newtext == "":
            self.position = [window_size[0] * self.position_ratio[0], window_size[1] * self.position_ratio[1]]
            self.rendered_text = pygame.sysfont.SysFont(self.font, int(self.font_size_ratio * window_size[1]), self.bold, self.italic).render(self.text, False, self.color)
            
        else:
            self.text = newtext
    
    
class QuickGrid:
    def __init__(self, initial_window_size, position_ratio: list[float, float], size: list[int, int], num_of_textboxes: int, grid_wh_ratio: list[float, float], level: int, gridname: str, charlimit=0, accepted_chars=True):
        self.grid_size = size
        self.position_ratio = position_ratio
        self.textboxes = {}
        self.level = level
        self.gridname = gridname
        self.accepted_chars = accepted_chars
        self.length_limit = charlimit
        self.grid_wh_ratio = grid_wh_ratio
        self.num_of_textboxes = num_of_textboxes
    
        
        individual_textbox_place_ratio_x = {}
        iterant_var = 1
        while (iterant_var/(size[0] * 2)) < 1:
            individual_textbox_place_ratio_x[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[0] * 2)))
            
            iterant_var += 2
            
        individual_textbox_place_ratio_y = {}
        iterant_var = 1
        while (iterant_var/(size[1] * 2)) < 1:
            individual_textbox_place_ratio_y[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[1] * 2)))
            
            iterant_var += 2
            
        self.textbox_dictionary_grid = {}
        for row, y_ratio in individual_textbox_place_ratio_y.items():
            temp_dict = {}
            for column, x_ratio in individual_textbox_place_ratio_x.items():
                temp_dict[column] = [x_ratio, y_ratio]
                
            self.textbox_dictionary_grid[row] = temp_dict
                
        actual_grid_wh_radius = [initial_window_size[0] * grid_wh_ratio[0] / 2, initial_window_size[1] * grid_wh_ratio[1] / 2]
        actual_grid_wh = [initial_window_size[0] * grid_wh_ratio[0], initial_window_size[1] * grid_wh_ratio[1]]
        actual_grid_position_topleft = [int((initial_window_size[0] * position_ratio[0]) - actual_grid_wh_radius[0]), int((initial_window_size[1] * position_ratio[1]) - actual_grid_wh_radius[1])]
        textbox_wh_ratio = [int(initial_window_size[0] / (actual_grid_wh_radius[0] * 2) * size[0]), int(initial_window_size[1] / (actual_grid_wh_radius[1] * 2) * size[1])]
                
        tries = self.num_of_textboxes
        for row_number, row in self.textbox_dictionary_grid.items():
            for column_number, position_ratio_individual_grid_object in row.items():
                if tries > 0:
                    textbox_position = [actual_grid_position_topleft[0] + (actual_grid_wh[0] * position_ratio_individual_grid_object[0]), actual_grid_position_topleft[1] + (actual_grid_wh[1] * position_ratio_individual_grid_object[1])]
                    textbox_position_ratio = [textbox_position[0] / initial_window_size[0], textbox_position[1] / initial_window_size[1]]
                    
                    concatenated_name = gridname + str(column_number) + str(row_number)
                    self.textboxes[concatenated_name] = TextBox(textbox_position_ratio, initial_window_size, textbox_wh_ratio, concatenated_name, level, radius=10, accepted_chars=accepted_chars, length_limit=charlimit)
                    tries -= 1
                
    def export_grid_textboxes(self, dict):
        for name, textbox in self.textboxes.items():
            dict[name] = textbox
            
    def reinit(self, initial_window_size: list[int, int], size: list[int, int], num_of_textboxes: int, grid_wh_ratio: list[float, float], dict: dict):
        self.num_of_textboxes = num_of_textboxes
        self.grid_size = size
        self.grid_wh_ratio = grid_wh_ratio
        self.textboxes = {}
        
        objects_for_deletion = []
        for name, obj in dict.items():
            if self.gridname in name:
                objects_for_deletion.append(name)
        
        for names in objects_for_deletion:
            del dict[names]
            
        
        individual_textbox_place_ratio_x = {}
        iterant_var = 1
        while (iterant_var/(size[0] * 2)) < 1:
            individual_textbox_place_ratio_x[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[0] * 2)))
            
            iterant_var += 2
            
        individual_textbox_place_ratio_y = {}
        iterant_var = 1
        while (iterant_var/(size[1] * 2)) < 1:
            individual_textbox_place_ratio_y[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[1] * 2)))
            
            iterant_var += 2
            
        self.textbox_dictionary_grid = {}
        for row, y_ratio in individual_textbox_place_ratio_y.items():
            temp_dict = {}
            for column, x_ratio in individual_textbox_place_ratio_x.items():
                temp_dict[column] = [x_ratio, y_ratio]
                
            self.textbox_dictionary_grid[row] = temp_dict
                
        actual_grid_wh_radius = [initial_window_size[0] * grid_wh_ratio[0] / 2, initial_window_size[1] * grid_wh_ratio[1] / 2]
        actual_grid_wh = [initial_window_size[0] * grid_wh_ratio[0], initial_window_size[1] * grid_wh_ratio[1]]
        actual_grid_position_topleft = [int((initial_window_size[0] * self.position_ratio[0]) - actual_grid_wh_radius[0]), int((initial_window_size[1] * self.position_ratio[1]) - actual_grid_wh_radius[1])]
        textbox_wh_ratio = [int(initial_window_size[0] / (actual_grid_wh_radius[0] * 2) * size[0]), int(initial_window_size[1] / (actual_grid_wh_radius[1] * 2) * size[1])]
        
        tries = self.num_of_textboxes
        for row_number, row in self.textbox_dictionary_grid.items():
            for column_number, position_ratio_individual_grid_object in row.items():
                if tries > 0:
                    textbox_position = [actual_grid_position_topleft[0] + (actual_grid_wh[0] * position_ratio_individual_grid_object[0]), actual_grid_position_topleft[1] + (actual_grid_wh[1] * position_ratio_individual_grid_object[1])]
                    textbox_position_ratio = [textbox_position[0] / initial_window_size[0], textbox_position[1] / initial_window_size[1]]
                    
                    concatenated_name = self.gridname + str(column_number) + str(row_number)
                    self.textboxes[concatenated_name] = TextBox(textbox_position_ratio, initial_window_size, textbox_wh_ratio, concatenated_name, self.level, radius=10, accepted_chars=self.accepted_chars, length_limit=self.length_limit)
                    tries -= 1
                    
        self.export_grid_textboxes(dict)


class EntityButtonGrid:
    def __init__(self, initial_window_size, position_ratio: list[float, float], size: list[int, int], entities: dict, grid_wh_ratio: list[float, float], level: int, gridname: str, dict: dict):
        self.grid_size = size
        self.position_ratio = position_ratio
        self.buttons = {}
        self.level = level
        self.gridname = gridname
        self.grid_wh_ratio = grid_wh_ratio
        self.num_of_buttons = len(entities.values())
    
        
        individual_textbox_place_ratio_x = {}
        iterant_var = 1
        while (iterant_var/(size[0] * 2)) < 1:
            individual_textbox_place_ratio_x[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[0] * 2)))
            
            iterant_var += 2
            
        individual_textbox_place_ratio_y = {}
        iterant_var = 1
        while (iterant_var/(size[1] * 2)) < 1:
            individual_textbox_place_ratio_y[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[1] * 2)))
            
            iterant_var += 2
            
        self.button_dictionary_grid = {}
        for row, y_ratio in individual_textbox_place_ratio_y.items():
            temp_dict = {}
            for column, x_ratio in individual_textbox_place_ratio_x.items():
                temp_dict[column] = [x_ratio, y_ratio]
                
            self.button_dictionary_grid[row] = temp_dict
                
        actual_grid_wh_radius = [initial_window_size[0] * grid_wh_ratio[0] / 2, initial_window_size[1] * grid_wh_ratio[1] / 2]
        
        
        
        actual_grid_wh = [initial_window_size[0] * grid_wh_ratio[0], initial_window_size[1] * grid_wh_ratio[1]]
        
        actual_grid_position_topleft = [int((initial_window_size[0] * position_ratio[0]) - actual_grid_wh_radius[0]), int((initial_window_size[1] * position_ratio[1]) - actual_grid_wh_radius[1])]
        textbox_wh_ratio = [int(initial_window_size[0] / (actual_grid_wh_radius[0] * 2) * size[0]), int(initial_window_size[1] / (actual_grid_wh_radius[1] * 2) * size[1])]
                
        tries = self.num_of_buttons
        
        names = list(entities.keys())
        
        for row_number, row in self.button_dictionary_grid.items():
            for column_number, position_ratio_individual_grid_object in row.items():
                if tries > 0:
                    textbox_position = [actual_grid_position_topleft[0] + (actual_grid_wh[0] * position_ratio_individual_grid_object[0]), actual_grid_position_topleft[1] + (actual_grid_wh[1] * position_ratio_individual_grid_object[1])]
                    textbox_position_ratio = [textbox_position[0] / initial_window_size[0], textbox_position[1] / initial_window_size[1]]
                    
                    concatenated_name = names.pop(0)
                    
                    
                    self.buttons[concatenated_name] = Button(textbox_position_ratio, initial_window_size, textbox_wh_ratio, concatenated_name, concatenated_name, "entity", self.level, radius=10,)
                    tries -= 1
                    
        for name, button in self.buttons.items():
            dict[name] = button
                
    def export_grid_buttons(self, dict):
        for name, button in self.buttons.items():
            dict[name] = button
            
    def reinit(self, initial_window_size: list[int, int], size: list[int, int], grid_wh_ratio: list[float, float], dict: dict, entities: dict):
        self.grid_size = size
        self.num_of_buttons = len(entities.values())
        self.grid_wh_ratio = grid_wh_ratio
        self.buttons = {}
        
        try:
            for name in list(entities.keys()):
                del dict[str(name)]
                
        except:
            pass
        
        individual_textbox_place_ratio_x = {}
        iterant_var = 1
        while (iterant_var/(size[0] * 2)) < 1:
            individual_textbox_place_ratio_x[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[0] * 2)))
            
            iterant_var += 2
            
        individual_textbox_place_ratio_y = {}
        iterant_var = 1
        while (iterant_var/(size[1] * 2)) < 1:
            individual_textbox_place_ratio_y[int((iterant_var - 1) / 2)] = (float(iterant_var/(size[1] * 2)))
            
            iterant_var += 2
            
        self.button_dictionary_grid = {}
        for row, y_ratio in individual_textbox_place_ratio_y.items():
            temp_dict = {}
            for column, x_ratio in individual_textbox_place_ratio_x.items():
                temp_dict[column] = [x_ratio, y_ratio]
                
            self.button_dictionary_grid[row] = temp_dict
                
        actual_grid_wh_radius = [initial_window_size[0] * grid_wh_ratio[0] / 2, initial_window_size[1] * grid_wh_ratio[1] / 2]
        actual_grid_wh = [initial_window_size[0] * grid_wh_ratio[0], initial_window_size[1] * grid_wh_ratio[1]]
        actual_grid_position_topleft = [int((initial_window_size[0] * self.position_ratio[0]) - actual_grid_wh_radius[0]), int((initial_window_size[1] * self.position_ratio[1]) - actual_grid_wh_radius[1])]
        textbox_wh_ratio = [int(initial_window_size[0] / (actual_grid_wh_radius[0] * 2) * size[0]), int(initial_window_size[1] / (actual_grid_wh_radius[1] * 2) * size[1])]
                
        tries = self.num_of_buttons
        
        names = list(entities.keys())
        
        for row_number, row in self.button_dictionary_grid.items():
            for column_number, position_ratio_individual_grid_object in row.items():
                if tries > 0:
                    textbox_position = [actual_grid_position_topleft[0] + (actual_grid_wh[0] * position_ratio_individual_grid_object[0]), actual_grid_position_topleft[1] + (actual_grid_wh[1] * position_ratio_individual_grid_object[1])]
                    textbox_position_ratio = [textbox_position[0] / initial_window_size[0], textbox_position[1] / initial_window_size[1]]
                    
                    concatenated_name = str(names.pop(0))
                    self.buttons[concatenated_name] = Button(textbox_position_ratio, initial_window_size, textbox_wh_ratio, concatenated_name, concatenated_name, "entity", self.level, radius=10)
                    tries -= 1
                    
        self.export_grid_buttons(dict)


class MenuPanel:
    def __init__(self, position_ratio: list[float, float], initial_window_size: list[int, int], width_height_ratio: list[int, int], level: int, radius=0):
        self.position_ratio_w_h = position_ratio
        self.position = [initial_window_size[0] * position_ratio[0], initial_window_size[1] * position_ratio[1]]
        self.panel_rect = pygame.Rect([self.position[0] - (initial_window_size[0] / width_height_ratio[0] / 2), self.position[1] - (initial_window_size[1] / width_height_ratio[1] / 2)], [initial_window_size[0] / width_height_ratio[0], initial_window_size[1] / width_height_ratio[1]])
        self.width_height_ratio = width_height_ratio
        self.level = level
        self.radius = radius
        
    def resize_and_reposition(self, window_size: list[int, int]):
        self.panel_rect.width = window_size[0] / self.width_height_ratio[0]
        self.panel_rect.height = window_size[1] / self.width_height_ratio[1]
        
        self.panel_rect.center = (window_size[0] * self.position_ratio_w_h[0], window_size[1] * self.position_ratio_w_h[1])
        
    def blit(self, surface, hover=False):
            if hover:
                pygame.draw.rect(surface, (180, 180, 198), self.panel_rect, border_radius=self.radius)
                    
            else:
                pygame.draw.rect(surface, (200, 200, 220), self.panel_rect, border_radius=self.radius)
                
            pygame.draw.rect(surface, (100, 100, 110), self.panel_rect, width=5, border_radius=self.radius)
            

class ImageObject:
    def __init__(self, initial_image_path: str, position_ratio: list[float, float], width_height_ratio: list[float, float], initial_window_size: list[int, int], level: int, is_square=False, has_hover_textbox=False, hover_textbox_text=[""]):
        self.image_path = initial_image_path
        self.position_ratio = position_ratio
        self.position = [initial_window_size[0] * position_ratio[0], initial_window_size[1] * position_ratio[1]]
        self.width_height_ratio = width_height_ratio
        self.level = level
        
        self.is_square = is_square
        
        self.has_hover_textbox = has_hover_textbox
        self.hover_textbox_text = hover_textbox_text
        
        if self.is_square:
            self.loaded_image = pygame.transform.scale(pygame.image.load(self.image_path), (initial_window_size[1] * width_height_ratio[1], initial_window_size[1] * width_height_ratio[1]))
        
        else:
            self.loaded_image = pygame.transform.scale(pygame.image.load(self.image_path), (initial_window_size[0] * width_height_ratio[0], initial_window_size[1] * width_height_ratio[1]))
        
    def resize_and_reposition(self, window_size, new_image_path = ""):
        if new_image_path != "":
            self.image_path = new_image_path
            
        else:
            pass
        
        self.position = [window_size[0] * self.position_ratio[0], window_size[1] * self.position_ratio[1]]
        
        if self.is_square:
            self.loaded_image = pygame.transform.scale(pygame.image.load(self.image_path), (window_size[1] * self.width_height_ratio[1], window_size[1] * self.width_height_ratio[1]))

        else:
            self.loaded_image = pygame.transform.scale(pygame.image.load(self.image_path), (window_size[0] * self.width_height_ratio[0], window_size[1] * self.width_height_ratio[1]))
        
    def blit(self, surface):
        image_rect = self.loaded_image.get_rect()
        
        image_rect.center = self.position
        
        surface.blit(self.loaded_image, (image_rect.x, image_rect.y))
        
        
class MenuRect:
    def __init__(self, position_ratio: list[float, float], width_height_ratio: list[float, float], initial_window_size: list[int, int], level: int, fill: bool, stroke: bool, fill_color: list[int, int, int], stroke_color: list[int, int, int], is_square=False, has_hover_textbox=False, hover_textbox_text=[""]):
        self.position_ratio = position_ratio
        self.width_height_ratio = width_height_ratio
        self.is_square = is_square
        self.position = [initial_window_size[0] * position_ratio[0], initial_window_size[1] * position_ratio[1]]
        
        if self.is_square:
            if initial_window_size[0] > initial_window_size[1]:
                self.width_height = [initial_window_size[1] * width_height_ratio[1], initial_window_size[1] * width_height_ratio[1]]
                
            else:
                self.width_height = [initial_window_size[0] * width_height_ratio[0], initial_window_size[0] * width_height_ratio[0]]
            
        else:
            self.width_height = [initial_window_size[0] * width_height_ratio[0], initial_window_size[1] * width_height_ratio[1]]
            
        self.fill = fill
        self.stroke = stroke
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.level = level
        
        self.rect = pygame.Rect(0, 0, self.width_height[0], self.width_height[1])
        self.rect.center = self.position
        
        self.has_hover_textbox = has_hover_textbox
        self.hover_textbox_text = hover_textbox_text
        
    def resize_and_reposition(self, window_size, new_fill=None, new_fill_color=None, new_stroke=None, new_stroke_color=None, new_hover_textbox_text=None):     
        if new_fill != None:
            self.fill = new_fill
        
        if new_fill_color != None:
            self.fill_color = new_fill_color
            
        if new_stroke != None:
            self.stroke = new_stroke
            
        if new_stroke_color != None:
            self.stroke_color = new_stroke_color
            
        if new_hover_textbox_text != None:
            self.hover_textbox_text = new_hover_textbox_text
        
        self.position = [window_size[0] * self.position_ratio[0], window_size[1] * self.position_ratio[1]]
        if self.is_square:
            if window_size[0] > window_size[1]:
                self.width_height = [window_size[1] * self.width_height_ratio[1], window_size[1] * self.width_height_ratio[1]]
                
            else:
                self.width_height = [window_size[0] * self.width_height_ratio[0], window_size[0] * self.width_height_ratio[0]]
                
        else:
            self.width_height = [window_size[0] * self.width_height_ratio[0], window_size[1] * self.width_height_ratio[1]]
        
        self.rect.width = self.width_height[0]
        self.rect.height = self.width_height[1]
        self.rect.center = self.position
        
    def blit(self, gameframeself):
        if self.stroke:
            if self.fill:
                pygame.draw.rect(gameframeself.gamescreen, self.fill_color, self.rect)
            
            list_copy = self.width_height
            list_copy.sort()
            stroke_width = int(list_copy[0] * .1)
            
            pygame.draw.rect(gameframeself.gamescreen, self.stroke_color, self.rect, width=stroke_width)
            
        elif self.fill:
                pygame.draw.rect(gameframeself.gamescreen, self.fill_color, self.rect)


class HoverTextBox:
    def __init__(self, font_size_ratio: float, placeholder_text: str, initial_window_size: list[int, int], accepted_object_names: list, font="twcen"):
        self.position = [0, 0]
        self.font_size_ratio = font_size_ratio
        self.placeholder_text = placeholder_text
        self.current_text = [placeholder_text]
        self.object_selected = ""
        self.font_object = pygame.font.SysFont(font, int(initial_window_size[1] * self.font_size_ratio),)
        self.rendered_text = []
        self.render_text_list()
        self.objects_with_hover_textboxes = accepted_object_names
        self.visible = False
        
    def render_text_list(self):
        self.rendered_text = []
        for text in self.current_text:
            self.rendered_text.append(self.font_object.render(text, False, (255, 255, 255)))
        
    def resize_and_change_font(self, window_size: list[int, int], new_font="twcen", new_font_size_ratio=None):
        try:
            if new_font_size_ratio != None:
                self.font_size_ratio = float(new_font_size_ratio)
                self.font_object = pygame.font.SysFont(new_font, int(window_size[1] * self.font_size_ratio),)
                
            else:
                self.font_object = pygame.font.SysFont(new_font, int(window_size[1] * self.font_size_ratio),)
                
        except:
            self.font_object = pygame.font.SysFont(new_font, int(window_size[1] * self.font_size_ratio),)
            
        self.render_text_list()
        
    def check_selection(self, gameframeself, override=False):
        if (gameframeself.menu.mouse_in_menu[0] == True and self.object_selected != gameframeself.menu.mouse_in_menu[1]) or override == True:
            self.object_selected = gameframeself.menu.mouse_in_menu[1]
            if self.object_selected in self.objects_with_hover_textboxes:
                self.visible = True
                
            else:
                self.visible = False
                
            if self.visible:
                try:
                    selected_object_rect = gameframeself.menu.buttons[self.object_selected].button_rect.copy()
                    if gameframeself.menu.buttons[self.object_selected].hover_textbox_text:
                        self.current_text = gameframeself.menu.buttons[self.object_selected].hover_textbox_text
                        
                    else:
                        self.visible = False
                        self.current_text = [self.placeholder_text]                
                    
                except KeyError:
                    try:
                        selected_object_rect = gameframeself.menu.rects[self.object_selected].rect.copy()
                        if gameframeself.menu.rects[self.object_selected].hover_textbox_text:
                            self.current_text = gameframeself.menu.rects[self.object_selected].hover_textbox_text
                        
                        else:
                            self.visible = False
                            self.current_text = self.placeholder_text
                        
                    except KeyError:
                        try:
                            selected_object_rect = gameframeself.menu.images[self.object_selected].loaded_image.get_rect()
                            selected_object_rect.center = gameframeself.menu.images[self.object_selected].position
                            if gameframeself.menu.images[self.object_selected].hover_textbox_text:
                                self.current_text = gameframeself.menu.images[self.object_selected].hover_textbox_text
                                
                            else:
                                self.visible = False
                                self.current_text = self.placeholder_text
                            
                        except:
                            selected_object_rect = None
                            self.visible = False
                            
            if self.visible == True and selected_object_rect != None:
                self.resize_and_change_font(gameframeself.gamescreen.get_size())
                
                text_rect = self.get_rect_size(gameframeself)
                text_rect.midtop = selected_object_rect.midbottom
                
                self.position = [text_rect.x, text_rect.y]
                
    def get_rect_size(self, gameframeself):
        biggest_width = 0
        height = 0
        for object in self.rendered_text:
            object = object.get_rect()
            if object.width > biggest_width:
                biggest_width = object.width
                
            height += object.height
            
        return pygame.Rect(self.position[0], self.position[1], biggest_width, height)
        
    
    def blit(self, gameframeself):
        self.check_selection(gameframeself)
        if self.visible:
            text_rect = self.get_rect_size(gameframeself)
            
            pygame.draw.rect(gameframeself.gamescreen, (100, 100, 110), text_rect, border_radius=int(text_rect.height / 5))

            start_midtop_pos = text_rect.midtop
            for object in self.rendered_text:
                temp_rect = object.get_rect()
                
                temp_rect.midtop = start_midtop_pos
                start_midtop_pos = temp_rect.midbottom
                
                gameframeself.gamescreen.blit(object, (temp_rect.x, temp_rect.y))