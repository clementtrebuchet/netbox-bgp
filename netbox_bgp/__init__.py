from extras.plugins import PluginConfig
from .version import __version__


class BGPConfig(PluginConfig):
    name = "netbox_bgp"
    verbose_name = "BGP"
    description = "Subsystem for tracking bgp related objects"
    version = __version__
    author = "Nikolay Yuzefovich"
    author_email = "mgk.kolek@gmail.com"
    base_url = "bgp"
    required_settings = []
    min_version = "3.2.0"
    max_version = "3.3.99"
    default_settings = {"device_ext_page": "full_width", "vrf_ext_page": "full_width"}

    def ready(self):
        """Register the signal handlers"""
        super(BGPConfig, self).ready()


config = BGPConfig  # noqa
