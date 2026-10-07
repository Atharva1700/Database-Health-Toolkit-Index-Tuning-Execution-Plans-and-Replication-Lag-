#!/usr/bin/env python3
"""Monitor replication lag between primary and replica."""
import psycopg2
import time
from datetime import datetime

class ReplicationMonitor:
    def __init__(self, primary_dsn: str, replica_dsn: str):
        self.primary = psycopg2.connect(primary_dsn)
        self.replica = psycopg2.connect(replica_dsn)
    
    def measure_lag(self) -> float:
        """Return replication lag in milliseconds."""
        with self.primary.cursor() as cur:
            cur.execute("SELECT now()::timestamp")
            primary_time = cur.fetchone()[0]
        
        with self.replica.cursor() as cur:
            cur.execute("SELECT now()::timestamp")
            replica_time = cur.fetchone()[0]
        
        lag_ms = (replica_time - primary_time).total_seconds() * 1000
        return max(lag_ms, 0)
    
    def monitor_continuous(self, interval_s: int = 5, duration_s: int = 300):
        """Monitor lag over time."""
        start = time.time()
        lags = []
        while time.time() - start < duration_s:
            lag = self.measure_lag()
            lags.append(lag)
            print(f"[{datetime.now().isoformat()}] Lag: {lag:.2f}ms")
            time.sleep(interval_s)
        
        return {
            "samples": len(lags),
            "max_lag_ms": max(lags),
            "avg_lag_ms": sum(lags) / len(lags)
        }
    
    def close(self):
        self.primary.close()
        self.replica.close()
