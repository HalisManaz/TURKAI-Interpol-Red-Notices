# Interpol Wanted List Web App
## Introduction
This project aims to fetch and display data from the Interpol wanted list. The data is fetched periodically from Interpol and stored in a message queue system. Then, it is consumed by a web server, which saves it into a database and displays it in a web page along with a timestamp. The architecture of the application is designed to run in three Docker containers.

## Project Structure
- app/
    - consumer.py
    - db.py
    - docker-compose.yml
    - page.py
    - requirements.txt
    - scraper.py
    - .env
    - .gitignore
    - README.md

## Prerequisites
* Docker
* Docker Compose

## Guideli of Running the Application
1. Clone this repository to your local machine.
2. Create a .env file and set the necessary environment variables. You can use the .env file in the project root as a template.
3. Open a terminal and navigate to the project root directory.
4. Run docker-compose up --build to build and start the Docker containers.
5. Open your web browser and go to http://localhost:8000 to access the web page.
