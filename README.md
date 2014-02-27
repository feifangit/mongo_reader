Mongo Reader
======

MongoDB HTTP interface.
Inspired by [sleepy.mongoose](https://github.com/10gen-labs/sleepy.mongoose)

Based on [Flask](http://flask.pocoo.org/) and [pymongo](https://github.com/mongodb/mongo-python-driver)

Compare with `sleepy.mongoose`:
>
 - Follows interfaces in `sleepy.mongoose`

Add
>
 - Replica set support

Changed
>
 - Replace `pymongo.connection.Connection` with `pymongo.MongoClient` 
 - Use WSGI interface provided by `Flask` instead of customized `BaseHTTPServer.HTTPServer`

## Interfaces
Interface format: `/<database>/<collection>/<command>`

### Current Supporting Commands:

#### _status: 
return collection status read from MongoDB
>
**request parameters**

>
**sample response**
>>
`/_status`
<pre>
{
  "ok": 1, 
  "status": {
    "avgObjSize": 230.44444444444446, 
    "count": 504, 
    "indexSizes": {
      "_id_": 40880, 
      "serverTime_1_errorCode_1_company_1_site_1": 40880, 
      "timeCreated_1_errorCode_1_company_1_site_1": 40880
    }, 
    "lastExtentSize": 16990208, 
    "nindexes": 3, 
    "ns": "stage5.transaction_p1", 
    "numExtents": 7, 
    "ok": 1.0, 
    "paddingFactor": 1.0, 
    "size": 116144, 
    "storageSize": 33763328, 
    "systemFlags": 1, 
    "totalIndexSize": 122640, 
    "userFlags": 0
  }
}
</pre>

#### _count: 
return size of query result
>
**request parameters**
>>
 - criteria, JSON dict, e.g: `{'code':1}`
>
**sample response**
>>
`/count?criteria:{"errorcode":1}`
<pre>
{
  "count": 504, 
  "ok": 1
}
</pre>        
>>
 - `count`: total size of the result data set based on criteria
 - `ok`: 1 for successfully quried, 0 for error

#### _find: 
return query result
>
**request parameters**
>>
 - criteria, JSON dict, e.g: `{'code':1}`
 - fields, JSON list, e.g: `['field1', 'field2']`
 - limit, a number, e.g: `50`
 - skip, a number, e.g: `20`
>
**sample response**
>>
`/_find?criteria:{"errorcode":1}&limit=2`
<pre>
{
  "count": 504, 
  "ok": 1, 
  "results": [
    {
      "_id": "da1fe7d3-2335-49cc-bdfb-dc92d248e1ec", 
      "company": 7, 
      "errorcode":1,
      "model": "xperia B", 
      "timecreated": {
        "$date": 1386103405000
      }
    }, 
    {
      "_id": "1a607f85-4f1f-4b54-915f-428e52244f9b", 
      "company": "5", 
      "errorcode":1,
      "model": "xperia C", 
      "timecreated": {
        "$date": 1386100597000
      }
    }
  ], 
  "size": 2
}
</pre>
>>
 - `count`: total size of the result data set based on criteria
 - `ok`: 1 for successfully quried, 0 for error
 - `results`: list of documents
 - `size`: size of result data set based on criteria, limit


About date/time in criteria:

    .../mydb/mycol/_find?criteria={"serverTime":{"$gte":{"$date":1393459200000}}}




## Run Application
### Start from command line
Available command line parameters:
>
 - `-p, --port` application listen port, `5000` by default
 - `-i, --ip` application listen ip, `0.0.0.0` by default
 - `-d` debug flag, will pass to `app.run(debug=?)`, `False` by default
 - `--mongoip` IP of mongod, `127.0.0.1` by default
 - `--mongoport` port of mongod, `27017` by default 
 - `--mongors` replica set name of MongoDB, `None` by default. if `--mongors` is provided, application will use `MongoReplicaSetClient` instead of `MongoClient`

    python app.py -p 8080

will start application and listen on port 8080

### Run with Gunicorn
parameters `-p, --port, -i, --ip, -d` is **not** available for running with Gunicorn.
You can run

    gunicorn -k gevent "app:build_app('--mongoport=27018 --mongoip=10.1.1.47')" -b 0.0.0.0:80
to start the application listen on 0.0.0.0:80, run with gevent and connect to a MongoDB instance on 10.1.1.47:27018



