
# Hospital Waste Management LCA

This project implements a Life Cycle Assessment (LCA) framework for hospital waste management using the Brightway2 framework. The model estimates the environmental impacts associated with different biomedical waste treatment technologies—including incineration, landfill, pyrolysis, chemical disinfection, autoclave, and microwave processes—by combining both direct and indirect emissions. Various scenarios (e.g., BASELINE, ENHANCED_INCINERATION, HIGH_TECH, etc.) are modeled to assess the influence of process improvements and policy interventions.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Notes](#Notes)

# Hospital Waste Management LCA

This project implements a Life Cycle Assessment (LCA) framework for hospital waste management using the Brightway2 framework. The model estimates the environmental impacts associated with different biomedical waste treatment technologies — including incineration, landfill, pyrolysis, chemical disinfection, autoclave, and microwave — by combining both direct and indirect emissions. Various scenarios (e.g., BASELINE, ENHANCED_INCINERATION, HIGH_TECH) are modeled to assess the influence of process improvements and policy interventions.

## Table of Contents

- [Introduction](#introduction)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Notes](#notes)

## Introduction

Hospital waste management is a critical environmental and public health issue. This project provides a modular, scalable LCA framework that:
- Models multiple treatment technologies with process-specific emission factors.
- Accounts for both direct and indirect emissions (e.g., energy use, transportation, infrastructure).
- Integrates scenario analysis to evaluate the effects of different waste segregation efficiencies, process improvements, and policy changes.
- Uses Brightway2 for database management and LCIA calculations and Pint for unit handling.

## Project structure

The project is organized as follows:

```
HospitalWasteManagement/
├── src/
│   ├── __init__.py
│   ├── config.py                # Project configuration and constants (emission factors, waste composition, scenarios, etc.)
│   ├── waste_stream.py          # Definition of the WasteStream class to represent waste flows.
│   ├── processes/               # Module containing treatment process implementations.
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base class for treatment processes.
│   │   ├── incineration.py      # Incineration process calculations.
│   │   ├── landfill.py          # Landfill process calculations.
│   │   ├── pyrolysis.py         # Pyrolysis process calculations.
│   │   ├── chem_disinfection.py # Chemical disinfection process calculations.
│   │   ├── autoclave.py         # Autoclave process calculations.
│   │   └── microwave.py         # Microwave process calculations.
│   ├── indirect.py              # Indirect emissions calculator based on hospital-specific factors.
│   ├── database.py              # Functions for setting up the Brightway2 project, managing databases, and handling flows.
│   ├── lcia.py                  # Functions for calculating LCIA scores.
│   └── main.py                  # Main execution script tying all components together.
├── tests/
│   ├── __init__.py
│   ├── test_waste_stream.py   # Unit tests for the WasteStream class.
│   ├── test_processes.py      # Unit tests for treatment process calculations.
│   └── test_database.py       # Unit tests for database and biosphere flow functions.
├── requirements.txt           # Python dependencies (see below)
└── README.md                  # This file.
```

## Installation

1. Clone the repository:

```powershell
git clone <repository-url>
cd HospitalWasteManagement
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
# macOS / Linux
# source venv/bin/activate
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows CMD
# venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

The `requirements.txt` file includes (at minimum):

- brightway2
- pint

Note: Brightway2 requires an initial setup step to create the local Brightway project metadata and the biosphere database. After installing dependencies, run one of the following to initialize Brightway2:

```python
python -c "import brightway2 as bw; bw.bw2setup()"
```

or from an interactive Python session:

```python
import brightway2 as bw
bw.bw2setup()
```

Brightway2 can require additional system-level dependencies on some platforms; consult Brightway2 documentation if setup fails.

## Usage

To run the LCA model and generate scenario results:

```powershell
python src/main.py
```

This script will:
- Set up the Brightway2 project and load the biosphere database (if not already initialized).
- Create a process database for hospital waste management activities.
- Generate waste streams for each hospital and adjust them based on segregation efficiency.
- Calculate direct emissions for each treatment process and add indirect emissions (if applicable).
- Compute LCIA scores for various impact categories.
- Export the results to `scenario_results.csv`.

## Testing

Run unit tests:

```powershell
python -m unittest discover -s tests -v
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of the change and any tests.

## License

This project is licensed under the MIT License.

## Notes

- `src/`: Source code for the project.
- `config.py`: External configurations and constants (emission factors, scenarios, etc.).

For details on individual modules and their behaviors see the source files in `src/` and `src/processes/`.
