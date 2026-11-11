# freshcart-pipelines

Data Engineering Assignment: **From Git to Gold – Version Control, ELT, ML Pipelines and Event Streaming**

## System Architecture Overview
1. **Part A: Git and CI/CD**: Version control and continuous automated testing using pytest and GitHub Actions.
2. **Part B: FreshCart ELT on Snowflake**: Multi-hop architecture (Bronze raw API payloads, Silver cleansed and deduplicated, Ref/Dim SCD Type 2 dimensions, Gold business-ready facts) with data quality gates.
3. **Part C: Orchestrated ML Pipeline with Mage**: Machine learning workflow predicting Iris species with runtime variable gates and parallel evaluation branch.
4. **Part D: Event Streaming with RabbitMQ**: Topic-based dispatch system (`rapido-dispatch`) routing ride and food requests across zones with explicit manual acknowledgements (ACK/NACK).

## Repository Structure
- `elt/`: FreshCart Snowflake ELT pipeline scripts, SQL migrations, and notebook.
- `iris_project/`: Mage ML orchestration project blocks, metadata, and quality gate tests.
- `stream/`: RabbitMQ dispatcher and driver consumers.
- `tests/`: Automated pytest suites for CI verification.
- `.github/workflows/`: GitHub Actions automation workflow definitions.
