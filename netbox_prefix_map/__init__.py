from netbox.plugins import PluginConfig

class NetBoxPrefixMapConfig(PluginConfig):
    name = 'netbox_prefix_map'
    verbose_name = ' NetBox Prefix Map'
    description = 'View prefixes in a map in NetBox'
    version = '0.1.2'
    base_url = 'prefix-map'

config = NetBoxPrefixMapConfig