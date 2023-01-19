import re

re_concrete = re.compile("concrete")
re_agglomerate = re.compile("agglomerate|chipboard")
re_wood = re.compile("wood")
re_brick = re.compile("brick")
re_stone = re.compile("gritstone|stone|millstone")
re_other_wall = re.compile("other|indetermined")

re_condo = re.compile("condo")
re_indiv = re.compile("individual")
re_2_to_11 = re.compile("2 to 11")
re_12 = re.compile("12+")

re_elec = re.compile("electricity|elec|joule")
re_gas = re.compile("gas|butane|gaz")
re_oil = re.compile("oil\b|fuel")
re_other_energy = re.compile("other|coal")

re_uninsulated = re.compile("uninsulated")
re_ext = re.compile("external")
re_int = re.compile("internal")

re_heat = re.compile("heat\b")
re_solar = re.compile("solar")

re_tile = re.compile("tile")
re_slate = re.compile("slate")
re_other_roof = re.compile("indeterminate|others")
re_zinc_alu = re.compile("zinc aluminum")

re_humidity = re.compile("humidity sensitive")
re_natural = re.compile("natural")
re_self = re.compile("self-regulating mechanical ventilation after 1982")

re_est = re.compile("est|east")
re_west = re.compile("ouest|west")
re_north = re.compile("nord|north")
re_south = re.compile("sud|south")

re_pvc = re.compile("pvc")
re_metal = re.compile("metal")

re_thermodynamic = re.compile("thermodynamic")
re_metal = re.compile("gas|lpg|butane")

re_non_insulated = re.compile("non insulated")
re_reflection = re.compile("reflection")
