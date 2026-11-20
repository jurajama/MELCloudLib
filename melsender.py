# coding=utf-8
from optparse import OptionParser
from melcloudlib import mcloud
import pprint

import time
import requests

import my_config as conf

# This application pulls data from MELcloud and sends to InfluxDB database
# Configure credentials and InfluxDB host information in my_config.py


def _escape(value):
    """Escape characters special in line protocol measurement names, tag keys/values and field keys."""
    return str(value).replace('\\', '\\\\').replace(',', '\\,').replace('=', '\\=').replace(' ', '\\ ')


def _field_value(value):
    """Format a field value for InfluxDB line protocol."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return '%di' % value
    if isinstance(value, float):
        return repr(value)
    return '"%s"' % str(value).replace('\\', '\\\\').replace('"', '\\"')


def make_line(measurement, tags, fields, timestamp_ns):
    """Build one InfluxDB line protocol line."""
    tag_str = ''.join(',%s=%s' % (_escape(k), _escape(v)) for k, v in sorted(tags.items()))
    field_str = ','.join('%s=%s' % (_escape(k), _field_value(v)) for k, v in fields.items())
    return '%s%s %s %d' % (_escape(measurement), tag_str, field_str, timestamp_ns)


def write_lines(lines, host, port, user, password, database, timeout=5):
    """Write line protocol lines to an InfluxDB 1.x database using the HTTP /write API."""
    response = requests.post(
        'http://%s:%s/write' % (host, port),
        params={'db': database, 'precision': 'ns'},
        auth=(user, password) if user else None,
        data='\n'.join(lines).encode('utf-8'),
        timeout=timeout)
    response.raise_for_status()  # InfluxDB answers 204 No Content on success


if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    mc = mcloud(debug=options.debug)
    mc.login(conf.MELCLOUD_USER, conf.MELCLOUD_PWD)

    # In addition to the listed parameters, melcloudlib always returns DeviceName
    paramNames = ['FanSpeed','RoomTemperature','SetTemperature','ActualFanSpeed','CurrentEnergyConsumed']
    allDevices = mc.getAllDevices(paramNames)

    timestamp_ns = int(time.time() * 1e9)

    lines = []
    for device in allDevices:
        lines.append(make_line(
            "mcloud",
            {"DeviceName": device['DeviceName']},
            {name: device[name] for name in paramNames},
            timestamp_ns))

    if lines:
        write_lines(lines, conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER,
                    conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE)
