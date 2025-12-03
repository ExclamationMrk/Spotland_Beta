import pygame
import tile_code
import tile_occupants_code
from random import randint

class Generation:
    def __init__(self, dimensions: list[int, int], tile_dimensions: list[int, int], water_rules: list, desert_rules: list,
                 hilly_rules: list, river_rules: list): 
        # biome_rules: len(list) = num of biomes, list_objects = int(generation attempts)
        # river_rules: len(list) == num of rivers, list_objects = list[width, direction]
        self.dimensions = dimensions
        self.tile_dimensions = tile_dimensions
        self.tile_spread = self.create_tile_spread()
        self.desert_generation(desert_rules)
        self.hilly_generation(hilly_rules)
        self.water_generation(water_rules)
        self.river_generation(river_rules)
        
        self.remove_blanks()
        
        self.tree_generation()
        self.rock_generation()

    def pull_random(self):
        random_tile_pos = [randint(0, self.dimensions[0] - 1), randint(0, self.dimensions[1] - 1)]
        return random_tile_pos

    def create_tile_spread(self):
        tile_dictionary = {}
        row = 0
        north_edge = True
        south_edge = False
        while (row < self.dimensions[1]):
            if ((row + 1) == self.dimensions[1]):
                south_edge = True
                
            tiles = {}
            current_tile = 0
            east_edge = False
            west_edge = True
            
            while (current_tile < self.dimensions[0]):
                if ((current_tile + 1) == self.dimensions[0]):
                    east_edge = True
                    
                tiles[current_tile] = tile_code.Tile(current_tile, row, self.tile_dimensions[0], self.tile_dimensions[1], {"n": north_edge, "s": south_edge, "e": east_edge, "w": west_edge}, "b")
                
                current_tile += 1
                west_edge = False

            tile_dictionary[row] = tiles
            row += 1
            north_edge = False
            
        return tile_dictionary
    
    def water_generation(self, water_rules: list): #water_rules: len(list) = num of waters, list_obj = generation attempts
        for water_generation_attempts in water_rules:
            temp = []
            finished = []
            
            seed = self.pull_random()
            temp.append(seed)
            
            while (water_generation_attempts > 0) and (len(temp) > 0):
                tile = temp.pop(0)
                finished.append(tile)
                tile = self.tile_spread[tile[1]][tile[0]]
                for key, tile_pos in tile.neighbors.items():
                    if (tile_pos != None) and (tile.gen_bias != key):
                        if ((randint(1, 4) > 1 or tile.gen_unbias == key)) or (len(water_rules) == 1):
                            if tile_pos not in temp:
                                temp.append(tile_pos)
                                water_generation_attempts -= 1
                                    
                            else:
                                water_generation_attempts -= 1
                                
                        else:
                             pass
                            
                else:
                    pass
                    
            for tile_pos in finished:
                self.tile_spread[tile_pos[1]][tile_pos[0]].update_type("w")
                    
    def desert_generation(self, desert_rules: list):
        for desert_generation_attempts in desert_rules:
            temp = []
            finished = []
            
            seed = self.pull_random()
            if self.tile_spread[seed[1]][seed[0]].type == 'b':
                temp.append(seed)
                
            else:
                continue
            
            while (desert_generation_attempts > 0) and (len(temp) > 0):
                tile = temp.pop(0)
                finished.append(tile)
                tile = self.tile_spread[tile[1]][tile[0]]
                if (tile.type == "b"):
                    for key, tile_pos in tile.neighbors.items():
                        if (tile_pos != None) and tile.gen_bias != key:
                            if ((randint(1, 4) > 1 or key == tile.gen_unbias) and (self.tile_spread[tile_pos[1]][tile_pos[0]].type == "b")) or (len(desert_rules) == 1):
                                if tile_pos not in temp:
                                    temp.append(tile_pos)
                                    desert_generation_attempts -= 1
                                    
                                else:
                                    desert_generation_attempts -= 1
                                
                            else:
                                pass
                            
                    else:
                        pass
                    
            for tile_pos in finished:
                self.tile_spread[tile_pos[1]][tile_pos[0]].update_type("d")
                
    def hilly_generation(self, hilly_rules: list):
        for hilly_generation_attempts in hilly_rules:
            temp = []
            finished = []
            
            seed = self.pull_random()
            if self.tile_spread[seed[1]][seed[0]].type == 'b':
                temp.append(seed)
                
            else:
                continue
            
            while (hilly_generation_attempts > 0) and (len(temp) > 0):
                tile = temp.pop(0)
                finished.append(tile)
                tile = self.tile_spread[tile[1]][tile[0]]
                if (tile.type == "b"):
                    for key, tile_pos in tile.neighbors.items():
                        if (tile_pos != None) and tile.gen_bias != key:
                            if ((randint(1, 4) > 1) and (self.tile_spread[tile_pos[1]][tile_pos[0]].type == "b")) or (len(hilly_rules) == 1):
                                if tile_pos not in temp:
                                    temp.append(tile_pos)
                                    hilly_generation_attempts -= 1
                                    
                                else:
                                    hilly_generation_attempts -= 1
                                
                            else:
                                pass
                            
                    else:
                        pass
                    
            for tile_pos in finished:
                self.tile_spread[tile_pos[1]][tile_pos[0]].update_type("h")
                
    def remove_blanks(self):
        for row in self.tile_spread.values():
            for tile in row.values():
                if tile.type == "b":
                    tile.update_type("g")
                    
    def river_generation(self, rivers_direction_width: list):
        for river_d_w in rivers_direction_width:
            if river_d_w[0] == "x":
                seed = [0, randint(river_d_w[1] - 1, self.dimensions[1] - 1)]
            
                while seed[0] < self.dimensions[0]:
                    river_offset = [1, randint(-1, 1)]
                    
                    width = (river_d_w[1] - 1)
                    
                    while width >= 0:
                        try:
                            self.tile_spread[seed[1] - width][seed[0]].update_type("w")
                            
                        except KeyError:
                            pass
                        
                        width -= 1
                        
                    seed[0] += river_offset[0]
                    seed[1] += river_offset[1]
                    
                
            elif river_d_w[0] == "y":
                seed = [randint(river_d_w[1] - 1, self.dimensions[0] - 1), 0]
            
                while seed[1] < self.dimensions[1]:
                    river_offset = [randint(-1, 1), 1]
                    
                    width = (river_d_w[1] - 1)
                    
                    while width >= 0:
                        try:
                            self.tile_spread[seed[1]][seed[0] - width].update_type("w")
                            
                        except KeyError:
                            pass
                        
                        width -= 1
                        
                        
                    seed[0] += river_offset[0]
                    seed[1] += river_offset[1]
            
            else:
                pass
            
    def tree_generation(self):
        tree_num_per_row = int((len(self.tile_spread[0]) / 4) + 1)
                
        for y, tile_row in self.tile_spread.items():
            tree_num_iterant = tree_num_per_row
            
            while tree_num_iterant > 0:
                index = randint(0, len(tile_row) - 1)
                if tile_row[index].type in ["g", "h", "d"]:
                    if randint(0, 4) == 0:
                        tile_row[index].add_occupants([tile_occupants_code.OccupantTemplate("sapling", tile_row[index])])
                    
                    else:
                        tile_row[index].add_occupants([tile_occupants_code.OccupantTemplate("tree", tile_row[index])])
                    
                else:
                    pass
                
                tree_num_iterant -= 1
                
    def rock_generation(self):
        rock_num_per_row = int((len(self.tile_spread[0]) / 6) + 1)
                
        for y, tile_row in self.tile_spread.items():
            rock_num_iterant = rock_num_per_row
            
            while rock_num_iterant > 0:
                index = randint(0, len(tile_row) - 1)
                if tile_row[index].type in ["g", "h", "d"]:
                    tile_row[index].add_occupants([tile_occupants_code.OccupantTemplate("rock", tile_row[index])])
                    
                else:
                    pass
                
                rock_num_iterant -= 1
                
    