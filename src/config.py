# src/config.py
import copy
from src.units import ureg

# ----------------------------------------------------------------------
# EMISSION FACTORS
# ----------------------------------------------------------------------
EMISSION_FACTORS = {
    "INCINERATION": {
        # Emission factors given per kWh.
        "carbon_content_fossil": 0.097 * ureg("kg/kWh"),      # kg CO₂/kWh (fossil-derived)
        "carbon_content_biogenic": 0.054 * ureg("kg/kWh"),      # kg CO₂/kWh (biogenic-derived)
        "energy_content": 5.3 * ureg("kWh/kg"),                # Bujak, J. (2010)
        "nitrogen_frac_organic": 9.1e-6,     # Unitless (kg NH₃ per kg waste)
        "sulfur_frac_organic": 0.0002,       # Unitless
        "so2_conversion": 0.85,              # Dimensionless
        "pm10_per_organic": 0.000031,        # kg pollutant per kg organic fraction
        "pm25_per_organic": 0.0000217,       # kg pollutant per kg organic fraction
        "nox_per_waste": 4.3e-6,             # kg pollutant per kg waste
        "hg_volatilization": 4.65e-5,        # kg pollutant per kg heavy metals
        "pb_volatilization": 6.218e-4,       # kg pollutant per kg heavy metals
        "combustion_efficiency": 0.97,       # Dimensionless
        "excess_air_ratio": 1.4,             # Dimensionless
    },
    "LANDFILL": {
        "time_period": 100,                  # Years
        "fast_decay_rate": 0.18,             # yr⁻¹
        "slow_decay_rate": 0.02,             # yr⁻¹
        "ch4_split": 0.5,                    # Dimensionless
        "co2_split": 0.5,                    # Dimensionless
        "nh3_split": 9.1e-6,                 # kg NH₃/kg waste
        "nmvoc_split": 0.0017,               # kg NMVOC/kg waste
        "hg_factor": 0.7,                    # Dimensionless
        "pb_factor": 0.3,                    # Dimensionless
    },
    "PYROLYSIS": {
        "co2_fossil_per_organic": 0.06887,   # kg CO₂ per kg organic fraction
        "ch4_fossil_per_organic": 0.004,       # kg CH₄ per kg organic fraction
        "nmvoc_per_organic": 0.000645,         # kg VOC per kg waste
        "pahs_per_organic": 0.000179,          # kg VOC per kg waste
        "dioxin_per_chlorinated": 3.71e-13,    # kg I-TEQ per m³
        "hg_per_mercury": 0.86e-6,             # kg pollutant per kg heavy metals
        "pb_per_heavy_metal": 0.45e-6,         # kg pollutant per kg heavy metals
    },
    "CHEM_DISINFECTION": {
        "disinfectant_ratio": 0.03,          # Dimensionless
        "chlorine_loss": 0.05,               # Dimensionless
        "chlorine_to_hcl_split": 0.6,        # Dimensionless
        "nitrogen_content": 0.03,            # Dimensionless
        "nitrogen_to_nh3": 0.2,              # Dimensionless
        "nmvoc_per_organic": 8.51e-7,        # kg per kg waste
        "pm10_per_organic": 2e-10,           # kg per m³
    },
    "AUTOCLAVE": {
        "nmvoc_per_organic": 8.81e-6,        # kg per kg waste
        "pm10_per_organic": 0,               # Set to zero
        "pm25_per_organic": 0,               # Set to zero
        "elec_per_waste": 0.269,             # tCO₂-e per ton of biomedical waste
        "grid_co2_factor": 0.4,              # kg CO₂/kWh
        "baseline_temp": 121,                # °C
        "operating_temp": 134,               # °C
        "nmvoc_temp_coeff": 0,               # Dimensionless
        "hg_leach_factor": 0                 # Dimensionless
    },
    "MICROWAVE": {
        "nmvoc_per_organic": 2.46e-5,        # kg per kg waste
        "pm10_per_organic": 1.476e-5,        # kg per kg waste
        "pm25_per_organic": 0,               # Set to zero
        "base_frequency": 2450,              # MHz
        "operating_frequency": 915,          # MHz
        "freq_impact_per_mhz": 1e-15,        # Dimensionless
        "plastic_nmvoc_boost": 0,            # Dimensionless
        "elec_per_waste": 0.7,               # kWh/kg
        "grid_co2_factor": 0.4,              # kg CO₂/kWh
        "metal_aerosol_factor": 0,           # Dimensionless
        "emission_limits": {
            "nmvoc": 0.0001,
            "pm10": 0.0001,
            "pm25": 0.0001
        },
        "enforce_emission_limits": True
    },
}

