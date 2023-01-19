from preprocessing.custom_regex import *
import numpy as np

columns_to_drop = [
    "balcony_depth",
    "building_use_type_code",
    "building_year",
    "consumption_measurement_date",
    "heat_generators",
    "main_water_heating_type",
    "nb_gas_meters_commercial",
    "nb_gas_meters_housing",
    "nb_gas_meters_total",
    "nb_housing_units",
    "nb_parking_spaces",
    "nb_power_meters_total",
    "nb_power_meters_housing",
    "nb_power_meters_commercial",
    "nb_units_total",
    "water_heaters",
    "post_code",
    "main_heat_generators",
    "additional_heat_generators",
    "additional_water_heaters",
]

columns_to_ohe = [
    "building_type",
    "building_use_type_description",
    "lower_floor_adjacency_type",
    "upper_floor_adjacency_type",
    "water_heating_type",
    "window_filling_type",
]

float_columns = [
    "altitude",
    "building_height_ft",
    "building_total_area_sqft",
    "living_area_sqft",
    "lowe_floor_thermal_conductivity",
    "nb_meters",
    "outer_wall_thermal_conductivity",
    "percentage_glazed_surfaced",
    "upper_floor_thermal_conductivity",
    "window_heat_retention_factor",
    "window_thermal_conductivity",
]

binary_columns = [
    "has_air_conditioning",
    "has_balcony",
    "heating_type",
    "lower_floor_material",
    "solar_heating",
    "solar_water_heating",
    "upper_floor_material",
]

re_columns = [
    (
        "bearing_wall_material",
        [
            "wall_material_concrete",
            "wall_material_agglomerate",
            "wall_material_wood",
            "wall_material_bricks",
            "wall_material_stone",
            "wall_material_other",
        ],
        [re_concrete, re_agglomerate, re_wood, re_brick, re_stone, re_other_wall],
    ),
    (
        "building_category",
        ["building_cate_indiv", "building_cate_condo"],
        [re_indiv, re_condo],
    ),
    (
        "building_class",
        ["building_class_indiv", "building_class_2_11", "building_class_12"],
        [re_indiv, re_2_to_11, re_12],
    ),
    (
        "heating_energy_source",
        [
            "heating_energy_source_elec",
            "heating_energy_source_gas",
            "heating_energy_wood",
            "heating_energy_source_oil",
            "heating_energy_source_other",
        ],
        [re_elec, re_gas, re_wood, re_oil, re_other_energy],
    ),
    (
        "lower_floor_insulation_type",
        ["lower_type_uninsulated", "lower_type_ext", "lower_type_int"],
        [re_uninsulated, re_ext, re_int],
    ),
    (
        "main_heating_type",
        [
            "main_heating_type_elec",
            "main_heating_type_gas",
            "main_heating_type_oil",
            "main_heating_type_heat_pump",
            "main_heating_type_wood",
        ],
        [re_elec, re_gas, re_oil, re_heat, re_wood],
    ),
    (
        "main_water_heaters",
        [
            "main_water_heaters_elec",
            "main_water_heaters_gas",
            "main_water_heaters_oil",
            "main_water_heaters_heat",
            "main_water_heaters_wood",
            "main_water_solar",
        ],
        [re_elec, re_gas, re_oil, re_heat, re_wood, re_solar],
    ),
    (
        "outer_wall_materials",
        [
            "outer_wall_materials_concrete",
            "outer_wall_materials_brick",
            "outer_wall_materials_stone",
            "outer_wall_materials_wood",
        ],
        [re_concrete, re_brick, re_stone, re_wood],
    ),
    (
        "roof_material",
        [
            "roof_material_tile",
            "roof_material_slate",
            "roof_material_other",
            "roof_material_alu",
        ],
        [re_tile, re_slate, re_other_roof, re_zinc_alu],
    ),
    (
        "upper_floor_insulation_type",
        [
            "upper_floor_insulation_type_int",
            "upper_floor_insulation_type_uninsulated",
            "upper_floor_insulation_type_ext",
        ],
        [re_int, re_uninsulated, re_ext],
    ),
    (
        "ventilation_type",
        [
            "ventilation_type_humidity",
            "ventilation_type_natural",
            "ventilation_type_self_regulating",
        ],
        [re_humidity, re_natural, re_self],
    ),
    (
        "window_orientation",
        [
            "orientation_est",
            "orientation_west",
            "orientation_north",
            "orientation_south",
        ],
        [re_est, re_west, re_north, re_south],
    ),
    (
        "window_frame_material",
        ["window_pvc", "window_wood", "window_metal"],
        [re_pvc, re_wood, re_metal],
    ),
    (
        "water_heating_energy_source",
        [
            "water_heating_type_electricity",
            "water_heating_type_thermodynamic",
            "water_heating_type_oil",
            "water_heating_type_wood",
        ],
        [re_elec, re_thermodynamic, re_oil, re_wood],
    ),
    (
        "wall_insulation_type",
        [
            "wall_insulation_type_non_insulated",
            "wall_insulation_type_ext",
            "wall_insulation_type_int",
            "wall_insulation_type_reflection",
        ],
        [re_non_insulated, re_ext, re_int, re_reflection],
    ),
]


