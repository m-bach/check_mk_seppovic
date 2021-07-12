#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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


# factory_settings["slapd_syncrepl_defaults"] = {
#                                                'levels': (0.0, 0.0)
#                                                }

def inventory_slapd_syncrepl(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_syncrepl(item, params, info):
    status = 0
    output = ''
    perfdata = []
    warn, crit = params.get('levels', (0.0, 0.0) )
    
    
    for line in info:
        instance, master, value = line
        
        if instance == item:
            if value.startswith("ERROR"):
                return 2, value
            
            value = float(value)
            if crit != 0 and value >= crit:
                status = max(status, 2)
                output += "Directory not in sync with Provider %s: %.2f(!!) (warn/crit=%.2f/%.2f)" % (master, value, warn, crit)
            elif warn != 0 and value >= warn:
                status = max(status, 1)
                output += "Directory not in sync with Provider %s: %.2f(!) (warn/crit=%.2f/%.2f)" % (master, value, warn, crit)
            else:
                status = max(status, 0)
                output += ""
                
        if status == 0:
            output = "Directory in sync with all Providers"

    return (status, output, [("time_offset", value, warn, crit)])


# check_info["slapd_syncrepl"] = {
#     'default_levels_variable': "slapd_syncrepl_defaults",
#     'check_function':          check_slapd_syncrepl,
#     'inventory_function':      inventory_slapd_syncrepl,
#     'service_description':     'SLAPD %s syncrepl status',
#     'has_perfdata':            True,
#     'group':                   'slapd_syncrepl',
# }
