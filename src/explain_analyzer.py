#!/usr/bin/env python3
"""Analyze EXPLAIN plans and flag missing indexes."""
import psycopg2
import json
from typing import List, Dict

class ExplainAnalyzer:
    def __init__(self, dsn: str):
        self.conn = psycopg2.connect(dsn)
    
    def analyze(self, query: str) -> Dict:
        """Analyze query execution plan."""
        with self.conn.cursor() as cur:
            cur.execute(f"EXPLAIN (FORMAT JSON) {query}")
            plan = json.loads(cur.fetchone()[0])
        
        issues = []
        if self._has_seq_scan(plan):
            issues.append({
                "type": "sequential_scan",
                "severity": "high",
                "suggestion": "consider adding index"
            })
        if self._has_sort(plan):
            issues.append({
                "type": "sort",
                "severity": "medium",
                "suggestion": "check sort key columns for index"
            })
        
        return {
            "query": query,
            "plan": plan,
            "issues": issues
        }
    
    def _has_seq_scan(self, plan: Dict) -> bool:
        if "Plan" in plan and plan["Plan"].get("Node Type") == "Seq Scan":
            return True
        return False
    
    def _has_sort(self, plan: Dict) -> bool:
        if "Plan" in plan and plan["Plan"].get("Node Type") == "Sort":
            return True
        return False
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    analyzer = ExplainAnalyzer("postgresql://postgres:postgres@localhost/postgres")
    result = analyzer.analyze("SELECT * FROM users WHERE id = 1")
    print(json.dumps(result, indent=2))
    analyzer.close()
