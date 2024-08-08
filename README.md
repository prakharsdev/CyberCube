# CyberCube
This project is an ETL (Extract, Transform, Load) pipeline designed to fetch, process, and store CVE (Common Vulnerabilities and Exposures) data from an external API. The ETL process extracts CVE data, transforms it into a structured format, and loads it into a PostgreSQL database. The stored data can then be queried and analyzed to gain insights into vulnerabilities, their severity, affected products, and more.

## 1. Code Structure
The project is organized into the following files and directories:
1.	**fetch.py:** Contains the logic to fetch raw CVE data from the external API.
2.	**transform_data.py:** Handles the transformation of raw data into a format suitable for database storage.
3.	**load_data.py:** Loads the transformed data into the PostgreSQL database, with optional batch processing for large datasets.
4.	**database.py:** Manages database connections, table creation, and initial setup.
5.	**logging_config.py:** Configures logging to capture ETL process logs, which are stored both in the console and a log file.
6.	**main.py:** Orchestrates the entire ETL process, calling the fetch, transform, and load functions in sequence.

### Explanation of Code Logic
1.	**Fetching Data (fetch.py):**
	The script sends a request to an external API to retrieve CVE data within a specified date range. The data is received in JSON format and returned for further processing.
2.	**Transforming Data (transform_data.py):**
	The raw JSON data is transformed into a structured format suitable for database storage. This includes flattening nested structures, standardizing field names, and ensuring that all necessary fields are present.
3.	**Loading Data (load_data.py):**
	The transformed data is inserted into the appropriate tables in the PostgreSQL database. Batch processing is used to handle large datasets efficiently, and errors are logged for further analysis.
4.	**Database Management (database.py):**
	This module handles the creation of database tables if they do not already exist, and manages connections to the PostgreSQL database using environment variables for configuration.
5.	**Logging (logging_config.py):**
	Logs are generated for each stage of the ETL process, providing detailed information on the operations performed and any errors encountered.
6.	**ETL Orchestration (main.py):**
	This script coordinates the entire ETL process by calling the fetch, transform, and load functions in sequence. It ensures that the database is ready and handles errors gracefully.

## 2. ETL Design and Data Model Explanation

### ETL Design
The ETL process is designed to be modular and scalable, allowing for easy maintenance and updates. The data flow is as follows:
1.	**Extract:** Data is extracted from an external API that provides up-to-date CVE information.
2.	**Transform:** The raw JSON data is cleaned, structured, and normalized to fit the database schema.
3.	**Load:** The transformed data is inserted into a PostgreSQL database, where it is stored for querying and analysis.

### Data Model Explanation
The data model is structured to capture detailed information about vulnerabilities, affected products, associated metrics, and references. The schema is normalized to reduce redundancy and improve data integrity.

### Columns and Table Explanation
1.	**cve_entries:**
-	Columns: id, cve_id, source_identifier, published, last_modified, vuln_status
-	Purpose: Stores core information about each CVE entry.
2.	**descriptions:**
-	Columns: id, cve_entry_id, lang, description
-	Purpose: Stores multilingual descriptions of each CVE, linked to the cve_entries table.
3.	**metrics:**
-	Columns: id, cve_entry_id, version, vector_string, attack_vector, attack_complexity, privileges_required, user_interaction, scope, confidentiality_impact, integrity_impact, availability_impact, base_score, base_severity, exploitability_score, impact_score
-	Purpose: Stores detailed CVSS metrics for each CVE, allowing for severity analysis and risk assessment.
4.	**weaknesses:**
-	Columns: id, cve_entry_id, source, description
-	Purpose: Captures details of weaknesses associated with each CVE, aiding in vulnerability categorization.
5.	**configurations:**
-	Columns: id, cve_entry_id, operator, negate
-	Purpose: Represents logical configurations under which products are vulnerable, linked to specific CVEs.
6.	**products:**
-	Columns: id, config_id, vulnerable, criteria, part, vendor, product, version, version_end_excluding
-	Purpose: Details affected products, including version information and vulnerability status.
7.	**cve_references:**
-	Columns: id, cve_entry_id, url, source, tags
-	Purpose: Stores references to external sources for each CVE, providing additional context and information.

### Database Schema and Design Reasoning
The database schema is designed with normalization principles in mind to ensure data integrity, reduce redundancy, and improve query performance. Each table has a specific purpose, and foreign keys are used to maintain relationships between related data (e.g., linking CVE entries to their descriptions, metrics, and affected products).
This design allows for efficient querying and analysis, enabling detailed insights into vulnerabilities, their impact, and the affected systems.
![ERD](https://github.com/user-attachments/assets/0a5db330-116b-4027-a365-c43b199c90d4)


## 3. How to Set Up
### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/prakharsdev/CyberCube.git
cd your_repository
```
### Step 2: Create a Virtual Environment
Set up a virtual environment using conda:
For conda:
```bash
conda create --name cybercube 
conda activate cybercube
```

### Step 3: Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a .env file in the root of your project directory with the following contents:
```bash
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```
These environment variables configure the connection to your PostgreSQL database.

### Step 5: Create the Database Tables
Run the main.py script to create the necessary database tables and execute the ETL process:
```bash
python main.py
```
The script will fetch CVE data, transform it, and load it into the PostgreSQL database.

## 4. Additional Information
**Logging**
The ETL process logs its operations to both the console and a file named etl_process.log. This log file can be found in the log directory. The logging configuration can be adjusted in logging_config.py.
Batch Processing
The load_data.py file supports batch processing for large datasets. You can toggle batch processing by setting the use_batch_processing parameter in the load_data() function.

**Error Handling**
If any errors occur during the ETL process, they are logged, and the process attempts to continue processing other data. You can review the logs for detailed error information.


**Future Improvements**
•	**Data Validation:** Implement additional data validation checks during the transformation process to ensure data integrity.
•	**Scalability:** Explore the use of distributed systems or cloud-based services to handle larger datasets more efficiently.

