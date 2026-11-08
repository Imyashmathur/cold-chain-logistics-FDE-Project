from pathlib import Path
from pandas as pd
import urllib
import os
from sqlalchemy import create_engine 
from dotenv import load_dotenv

#__file__ is 'experiment/phase-0/ingest_legacy_data.py'
script_dir = Path(__file__).resolve.parent # points to experiment/phase-0
project_root = script_dir.parents[0] # climbs up 1 levels to project root

load_dotenv(project_root / ".env")

data_path = project_root / "data" / "raw" / "dynamic_supply_chain_logistics_dataset.csv"

db_host = os.getenv("SQL_SERVER_HOST", "localhost")
db_port = os.getenv("SQL_SERVER_PORT", "1433")