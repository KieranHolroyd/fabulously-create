"""Cross-chapter bridge targets (absolute = chapter_base + n).

Foundations 100+, Create 200+, Storage 300+, Refined Storage 324+,
Automation 400+, Powah 424+, RFTools 445+, Flux 470+, Late 500+,
Mekanism 600+, Mek Generators 650+, Extreme Reactors 700+,
Modern Industrialization 750+, Industrial Foregoing 800+, Immersive Engineering 850+.
Factory Challenges 1000+.
"""


def quest_id(n: int) -> str:
    """Stable FTB quest id for an absolute quest number.

    FTB Quests ids are parsed as signed 64-bit longs; a leading hex digit
    of 8-F overflows Long.MAX_VALUE and gets silently discarded/regenerated
    at load, which orphans every lang file key referencing the original id.
    Keep the leading nibble (the "3") in 0-7.
    """
    return f"31{n:014X}"


# Foundations
F_IRON = 106
F_WAYSTONE = 110
F_LEATHER = 123

# Create
C_BRASS = 223
C_PRECISION = 227
C_TRACK = 238

# Factory Challenge source milestones
FLUX_GARGANTUAN = 479
MEKANISM_ATOMIC_ALLOY = 621

# Storage / automation bridges
S_BACKPACK = 300
S_TERMINAL = 309
A_TERMINAL = 409
A_ALTERNATOR = 411

# First quest of dedicated tech chapters (absolute)
MEKANISM_START = 600

# Powah / RFTools / Flux bridge points (absolute)
POWAH_ENERGY_CELL = 427  # powah:energy_cell_starter (base 424 + 3)
RFTOOLS_MACHINE_FRAME = 445
RFTOOLS_DIMENSIONAL_CELL = 450  # rftoolspower:dimensionalcell (base 445 + 5)
CREATE_START = 200
STORAGE_START = 300
AUTOMATION_START = 400
LATE_GAME_START = 500
