"""
Locates the current wifi-enabled computer using nearby access points and
a Google API used by Firefox.

To use, call `linux_scan` or `osx_scan`, then give the result to `locate`.

Example:
```
result = locate(linux_scan("wlan0"))
print(result)
```
"""


import re
import requests
import subprocess


def linux_scan(device='wlan0'):
    """
    Using the specified device (e.g. wlan0 or wlp3s0 or eth0), returns
    a list of wifi access point tuples.
    """
    proc = subprocess.Popen(['iwlist', device, 'scan'],
                            stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode('ascii')
    return [(tup[0], tup[2], tup[1]) for tup in re.findall(
            r'Cell \d+ - Address: ((?:[A-F0-9]{2}:){5}[A-F0-9]{2}).*?'
            r'Signal level=([-0-9]+) dBm.*?'
            r'ESSID:"([^"]+)"',
            output,
            re.DOTALL)]


def osx_scan():
    """
    Returns a list of wifi access point tuples.
    (TODO: untested, based on sample output to `airport -s` found online)
    """
    proc = subprocess.Popen([
        '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport',
        '-s'], stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode('ascii')
    return [(tup[1], tup[0], tup[2]) for tup in re.findall(
            r'\s*(.*?)\s+((?:[A-F0-9]{2}:){5}[A-F0-9]{2})\s+([-0-9]+)\s',
            output)]


def locate(scan_result):
    """
    Given `scan_result` from `linux_scan` or `osx_scan`, returns the nested
    tuple `accuracy, (lat,lng)`.
    """
    url = 'https://maps.googleapis.com/maps/api/browserlocation/json'
    qs = [('browser', 'firefox'), ('sensor', 'true')]
    qs.extend(('wifi', 'mac:{0}|ssid:{1}|ss:{2}'.format(*tup))
              for tup in scan_result)
    response = requests.get(url, params=qs)
    res = response.json()

    return res['accuracy'], \
        (res['location']['lat'], res['location']['lng'])
