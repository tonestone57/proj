class ForensicAgent:
    def analyze(self, network_trace):
        findings = {
            "compromised_services": [],
            "mapped_cves": [],
            "anomalies": []
        }
        if "exploit" in network_trace:
            findings["compromised_services"].append("web_service")
            findings["mapped_cves"].append("CVE-2025-XXXX")
        return findings
