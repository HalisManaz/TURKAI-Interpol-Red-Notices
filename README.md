# Interpol Wanted List Web App
## Introduction
This project aims to fetch and display data from the Interpol wanted list. The data is fetched periodically from Interpol and stored in a message queue system. Then, it is consumed by a web server, which saves it into a database and displays it in a web page along with a timestamp. The architecture of the application is designed to run in three Docker containers.
