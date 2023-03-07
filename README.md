# **Interpol Red Notices Web Application**
## **Introduction**
This project aims to fetch and display data from the Interpol wanted list. The data is fetched periodically from Interpol and stored in a message queue system. Then, it is consumed by a web server, which saves it into a database and displays it in a web page along with a timestamp. The architecture of the application is designed to run in three Docker containers.

<p align="center">
  <img src="https://turkai.com/wp-content/uploads/2023/01/logo.turkai.white_.png" alt="TURK AI Image" width="400">
</p>

## **Project Structure**
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
    - pytest.ini
    - test
      - test_consumer.py
      - test_page.py
      - test_db.py
      - test_scraper.py

## **Prerequisites**
* Docker
* Docker Compose

## **Guideline of Running the Application**
1. Clone this repository to your local machine.
2. Create a .env file and set the necessary environment variables. You can use the .env file in the project root as a template.
3. Open a terminal and navigate to the project root directory.
4. Run docker-compose up --build to build and start the Docker containers.
5. Open your web browser and go to http://localhost:8000 to access the web page.


## **Architecture**
The application is composed of three Docker containers:

1. **'Container A'**: This container periodically fetches the data from the Interpol wanted list and puts it into the message queue system in Container C.

2. **'Container B'**: This container is a Python-based web server that listens to the message queue system in Container C. It saves the data in the required database and displays it on a simple HTML web page along with a timestamp. Whenever a new piece of data is consumed from the queue, the web page is updated. If an already saved record is updated, an alarm is displayed on the web page.

3. **'Container C'**: This container contains the message queue system RabbitMQ.

<p align="center">
  <img src="https://drive.google.com/uc?id=12GTakkG486hZrwW7_GD9yfp8-gDCw7dK" alt="TURK AI Image" width="600">
</p>

## **Environment Variables**
The application requires several environment variables to be set in order to function properly. These are the following:

* **'MONGODB_USERNAME'**: The username used to connect to the MongoDB instance.
* **'MONGODB_PASSWORD'**: The password used to connect to the MongoDB instance.
* **'MONGODB_CLUSTER'**: The cluster address of the MongoDB instance.
* **'MONGODB_DATABASE'**: The name of the database to use in the MongoDB instance.
* **'MONGODB_COLLECTION'**: The name of the collection to use in the MongoDB instance.
* **'INTERVAL'**: The interval (in seconds) at which the scraper should scrape for new data.
* **'RABBITMQ_HOST'**: The host address of the RabbitMQ instance.


Make sure to set these environment variables before starting the application. You can do this by creating a .env file in the root of the project and setting the values there. An example .env file has been provided for reference.

## **Documentation**
The following documentation is available in the app/ directory:

* **'requirements.txt'**: A list of Python dependencies required to run the application.
* **'docker-compose.yml'**: The Docker Compose configuration file for the application.
* **'consumer.py'**: The Python script that runs in Container A to fetch data from the Interpol API and put it into the message queue.
* **'scraper.py'**: The Python script that scrapes data from the Interpol API.
* **'db.py'**: The Python script that handles database interactions.
page.py: The Python script that creates the web page.
* **'test/'**: a folder that contains test files.
* **'TURK AI Python Developer Task Presentation.pptx'**: a PowerPoint presentation that explains the project requirements and implementation details.
* **'.gitignore'**: a file that specifies files and folders to be ignored by Git.
* **'pytest.ini'**: a file that contains configuration settings for pytest.
* **'page.py'**: a Python script that contains a Streamlit web application that displays messages from the MongoDB database.
* **'README.md'**: The file you are currently reading.

## **License**
This project is licensed under the [<u>MIT License</u>](https://opensource.org/license/mit/)