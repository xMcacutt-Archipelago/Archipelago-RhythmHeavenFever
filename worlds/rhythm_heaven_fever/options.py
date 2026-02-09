from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions, OptionSet


class RequiredRank(Choice):
    """
    The rank required to receive a check on a level.

    OK: Any passing rank will reward a check

    Superb: Better than OK, while still allowing a few misses
    """
    display_name = "Required Rank"
    option_ok = 0
    option_superb = 1
    default = 1


class IncludeEndless(Toggle):
    """
    Adds endless games to the pool.
    Each endless game has a high score that must be reached to send a check.
    """
    display_name = "Include Endless"


class RemixCount(Range):
    """
    Number of remixes before goal. (Reduces total number of levels to be played).
    """
    display_name = "Remix Count"
    range_start = 3
    range_end = 10
    default = 5


rhythm_heaven_fever_option_groups = [
    OptionGroup("Core", [
        RequiredRank,
        RemixCount,
        IncludeEndless
    ])
]


@dataclass
class RhythmHeavenFeverOptions(PerGameCommonOptions):
    required_rank: RequiredRank
    remix_count: RemixCount
    include_endless: IncludeEndless
