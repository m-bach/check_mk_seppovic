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
# <<<slapd_stats_connections:sep(44)>>>
# ldap-slave1,Total,8555
# ldap-slave1,Current,16




# no default thresholds
# factory_settings["slapd_stats_connections_defaults"] = {
#                                                         "Current": (0, 0),
#                                                         "rate": (0.0, 0.0),
#                                                         "Total": (0, 0),
# }

def inventory_slapd_stats_connections(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_stats_connections(item, params, info):
    perfdata = []
    output   = ''
    status = 0
    this_time = time.time()

    map_metric = { 'Total': 'connections',
                   'Current': 'active' }
    
    for line in info:
        instance, op, value = line  
        warn, crit = params.get(op, (0, 0) )
        warn = savefloat(warn)
        crit = savefloat(crit)
        
        if instance == item:
            if op == "Total":
                value = saveint(value)
            
                countername = "slapd.stats.connections.%s" % op
                rate = get_rate(countername, this_time, value)
                r_warn, r_crit = params.get("connections_rate", (0.0, 0.0))
                
                perfdata.append(("connections_rate", rate, r_warn, r_crit))
                if r_crit != 0 and rate >= r_crit:
                    status = max(status, 2)
                    output += "Connectionrate: %.2f(!!) warn/crit=%.2f/%.2f; " % (rate, r_warn, r_crit)
                elif r_warn != 0 and rate >= r_warn:
                    status = max(status, 1)
                    output += "Connectionrate: %.2f(!) warn/crit=%.2f/%.2f; " % (rate, r_warn, r_crit)
                else:
                    status = max(status, 0)
                    output += "Connectionrate: %.2f; " % rate
               
            if op == "Current":
                value = saveint(value)
                
            if crit != 0 and value >= crit:
                status = max(status, 2)
                output += "%s Connections: %d (!!) warn/crit=%.2f/%.2f; " % (op, value, warn, crit)
            elif warn != 0 and value >= warn:
                status = max(status, 1)
                output += "%s Connections: %d (!) warn/crit=%.2f/%.2f; " % (op, value, warn, crit)
            else:
                status = max(status, 0)
                output += "%s Connections: %d; " % (op, value)
            
            perfdata.append((map_metric[op], value, warn, crit))
    
    if output == '':
        # In case of missing information we assume that the login into
        # LDAP has failed and we simply skip this check. It won't
        # switch to UNKNOWN, but will get stale.
        raise MKCounterWrapped("No LDAP Connection available.")
  
    return (status, output, perfdata)
    

# check_info["slapd_stats_connections"] = {
#     'default_levels_variable': "slapd_stats_connections_defaults",
#     'check_function':          check_slapd_stats_connections,
#     'inventory_function':      inventory_slapd_stats_connections,
#     'service_description':     'SLAPD %s Connections',
#     'has_perfdata':            True,
#     'group':                   'slapd_stats_connections',
# }
