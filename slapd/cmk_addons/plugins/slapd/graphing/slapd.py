#!/usr/bin/env python3

#
# (c) 2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
)

metric_info["slapd_abandon"] = {
    "title": _("Abandon Ops completed"),
    "unit": "1/s",
    "color": "12/a",
}

metric_info["slapd_add"] = {
    "title": _("Add Ops completed"),
    "unit": "1/s",
    "color": "14/a",
}

metric_info["slapd_bind"] = {
    "title": _("Bind Ops completed"),
    "unit": "1/s",
    "color": "16/a",
}

metric_info["slapd_compare"] = {
    "title": _("Compare Ops completed"),
    "unit": "1/s",
    "color": "22/a",
}

metric_info["slapd_delete"] = {
    "title": _("Delete Ops completed"),
    "unit": "1/s",
    "color": "24/a",
}

metric_info["slapd_extended"] = {
    "title": _("Extended Ops completed"),
    "unit": "1/s",
    "color": "26/a",
}

metric_info["slapd_modify"] = {
    "title": _("Modify Ops completed"),
    "unit": "1/s",
    "color": "32/a",
}

metric_info["slapd_modrdn"] = {
    "title": _("ModRDN Ops completed"),
    "unit": "1/s",
    "color": "34/a",
}

metric_info["slapd_search"] = {
    "title": _("Search Ops completed"),
    "unit": "1/s",
    "color": "36/a",
}

metric_info["slapd_unbind"] = {
    "title": _("Unbind Ops completed"),
    "unit": "1/s",
    "color": "42/a",
}

metric_info["slapd_entries_sent"] = {
    "title": _("Entries sent"),
    "unit": "1/s",
    "color": "23/a",
}

metric_info["slapd_pdu_sent"] = {
    "title": _("PDUs sent"),
    "unit": "1/s",
    "color": "33/a",
}

metric_info["slapd_referrals_sent"] = {
    "title": _("Referrals sent"),
    "unit": "1/s",
    "color": "43/a",
}

metric_info["slapd_waiters_read"] = {
    "title": _("Read Waiters"),
    "unit": "count",
    "color": "25/a",
}

metric_info["slapd_waiters_write"] = {
    "title": _("Write Waiters"),
    "unit": "count",
    "color": "35/a",
}
