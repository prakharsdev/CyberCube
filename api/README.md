This API is created using Flask for querying and analyzing CVE (Common Vulnerabilities and Exposures) data stored in a PostgreSQL database. The API allows users to retrieve detailed information on vulnerabilities, their severity, affected products, and more. To ensure security and performance, the API implements features such as API key authentication, rate limiting, and caching.
## 1. Code Structure
The project is organized into the following files and directories:
-	**app.py:** The main entry point for the Flask application. It initializes the Flask app, sets up caching and rate limiting, and registers all API routes. It also manages application-wide error handling and database connection teardown.
-	**db.py:** Manages database connections using PostgreSQL. The connection parameters are sourced from environment variables, ensuring security and flexibility. This module provides functions to query the database and close the connection properly.
-	**queries.py:** Contains SQL queries used by the API endpoints to retrieve data from the PostgreSQL database. These queries cover various analytical functions, such as retrieving the distribution of vulnerabilities by severity, identifying products with the most vulnerabilities, and more.
-	**routes.py:** Defines the HTTP routes (API endpoints) for accessing the CVE data. Each route is secured with API key validation and implements caching and rate limiting to improve performance and prevent abuse. The module also includes utility functions for rendering query results as HTML tables or JSON.
-	**log_config.py:** Configures logging for the API, directing logs to both the console and a file (api.log). This setup ensures that detailed logs are kept for debugging and monitoring purposes.

### Explanation of Code Logic
1.	**Flask Application Setup (app.py):**
-	The Flask app is initialized, and middleware for caching, rate limiting, and logging is set up.
-	The routes defined in routes.py are registered with the app, making the endpoints available.
-	Error handlers are set up to manage common HTTP errors like 404 (Not Found), 401 (Unauthorized), and 429 (Too Many Requests).
-	When the app starts, it listens for incoming HTTP requests and processes them accordingly.
2.	**Database Interaction (db.py):**
-	The database connection is established using PostgreSQL, with connection details pulled from environment variables.
-	query_db() executes SQL queries and fetches results, while close_db_connection() ensures that the database connection is properly closed after use.
3.	**Query Definitions (queries.py):**
-	SQL queries are defined to fetch specific data from the database, such as severity distributions, the worst products, and top vulnerabilities by impact or exploitability.
4.	**Routing and API Logic (routes.py):**
-	Routes are defined for each API endpoint, with functions handling incoming requests, querying the database, and returning formatted responses.
-	Security measures, like API key validation, are implemented to restrict access to authorized users.
-	Utility functions are used to render the results in various formats, such as JSON or HTML tables.
5.	**Logging Configuration (log_config.py):**
-	Logging is configured to capture detailed logs of API activity, errors, and performance, aiding in monitoring and debugging.

## 2. Chosen Open API and Rationale for Selection
**Chosen API:** NVD (National Vulnerability Database) API
The NVD API was selected for this project because it provides comprehensive and up-to-date information about CVEs, which is essential for security analysis. The API offers structured data on vulnerabilities, including their descriptions, severity metrics, and associated products. This makes it a reliable source for building a database that can be queried for insights into software vulnerabilities.
Rationale for Selection:
-	**Comprehensive Data:** The NVD API offers detailed information on a wide range of vulnerabilities, including CVSS scores, affected products, and references.
-	**Structured Format:** The API provides data in a well-structured JSON format, making it easy to parse and integrate into the ETL pipeline.
-	**Regular Updates:** The NVD API is frequently updated with new vulnerabilities, ensuring that the data remains current and relevant.
  
### Why Flask Was Chosen Over Other Frameworks
Flask was chosen as the framework for this API for several key reasons, particularly when compared to alternatives like GraphQL and traditional REST frameworks:
1. **Simplicity and Flexibility:**
-	Flask is a micro-framework, meaning it comes with minimal built-in features, allowing developers to add only what is needed. This is ideal for a project like this, where specific tools (e.g., caching, rate limiting) are needed without the overhead of a full-stack framework.
-	Flask’s simplicity allows for easy setup and quick iteration, which is beneficial during the development of APIs that need to be scalable and customizable.
2. **Easy Integration with SQL Databases:**
-	Flask seamlessly integrates with SQL databases, particularly with extensions like SQLAlchemy or directly with psycopg2 for PostgreSQL. This makes it easier to manage database interactions within the API.
-	The project's need to handle complex SQL queries is well-served by Flask’s straightforward request handling and database integration capabilities.
3. **Lightweight and Scalable:**
-	Flask’s lightweight nature makes it an excellent choice for APIs that need to be deployed in various environments, from local development to cloud-based production systems.
-	The framework is scalable, allowing the API to grow in complexity as the project evolves without needing a complete overhaul of the architecture.
4. **Community and Ecosystem:**
-	Flask has a large and active community, providing a wealth of extensions, plugins, and support resources. This makes it easier to find solutions and best practices for common tasks like authentication, logging, and deployment.
-	The ecosystem around Flask includes robust tools for testing, deployment, and monitoring, which are critical for maintaining a reliable API.
5. **Comparison to GraphQL:**
-	GraphQL offers a more flexible querying mechanism, allowing clients to specify exactly what data they need. However, for this project, the simplicity and predictability of REST-like endpoints (using Flask) were preferred, especially given the structured nature of the data being served.
-	Implementing GraphQL might introduce additional complexity in both the server and client-side logic, which was unnecessary given the API’s straightforward requirements.
6. **Comparison to Full REST Frameworks:**
-	Full REST frameworks like Django REST Framework provide many built-in features out of the box, such as authentication, serialization, and more. However, these also come with additional complexity and overhead.
-	Flask provides just enough structure to implement REST-like APIs without the rigidity of a full REST framework, allowing for more control over the application’s architecture.
In summary, Flask was chosen for its simplicity, flexibility, and strong integration with SQL databases, making it well-suited for developing a scalable and maintainable API for querying CVE data.

