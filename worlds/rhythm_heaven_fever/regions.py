from __future__ import annotations
from worlds.rhythm_heaven_fever import *
from BaseClasses import MultiWorld, Region, Entrance
from typing import List, Dict, TYPE_CHECKING

from .data import *
if TYPE_CHECKING:
    from . import RhythmHeavenFeverWorld

def connect_regions(world: RhythmHeavenFeverWorld, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.multiworld.get_region(from_name, world.player)
    exit_region = world.multiworld.get_region(to_name, world.player)
    return entrance_region.connect(exit_region, entrance_name)


def create_region(world: RhythmHeavenFeverWorld, name: str):
    reg = Region(name, world.player, world.multiworld)
    create_locations(world, reg)
    world.multiworld.regions.append(reg)


def connect_all_regions(world: RhythmHeavenFeverWorld):
    if world.options.include_endless:
        connect_regions(world, "Menu", "Endless Games", "Menu -> Endless Games")
    connect_regions(world, "Menu", "Extra Games", "Menu -> Extra Games")
    connect_regions(world, "Menu", "Album 1", "Menu -> Album 1")
    for album_index in range(1, world.options.remix_count):
        reg = connect_regions(world, f"Album {album_index}", f"Album {album_index + 1}", f"Album {album_index} -> Album {album_index + 1}")
        reg.access_rule = lambda state, album=album_index: state.has(f"Album {album + 1}", world.player)


def create_regions(world: RhythmHeavenFeverWorld):
    create_region(world, "Menu")
    if world.options.include_endless:
        create_region(world, "Endless Games")
    create_region(world, "Extra Games")
    for album_index in range(world.options.remix_count):
        create_region(world, f"Album {album_index + 1}")