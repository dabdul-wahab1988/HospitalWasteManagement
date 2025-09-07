# HospitalWasteManagement/src/database.py

import logging
from pathlib import Path
from typing import Dict, Any
import brightway2 as bw

def setup_project(project_name: str) -> bw.Database:
    if project_name not in bw.projects:
        bw.projects.create_project(project_name)
        logging.info(f"Created project '{project_name}'.")
    bw.projects.set_current(project_name)
    bw.bw2setup()  # Sets up biosphere3.
    logging.info("Biosphere3 setup complete.")
    return bw.Database("biosphere3")

def build_flow_index(bio_db: bw.Database) -> Dict[str, Any]:
    index = {}
    for flow in bio_db:
        index[flow["code"]] = flow
    return index

def get_flow_by_uuid(flow_index: Dict[str, Any], uuid: str) -> Any:
    if uuid in flow_index:
        return flow_index[uuid]
    else:
        logging.error(f"Flow with UUID {uuid} not found.")
        raise KeyError(f"Flow with UUID {uuid} missing.")

def retrieve_flows(flow_index: Dict[str, Any]) -> Dict[str, Any]:
    flow_uuids = {
        "co2_fossil": "aa7cac3a-3625-41d4-bc54-33e2cf11ec46",
        "co2_biogenic": "d6235194-e4e6-4548-bfa3-ac095131aef4",
        "ch4_fossil": "70ef743b-3ed5-4a6d-b192-fb6d62378555",
        "ch4_biogenic": "da1157e2-7593-4dfd-80dd-a3449b37a4d8",
        "nox": "77357947-ccc5-438e-9996-95e65e1e1bce",
        "so2": "78c3efe4-421c-4d30-82e4-b97ac5124993",
        "pm25": "66f50b33-fd62-4fdd-a373-c5b0de7de00d",
        "hg": "5ec9c16a-959d-44cd-be7d-a935727d2151",
        "pb": "2718482b-8399-442e-b89a-52fbcc22d2e6",
        "dioxin": "f77c5e36-ee47-4437-b757-03139bb1d6d6",
        "pahs": "13d898ac-b9be-4723-a153-565e2a9144ac",
        "nmvoc": "33b38ccb-593b-4b11-b965-10d747ba3556",
        "nh3": "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
        "pm10": "7678cec7-b8e1-439d-8242-99cd452834b1",
        "chlorine_air": "247ac273-60fa-4e21-9408-793f75fa1d37",
        "land_occupation": "1eaa9ea4-40b8-414a-b198-5626400372e1",
    }
    flows = {}
    for key, uuid in flow_uuids.items():
        try:
            flows[key] = get_flow_by_uuid(flow_index, uuid)
        except KeyError:
            flows[key] = None
    return flows

def create_or_reset_db(db_name: str) -> bw.Database:
    if db_name in bw.databases:
        bw.Database(db_name).delete()
        logging.info(f"Deleted existing database '{db_name}'.")
    db = bw.Database(db_name)
    db.register()
    logging.info(f"Created and registered database '{db_name}'.")
    return db

from typing import Any

def create_activity(db: bw.Database, code: str, name: str, unit: str = "kilogram") -> Any:
    """
    Creates a new activity in the specified database.
    
    Args:
        db (bw.Database): The database in which to create the activity.
        code (str): A unique code for the activity.
        name (str): The name of the activity.
        unit (str): The unit for the activity (default is "kilogram").
    
    Returns:
        Any: The newly created activity.
    """
    act = db.new_activity(code=code)
    act["name"] = name
    act["unit"] = unit
    act.save()
    return act

def add_production_exchange(act: Any, amount: float = 1.0):
    for exc in list(act.exchanges()):
        if exc["type"] == "production":
            exc.delete()
    act.new_exchange(
        amount=amount,
        type="production",
        unit=act["unit"],
        input=act.key
    ).save()

def add_biosphere_exchanges(act: Any, emissions: Dict[str, Any], flows: Dict[str, Any]):
    for flow_name, amount in emissions.items():
        flow_obj = flows.get(flow_name)
        if flow_obj is None:
            logging.error(f"Missing flow for '{flow_name}'. Skipping exchange.")
            continue
        if abs(amount.magnitude) <= 1e-15:
            continue
        try:
            act.new_exchange(
                amount=amount.magnitude,
                type="biosphere",
                unit=str(amount.units),
                input=flow_obj.key
            ).save()
        except Exception as e:
            logging.error(f"Failed to add exchange for '{act['name']}' with flow '{flow_name}': {e}")
