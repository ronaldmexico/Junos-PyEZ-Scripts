#!/usr/bin/env python
# Author	: Brad Egan
# Purpose	: Log route information across a set of routers.
#			  Uses modified routes.yml and new mpls.yml definitions.
# Date 		: 2014-01-24

import datetime
import yaml

from jnpr.junos import Device
from jnpr.junos.op.routes import RtExactTable
from jnpr.junos.op.mpls import MplsIngressTable

# load the config file named config.yml
config = yaml.load(open('config.yml'))

def main():
    # iterate through the hosts specified in the config
    for host in config['hosts']:
        # use the getdevice function to connect to the router
        # and bind the views
        rt_tables, lsps = getdevice(host)

        # assign router array to variable
        router_list = config['hosts']

        # assign router's route array to variable
        router = router_list[host]
        routes_config = router['routes']

        # loop through each prefix in the config file
        for prefix in routes_config:
        # get routes for specific prefix
            rts = rt_tables.get(prefix)
        # check if keys exist in 'rts' dict
            if rts.keys():
            # loop through each table
                for table in rts:
                    # get route details using getnexthop() function
                        nh_ip, proto, nh_lsp, nh_age = getnexthop(table, prefix, rts)
                        if nh_lsp is not None:
                        # LSP exists, so get the LSP path
                            lsps.get(name=nh_lsp)
                            lsp_path = getpath(nh_lsp, lsps)
                            # write the details to a file named after the host
                            with open('/var/log/route-stats/%s' % host, 'a') as f:
                                timestamp = datetime.datetime.now()
                                f.write(str(timestamp)+' ')
                                f.write('Host=%s,Table=%s,Protocol=%s,Prefix=%s,LSP=%s,Path=%s,NextHopIP=%s,Age=%s\n' % (host, table.name, proto, prefix, nh_lsp, lsp_path, nh_ip, nh_age))
                        else:
                        # write the details to a file if the route is found
                            with open('/var/log/route-stats/%s' % host, 'a') as f:
                                timestamp = datetime.datetime.now()
                                f.write(str(timestamp)+' ')
                                f.write('Host=%s,Table=%s,Protocol=%s,Prefix=%s,NextHopIP=%s,Age=%s\n' % (host, table.name, proto, prefix, nh_ip, nh_age))
            else:
            # no keys in rts, so router doesn't have the prefix in it's table
                with open('/var/log/route-stats/%s' % host, 'a') as f:
                    timestamp = datetime.datetime.now()
                    f.write(str(timestamp)+' ')
                    f.write('Route for %s was not found on %s\n' % (prefix, host))

def getdevice(router):
    # load the Device object and then open the connection
    rtr = Device(host=router, user=config['user'], password=config['pass'])
    rtr.open()

    # Bind the table to the device and then load the information
    rt_tables = RtExactTable(rtr)
    lsps = MplsIngressTable(rtr)

    return rt_tables, lsps

def getnexthop(table, prefix, rts):
    # pull the routes for the specific prefix
    tbl = rts[table.name]
    tbl_rts = tbl['routes']
    dst = tbl_rts[prefix]
    ip = dst.to
    proto = dst.proto
    lsp = dst.lsp
    age = dst.age
    return ip, proto, lsp, age

def getpath(lsp, lsps):
    lsp_attr = lsps[lsp]
    path = lsp_attr.active_path
    return path

main()