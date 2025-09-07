# HospitalWasteManagement/src/processes/incineration.py
import copy
import pint
from src.processes.base import TreatmentProcess
from src.units import ureg
import logging

class IncinerationProcess(TreatmentProcess):
    """
    Implements direct emission calculations for incineration.
    
    The calculation is based on the waste's organic composition. Two distinct portions
    of the organic fraction are considered: one corresponding to fossil-derived organics
    (e.g., needles and sharps plastic) and another for biogenic organics.
    
    Emission calculations:
      - CO₂ emissions: Fossil-derived carbon is converted to CO₂ using the factor (44/12),
        and similarly for biogenic carbon.
      - SO₂ emissions: Calculated based on the total organic fraction and a conversion factor.
      - NOₓ, PM10, and PM25: Directly computed using the waste mass and emission factors.
      - Mercury (hg) and Lead (pb): Computed based on the metallic composition fractions.
    
    Scenario adjustments:
      If a scenario dictionary is provided and contains an "incineration_flue_gas_efficiency" key,
      the factors for PM10, PM25, and NOₓ are scaled to reflect improvements from flue-gas cleaning.
    """
    def calculate_direct_emissions(self, waste, scenario: dict = None) -> dict:
        logging.debug(f"{self.name} - Input waste composition: {waste.composition}")
        f = copy.deepcopy(self.factors)
        
        # Apply scenario adjustments for flue gas cleaning.
        if scenario and "incineration_flue_gas_efficiency" in scenario:
            efficiency = scenario["incineration_flue_gas_efficiency"]
            f["pm10_per_organic"] *= (1 - efficiency)
            f["pm25_per_organic"] *= (1 - efficiency)
            f["nox_per_waste"] *= (1 - efficiency)
        
        # Calculate total organic fraction.
        total_organic = (
            waste.composition.get("general_waste", {}).get("non_hazardous", 0) +
            waste.composition.get("infectious_waste", {}).get("body_fluids", 0) +
            waste.composition.get("infectious_waste", {}).get("lab_cultures", 0) +
            waste.composition.get("pharmaceutical_waste", {}).get("pharmaceuticals", 0) +
            waste.composition.get("chemical_waste", {}).get("cytotoxic_organic", 0) +
            waste.composition.get("radioactive_waste", {}).get("radioactive_organic", 0) +
            waste.composition.get("sharps_waste", {}).get("needles_sharps_plastic", 0)
        )
        fossil_organic = waste.composition.get("sharps_waste", {}).get("needles_sharps_plastic", 0)
        biogenic_organic = total_organic - fossil_organic
        
        # Use the full Pint quantity for mass.
        mass_q = waste.mass.to("kg")  # mass_q has units [kg]
        
        # Calculate energy in kWh: (kg) * (kWh/kg) = kWh.
        energy = mass_q * f["energy_content"]
        
        emissions = {
            # fossil_organic is dimensionless; energy has units [kWh],
            # f["carbon_content_fossil"] has units [kg/kWh] so the product is in [kg].
            "co2_fossil": fossil_organic * energy * f["carbon_content_fossil"] * (44 / 12),
            "co2_biogenic": biogenic_organic * energy * f["carbon_content_biogenic"] * (44 / 12),
            "so2": total_organic * mass_q.magnitude * f["so2_conversion"] * (64 / 32) * ureg("kg"),
            "nox": mass_q.magnitude * f["nox_per_waste"] * ureg("kg"),
            "pm10": mass_q.magnitude * total_organic * f["pm10_per_organic"] * ureg("kg"),
            "pm25": mass_q.magnitude * total_organic * f["pm25_per_organic"] * ureg("kg"),
            "hg": mass_q.magnitude * waste.composition.get("heavy_metals_waste", {}).get("mercury_waste", 0) * f["hg_volatilization"] * ureg("kg"),
            "pb": mass_q.magnitude * waste.composition.get("heavy_metals_waste", {}).get("other_heavy_metals", 0) * f["pb_volatilization"] * ureg("kg"),
        }
        
        if f.get("combustion_efficiency", 1.0) < 0.95:
            penalty = (0.95 - f["combustion_efficiency"]) * 2
            emissions["pm10"] *= (1 + penalty)
            emissions["pm25"] *= (1 + penalty)
        
        logging.debug(f"{self.name} - Calculated emissions: {emissions}")
        return emissions
