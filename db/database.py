import psycopg2
import os
import logging
from dotenv import load_dotenv
from log.logging_config import setup_logging  # Updated import path

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

try:
    # Database connection setup using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error("Failed to connect to the database.", exc_info=True)
    raise e

def create_tables():
    try:
        # Create cve_entries table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cve_entries (
                id SERIAL PRIMARY KEY,
                cve_id TEXT UNIQUE,
                source_identifier TEXT,
                published TIMESTAMP,
                last_modified TIMESTAMP,
                vuln_status TEXT
            )
        ''')
        logger.debug("cve_entries table created or already exists.")

        # Create descriptions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS descriptions (
                id SERIAL PRIMARY KEY,
                cve_entry_id INTEGER REFERENCES cve_entries(id),
                lang TEXT,
                description TEXT
            )
        ''')
        logger.debug("descriptions table created or already exists.")

        # Create metrics table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id SERIAL PRIMARY KEY,
                cve_entry_id INTEGER REFERENCES cve_entries(id),
                version TEXT,
                vector_string TEXT,
                attack_vector TEXT,
                attack_complexity TEXT,
                privileges_required TEXT,
                user_interaction TEXT,
                scope TEXT,
                confidentiality_impact TEXT,
                integrity_impact TEXT,
                availability_impact TEXT,
                base_score FLOAT,
                base_severity TEXT,
                exploitability_score FLOAT,
                impact_score FLOAT
            )
        ''')
        logger.debug("metrics table created or already exists.")

        # Create weaknesses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS weaknesses (
                id SERIAL PRIMARY KEY,
                cve_entry_id INTEGER REFERENCES cve_entries(id),
                source TEXT,
                description TEXT
            )
        ''')
        logger.debug("weaknesses table created or already exists.")

        # Create configurations table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS configurations (
                id SERIAL PRIMARY KEY,
                cve_entry_id INTEGER REFERENCES cve_entries(id),
                operator TEXT,
                negate BOOLEAN
            )
        ''')
        logger.debug("configurations table created or already exists.")

        # Create products table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                config_id INTEGER REFERENCES configurations(id),
                vulnerable BOOLEAN,
                criteria TEXT,
                part TEXT,
                vendor TEXT,
                product TEXT,
                version TEXT,
                version_end_excluding TEXT
            )
        ''')
        logger.debug("products table created or already exists.")

        # Create references table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cve_references (
                id SERIAL PRIMARY KEY,
                cve_entry_id INTEGER REFERENCES cve_entries(id),
                url TEXT,
                source TEXT,
                tags TEXT[]
            )
        ''')
        logger.debug("cve_references table created or already exists.")

        conn.commit()
        logger.info("All tables created successfully.")
    except Exception as e:
        logger.error("Error occurred while creating tables.", exc_info=True)
        raise e
