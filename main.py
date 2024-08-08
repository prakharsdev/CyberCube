from db.database import create_tables, conn, cur
from ingestion.fetch_data import fetch_data
from transformation.transform_data import transform_data
from loading.load_data import load_data
import logging
from log.logging_config import setup_logging  # Updated import path

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    try:
        create_tables()

        cve_data = fetch_data()
        if cve_data:
            transformed_data = transform_data(cve_data)
            load_data(transformed_data)
        else:
            logger.warning("No data fetched to process.")

    except Exception as e:
        logger.error("An error occurred in the ETL process.", exc_info=True)
    finally:
        # Close the connection
        try:
            cur.close()
            conn.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error("Failed to close the database connection.", exc_info=True)

if __name__ == "__main__":
    main()
