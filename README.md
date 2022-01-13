# telegraf-python-draytek
Python script for use with telegraf to poll various stats from a DrayTek Modem via Telnet.
A big part of the script is borrowed from [linuxthings.co.uk](https://linuxthings.co.uk/blog/monitoring-a-draytek-router-with-collectd-and-grafana). I have adapted it so that it works directly with Telegraf.

## Installation
1. Copy the script `draytekstatus.py` to a directory of your choice (I use `/opt/telegraf`)
2. Make the script executable `chmod +x /opt/telegraf/draytekstatus.py`
3. Configure the script
```
[[inputs.exec]]
  commands = ["python3 /opt/telegraf/draytekstatus.py"]
  timeout = "15s"
  data_format = "influx"
```
4. Restart telegraf
