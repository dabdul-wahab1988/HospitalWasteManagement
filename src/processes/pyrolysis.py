# HospitalWasteManagement/src/processes/pyrolysis.py
from src.processes.base import TreatmentProcess
import pint
from src.units import ureg
import logging

class PyrolysisProcess(TreatmentProcess):
    """
    Implements direct emission calculations for the pyrolysis treatment process.
    
    Pyrolysis is a thermal treatment method that decomposes waste material in the absence of oxygen.
    This process converts organic and chlorinated fractions of the waste into various emissions.
    
    Emission calculations:
      - Fossil CO₂: Calculated using the total organic fraction and the emission factor 'co2_fossil_per_organic'.
      - Fossil CH₄: Calculated using the total organic fraction and the emission factor 'ch4_fossil_per_organic'.
      - NMVOC: Calculated using the total organic fraction and the emission factor 'nmvoc_per_organic'.
      - PAHs: Calculated using the total organic fraction and the emission factor 'pahs_per_organic'.
      - Dioxin: Calculated using the total chlorinated material and the emission factor 'dioxin_per_chlorinated'.
      - Mercury (hg) and Lead (pb): Calculated based on the respective fractions in the heavy metals waste.
    
    Note:
      - The method accepts an optional `scenario` dictionary. In this basic implementation, scenario
        parameters are not used to modify the factors, but the parameter is available for future extensions.
    """
    def calculate_direct_emissions(self, waste, scenario: dict = None) -> dict:
        logging.debug(f"{self.name} - Input waste composition: {waste.composition}")
        # Use the emission factors provided for pyrolysis.
        f = self.factors
        
        # Calculate total organic fraction from the provided waste composition.
        total_organic = (
            waste.composition.get("general_waste", {}).get("non_hazardous", 0) +
            waste.composition.get("infectious_waste", {}).get("body_fluids", 0) +
            waste.composition.get("infectious_waste", {}).get("lab_cultures", 0) +
            waste.composition.get("pharmaceutical_waste", {}).get("pharmaceuticals", 0) +
            waste.composition.get("chemical_waste", {}).get("cytotoxic_organic", 0) +
            waste.composition.get("radioactive_waste", {}).get("radioactive_organic", 0) +
            waste.composition.get("sharps_waste", {}).get("needles_sharps_plastic", 0)
        )
        
        # Calculate total chlorinated fraction from the provided waste composition.
        total_chlor = (
            waste.composition.get("pharmaceutical_waste", {}).get("pharmaceuticals_halogenated", 0) +
            waste.composition.get("chemical_waste", {}).get("cytotoxic_halogenated", 0)
        )
        
        # Convert waste mass to kilograms.
        mass = waste.mass.to("kg").magnitude
        
        # Calculate emissions for each pollutant.
        emissions = {
            "co2_fossil": mass * total_organic * f["co2_fossil_per_organic"] * ureg("kg"),
            "ch4_fossil": mass * total_organic * f["ch4_fossil_per_organic"] * ureg("kg"),
            "nmvoc": mass * total_organic * f["nmvoc_per_organic"] * ureg("kg"),
            "pahs": mass * total_organic * f["pahs_per_organic"] * ureg("kg"),
            "dioxin": mass * total_chlor * f["dioxin_per_chlorinated"] * ureg("kg"),
            "hg": mass * waste.composition.get("heavy_metals_waste", {}).get("mercury_waste", 0) * f["hg_per_mercury"] * ureg("kg"),
            "pb": mass * waste.composition.get("heavy_metals_waste", {}).get("other_heavy_metals", 0) * f["pb_per_heavy_metal"] * ureg("kg"),
        }
        
        logging.debug(f"{self.name} - Calculated emissions: {emissions}")
        return emissions
