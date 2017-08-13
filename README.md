# collectd-python-receiver

This repository has a simple collectd (https://github.com/collectd) metrics receiver. The code is derived from (a small subset of) python-bucky [https://github.com/trbs/bucky].

run the receiver_bucky file to print the metrics values. The print will be in the following format:
{'Hostname', 'Metric-Name', 'Metric-Value', 'TimeStamp'}

Modify the configuration - in cfg.py - depending on your environment. 
