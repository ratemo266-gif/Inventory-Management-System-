# Retail Inventory Management System

A production-grade Python microservice framework that provides an administrative portal for an e-commerce platform. This system exposes a Flask-based REST API featuring complete JSON CRUD capabilities, an interactive Command Line Interface (CLI) application management console, integration with the live OpenFoodFacts API, and an isolated unit testing suite.

---

## Architecture Overview

The system is designed with a detached client-server model:
1. **Backend Server (`app.py`)**: Manages the local inventory store array, handles auto-increment IDs safely, exposes endpoints using proper HTTP methods (`GET`, `POST`, `PATCH`, `DELETE`), and proxies calls to the external OpenFoodFacts global product database.
2. **CLI Client Interface (`cli.py`)**: An administrative terminal portal that communicates over HTTP requests, giving managers the ability to handle manual changes or pull live web items directly into local database registries.
3. **Automated Test Harness (`test_app.py`)**: A structural validation suite using `unittest` and dependency mocking to test endpoints safely without polluting production servers.

---

##  Installation & System Setup

Ensure you have Python 3.x installed on your computer. Follow these commands to set up the environment:

### 1. Clone & Initialize the Project Directory
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Inventory-Management-System

python3 -m venv venv
source venv/bin/activate 

## Install Dependencies

pip install Flask requests

##Step 1: Start the Flask API Core Engine
##In your first terminal tab, kick off the API service server:
python app.py

##Step 2: Open the Administrative Management Portal
## In your second terminal tab, launch the console user dashboard client:
 python cli.py

 ## step 3:Execute the Validation Test Suite
 python test_app.py