# ----------------------------------------------------------------------
# DEFAULT WASTE COMPOSITION
# ----------------------------------------------------------------------
DEFAULT_COMPOSITION = {
    "general_waste": {
        "non_hazardous": 0.65,
    },
    "infectious_waste": {
        "body_fluids": 0.12,
        "lab_cultures": 0.06,
    },
    "sharps_waste": {
        "needles_sharps_plastic": 0.02,
        "needles_sharps_metal": 0.02,
    },
    "pharmaceutical_waste": {
        "pharmaceuticals": 0.04,
        "pharmaceuticals_halogenated": 0.01,
    },
    "chemical_waste": {
        "lab_reagents": 0.03,
        "lab_cultures_disinfectants": 0.005,
        "cytotoxic_organic": 0.015,
        "cytotoxic_halogenated": 0.005,
    },
    "heavy_metals_waste": {
        "mercury_waste": 0.015,
        "other_heavy_metals": 0.015,
    },
    "radioactive_waste": {
        "radioactive_metals": 0.005,
        "radioactive_organic": 0.002,
    },
}

# ----------------------------------------------------------------------
# HOSPITAL-SPECIFIC INDIRECT FACTORS
# ----------------------------------------------------------------------
HOSPITAL_INDIRECT_FACTORS = {
    "KBTH": {
        "energy_inputs": {
            "energy_use_kWh_per_kg": 0.12,
            "co2_fossil_per_kWh": 0.40,
            "so2_per_kWh": 0.0002,
            "pm25_per_kWh": 0.00012,
        },
        "transportation": {
            "distance_km": 0.5,
            "truck_load_t": 0.44,
            "co2_fossil_per_tkm": 0.08,
            "nox_per_tkm": 0.0012,
        },
        "infrastructure": {
            "construction_co2_per_kg": 0.02,
            "land_use_factor": 0.001 * 0.44,
        },
        "downstream": {
            "residue_ratio": 0.04,
            "residue_co2_per_kg": 0.15,
            "residue_so2_per_kg": 0.0005,
        },
    },
    "KATH": {
        "energy_inputs": {
            "energy_use_kWh_per_kg": 0.12,
            "co2_fossil_per_kWh": 0.40,
            "so2_per_kWh": 0.0002,
            "pm25_per_kWh": 0.00012,
        },
        "transportation": {
            "distance_km": 4,
            "truck_load_t": 0.31,
            "co2_fossil_per_tkm": 0.08,
            "nox_per_tkm": 0.0012,
        },
        "infrastructure": {
            "construction_co2_per_kg": 0.02,
            "land_use_factor": 0.001 * 0.31,
        },
        "downstream": {
            "residue_ratio": 0.04,
            "residue_co2_per_kg": 0.15,
            "residue_so2_per_kg": 0.0005,
        },
    },
    "CCTH": {
        "energy_inputs": {
            "energy_use_kWh_per_kg": 0.12,
            "co2_fossil_per_kWh": 0.40,
            "so2_per_kWh": 0.0002,
            "pm25_per_kWh": 0.00012,
        },
        "transportation": {
            "distance_km": 9.2,
            "truck_load_t": 0.122,
            "co2_fossil_per_tkm": 0.08,
            "nox_per_tkm": 0.0012,
        },
        "infrastructure": {
            "construction_co2_per_kg": 0.02,
            "land_use_factor": 0.001 * 0.122,
        },
        "downstream": {
            "residue_ratio": 0.04,
            "residue_co2_per_kg": 0.15,
            "residue_so2_per_kg": 0.0005,
        },
    },
    "BRH": {
        "energy_inputs": {
            "energy_use_kWh_per_kg": 0.12,
            "co2_fossil_per_kWh": 0.40,
            "so2_per_kWh": 0.0002,
            "pm25_per_kWh": 0.00012,
        },
        "transportation": {
            "distance_km": 1.4,
            "truck_load_t": 0.1,
            "co2_fossil_per_tkm": 0.08,
            "nox_per_tkm": 0.0012,
        },
        "infrastructure": {
            "construction_co2_per_kg": 0.02,
            "land_use_factor": 0.001 * 0.1,
        },
        "downstream": {
            "residue_ratio": 0.04,
            "residue_co2_per_kg": 0.15,
            "residue_so2_per_kg": 0.0005,
        },
    },
    "UCCH": {
        "energy_inputs": {
            "energy_use_kWh_per_kg": 0.12,
            "co2_fossil_per_kWh": 0.40,
            "so2_per_kWh": 0.0002,
            "pm25_per_kWh": 0.00012,
        },
        "transportation": {
            "distance_km": 4.7,
            "truck_load_t": 0.023,
            "co2_fossil_per_tkm": 0.08,
            "nox_per_tkm": 0.0012,
        },
        "infrastructure": {
            "construction_co2_per_kg": 0.02,
            "land_use_factor": 0.001 * 0.023,
        },
        "downstream": {
            "residue_ratio": 0.04,
            "residue_co2_per_kg": 0.15,
            "residue_so2_per_kg": 0.0005,
        },
    },
}

