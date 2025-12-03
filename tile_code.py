import pygame
from random import randint
import math

class Tile:
    def __init__(self, x: int, y: int, width: int, height: int, edges: dict, type: str):
        self.location = [x, y]
        self.dimensions = [width, height]
        self.type = type
        self.neighbors = self.get_neighbors(edges)
        self.tile_occupants = []
        self.occupant_limit = 2
        self.entity_occupied = False
        self.enemy_occupied = False
        self.color = self.determine_color(update=False)
        self.outline_size = int(math.sqrt(self.dimensions[0] * self.dimensions[1]) / 20)
        
        if self.outline_size == 0:
            self.outline_size = 1
        
        self.gen_bias = self.determine_bias()
        self.gen_unbias = self.determine_bias(self.gen_bias)
        
        
    def update_type(self, type: str):
        self.type = type
        self.determine_color()
        
    def determine_bias(self, opposite=None):
        random = randint(1, 4)
        if opposite == None:
            if random == 1:
                return "n"
            
            elif random == 2:
                return "s"
            
            elif random == 3:
                return "e"
            
            else:
                return "w"
            
        elif opposite == "n":
            return "s"
        
        elif opposite == "s":
            return "n"
        
        elif opposite == "e":
            return "w"
        
        else:
            return "e"
        
    def determine_color(self, update=True):
        if self.type == "b":
            rgb = randint(120, 180)
            color = (rgb, rgb, rgb)
        
        elif self.type == "w":
            color = (0, randint(100, 110), randint(200, 220))
            
        elif self.type == "d":
            color = (187, randint(78, 98), randint(52, 62))
        
        elif self.type == "g":
            color = (50, randint(150, 172), randint(30, 70))
            
        elif self.type == "h":
            color = (60, randint(134, 142), randint(80, 100))
        
        else:
            color = (0, 0, 0)
            
        if update:
            self.color = color
            
        else:
            return color
        
    def add_occupants(self, occupants: list):
        if len(self.tile_occupants) < self.occupant_limit:
            for occupant in occupants:
                if len(self.tile_occupants) >= self.occupant_limit:
                    return False
                
                self.tile_occupants.append(occupant)
                
        else:
            return False
            
    def get_neighbors(self, on_edge):
        neighbors = {"n": None, "s": None, "e": None, "w": None}
        
        if on_edge["n"]:
            if on_edge["e"]:
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
                
            elif on_edge["w"]:
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                
            else:
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
            
        elif on_edge["s"]:
            if on_edge["e"]:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
                
            elif on_edge["w"]:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                
            else:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
                
        else:
            if on_edge["w"]:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                
            elif on_edge["e"]:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
                
            else:
                neighbors["n"] = [self.location[0], self.location[1] - 1]
                neighbors["s"] = [self.location[0], self.location[1] + 1]
                neighbors["e"] = [self.location[0] + 1, self.location[1]]
                neighbors["w"] = [self.location[0] - 1, self.location[1]]
                
        return neighbors
    
    def update_occupants(self, surface, position_and_dimension_data, gameframeself, selected=False):
        number_of_occupants = len(self.tile_occupants)
        for num, occupant in enumerate(self.tile_occupants):
            invididual_position_and_dimension_data = ((position_and_dimension_data[0][0] + (num * (position_and_dimension_data[1][0] / number_of_occupants)), (position_and_dimension_data[0][1])), (position_and_dimension_data[1][0] / number_of_occupants, position_and_dimension_data[1][1] / number_of_occupants))
            occupant.update(gameframeself)
            occupant.blit(surface, invididual_position_and_dimension_data[0], invididual_position_and_dimension_data[1])
        
    def blit(self, surface, offset: list[int, int], viewscale: float, tile_spread, selected=False):
        position_and_dimension_data = ((offset[0] + (self.location[0] * self.dimensions[0] * viewscale),
                                        offset[1] + (self.location[1] * self.dimensions[1] * viewscale)),
                                        (self.dimensions[0] * viewscale, self.dimensions[1] * viewscale))
                        
        pygame.draw.rect(surface, self.color, position_and_dimension_data)
        number_of_occupants = len(self.tile_occupants)
        
        occupants_to_delete = []
        for num, occupant in enumerate(self.tile_occupants):
            if occupant.health <= 0:
                occupants_to_delete.append(num)
                
            
            else:
                invididual_position_and_dimension_data = ((position_and_dimension_data[0][0] + (num * (position_and_dimension_data[1][0] / number_of_occupants)), (position_and_dimension_data[0][1])), (position_and_dimension_data[1][0] / number_of_occupants, position_and_dimension_data[1][1] / number_of_occupants))
                occupant.blit(surface, invididual_position_and_dimension_data[0], invididual_position_and_dimension_data[1])
                
        while len(occupants_to_delete) > 0:
            self.tile_occupants.pop(occupants_to_delete[-1])
            occupants_to_delete.pop(-1)
        
        if selected:
            pygame.draw.rect(surface, (255, 255, 255), position_and_dimension_data, width=int((self.outline_size * viewscale)))