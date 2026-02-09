from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, TYPE_CHECKING
from worlds.rhythm_heaven_fever import *
from .data import levels_dict
from typing import Dict, Optional
from BaseClasses import Item, ItemClassification, MultiWorld, Location
from .data import *

if TYPE_CHECKING:
    from . import RhythmHeavenFeverWorld


class RhythmHeavenFeverItem(Item):
    game: str = "Rhythm Heaven Fever"


def get_random_item_names(rand, k: int, weights: dict[str, int]) -> list[str]:
    random_items = rand.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=k)
    return random_items


def create_single(name: str, world: RhythmHeavenFeverWorld, item_class: ItemClassification = None) -> None:
    classification = rhythm_heaven_fever_item_table[name].classification if item_class is None else item_class
    world.item_pool.append(RhythmHeavenFeverItem(name, classification, rhythm_heaven_fever_item_table[name].code, world.player))


def create_multiple(name: str, amount: int, world: RhythmHeavenFeverWorld, item_class: ItemClassification = None):
    for i in range(amount):
        create_single(name, world, item_class)


def create_items(world: RhythmHeavenFeverWorld):
    total_location_count: int = len(world.multiworld.get_unfilled_locations(world.player))

    for album_index in range(world.options.remix_count):
        if album_index == 0:
            continue
        create_single(f"Album {album_index + 1}", world)

    if world.options.include_endless.value:
        for endless_game in levels_dict["endless"]:
            create_single(f"Endless Game - {endless_game}", world)

    for extra_game in levels_dict["extra"]:
        create_single(f"Extra Game - {extra_game}", world)

    for toy in levels_dict["toys"]:
        create_single(f"{toy} Toy", world)

    # Junk
    remaining_locations: int = total_location_count - len(world.multiworld.worlds[world.player].item_pool)
    junk_count: int = remaining_locations
    junk = get_random_item_names(world.random, junk_count, junk_weights)
    for name in junk:
        create_single(name, world)
    world.multiworld.itempool += world.item_pool


junk_weights = {
    f"Random {BOOK}": 50,
    f"Random {MUSIC}": 50
}


@dataclass(frozen=True)
class ItemData:
    code: Optional[int]
    classification: Optional[ItemClassification]


def generate_item_table() -> Dict[str, ItemData]:
    item_table = {}
    for album_index in range(10):
        if album_index == 0:
            continue
        else:
            # Blocks of levels have ids 2, 3, 4, etc up to 10 for the final block of levels
            item_table[f"Album {album_index + 1}"] = ItemData(album_index + 1, ItemClassification.progression)

    for i, toy in enumerate(levels_dict["toys"]):
        # Toys have ids 0x100, 0x101, 0x102, 0x103
        item_table[f"{toy} Toy"] = ItemData(i + 0x100, ItemClassification.filler)

    for i, endless_game in enumerate(levels_dict["endless"]):
        # Endless games have ids 0x200, 0x201, 0x202, 0x203
        item_table[f"Endless Game - {endless_game}"] = ItemData(i + 0x200, ItemClassification.progression)

    for i, extra_game in enumerate(levels_dict["extra"]):
        # Extra games have ids 0x300, 0x301, 0x302, 0x303
        item_table[f"Extra Game - {extra_game}"] = ItemData(i + 0x300, ItemClassification.progression)

    item_table[f"Random {MUSIC}"] = ItemData(0x400, ItemClassification.filler)
    item_table[f"Random {BOOK}"] = ItemData(0x401, ItemClassification.filler)
    return item_table


rhythm_heaven_fever_item_table = generate_item_table()