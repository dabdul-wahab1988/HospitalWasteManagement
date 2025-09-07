# src/waste_stream.py
import copy
from dataclasses import dataclass, field
from typing import Dict
import pint
from src import config
from src.units import ureg

@dataclass
class WasteStream:
    """
    Represents a waste stream with a given mass (with unit) and a material composition.

    Attributes:
        mass (pint.Quantity): The total mass of the waste stream. e.g., 100 * ureg("kg").
        composition (Dict[str, Dict[str, float]]): A nested dictionary that defines the fraction
            of each material group present in the waste, e.g.:
                {
                    "general_waste": { ... },
                    "infectious_waste": { ... },
                    "sharps_waste": { ... },
                    "pharmaceutical_waste": { ... },
                    "chemical_waste": { ... },
                    "heavy_metals_waste": { ... },
                    "radioactive_waste": { ... }
                }
            The default composition is loaded from the config module.
    """
    mass: pint.Quantity  # e.g., 100 * ureg("kg")
    composition: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: copy.deepcopy(config.DEFAULT_COMPOSITION)
    )

    def adjust_for_segregation(self, efficiency: float) -> 'WasteStream':
        """
        Adjusts the waste composition based on a segregation efficiency factor.

        **Interpreted as follows**:
          - A value of 1.0 means *all* hazardous fractions are effectively segregated out
            from this waste stream (fully removed).
          - A value of 0.0 means *no* segregation occurs (the entire hazardous fraction
            remains in the stream).

        In other words, the fraction that *remains* in this waste is multiplied by (1 - efficiency).

        Hazardous fractions subject to segregation include:
          - "needles_sharps_plastic" from sharps_waste,
          - "cytotoxic_organic" and "lab_reagents" from chemical_waste.

        Args:
            efficiency (float): A value between 0 and 1 representing the segregation efficiency.

        Returns:
            WasteStream: A new WasteStream instance with the adjusted composition.
        """
        # Create a deep copy of the current composition so as not to modify the original.
        new_comp = copy.deepcopy(self.composition)
        
        # Adjust hazardous fractions based on the provided segregation efficiency.
        if "needles_sharps_plastic" in new_comp.get("sharps_waste", {}):
            new_comp["sharps_waste"]["needles_sharps_plastic"] *= (1 - efficiency)
        if "cytotoxic_organic" in new_comp.get("chemical_waste", {}):
            new_comp["chemical_waste"]["cytotoxic_organic"] *= (1 - efficiency)
        if "lab_reagents" in new_comp.get("chemical_waste", {}):
            new_comp["chemical_waste"]["lab_reagents"] *= (1 - efficiency)
        
        # Return a new WasteStream instance with the same mass but adjusted composition.
        return WasteStream(mass=self.mass, composition=new_comp)
