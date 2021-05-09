# sharkattacks API

This is a Flask API that interacts with a Redis database.

## Installation

Installation is simple. Copy over the folder and enter it. Once inside, start up the containers with docker-compose.

```bash
cd sharkattacks
docker-compose up --build
```

## Usage

To all possible routes of the Flask app and what they do, hit the / route of the app for the front page.
```bash
curl localhost:5033/
```

Before any of the routes can be used, you must first load the data from the ```sharkattacks.json``` data file provided.
```bash
curl localhost:5033/loaddata
```

### For the midterm, the routes of interest are
- ```/``` for information on what each route does
- ```/loaddata/``` is required before using the API or it will not work
- ```/records/info/``` gives more infomation about what is stored in the database
- ```/records/attribval/<attribute>/<value>/``` gets all records with an attribute with a certain value (for example, Country: AUSTRALIA)
- ```/records/contains/<word>/``` gets all records that have a specific work in any of their fields
- ```/records/id/<record id>/``` get a specific record. The id to specify is the value of the 'original order' field
- ```/records/delete/<record id>/``` deletes a specific record (id is original order)
- ```/records/add/``` a route to POST a new json-formatted shark attack record to the databse. see ```/records/info/``` on which fields to specify.
- ```/records/edit/<record id>/<attribute>/<value>/``` edits the record specified by record id to have an attribute of specified value
- ```/job/<job id>/``` returns information about a job given its id
- ```/result/<job id>/``` view the result of a job given id
- ```/viz/<attribute>/<startyear>/<endyear>/``` visualizes an attribute between and including the start and end years. attribute can be Age (only Age so far, can add more)
- ```/download/<file name>/``` download the file to the local user. meant to be used with ```/viz/...``` to download the plot produced.

## Stopping
Once finished with the app, the Docker containers must be stopped and then removed.
```bash
docker stop gctoutin-flask
docker stop gctoutin-redis
docker rm gctoutin-flask
docker rm gctoutin-redis
```
Their deletion can be confirmed with ```docker ps -a```

## License
[MIT](https://choosealicense.com/licenses/mit/)
