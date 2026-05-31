# Automated HR Candidate Orchestration Pipeline

## 📌 Project Overview
This project is an automated Data Engineering pipeline built with Apache Airflow. It orchestrates the end-to-end extraction, screening, scheduling, and onboarding of job candidates. By replacing manual HR tracking with a scheduled Directed Acyclic Graph (DAG), this pipeline ensures data integrity, eliminates lost candidate records, and accelerates the hiring lifecycle.

**Core Workflow:**
1. **Extract:** Fetches raw candidate data via mock API endpoints.
2. **Transform & Screen:** Parses resumes and filters candidates based on strict HR criteria.
3. **Schedule:** Allocates interview slots and manages calendar metadata.
4. **Load (Onboard):** Generates payroll and compliance data (Aadhar, PAN) for successful hires.

## 🛠 Tech Stack
* **Orchestration:** Apache Airflow
* **Language:** Python 3.x
* **Data Manipulation:** Pandas
* **Environment:** ARM64 (Apple M1 Silicon)

---

## 🚀 Engineering Challenges & Solutions

Building this pipeline required significant debugging and architectural planning to ensure isolated tasks could communicate effectively. Here are the major technical hurdles overcome during development:

### 1. The "Cold Start" Database Problem
* **The Challenge:** Initializing the pipeline caused immediate `FileNotFoundError` and `EmptyDataError` crashes because downstream tasks attempted to read state from tables that did not yet exist.
* **The Solution:** Engineered empty CSV staging files initialized with strict, predefined headers. This simulated a SQL `CREATE TABLE` execution, establishing the necessary schema blueprint before the automated pipeline was triggered.

### 2. Schema Drifts & Downstream Crashes
* **The Challenge:** Independent tasks were failing with `KeyError` exceptions because upstream transformations were conditionally dropping columns if no data was present.
* **The Solution:** Architected a comprehensive upstream schema (the "God Payload"). By initializing all required downstream columns with null/blank values early in the DAG, I established a strict "data contract" that guaranteed pipeline stability regardless of the data payload size.

### 3. Dependency Bloat & ARM Architecture Conflicts
* **The Challenge:** The local environment experienced `ModuleNotFoundError` crashes due to heavy external libraries (like Numpy) failing to compile correctly on an M1 Mac architecture for simple null-value handling.
* **The Solution:** Refactored the data transformation scripts to remove unnecessary dependencies. Replaced `np.nan` with pure Python's built-in `None`, reducing the environment weight, eliminating compilation errors, and adhering to the "dependency minimization" principle.

### 4. Logic Debugging & Task Isolation
* **The Challenge:** Inherited scripts contained syntax errors, missing indentation blocks, and hardcoded typos (e.g., `interviewer_metadata` instead of `interview_metadata`).
* **The Solution:** Applied defensive debugging techniques and leveraged Airflow's "Fail Fast" methodology. Rewrote the onboarding logic to safely filter and append records dynamically using Pandas `loc` operations, ensuring idempotency on task retries.

---

## 🔮 Future Enhancements
Currently, this pipeline utilizes local file storage to mock database state and task handoffs. In a production enterprise environment, I plan to upgrade this architecture by:
1. **Cloud Storage Integration:** Migrating local staging files to **AWS S3** buckets.
2. **Database Migration:** Replacing CSV manipulation with direct SQL `UPSERT` commands via Airflow `PostgresHook` or `SnowflakeHook`.
3. **Metadata Passing:** Implementing Airflow **XComs** to securely pass state and file URIs between worker nodes instead of relying on local disk memory.
4.![Future Scaled Architecture Diagram](docs/future_architecture.png)

---

### Acknowledgments
*The foundational architecture and initial script templates for this project were provided by the Analytics Vidhya Data Engineering curriculum. The code in this repository represents my personal implementation, featuring custom debugging, schema design, and dependency optimization to ensure full pipeline execution in a local Airflow environment.*