# sharkattacks API

This is a Flask API that interacts with a Redis database.

## Installation

Installation is simple. Copy over the folder and enter it. Once inside, start up the containers with kubernetes.

```bash
cd sharkattacks
make all-kube
```

## Usage

To use the Flask service, you need the IP address of the Flask service.
```bash
kubectl get services -o wide
```
Example output:
```
NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE   SELECTOR
shark-flask-service           ClusterIP   10.110.18.41     <none>        5000/TCP         60m   app=shark-flask
shark-service                 ClusterIP   10.99.4.21       <none>        6379/TCP         61m   app=shark-redis
```

You will also need a Python debug pod to access this IP address from inside the cluster. This pod contains an environment that can access the Flask API.
```bash
kubectl apply -f deployment-python-debug.yml
kubectl get pods -o wide
kubectl exec -it <name of python pod from previous output> -- /bin/bash
```

#### Note: you may need to change the REDIS_IP environment variable to the IP for ```shark-service```

To get all possible routes of the Flask app and what they do, hit the / route of the app for the front page.
```bash
curl 10.110.18.41:5000/
```

Before any of the routes can be used, you must first load the data from the ```sharkattacks.json``` data file provided.
```bash
curl 10.110.18.41:5000/loaddata
```

### Routes
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

### Examples
- ```curl 10.110.18.41:5000/records/attribval/Year/2015/```
- ```curl 10.110.18.41:5000/records/contains/surf/```
- ```curl 10.110.18.41:5000/records/id/2023/```
- ```curl 10.110.18.41:5000/records/delete/2023/```
- ```curl 10.110.18.41:5000/records/add/ -X POST -H "Content-Type: application/json" -d '@./example.json'``` 
- ```curl 10.110.18.41:5000/records/edit/2023/Species/tiger/```
- ```curl 10.110.18.41:5000/job/c1681e6f-7c74-42ff-8545-0f676f3e0407/```
- ```curl 10.110.18.41:5000/result/c1681e6f-7c74-42ff-8545-0f676f3e0407/```
- ```curl 10.110.18.41:5000/viz/Age/2017/2019/```
- ```curl 10.110.18.41:5000/download/c1681e6f-7c74-42ff-8545-0f676f3e0407/ > output.png``` 

#### Expected output
For most of these routes, the expected output must be found in ```/result/<job id>/```
- ```curl 10.110.18.41:5000/records/attribval/Year/2015/``` returns a list of dicts
- ```curl 10.110.18.41:5000/records/contains/surf/``` returns a list of dicts
- ```curl 10.110.18.41:5000/records/id/2023/``` returns a dict
- ```curl 10.110.18.41:5000/records/delete/2023/``` returns a list
- ```curl 10.110.18.41:5000/records/add/ -X POST -H "Content-Type: application/json" -d '@./example.json'``` returns a boolean
- ```curl 10.110.18.41:5000/records/edit/2023/Species/tiger/``` returns True
- ```curl 10.110.18.41:5000/job/c1681e6f-7c74-42ff-8545-0f676f3e0407/``` returns a dict
- ```curl 10.110.18.41:5000/result/c1681e6f-7c74-42ff-8545-0f676f3e0407/``` returns different things depending on what the job id is.
- ```curl 10.110.18.41:5000/viz/Age/2017/2019/``` returns a dict
- ```curl 10.110.18.41:5000/download/c1681e6f-7c74-42ff-8545-0f676f3e0407/ > output.png``` returns bytes

## License
[MIT](https://choosealicense.com/licenses/mit/)
