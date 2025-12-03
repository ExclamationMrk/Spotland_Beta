import pygame

def initialisation_function(self, tool):
    if tool == "stone_pickaxe":
        self.type = "mining"
        self.damage = 2
        self.name = "Stone Pickaxe"
        self.tier = 1
        self.image = pygame.image.load("images\items/tools\pickaxe_stone.png")
        self.func = pickaxe
        
    else:
        self.type = None
        self.damage = 1
        self.name = "Hand"
        self.tier = 1
        self.image = ""
        self.func = hand
        
class ToolTemplate:
    def __init__(self, tool):
        self.damage = 1
        self.name = ""
        self.attacking = False
        self.type = None      # ex "logging", "mining", None, 
        self.tier = 1
        self.image = ""
        self.func = ""
        self.attack_range = 1
        
        initialisation_function(self=self, tool=tool)
        

#Non attacking returns resources, while attacking returns tiles hit with attack
def hand(self, parentself, tile_spread, target_tile):
    resources_gained = [[], False]
    
    if "attacking" not in parentself.focus:
        try:
            if tile_spread[target_tile[1]][target_tile[0]].tile_occupants[0].natural:
                resources_gained = tile_spread[target_tile[1]][target_tile[0]].tile_occupants[0].on_hit(self, float(parentself.strength))
                
                if resources_gained[1] == False:
                    if tile_spread[target_tile[1]][target_tile[0]].tile_occupants[1].natural:
                        resources_gained = tile_spread[target_tile[1]][target_tile[0]].tile_occupants[1].on_hit(self, float(parentself.strength))
                
                    return resources_gained
                
                else:
                    return resources_gained
                
            else:
                return resources_gained
        
        except IndexError:
            return resources_gained
        
    else:
        return [target_tile]
    
def pickaxe(self, parentself, tile_spread, target_tile):
    resources_gained = [[], False]
    
    if "attacking" not in parentself.focus:
        try:
            if tile_spread[target_tile[1]][target_tile[0]].tile_occupants[0].natural:
                resources_gained = tile_spread[target_tile[1]][target_tile[0]].tile_occupants[0].on_hit(tool=self, strength=float(parentself.strength))
                
                if resources_gained[1] == False:
                    if tile_spread[target_tile[1]][target_tile[0]].tile_occupants[1].natural:
                        resources_gained = tile_spread[target_tile[1]][target_tile[0]].tile_occupants[1].on_hit(self, float(parentself.strength))
                
                    return resources_gained
                
                else:
                    return resources_gained
                
            else:
                return resources_gained
    
        except IndexError:
            return resources_gained
        
    else:
        return [target_tile]
    