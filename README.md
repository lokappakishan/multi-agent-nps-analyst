# NPS Analyst in a Box

An AI-powered customer feedback analysis system designed to transform customer survey data into actionable business insights using Python, pandas, and specialised AI agents.

## Problem Statement

Businesses collect customer satisfaction ratings and written feedback, but turning this information into reliable insights and prioritised actions requires several analytical steps.

This project aims to automate parts of that workflow by combining deterministic numerical analysis with AI-assisted interpretation of customer feedback.

## Planned Capabilities

- Calculate Net Promoter Score (NPS) and track trends over time.
- Analyse NPS across products, customer segments, and channels.
- Identify recurring themes in written customer feedback.
- Identify potential churn warning signals.
- Analyse revenue associated with customer segments.
- Generate evidence-based recommendations and a structured business report.

## Architecture

The planned workflow is:

```text
Survey CSV
    ↓
Data Loading and Validation
    ↓
Deterministic Analysis with Python and pandas
    ↓
Specialised AI Agents
    ↓
Orchestration
    ↓
Business Insights and Recommendations
```

Python will handle numerical calculations, while AI agents will interpret analytical results and customer feedback. This separation is intended to improve reproducibility and reduce the risk of unsupported numerical claims.

## Technology Stack

- Python
- pandas
- uv for Python project and dependency management
- Git and GitHub