## How to Use the API
**Step 1:**
Run the API
Start the Flask application:
```bash
python app.py
```

The API will be available at 
```
http://localhost:5000/
```

**Step 2:** Testing the API with Postman
Postman is a popular tool for testing and interacting with APIs. Below are the steps to set up and test the CVE Data API using Postman.
1.	**Install Postman:** If you haven’t already, download and install Postman from the official [website](https://www.postman.com/downloads/).
2.	**Create a new request:**
-	Set the request method to GET.
-	Enter the URL (e.g., http://localhost:5000/api/vulnerabilities).
-	Under the Headers tab, add a key X-API-Key with the value of your API key.
3.	**Send the request:** Click the Send button to make the request and view the response.
4.	**Explore other endpoints:** Test other API endpoints by adjusting the URL and parameters as needed.
4. API Documentation
 	
## API Endpoints
All endpoints below require a GET request and must include the X-API-Key header with your API key for authentication. Successful requests return a 200 OK status, and responses are provided as JSON or HTML tables, depending on the endpoint.

### 1. Get Vulnerabilities
-**Endpoint:** /api/vulnerabilities
-**Parameters:**
     ~cve_id (optional): Filter by a specific CVE ID.
     ~product_id (optional): Filter by a specific product ID.
-**Response:** List of vulnerabilities based on the provided filters.
![image](https://github.com/user-attachments/assets/9233834a-327c-41eb-a378-78c764fc856a)

### 2. Get Severity Distribution
-**Endpoint:** /api/severity-distribution
-**Response:** Count of vulnerabilities grouped by severity level.
![image](https://github.com/user-attachments/assets/4a2dd208-beca-4f5d-962d-e5a58fd00291)


### 3. Get Worst Products
-**Endpoint:** /api/worst-products
-**Response:** List of products with the highest number of vulnerabilities.
![image](https://github.com/user-attachments/assets/08327c10-ebbc-4533-97f1-c9d2dcc435ff)


### 4. Get Top Impact Vulnerabilities
-**Endpoint:** /api/top-impact-vulnerabilities
-**Response:** Top 10 vulnerabilities with the highest impact scores.
![image](https://github.com/user-attachments/assets/738b8652-fd1b-4629-a945-5283d311c15a)


### 5. Get Top Exploitability Vulnerabilities
-**Endpoint:** /api/top-exploitability-vulnerabilities
-**Response:** Top 10 vulnerabilities with the highest exploitability scores.
![image](https://github.com/user-attachments/assets/36c4beb2-bacf-4f66-a99f-ac034efc80a7)


### 6. Get Top Attack Vectors
-**Endpoint:** /api/top-attack-vectors
-**Response:** Most common attack vectors associated with vulnerabilities.
![image](https://github.com/user-attachments/assets/f8c6c5b0-611c-4327-9362-447e3c0f5001)


## Additional Analytical Endpoints

### 7. Get Common Weaknesses
-**Endpoint:** /api/common-weaknesses
-**Response:** List of the most common weaknesses (CWEs) associated with vulnerabilities.
![image](https://github.com/user-attachments/assets/688cad5a-27e4-4f0a-b4ce-394559433ba0)


### 8. Get Most Affected Vendors
-**Endpoint:** /api/most-affected-vendors
-**Response:** Vendors with the most products affected by vulnerabilities.
![image](https://github.com/user-attachments/assets/464365f3-48c2-499c-b152-789d9529110a)


### 9. Get Most Common Configurations
-**Endpoint:** /api/most-common-configurations
-**Response:** Most frequently occurring configurations linked to vulnerabilities.
![image](https://github.com/user-attachments/assets/20f26133-2c05-4739-9299-7079498fd50c)


### 10. Get Vulnerability Trends
-**Endpoint:** /api/vulnerability-trends
-**Response:** Trend analysis of vulnerabilities over time.
![image](https://github.com/user-attachments/assets/0e5f483d-50a2-4c7a-8325-0ac771c978d2)


### 11. Get Products with Common Attack Vectors
-**Endpoint:** /api/products-common-attack-vectors
-**Response:** Products frequently associated with common attack vectors.
![image](https://github.com/user-attachments/assets/8b3acba1-0e1d-4d4f-9d11-44c17b86dba0)

  
## Error Handlers
The API includes the following error handlers to manage common issues:
-	**401 Unauthorized:** Triggered when an invalid or missing API key is provided. Returns a 401 status with a message explaining the issue.
-	**404 Not Found:** Triggered when an endpoint or resource is not found. Returns a 404 status with a message indicating the resource was not found.
-	**429 Too Many Requests:** Triggered when a client exceeds the rate limit. Returns a 429 status with a message advising the client to wait before making further requests.

## 5. Additional Information
**Logging**
API logs are saved to api.log and also output to the console. The logging configuration can be modified in log_config.py.

**Caching and Rate Limiting**
The API uses Flask-Caching to cache responses for frequently accessed endpoints, improving performance. Rate limiting is implemented using Flask-Limiter to prevent abuse.

**Security**
-	**API Key Authentication:** All endpoints require a valid API key.
-	**Rate Limiting:** Prevents excessive requests from a single IP address, ensuring fair use.

**Future Improvements**
-	**Expanded Query Options:** Add more filtering and sorting options to existing endpoints.
-	**Enhanced Security:** Implement OAuth2 or JWT for more robust authentication.
-	**Monitoring and Alerts:** Integrate monitoring tools to track API usage and detect anomalies.
