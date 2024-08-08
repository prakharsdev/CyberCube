import logging
from log.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def transform_data(cve_data):
    logger.info("Transforming data.")
    transformed_data = []

    if "vulnerabilities" in cve_data:
        for item in cve_data["vulnerabilities"]:
            cve = item.get("cve", {})
            
            transformed_entry = {
                "cve_id": cve.get("id", "N/A"),
                "source_identifier": cve.get("sourceIdentifier", ""),
                "published": cve.get("published", ""),
                "last_modified": cve.get("lastModified", ""),
                "vuln_status": cve.get("vulnStatus", ""),
                "descriptions": [],
                "metrics": [],
                "weaknesses": [],
                "configurations": [],
                "references": []
            }
            
            # Transform descriptions
            descriptions = cve.get("descriptions", [])
            for desc in descriptions:
                transformed_entry["descriptions"].append({
                    "lang": desc.get("lang", "N/A"),
                    "description": desc.get("value", "No description available")
                })
            
            # Transform metrics
            metrics = cve.get("metrics", {}).get("cvssMetricV31", [])
            for metric in metrics:
                cvss_data = metric.get("cvssData", {})
                transformed_entry["metrics"].append({
                    "version": cvss_data.get("version", "N/A"),
                    "vector_string": cvss_data.get("vectorString", "N/A"),
                    "attack_vector": cvss_data.get("attackVector", "N/A"),
                    "attack_complexity": cvss_data.get("attackComplexity", "N/A"),
                    "privileges_required": cvss_data.get("privilegesRequired", "N/A"),
                    "user_interaction": cvss_data.get("userInteraction", "N/A"),
                    "scope": cvss_data.get("scope", "N/A"),
                    "confidentiality_impact": cvss_data.get("confidentialityImpact", "N/A"),
                    "integrity_impact": cvss_data.get("integrityImpact", "N/A"),
                    "availability_impact": cvss_data.get("availabilityImpact", "N/A"),
                    "base_score": cvss_data.get("baseScore", 0.0),
                    "base_severity": cvss_data.get("baseSeverity", "N/A"),
                    "exploitability_score": metric.get("exploitabilityScore", 0.0),
                    "impact_score": metric.get("impactScore", 0.0)
                })

            # Transform weaknesses
            weaknesses = cve.get("weaknesses", [])
            for weakness in weaknesses:
                descriptions = weakness.get("description", [])
                for desc in descriptions:
                    transformed_entry["weaknesses"].append({
                        "source": weakness.get("source", "N/A"),
                        "description": desc.get("value", "N/A")
                    })

            # Transform configurations
            configurations = cve.get("configurations", [])
            for config in configurations:
                operator = config.get("operator", "N/A")
                negate = config.get("negate", False)
                nodes = config.get("nodes", [])
                for node in nodes:
                    for cpe in node.get("cpeMatch", []):
                        criteria = cpe.get("criteria", "")
                        parts = criteria.split(":")
                        transformed_entry["configurations"].append({
                            "operator": operator,
                            "negate": negate,
                            "vulnerable": cpe.get("vulnerable", False),
                            "criteria": criteria,
                            "part": parts[2] if len(parts) > 2 else "N/A",
                            "vendor": parts[3] if len(parts) > 3 else "N/A",
                            "product": parts[4] if len(parts) > 4 else "N/A",
                            "version": parts[5] if len(parts) > 5 else "N/A",
                            "version_end_excluding": cpe.get("versionEndExcluding", "N/A")
                        })

            # Transform references
            references = cve.get("references", [])
            for ref in references:
                transformed_entry["references"].append({
                    "url": ref.get("url", "N/A"),
                    "source": ref.get("source", "N/A"),
                    "tags": ref.get("tags", [])
                })

            transformed_data.append(transformed_entry)
    
    logger.info("Transformation completed.")
    return transformed_data
