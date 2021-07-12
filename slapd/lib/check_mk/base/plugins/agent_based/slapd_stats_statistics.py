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
# <<<slapd_stats_statistics:sep(44)>>>
# ldap-slave1,Entries,111386
# ldap-slave1,Referrals,0
# ldap-slave1,PDU,213505
# ldap-slave1,Bytes,17979195


# no default thresholds
# factory_settings["slapd_stats_statistics_defaults"] = {
#                                                         "Entries": (0,0),
#                                                         "Referarals": (0,0),
#                                                         "PDU": (0,0),
#                                                         "Bytes": (0,0),
# }

def inventory_slapd_stats_statistics(info):
    inv = []
    for line in info:
        if (line[0], {}) not in inv:
            inv.append((line[0], {}))
    return inv
 

def check_slapd_stats_statistics(item, params, info):
    perfdata = []
    output   = ''
    status = 0
    this_time = time.time()

    map_metric = { 'Entries': 'slapd_entries_sent',
                   'Referrals': 'slapd_referrals_sent',
                   'PDU': 'slapd_pdu_sent',
                   'Bytes': 'net_data_sent' }
    
    for line in info:
        instance, op, value = line  
        warn, crit = params.get(op, (0, 0) )
        
        if instance == item:
            countername = "slapd.stats.statistics.%s" % op
            rate = get_rate(countername, this_time, saveint(value))                 

            if crit != 0 and rate >= crit:
                status = max(status, 2)
                output += "Rate of sent %s: %d (!!) warn/crit=%d/%d; " % (op, rate, warn, crit)
            elif warn != 0 and rate >= warn:
                status = max(status, 1)
                output += "Rate of sent %s: %d (!) warn/crit=%d/%d; " % (op, rate, warn, crit)
            else:
                status = max(status, 0)
            
            
            perfdata.append((map_metric[op], rate, warn, crit))
        
    return (status, output, perfdata)
 


# check_info["slapd_stats_statistics"] = {
#     'default_levels_variable': "slapd_stats_statistics_defaults",
#     'check_function':          check_slapd_stats_statistics,
#     'inventory_function':      inventory_slapd_stats_statistics,
#     'service_description':     'SLAPD %s statistics',
#     'has_perfdata':            True,
#     'group':                   'slapd_stats_statistics',
# }
