import pygame
import math
import gameframe_code
import menu_code
from random import randint
import os

os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.init()

window_dimensions = [1000, 1000]
                
game_frame = gameframe_code.GameFrame(window_dimensions)

clock = pygame.time.Clock()

map_tick_event = pygame.USEREVENT + 1
pygame.time.set_timer(map_tick_event, 20)

entity_tick_event = pygame.USEREVENT + 2
pygame.time.set_timer(entity_tick_event, 200)
          
try:
    game_frame.blit()
    running = True
    
except:
    pass
    running = True

while (running):
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        
        if game_frame.pause_state == 0:  
            if keys[pygame.K_UP]:
                game_frame.updateview('n')
                
            elif keys[pygame.K_DOWN]:
                game_frame.updateview('s')
                
            if keys[pygame.K_RIGHT]:
                game_frame.updateview('w')
                
            elif keys[pygame.K_LEFT]:
                game_frame.updateview('e')

            if keys[pygame.K_s]:
                type = randint(0, 4)
                mushrooms = ["toadstool", "oyster", "psilocybe", "portobello", "morel"]
                starting_pos = [randint(0, game_frame.generation.dimensions[0] - 1), randint(0, game_frame.generation.dimensions[1] - 1)]
                game_frame.player.spawn_entity(mushrooms[type], game_frame.generation.tile_dimensions, starting_pos)
                
            if game_frame.menu.in_text_box == None:
                if keys[pygame.K_r]:
                    game_frame.updateview('r')
                    
                if keys[pygame.K_EQUALS]:
                    game_frame.updateview('+')
                    
                elif keys[pygame.K_MINUS]:
                    game_frame.updateview('-')

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.VIDEORESIZE:
                game_frame.blit()
                
            if event.type == pygame.KEYDOWN:
                for textbox in game_frame.menu.textboxes.values():
                    if textbox.actively_typing:
                        textbox.add_chars(pygame.key.name(event.key), game_frame.gamescreen.get_size())
                        if pygame.key.name(event.key) == "return":
                            game_frame.menu.in_text_box = None
                        
                if pygame.key.name(event.key) == "backspace" and game_frame.menu.in_text_box != None:
                    game_frame.menu.menulevel = 0
            
            if event.type == map_tick_event:
                game_frame.tick()
                            
            if event.type == entity_tick_event:
                game_frame.tick_entities()
                
            # Mouse Stuff
            if game_frame.menu.mouse_in_menu[0] == False:
                if event.type == pygame.MOUSEBUTTONDOWN and keys[pygame.K_LALT]:
                    game_frame.update_clicked(mouse_button_action = "down")
                                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game_frame.menu.mouse_in_menu[0]:
                        pass
                        
                    else:
                        game_frame.select()
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    game_frame.update_clicked()
                    game_frame.update_clicked(mouse_button_action = "up")
                        
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_frame.menu.clicked(game_frame.gamescreen, game_frame.player, game_frame)
                    
        game_frame.blit_overlay()
        clock.tick(60)
        pygame.display.flip()
        
pygame.quit()