import copy
import typing
from typing import *
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, Location, LocationProgressType
from Options import OptionError, Accessibility
from worlds.AutoWorld import WebWorld, World
from .items import *
from .locations import *
from .options import *
from .regions import*
from .data import *
from .rules import *

class RhythmHeavenFeverWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Rhythm Heaven Fever randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CallMeZero", "xMcacutt"]
    )

    tutorials = [setup_en]
    option_groups = rhythm_heaven_fever_option_groups


class RhythmHeavenFeverWorld(World):
    """

    """
    game = "Rhythm Heaven Fever"
    rhythm_heaven_fever_world_version = "v1.0.0"
    options_dataclass = RhythmHeavenFeverOptions
    options: RhythmHeavenFeverOptions
    topology_present = True
    item_name_to_id = {name: item.code for name, item in rhythm_heaven_fever_item_table.items()}
    location_name_to_id = {name: item.code for name, item in rhythm_heaven_fever_location_table.items()}

    web = RhythmHeavenFeverWeb()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_pool = []


    def generate_puml(self):
        from Utils import visualize_regions
        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Menu"), f"{self.player}_world.puml",
           show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])


    def fill_slot_data(self) -> Mapping[str, Any]:
        #self.generate_puml()
        return {
            "Required Rank": self.options.required_rank.value,
            "Include Endless": self.options.include_endless.value,
            "Remix Count": self.options.remix_count.value
        }

    def handle_ut_yamless(self, slot_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
        if not slot_data:
            return None
        self.options.required_rank = slot_data["Required Rank"]
        self.options.include_endless = slot_data["Include Endless"]
        self.options.remix_count = slot_data["Remix Count"]
        return slot_data

    def get_filler_item_name(self) -> str:
        return get_random_item_names(self.random, 1, junk_weights)[0]

    def generate_early(self) -> None:
        self.handle_ut_yamless(None)

    def create_item(self, name: str) -> Item:
        item_info = rhythm_heaven_fever_item_table[name]
        return RhythmHeavenFeverItem(name, item_info.classification, item_info.code, self.player)

    def create_items(self):
        create_items(self)

    def create_event(self, region_name: str, event_loc_name: str, event_item_name: str) -> None:
        region: Region = self.multiworld.get_region(region_name, self.player)
        loc: RhythmHeavenFeverLocation = RhythmHeavenFeverLocation(self.player, event_loc_name, None, region)
        loc.place_locked_item(RhythmHeavenFeverItem(event_item_name, ItemClassification.progression, None, self.player))
        region.locations.append(loc)

    def create_regions(self):
        create_regions(self)
        connect_all_regions(self)

    def set_rules(self):
        for extra_game in levels_dict["extra"]:
            loc = self.get_location(f"{extra_game}")
            loc.access_rule = lambda state, game=extra_game: state.has(f"Extra Game - {extra_game}", self.player)
        self.multiworld.completion_condition[self.player] \
            = lambda state: state.can_reach_location(f"Remix {self.options.remix_count}", self.player)