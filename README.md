# sharkattacks
COE 332 Final project. REST API to get information about shark attacks as of February 11, 2021

## Purpose

This API allows the user to request data about shark attacks.

### Thru the flask API

The user can load the json data to the API

can get list of attributes in the data

can query the data to return all objects with a <attribute>

return date range

return age range

return location
etc

can request a map

choose type of plot and x and y and title

### workers

everything in the Flask API is connected to the Redis DB. the workers do the jobs that were submitted to the queue

### Redis db

All data points are stored in the Redis db

### makefile

makefile is useful in development

## docker and kubernetes

must be deployable on kubernetes
