from __future__ import annotations

from dataclasses import dataclass
from enum import EnumType, Enum
from typing import TYPE_CHECKING, NamedTuple, Any
from BaseClasses import Location, Region
from BaseClasses import Location, Region, LocationProgressType

from worlds.rhythm_heaven_fever.data import *
from worlds.rhythm_heaven_fever import *
if TYPE_CHECKING:
    from . import RhythmHeavenFeverWorld


class RhythmHeavenFeverLocation(Location):
    game: str = "Rhythm Heaven Fever"


@dataclass(frozen=True)
class LocData:
    code: int
    region: str
    progress_type: LocationProgressType = LocationProgressType.DEFAULT


def create_location(player: int, reg: Region, name: str, code: int, progress_type: LocationProgressType = LocationProgressType.DEFAULT):
    location = RhythmHeavenFeverLocation(player, name, code, reg)
    location.progress_type = progress_type
    reg.locations.append(location)


def create_locations_from_dict(world, loc_dict, reg, player):
    for (key, data) in loc_dict.items():
        if data.region != reg.name:
            continue
        create_location(player, reg, key, data.code)


def create_locations(world: RhythmHeavenFeverWorld, reg: Region):
    if world.options.include_endless.value:
        create_locations_from_dict(world, rhythm_heaven_fever_endless_games, reg, world.player)
    create_locations_from_dict(world, rhythm_heaven_fever_extra_games, reg, world.player)
    create_locations_from_dict(world, rhythm_heaven_fever_core_games, reg, world.player)


def generate_location_tables():
    result_dict = {}
    for remix_index, (remix_name, level_list) in enumerate(levels_dict["core"].items()):
        for level_index, level in enumerate(level_list):
            rhythm_heaven_fever_core_games[level] = LocData(remix_index * 5 + level_index + 0x100, f"Album {remix_index + 1}")
        rhythm_heaven_fever_core_games[remix_name] = LocData(remix_index * 5 + 4, f"Album {remix_index + 1}")
    for endless_index, endless_name in enumerate(levels_dict["endless"]):
        rhythm_heaven_fever_endless_games[f"{endless_name} High Score"] = LocData(endless_index + 0x200, "Endless Games")
    for extra_index, extra_name in enumerate(levels_dict["extra"]):
        rhythm_heaven_fever_extra_games[extra_name] = LocData(extra_index + 0x300, "Extra Games")
    return result_dict


rhythm_heaven_fever_endless_games = {}
rhythm_heaven_fever_extra_games = {}
rhythm_heaven_fever_core_games = {}
generate_location_tables()

rhythm_heaven_fever_location_table = {
    **rhythm_heaven_fever_endless_games,
    **rhythm_heaven_fever_extra_games,
    **rhythm_heaven_fever_core_games
}
