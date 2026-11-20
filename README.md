# MELCloudLib
Library to interact with Mitsubishi Electric MELCloud.

Currently supports only reading device parameters, see demo.py for example.
Works with both python2.7 and python3.

``python3 demo.py -u user@demo.com -p mypassword``

Add switch -d to enable debug mode. Then you will see all the parameters that API returns and know what can be queried from your device, or know how to modify the code to work in your environment.


## Sending data to InfluxDB

`melsender.py` reads data from MELCloud and writes it to an InfluxDB database. Run it e.g. periodically from cron:

``python3 melsender.py``

Add switch -d to enable debug mode.

Credentials and InfluxDB connection details are configured in `my_config.py`. Each setting is read from an environment variable (`MELCLOUD_USER`, `MELCLOUD_PWD`, `INFLUXDB_HOST`, `INFLUXDB_PORT`, `INFLUXDB_USER`, `INFLUXDB_PWD`, `INFLUXDB_DATABASE`); if a variable is not set, the example default value in the file is used.

Data is written with raw HTTP calls to the InfluxDB 1.x `/write` API using the `requests` package (`pip install requests`); the `influxdb` Python package is not needed.

**Note:** Only InfluxDB release 1.x is supported. InfluxDB 2.x and later are not supported.
