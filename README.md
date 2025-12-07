# Autonomous Data Analyst Agent (ADAA)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![AWS](https://img.shields.io/badge/cloud-AWS-orange)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple)

## 📖 Project Overview

**The Problem:** Business stakeholders often face significant latency (24-48 hours) when requesting ad-hoc data insights from data teams. This bottleneck slows down decision-making and forces analysts to spend 60% of their time on repetitive SQL queries.

**The Solution:** The **Autonomous Data Analyst Agent (ADAA)** is a secure, retrieval-augmented generation (RAG) system deployed on AWS. It allows non-technical users to ask natural language questions (e.g., *"What was our retention rate last week compared to Q3 targets?"*) and receive accurate, SQL-backed answers and visualizations in real-time.

**Key Differentiator:** Unlike basic text-to-SQL scripts, this system implements a **Self-Correction Loop**. If the agent generates invalid SQL, it analyzes the error message, corrects its own logic, and retries the query without human intervention.

---

## 🏗 Architecture & System Design

This project follows a serverless, event-driven architecture designed for high availability and low cost.

![Architecture Diagram](docs/architecture/system-diagram.png)
*(Note: Diagram placeholder - High-level flow: User -> API Gateway -> Lambda (LangGraph) -> Bedrock -> Redshift)*

### **Core Components**
* **Orchestration:** `LangGraph` (Python) manages the agent state and reasoning loops.
* **LLM Backend:** `AWS Bedrock` (Claude 3.5 Sonnet) ensures data privacy (no data leaves the VPC).
* **Data Warehouse:** `AWS Redshift` (Provisioned) as the source of truth.
* **Infrastructure:** `Terraform` manages all AWS resources (IaC).
* **Pipeline:** `Apache Airflow` orchestrates nightly metadata schema updates to keep the agent's context fresh.

---

## 🛠 Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Standard for GenAI & Data Engineering. |
| **Framework** | LangChain / LangGraph | Enables cyclic graph flows (Reason -> Act -> Observe) required for complex SQL debugging. |
| **Cloud Provider** | AWS (Lambda, API Gateway) | Serverless architecture scales to zero, minimizing costs for internal tools. |
| **LLM** | Claude 3.5 Sonnet (via Bedrock) | Selected for superior SQL generation benchmarks and strict enterprise data compliance. |
| **CI/CD** | GitHub Actions | Automated testing and linting (Ruff/Black) on every PR. |

---

## 🔒 Security & Governance (Trust & Safety)

As this tool interacts with enterprise data, security is a primary design constraint:

1.  **Read-Only Access:** The database credentials used by the agent are strictly `READ ONLY`.
2.  **PII Redaction:** A middleware layer detects and masks Personally Identifiable Information (PII) before it reaches the LLM.
3.  **Audit Logging:** Every question, generated SQL query, and data response is logged to CloudWatch for compliance auditing.

---

## 🚀 Getting Started

### Prerequisites
* AWS CLI configured with appropriate permissions.
* Python 3.11+ and `poetry` (or `pip`).
* Docker (for local testing).

### Local Development
To run the agent locally against a mock database:

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/autonomous-data-analyst.git](https://github.com/yourusername/autonomous-data-analyst.git)

# 2. Install dependencies using Makefile
make install

# 3. Run the test suite
make test

# 4. Start the local server
make run-local
