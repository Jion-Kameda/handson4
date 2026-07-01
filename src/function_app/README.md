# Azure Functions App (Python v2)

## Overview
This directory is the deployment unit for Azure Functions.
It exposes two HTTP GET APIs:

- `/api/multiply?A=<number>&B=<number>`
- `/api/divide?A=<number>&B=<number>`

## Local Run
1. Install Python 3.11.
2. Install Azure Functions Core Tools v4.
3. Copy `local.settings.sample.json` to `local.settings.json`.
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Start Functions host:
   - `func start`

## Unit Tests
1. Install runtime and test dependencies:
   - `pip install -r requirements.txt -r requirements-dev.txt`
2. Run tests from the repository root:
   - `pytest tests -q`

This command is suitable for future GitHub Actions CI execution.

## Response Format
- Success: JSON with `operation`, `a`, `b`, `result`
- Error: JSON with `error`

## Notes for GitHub Actions Deployment
- Deploy the directory `src/function_app` as the function app package root.
- Ensure Python 3.11 is used in workflow runner/setup.
