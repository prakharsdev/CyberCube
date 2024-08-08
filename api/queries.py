def get_vulnerabilities_by_cve_id():
    return """
    SELECT * FROM cve_entries
    WHERE cve_id = %s;
    """

def get_vulnerabilities_by_product_id():
    return """
    SELECT cve_entries.*
    FROM cve_entries
    JOIN configurations ON cve_entries.id = configurations.cve_entry_id
    JOIN products ON configurations.id = products.config_id
    WHERE products.id = %s;
    """

def get_all_vulnerabilities():
    return """
    SELECT * FROM cve_entries;
    """

def get_severity_distribution():
    return """
    SELECT metrics.base_severity, COUNT(*)
    FROM metrics
    GROUP BY metrics.base_severity;
    """

def get_worst_products():
    return """
    SELECT products.product, COUNT(*) AS vulnerability_count
    FROM products
    JOIN configurations ON products.config_id = configurations.id
    JOIN cve_entries ON configurations.cve_entry_id = cve_entries.id
    GROUP BY products.product
    ORDER BY vulnerability_count DESC
    LIMIT 10;
    """

def get_top_impact_vulnerabilities():
    return """
    SELECT cve_entries.cve_id, metrics.impact_score
    FROM cve_entries
    JOIN metrics ON cve_entries.id = metrics.cve_entry_id
    ORDER BY metrics.impact_score DESC
    LIMIT 10;
    """

def get_top_exploitability_vulnerabilities():
    return """
    SELECT cve_entries.cve_id, metrics.exploitability_score
    FROM cve_entries
    JOIN metrics ON cve_entries.id = metrics.cve_entry_id
    ORDER BY metrics.exploitability_score DESC
    LIMIT 10;
    """

def get_top_attack_vectors():
    return """
    SELECT metrics.attack_vector, COUNT(*) AS count
    FROM metrics
    GROUP BY metrics.attack_vector
    ORDER BY count DESC
    LIMIT 10;
    """

#Additional queries

#What are the most common weaknesses (CWEs) associated with vulnerabilities?
def get_common_weaknesses():
    return """
    SELECT weaknesses.description, COUNT(*) AS occurrence
    FROM weaknesses
    GROUP BY weaknesses.description
    ORDER BY occurrence DESC
    LIMIT 10;
    """
#Which vendors have the most products affected by vulnerabilities?
def get_most_affected_vendors():
    return """
    SELECT products.vendor, COUNT(DISTINCT products.product) AS affected_product_count
    FROM products
    JOIN configurations ON products.config_id = configurations.id
    JOIN cve_entries ON configurations.cve_entry_id = cve_entries.id
    GROUP BY products.vendor
    ORDER BY affected_product_count DESC
    LIMIT 10;
    """
#What configurations (combinations of product versions and criteria) are most frequently associated with vulnerabilities?
def get_most_common_configurations():
    return """
    SELECT configurations.operator, COUNT(*) AS occurrence
    FROM configurations
    JOIN products ON configurations.id = products.config_id
    GROUP BY configurations.operator
    ORDER BY occurrence DESC
    LIMIT 10;
    """
#How has the frequency of vulnerabilities changed over time (e.g., monthly trends)?
def get_vulnerability_trends():
    return """
    SELECT DATE_TRUNC('month', published) AS month, COUNT(*) AS count
    FROM cve_entries
    GROUP BY month
    ORDER BY month DESC;
    """
#Which products are frequently associated with multiple CVEs that share the same attack vector?
def get_products_with_common_attack_vectors():
    return """
    SELECT products.product, metrics.attack_vector, COUNT(*) AS cve_count
    FROM products
    JOIN configurations ON products.config_id = configurations.id
    JOIN cve_entries ON configurations.cve_entry_id = cve_entries.id
    JOIN metrics ON cve_entries.id = metrics.cve_entry_id
    GROUP BY products.product, metrics.attack_vector
    HAVING COUNT(*) > 1
    ORDER BY cve_count DESC
    LIMIT 10;
    """
