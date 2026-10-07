# Database Health Toolkit

Self-directed database operations study: index tuning, execution plans, replication monitoring, backups, schema versioning.

**Stack:** PostgreSQL, Docker, Python, Liquibase

**Components:**
- EXPLAIN plan analyzer (flags missing indexes)
- Primary/replica replication lag monitoring
- Backup and tested restore procedures
- Schema migrations via versioned Liquibase

**Setup:** Local Docker environment with primary and replica PostgreSQL instances.
