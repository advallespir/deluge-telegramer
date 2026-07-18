#
# __init__.py
#
# Copyright (C) 2016-2019 Noam <noamgit@gmail.com>
# https://github.com/noam09
#
# Deluge is free software. GPLv3.
#

from deluge.plugins.init import PluginInitBase
import logging

log = logging.getLogger(__name__)


class CorePlugin(PluginInitBase):
    def __init__(self, plugin_name):
        try:
            from .core import Core as _plugin_cls
            self._plugin_cls = _plugin_cls
        except ImportError as e:
            log.error(
                "Telegramer: Failed to load plugin! %s. "
                "Make sure python-telegram-bot>=20.0 is installed and visible to Deluge. "
                "If using linuxserver/deluge, add PYTHONPATH=/lsiopy/lib/python3.12/site-packages "
                "and INSTALL_PIP_PACKAGES=python-telegram-bot>=20.0|setuptools<70 to your environment.",
                str(e)
            )
            raise
        super(CorePlugin, self).__init__(plugin_name)


class GtkUIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .gtkui import GtkUI as _plugin_cls
        self._plugin_cls = _plugin_cls
        super(GtkUIPlugin, self).__init__(plugin_name)


class WebUIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .webui import WebUI as _plugin_cls
        self._plugin_cls = _plugin_cls
        super(WebUIPlugin, self).__init__(plugin_name)


class Gtk3UIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .gtk3ui import Gtk3UI as GtkUIPluginClass
        self._plugin_cls = GtkUIPluginClass
        super(Gtk3UIPlugin, self).__init__(plugin_name)
