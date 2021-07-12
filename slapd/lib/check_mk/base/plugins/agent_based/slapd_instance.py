#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#################################################################
#---------------------------------------------------------------#
# Author: Markus Weber                                          #
# Contact: markus.weber@lfst.bayern.de                          #
# License: GPL                                                  #
# File: slapd_stats                                             #
# Version: 1.1                                                  #
# Revision: 08.03.2016                                          #
# Description: Monitor openldap via Monitoring DB.              #
#                                                               #
#################################################################


# Example Output:
# <<<slapd_instance:sep(124)>>>
# ldap-slave1|0.0000
# <<<slapd_instance:sep(124)>>>
# ldap-slave2|ERROR - could not bind as cn=Monitor : Invalid credentials at ./slapd.pl line 344
#  at ./slapd.pl line 344


# factory_settings["slapd_instance_defaults"] = {
#                                                'maxConnectionTime': (0.0, 0.0)
#                                                }

def inventory_slapd_instance(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_instance(item, params, info):
    status = 0
    output = ''
    
    for line in info:
        instance, value = line
        warn, crit = params.get('maxConnectionTime', (0.0, 0.0) )
        
        if instance == item:
            if value.startswith("ERROR"):
                return 2, value
            
            value = float(value)
            if crit != 0 and value >= crit:
                status = max(status, 2)
                output += "Connected in %.2f (!!) seconds warn/crit=%.2f/%.2f" % (value, warn, crit)
            elif warn != 0 and value >= warn:
                status = max(status, 1)
                output += "Connected in %.2f (!) seconds warn/crit=%.2f/%.2f" % (value, warn, crit)
            else:
                status = max(status, 0)
                output += "Connected in %.2f seconds" % value
                
            return (status, output, [("connection_time", value, warn, crit)])


# check_info["slapd_instance"] = {
#     'default_levels_variable': "slapd_instance_defaults",
#     'check_function':          check_slapd_instance,
#     'inventory_function':      inventory_slapd_instance,
#     'service_description':     'SLAPD %s',
#     'has_perfdata':            True,
#     'group':                   'slapd_instance',
# }
