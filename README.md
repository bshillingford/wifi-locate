## wifi-locate (Python)

Locates the current Wi-Fi-enabled Linux or OS X machine, using nearby Wi-Fi access points.

To use, call `linux_scan` or `osx_scan`, then give the result to `locate` which returns `(accuracy, (lat,lng))`.

Example:
```
result = locate(linux_scan("wlan0"))
print(result)
```

