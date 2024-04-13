from math import sqrt
from typing import Any

import pygame

class HexesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.hexes_dict =Grid()


    def add(self, *hexes, **kwargs):
        for hex in hexes:
            super().add(hex, **kwargs)  # Add sprite to the standard Group
            cube_pos = hex.offset_to_cube_coords(hex.grid_pos)
            self.hexes_dict[hex] = [hex.grid_pos, cube_pos]  # Add sprite to the lookup dictionary


    def __getitem__(self, item):
        return self.hexes_dict[item]

    def __setitem__(self, key, value):
        self.hexes_dict[key].kill()
        self.hexes_dict.pop(self.hexes_dict[key])
        self.add(value)

    def get_hex_offset_coord (self, hex):

        cube_pos = self.hexes_dict.get_keys(hex)[0]

        return cube_pos

    def get_hex_cube_coords(self, hex):

        cube_pos = self.hexes_dict.get_keys(hex)[1]
        return cube_pos



class KeyAlreadyExistsError(Exception):
    pass
class Grid(dict):
    # """An extension of a basic dictionary with a fast, consistent lookup by value implementation."""
    def __init__(self):
        super().__init__()
        self.key_to_value = {}
        self.value_to_keys = {}

    def __setitem__(self, value: Any, keys: list[Any])  -> None:


        for key in keys:
            if key not in self.key_to_value.keys():
                self.key_to_value[key] = value
                if value in self.value_to_keys:
                    self.value_to_keys[value].append(key)
                else:
                    self.value_to_keys[value] = [key]
            else:
                raise KeyAlreadyExistsError(f"Key '{key}' already exists in the dictionary.")

    def __getitem__(self, key):
        return self.key_to_value.get(key)
    def __len__(self):
        return len(self.key_to_value)
    def __iter__(self):
        return iter(self.key_to_value)

    def pop(self, value):
        keys=  self.value_to_keys.get(value, set())
        for key in keys:
            self.key_to_value.pop(key)
        self.value_to_keys.pop(value)

    def get_keys(self, value):
        return self.value_to_keys.get(value, set())

