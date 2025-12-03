from random import randint
import pygame
        
def initialisation_function(occupant_id, self):
    if occupant_id == "tree":
        self.health = randint(10, 13)
        self.max_health = self.health
        self.name = "Tree"
        self.drop_items = {"wood": [2, randint(1, 2)], "sapling": [randint(1, 2), randint(1, 2)]}
        self.on_hit_drop_items = {"wood": [2, 1]}
        self.tool_needed = "logging"
        self.tier_needed = 1
        self.func = tree
        self.walkable = True
        
        tree_image = str(randint(1, 5))
        if self.biome_type == "g":
            concatenated_string = "images/tile_occupants/trees/chestnut_tree-0" + tree_image + ".png"
            self.image = pygame.image.load(concatenated_string)
            
        elif self.biome_type == "h":
            concatenated_string = "images/tile_occupants/trees/evergreen_tree-0" + tree_image + ".png"
            self.image = pygame.image.load(concatenated_string)
            
        elif self.biome_type == "d":
            concatenated_string = "images/tile_occupants/trees/cactus-0" + tree_image + ".png"
            self.image = pygame.image.load(concatenated_string)
        
        else:
            pass
            
    elif occupant_id == "sapling":
        self.health = randint(1, 3)
        self.max_health = self.health
        self.name = "Sapling"
        self.drop_items = {"sapling": [1, 1]}
        self.func = sapling
        self.walkable = True
        
        if self.biome_type == "g":
            self.image = pygame.image.load("images/tile_occupants/trees/chestnut_tree-06.png")
            
        elif self.biome_type == "h":
            self.image = pygame.image.load("images/tile_occupants/trees/evergreen_tree-06.png")
            
        elif self.biome_type == "d":
            self.image = pygame.image.load("images/tile_occupants/trees/cactus-06.png")
        
        else:
            pass
        
    elif occupant_id == "rock":
        self.health = randint(10, 20)
        self.max_health = self.health
        self.name = "Rock"
        self.drop_items = {"stone": [2, 5], "copper": [1, 1], "iron": [3, 1]}
        self.on_hit_drop_items = {"stone": [2, 1], "copper": [10, 1], "iron": [10, 1]}
        self.func = rock
        self.tier_needed = 1
        self.tool_needed = "mining"
        self.walkable = False
    
        if randint(1, 1000) == 1:
            self.image = pygame.image.load("images/tile_occupants/rock-related/rock-04.png")
            
        else:
            image = randint(1, 3)
            concatenated_string = "images/tile_occupants/rock-related/rock-0" + str(image) + ".png"
            self.image = pygame.image.load(concatenated_string)
            
    elif occupant_id == "toadstool_corpse":
        self.health = 1
        self.max_health = 1
        self.name = "Corpse"
        self.drop_items = {"spore": [1, 1]}
        self.func = item
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/blood/toadstool_corpse.png")
        
    elif occupant_id == "oyster_corpse":
        self.health = 1
        self.max_health = 1
        self.name = "Corpse"
        self.drop_items = {"spore": [1, 1]}
        self.func = item
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/blood/oyster_corpse.png")
        
    elif occupant_id == "psilocybe_corpse":
        self.health = 1
        self.max_health = 1
        self.name = "Corpse"
        self.drop_items = {"spore": [1, 1]}
        self.func = item
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/blood/psilocybe_corpse.png")
        
    elif occupant_id == "portobello_corpse":
        self.health = 1
        self.max_health = 1
        self.name = "Corpse"
        self.drop_items = {"spore": [1, 1]}
        self.func = item
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = False
        self.image = pygame.image.load("images\entities\mushrooms/blood/portobello_corpse.png")
        
    elif occupant_id == "morel_corpse":
        self.health = 1
        self.max_health = 1
        self.name = "Corpse"
        self.drop_items = {"morel_spore": [1, 1]}
        self.func = item
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/blood/morel_corpse.png")
         
    elif occupant_id == "toadstool_spore":
        self.health = 1
        self.max_health = 1
        self.name = "Toadstool Spore"
        self.drop_items = {}
        self.spore_type = 0
        self.func = spore
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/spores/mushroom_spore_toadstool.png")
        
    elif occupant_id == "oyster_spore":
        self.health = 1
        self.max_health = 1
        self.name = "Oyster Spore"
        self.drop_items = {}
        self.spore_type = 1
        self.func = spore
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/spores/mushroom_spore_oyster.png")
        
    elif occupant_id == "psilocybe_spore":
        self.health = 1
        self.max_health = 1
        self.name = "Psilocybe Spore"
        self.drop_items = {}
        self.spore_type = 2
        self.func = spore
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/spores/mushroom_spore_psilocybe.png")
        
    elif occupant_id == "portobello_spore":
        self.health = 1
        self.max_health = 1
        self.name = "Portobello Spore"
        self.drop_items = {}
        self.spore_type = 3
        self.func = spore
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/spores/mushroom_spore_portobello.png")
        
    elif occupant_id == "morel_spore":
        self.health = 1
        self.max_health = 1
        self.name = "Morel Spore"
        self.drop_items = {}
        self.spore_type = 4
        self.func = spore
        self.tier_needed = 1
        self.tool_needed = None
        self.walkable = True
        self.image = pygame.image.load("images\entities\mushrooms/spores/mushroom_spore_morel.png")
            
    else:
        self.health = 1
        self.max_health = self.health
        self.name = str(occupant_id).upper()
        self.drop_items = {str(occupant_id): [1, 1]}
        self.on_hit_drop_items = {}
        self.func = item
        self.tier_needed = 0
        self.tool_needed = None
        self.walkable = True
        
        try:
            concatenated_string = "images\items\inventory_items/" + occupant_id + ".png"
            self.image = pygame.image.load(concatenated_string)
            
            
        except:
            self.image = pygame.image.load("images\items\inventory_items/building.png")