# ----------------------------------------------------------------------
# IMPACT CATEGORIES & NORMALIZATION FACTORS (for LCIA)
# ----------------------------------------------------------------------
IMPACT_CATEGORIES = {
    "Human Toxicity (HT)": (
        'CML v4.8 2016', 'human toxicity', 'human toxicity (HTP inf)'
    ),
    "Climate Change (CC)": (
        'CML v4.8 2016', 'climate change', 'global warming potential (GWP100)'
    ),
    "Eutrophication (EP)": (
        'CML v4.8 2016', 'eutrophication', 'eutrophication (fate not incl.)'
    ),
    "Acidification (AP)": (
        'CML v4.8 2016', 'acidification', 'acidification (incl. fate, average Europe total, A&B)'
    ),
    "Marine Aquatic Eco-Toxicity (MAE)": (
        'CML v4.8 2016', 'ecotoxicity: marine', 'marine aquatic ecotoxicity (MAETP inf)'
    ),
    "Terrestrial Eco-Toxicity (TE)": (
        'CML v4.8 2016', 'ecotoxicity: terrestrial', 'terrestrial ecotoxicity (TETP inf)'
    ),
    "Freshwater Eco-Toxicity (FAE)": (
        'CML v4.8 2016', 'ecotoxicity: freshwater', 'freshwater aquatic ecotoxicity (FAETP inf)'
    ),
    "Photochemical Oxidation (PO)": (
        'CML v4.8 2016', 'photochemical oxidant formation', 'photochemical oxidation (high NOx)'
    ),
}

NORMALIZATION_FACTORS = {
    "Human Toxicity (HT)": 8.86e12,
    "Climate Change (CC)": 4.18e12,
    "Eutrophication (EP)": 3.77e9,
    "Acidification (AP)": 3.36e11,
    "Marine Aquatic Eco-Toxicity (MAE)": 6.24e12,
    "Terrestrial Eco-Toxicity (TE)": 5.09e10,
    "Freshwater Eco-Toxicity (FAE)": 3.07e10,
    "Photochemical Oxidation (PO)": 3.51e11,
}
