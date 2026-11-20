# coding=utf-8
import os

# Values are read from environment variables; the defaults below are
# example values used when the variable is not set.

# Username for MELcloud
MELCLOUD_USER = os.environ.get("MELCLOUD_USER", "xx@yy.com")

# Password for MELcloud
MELCLOUD_PWD = os.environ.get("MELCLOUD_PWD", "secret")

# Connection details of InfluxDB database
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxhost.xxx.com")
INFLUXDB_PORT = int(os.environ.get("INFLUXDB_PORT", 8086))
INFLUXDB_USER = os.environ.get("INFLUXDB_USER", "raspi")
INFLUXDB_PWD = os.environ.get("INFLUXDB_PWD", "secret")
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE", "raspidata")
