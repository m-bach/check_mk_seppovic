#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#################################################################
#---------------------------------------------------------------#
# Author: Markus Weber                                          #
# Contact: markus.weber@lfst.bayern.de                          #
# License: GPL                                                  #
# File: slapd_stats                                             #
# Version: 1.0                                                  #
# Revision: 30.10.2015                                          #
# Description: Monitor openldap via Monitoring DB.              #
#                                                               #
#################################################################


# Example Output:
# <<<slapd_stats_waiters:sep(44)>>>
# ldap-master02,Write,0
# ldap-master02,Read,2





# no default thresholds
# factory_settings["slapd_stats_waiters_defaults"] = {
#                                                         "Write": (0,0),
#                                                         "Read": (0,0),
# }

def inventory_slapd_stats_waiters(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_stats_waiters(item, params, info):
    perfdata = []
    output   = ''
    status = 0
    
    for line in info:
        instance, op, value = line
        value = saveint(value)
        warn, crit = params.get(op, (0, 0) )
        
        if instance == item:
            if crit != 0 and value >= crit:
                status = max(status, 2)
                output += "%s Waiters: %d (!!) warn/crit=%d/%d; " % (op, value, warn, crit)
            elif warn != 0 and value >= warn:
                status = max(status, 1)
                output += "%s Watiers: %d (!) warn/crit=%d/%d; " % (op, value, warn, crit)
            else:
                status = max(status, 0)
                output += "%s Waiters: %d; " % (op, value)
        
            perfdata.append(("slapd_waiters_%s" % op.lower(), value, warn, crit))
    
    if output == '':
        # In case of missing information we assume that the login into
        # LDAP has failed and we simply skip this check. It won't
        # switch to UNKNOWN, but will get stale.
        raise MKCounterWrapped("No LDAP Connection available.")
  
    return (status, output, perfdata)
    

# check_info["slapd_stats_waiters"] = {
#     'default_levels_variable': "slapd_stats_waiters_defaults",
#     'check_function':          check_slapd_stats_waiters,
#     'inventory_function':      inventory_slapd_stats_waiters,
#     'service_description':     'SLAPD %s Waiters',
#     'has_perfdata':            True,
#     'group':                   'slapd_stats_waiters',
# }
