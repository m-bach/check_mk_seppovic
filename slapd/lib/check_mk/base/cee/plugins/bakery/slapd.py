#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register

def get_slapd_files(conf: Dict[str, Any]) -> FileGenerator:
    yield Plugin(base_os=OS.LINUX,
                 source=Path("slapd.pl"))

    content = ["%slapd_instances = ("]

    for instance, instconf in conf:
        content += ["  '%s' => {" % instance]
        for key, value in instconf.items():
            if key == 'syncrepl':
                content += ["    'syncrepl' => ["]
                for syncreplconf in value:
                    content += ["      {"]
                    for key, value in syncreplconf.items():
                        content += ["      '%s' => '%s'," % (key, value)]
                    content += ["      },"]
                content += ["    ],"]
            else:
                content += ["    '%s' => '%s'," % (key, value)]
        content += ["  },"]

    content += [");"]

    yield PluginConfig(base_os=OS.LINUX,
                       lines=content,
                       target=Path("slapd.cfg"),
                       include_header=True)

register.bakery_plugin(
    name="slapd",
    files_function=get_slapd_files,
)