def compute_conditions(data):
    """Compute the conditions for each row of the data.

    Args:
        data (pandas.DataFrame): The data to compute the conditions for.

    Returns:
        ordinal_columns (list): The list of ordinal columns.
    """
    ordinal_columns = [
        # transform is_crossing_building
        (
            "is_crossing_building",
            [
                (data["is_crossing_building"] == "not through"),
                (data["is_crossing_building"] != "not through"),
            ],
            [False, True],
        ),
        # transform nb_commercial_units
        (
            "nb_commercial_units",
            [
                (data["nb_commercial_units"].isin([np.nan, 0.0])),
                (~data["nb_commercial_units"].isin([0.0, np.nan])),
            ],
            [True, False],
        ),
        (
            "outer_wall_thickness",
            [(data["outer_wall_thickness"] <= 20), (data["outer_wall_thickness"] > 20)],
            [True, False],
        ),
        (
            "renewable_energy_sources",
            [
                (data["renewable_energy_sources"].isnull()),
                (data["renewable_energy_sources"] != np.nan),
            ],
            [False, True],
        ),
        (
            "window_glazing_type",
            [
                (data["window_glazing_type"] == "double glazing"),
                (data["window_glazing_type"] != "double glazing"),
            ],
            [True, False],
        ),
        (
            "clay_risk_level",
            [
                (data["clay_risk_level"] == "low"),
                (data["clay_risk_level"] == "medium"),
                (data["clay_risk_level"] == "high"),
                (data["clay_risk_level"].isnull()),
            ],
            [1, 2, 3, 0],
        ),
        (
            "radon_risk_level",
            [
                (data["radon_risk_level"] == "low"),
                (data["radon_risk_level"] == "medium"),
                (data["radon_risk_level"] == "high"),
                (data["radon_risk_level"].isnull()),
            ],
            [1, 2, 3, 0],
        ),
        (
            "thermal_inertia",
            [
                (data["thermal_inertia"] == "low"),
                (data["thermal_inertia"] == "medium"),
                (data["thermal_inertia"] == "high"),
                (data["thermal_inertia"] == "very high"),
                (data["thermal_inertia"].isnull()),
            ],
            [1, 2, 3, 4, 0],
        ),
        (
            "building_period",
            [
                (data["building_period"] == "bad sup"),
                (data["building_period"] == "<1948"),
                (data["building_period"] == "1949-1970"),
                (data["building_period"] == "1970-1988"),
                (data["building_period"] == "1989-1999"),
                (data["building_period"] == "2000-2005"),
                (data["building_period"] == "2006-2012"),
                (data["building_period"] == ">2012"),
                (data["building_period"].isnull()),
            ],
            [0, 1, 2, 3, 4, 5, 6, 7, 0],
        ),
    ]
    return ordinal_columns
