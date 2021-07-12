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
# <<<slapd_stats_operations:sep(44)>>>
# ldap-instance1,Delete,0,0
# ldap-instance1,Bind,82095,82095
# ldap-instance1,Add,0,0
# ldap-instance1,Abandon,0,0
# ldap-instance1,Extended,14978,14978
# ldap-instance1,Search,74380,74379
# ldap-instance1,Modify,0,0
# ldap-instance1,Unbind,16423,16423
# ldap-instance1,Modrdn,0,0
# ldap-instance1,Compare,0,0



# no default thresholds
# factory_settings["slapd_stats_operations_defaults"] = {
#                                                        'deviance': (0, 0),
#                                                        'Delete': (0, 0),
#                                                        'Bind': (0, 0),
#                                                        'Add': (0, 0),
#                                                        'Abandon': (0, 0),
#                                                        'Extended': (0, 0),
#                                                        'Search': (0, 0),
#                                                        'Modify': (0, 0),
#                                                        'Unbind': (0, 0),
#                                                        'Modrdn': (0, 0),
#                                                        'Compare': (0, 0),
#                                                        }

def inventory_slapd_stats_operations(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_stats_operations(item, params, info):
    perfdata = []
    output   = ''
    status = 0
    this_time = time.time()
    deviance = 0
    
    for line in info:
        instance, op, initiated, completed = line
        deviance = max(deviance, abs(saveint(initiated) - saveint(completed)))
        warn, crit = params.get(op, (0, 0) )
        
        if instance == item:
            countername = "slapd.stats.operations.%s" % op
            rate = get_rate(countername, this_time, saveint(completed))
            
            if crit != 0 and rate >= crit:
                status = max(status, 2)
                output += "%s rate %.2f (!!); " % (op, rate)
            elif warn != 0 and rate >= warn:
                status = max(status, 1)
                output += "%s rate %.2f (!!)" % (op, rate)
            else:
                status = max(status, 0)
                
            perfdata.append(("slapd_%s" % line[1].lower(), rate, warn, crit))
        
    # deviance check    
    warn_dev, crit_dev = params.get('deviance', (0, 0) )
    if crit_dev != 0 and deviance >= crit_dev:
        status = max(status, 2)
        output += "deviance of initiated and completed operations is %d(!!) for at least one operation type (warn/crit=%d/%d)" % (deviance, warn_dev, crit_dev)
    elif warn_dev != 0 and deviance >= warn_dev:
        status = max(status, 1)
        output += "deviance of initiated and completed operations is %d(!) for at least one operation type (warn/crit=%d/%d)" % (deviance, warn_dev, crit_dev)
    else:
        status = max(status, 0)
        
    return (status, output, perfdata)
 


# check_info["slapd_stats_operations"] = {
#     'default_levels_variable': "slapd_stats_operations_defaults",
#     'check_function':          check_slapd_stats_operations,
#     'inventory_function':      inventory_slapd_stats_operations,
#     'service_description':     'SLAPD %s Operations',
#     'has_perfdata':            True,
#     'group':                   'slapd_stats_operations',
# }
