from flask import Blueprint, jsonify, request, abort, render_template_string
from functools import wraps
from db import query_db
import queries  # Import the queries

API_KEY = "CyBeRcUbe123456789"

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return func(*args, **kwargs)
        else:
            abort(401)  # Unauthorized
    return wrapper

def register_routes(app, cache, limiter):
    @app.route('/')
    def home():
        return "Welcome to the CVE API!"

    @app.route('/api/vulnerabilities', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def get_vulnerabilities():
        cve_id = request.args.get('cve_id')
        product_id = request.args.get('product_id')

        if cve_id:
            results = query_db(queries.get_vulnerabilities_by_cve_id(), [cve_id])
        elif product_id:
            results = query_db(queries.get_vulnerabilities_by_product_id(), [product_id])
        else:
            results = query_db(queries.get_all_vulnerabilities())

        return render_table(results)

    @app.route('/api/severity-distribution', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def severity_distribution():
        results = query_db(queries.get_severity_distribution())
        return render_table(results)

    @app.route('/api/worst-products', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def worst_products():
        results = query_db(queries.get_worst_products())
        return render_table(results)

    @app.route('/api/top-impact-vulnerabilities', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def top_impact_vulnerabilities():
        results = query_db(queries.get_top_impact_vulnerabilities())
        return render_table(results)

    @app.route('/api/top-exploitability-vulnerabilities', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def top_exploitability_vulnerabilities():
        results = query_db(queries.get_top_exploitability_vulnerabilities())
        return render_table(results)

    @app.route('/api/top-attack-vectors', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
    @cache.cached(timeout=60)  # Cache this route for 60 seconds
    def top_attack_vectors():
        results = query_db(queries.get_top_attack_vectors())
        return render_table(results)
    
    # New Routes for Additional Analytical Questions

    @app.route('/api/common-weaknesses', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")
    @cache.cached(timeout=60)
    def common_weaknesses():
        results = query_db(queries.get_common_weaknesses())
        return render_table(results)

    @app.route('/api/most-affected-vendors', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")
    @cache.cached(timeout=60)
    def most_affected_vendors():
        results = query_db(queries.get_most_affected_vendors())
        return render_table(results)

    @app.route('/api/most-common-configurations', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")
    @cache.cached(timeout=60)
    def most_common_configurations():
        results = query_db(queries.get_most_common_configurations())
        return render_table(results)

    @app.route('/api/vulnerability-trends', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")
    @cache.cached(timeout=60)
    def vulnerability_trends():
        results = query_db(queries.get_vulnerability_trends())
        return render_table(results)

    @app.route('/api/products-common-attack-vectors', methods=['GET'])
    @require_api_key
    @limiter.limit("5 per minute")
    @cache.cached(timeout=60)
    def products_common_attack_vectors():
        results = query_db(queries.get_products_with_common_attack_vectors())
        return render_table(results)

    # Error handler for 401 Unauthorized
    @app.errorhandler(401)
    def unauthorized_error(e):
        return jsonify({"error": "Unauthorized", "message": "Invalid or missing API key."}), 401

def render_table(data):
    if not data:
        return "No data available"

    table_html = '''
    <table border="1">
        <thead>
            <tr>
                {}
            </tr>
        </thead>
        <tbody>
            {}
        </tbody>
    </table>
    '''

    # Generate the table headers
    headers = ''.join([f'<th>{key}</th>' for key in data[0].keys()])

    # Generate the table rows
    rows = ''
    for row in data:
        row_html = ''.join([f'<td>{value}</td>' for value in row.values()])
        rows += f'<tr>{row_html}</tr>'

    # Format the full table HTML
    table_html = table_html.format(headers, rows)

    return render_template_string(table_html)
