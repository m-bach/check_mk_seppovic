#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# 2021 Heinlein Consulting GmbH
#      Robert Sander <r.sander@heinlein-support.de>

#################################################################
#---------------------------------------------------------------#
# Author: Markus Weber                                          #
# Contact: markus.weber@lfst.bayern.de                          #
# License: GPL                                                  #
# File: slapd_syncrepl                                          #
# Version: 1.1                                                  #
# Revision: 08.03.2016                                          #
# Description: Monitor openldap via Monitoring DB.              #
#                                                               #
#################################################################


# Example Output:
# <<<slapd_syncrepl:sep(44)>>>
# ldap-master02,ldap-master01,0.00
# ldap-master02,ldap-master03,0.00

from .agent_based_api.v1 import (
    check_levels,
    get_rate,
    get_value_store,
    register,
    render,
    Result,
    Metric,
    State,
    ServiceLabel,
    Service,
)
import time

def parse_slapd_syncrepl(string_table):
    section = {}
    for instance, master, value in string_table:
        if not instance in section:
            section[instance] = {}
        section[instance][master] = value
    return section

register.agent_section(
    name="slapd_syncrepl",
    parse_function=parse_slapd_syncrepl,
)

def discover_slapd_syncrepl(section):
    for instance in section:
        for master, value in section[instance].items():
            yield Service(item="%s %s" % (instance, master))

def check_slapd_syncrepl(item, params, section):
    instance, master = item.split(" ")
    if instance in section:
        if master in section[instance]:
            value = section[instance][master]
            if value.startswith("ERROR"):
                yield Result(state=State.CRIT,
                             summary=value)
            else:
                yield from check_levels(
                    float(value),
                    levels_upper=params.get("levels"),
                    label="Difference with Provider %s" % master,
                    metric_name="time_difference",
                    render_func=render.timespan,
                )

register.check_plugin(
    name="slapd_syncrepl",
    service_name="SLAPD %s syncrepl status",
    sections=["slapd_syncrepl"],
    discovery_function=discover_slapd_syncrepl,
    check_function=check_slapd_syncrepl,
    check_default_parameters={},
    check_ruleset_name="slapd_syncrepl",
)
