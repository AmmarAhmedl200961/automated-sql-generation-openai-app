# AI-Powered SQL Query Generator

![GitHub last commit](https://img.shields.io/github/last-commit/AmmarAhmedl200961/automated-sql-generation-openai-app)
![GitHub issues](https://img.shields.io/github/issues/AmmarAhmedl200961/automated-sql-generation-openai-app)
![GitHub stars](https://img.shields.io/github/stars/AmmarAhmedl200961/automated-sql-generation-openai-app?style=social)
![GitHub forks](https://img.shields.io/github/forks/AmmarAhmedl200961/automated-sql-generation-openai-app?style=social)
![Python version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/github/license/AmmarAhmedl200961/automated-sql-generation-openai-app)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](URL_TO_YOUR_APP)


This Streamlit app processes CSV data, generates SQL queries using OpenAI's API, and provides optimized SQL queries. The schema for the app is static and hardcoded to use an "employees" table.

## Contents
---
- [AI-Powered SQL Query Generator](#ai-powered-sql-query-generator)
  - [Contents](#contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Note](#note)
  - [License](#license)

## Features
- Upload CSV data to create and populate a SQLite database.
- Generate SQL queries based on natural language questions.
- Optimize SQL queries for better performance.
- View query results directly in the app.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AmmarAhmedl200961/automated-sql-generation-openai-app.git
    ```
2. Navigate to the project directory:
    ```bash
    cd automated-sql-generation-openai-app
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the app:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Enter your OpenAI API key.
2. Upload your CSV data in the specified format.
3. Enter a natural language question to generate SQL.
4. View the generated and optimized SQL queries and their results.

## Note
The schema is static and hardcoded to use an "employees" table.

## License
This project is licensed under the MIT License.
