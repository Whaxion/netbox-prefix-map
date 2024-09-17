# NetBox Prefix Map

![Screenshot](/netbox-prefix-map.png)

## Summary
A NetBox plugin that enable a new way to visualize available IPs inside a Prefix

## Install
The plugin is available as a Python package and can be installed with pip.

Run `pip install netbox-prefix-map` in your virtual env.

To ensure NetBox Prefix Map plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the NetBox root directory (alongside `requirements.txt`) and list the `netbox-prefix-map` package:

```no-highlight
# echo netbox-prefix-map >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your `configuration.py`

```python
# In your configuration.py
PLUGINS = ["netbox_prefix_map"]
```

First run `source /opt/netbox/venv/bin/activate` to enter the Python virtual environment.


Then run 
```bash
cd /opt/netbox/netbox
pip3 install netbox-prefix-map
python3 manage.py collectstatic --no-input
```

## Mentions
README inspired by [NetBox Topology Views Plugin](https://github.com/netbox-community/netbox-topology-views)