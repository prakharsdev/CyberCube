from psycopg2 import sql
from db.database import conn, cur
import logging
from log.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

BATCH_SIZE = 1000  # Example batch size

def load_data(transformed_data, use_batch_processing=True):
    if transformed_data:
        logger.info(f"Loading data for {len(transformed_data)} vulnerabilities.")

        def process_batch(batch):
            try:
                for item in batch:
                    cve_id = item["cve_id"]
                    source_identifier = item["source_identifier"]
                    published = item["published"]
                    last_modified = item["last_modified"]
                    vuln_status = item["vuln_status"]

                    cur.execute(
                        sql.SQL("INSERT INTO cve_entries (cve_id, source_identifier, published, last_modified, vuln_status) VALUES (%s, %s, %s, %s, %s) RETURNING id"),
                        [cve_id, source_identifier, published, last_modified, vuln_status]
                    )
                    entry_id = cur.fetchone()[0]

                    # Insert into descriptions table
                    for desc in item["descriptions"]:
                        cur.execute(
                            sql.SQL("INSERT INTO descriptions (cve_entry_id, lang, description) VALUES (%s, %s, %s)"),
                            [entry_id, desc["lang"], desc["description"]]
                        )

                    # Insert into metrics table
                    for metric in item["metrics"]:
                        cur.execute(
                            sql.SQL("""
                                INSERT INTO metrics (cve_entry_id, version, vector_string, attack_vector, attack_complexity, privileges_required, user_interaction, scope, confidentiality_impact, integrity_impact, availability_impact, base_score, base_severity, exploitability_score, impact_score)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """),
                            [
                                entry_id, metric["version"], metric["vector_string"], metric["attack_vector"],
                                metric["attack_complexity"], metric["privileges_required"], metric["user_interaction"],
                                metric["scope"], metric["confidentiality_impact"], metric["integrity_impact"],
                                metric["availability_impact"], metric["base_score"], metric["base_severity"],
                                metric["exploitability_score"], metric["impact_score"]
                            ]
                        )

                    # Insert into weaknesses table
                    for weakness in item["weaknesses"]:
                        cur.execute(
                            sql.SQL("INSERT INTO weaknesses (cve_entry_id, source, description) VALUES (%s, %s, %s)"),
                            [entry_id, weakness["source"], weakness["description"]]
                        )

                    # Insert into configurations and products table
                    for config in item["configurations"]:
                        cur.execute(
                            sql.SQL("INSERT INTO configurations (cve_entry_id, operator, negate) VALUES (%s, %s, %s) RETURNING id"),
                            [entry_id, config["operator"], config["negate"]]
                        )
                        config_id = cur.fetchone()[0]

                        cur.execute(
                            sql.SQL("INSERT INTO products (config_id, vulnerable, criteria, part, vendor, product, version, version_end_excluding) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"),
                            [config_id, config["vulnerable"], config["criteria"], config["part"], config["vendor"], config["product"], config["version"], config["version_end_excluding"]]
                        )

                    # Insert into references table
                    for ref in item["references"]:
                        cur.execute(
                            sql.SQL("INSERT INTO cve_references (cve_entry_id, url, source, tags) VALUES (%s, %s, %s, %s)"),
                            [entry_id, ref["url"], ref["source"], ref["tags"]]
                        )

                    logger.debug(f"Processed and loaded CVE: {cve_id}")

                conn.commit()  # Commit the batch
                logger.info(f"Batch committed successfully.")
                logger.debug(f"Processed and loaded CVE: {cve_id}")
            except Exception as e:
                logger.error(f"Error occurred during batch processing. Rolling back.", exc_info=True)
                conn.rollback()  # Rollback if any error occurs in the batch
                raise e  # Re-raise the exception to be handled outside

        if use_batch_processing:
            for i in range(0, len(transformed_data), BATCH_SIZE):
                batch = transformed_data[i:i + BATCH_SIZE]
                process_batch(batch)
        else:
            process_batch(transformed_data)

        logger.info("Data loading completed successfully.")