class OccupantTemplate:
    def __init__(self, occupant_id: str, parent_tile_object, initialisation_function=initialisation_function):
        self.occupant_id = occupant_id
        self.name = ""
        self.image = ""
        self.func = ""
        self.age = 0
        self.max_health = 0
        self.health = 0
        self.tool_needed = None
        self.tier_needed = 1
        self.biome_type = parent_tile_object.type
        self.walkable = True
        self.natural = True
        self.drop_items = {} # {item index: [1/chance, num]}
        self.on_hit_drop_items = {} # {item index: [1/chance, num]}
        
        initialisation_function(occupant_id, self=self)
        
    def on_hit(self, tool, strength: float):
        if (self.tool_needed == None) or (tool.type == self.tool_needed and tool.tier >= self.tier_needed):
            self.health -= (tool.damage * strength)
            items_dropped = [[], False]
            
            if self.health > 0:
                for item, [chance, amount] in self.on_hit_drop_items.items():
                    while amount > 0:
                        if randint(1, chance) == 1:
                            items_dropped[0].append(item)
                            
                        amount -= 1
                        
                items_dropped[1] = True
                        
            else:
                for item, [chance, amount] in self.drop_items.items():
                    while amount > 0:
                        if randint(1, chance) == 1:
                            items_dropped[0].append(item)
                            
                        amount -= 1
                        
                
                items_dropped[1] = True
                    
            return items_dropped
        
        else:
            return [[], False]
        
    def update(self, gameframeself):
        self.func(self, gameframeself)
        
    def blit(self, surface, tile_top_left_pos: list[int, int], tile_size: list[int, int]):
        loaded_image = pygame.transform.scale(self.image, tile_size)
        surface.blit(loaded_image, tile_top_left_pos)
        

def tree(self, gameframeself):
    self.age += 1
        
def sapling(self, gameframeself):
    self.age += 1
    
    if self.age > 2:
        self.id = "tree"
        initialisation_function("tree", self=self)
        
def rock(self, gameframeself):
    self.age += 1
    
def item(self, gameframeself):
    self.age += 1
    
def spore(self, gameframeself):
    self.age += 1
    
    if self.age > 2:
        mushrooms = ["toadstool", "oyster", "psilocybe", "portobello", "morel"]
        gameframeself.player.spawn_entity(mushrooms[self.spore_type], [gameframeself.generation.tile_dimensions[0] * gameframeself.viewscale, gameframeself.generation.tile_dimensions[1] * gameframeself.viewscale], gameframeself.generation.pull_random())
        self.health = 0
             
    