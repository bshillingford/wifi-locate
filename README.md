## wifi-locate (Python)

Locates the Wi-Fi-enabled machine using nearby Wi-Fi access points' relative signal strengths. Uses Google's API.

To use, call `linux_scan` or `osx_scan`, then give the result to `locate` which returns `(accuracy, (lat,lng))`.

Pretty useful for `xflux` or fetching weather.

## Quick start:
Install:
```bash
pip install git+https://github.com/bshillingford/wifi-locate
```

Example:
```python
from wifilocate import locate, linux_scan
accuracy, latlng = locate(linux_scan(device="wlan0"))
print(accuracy, latlng)  # e.g. 25, (50.1234567, -1.234567)
```

## Details

Calls Google's API (most likely used in Firefox, based on the URL). The module supports Python 2 and 3, and only depends on [requests](http://docs.python-requests.org/en/master/). If you don't yet have requests, consider my dependency on it a favour. It's great.

In Linux this uses `iwlist`, and in OS X it uses a little-known but built-in utility called `airport`.
