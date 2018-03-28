#!/usr/bin/python

import netsnmp
import sys
import argparse

oidvars = netsnmp.VarList(netsnmp.Varbind('ifIndex',), netsnmp.Varbind('ifDescr',), netsnmp.Varbind('ifOperStatus',), netsnmp.Varbind('ifAdminStatus',), )

def parseargs():
    parser = argparse.ArgumentParser(description='Checks interfaces status. If ifAdminStatus is set to up and ifOperStatus is not "1" (not up) we assume critical, also able to filter out interfaces that should not be checked.')
    parser.add_argument('-H' '--host', dest='host', help='host or ip to query', required=True)
    parser.add_argument('-C' '--community', dest='community', default='public', help='host or ip to query')
    parser.add_argument('-f' '--filter', dest='filter', help='index filter <idx,idx,idx> a comma separated list of indexes to ignore')
    parser.add_argument('-F' '--filtercreate', dest='createfilter', action='store_true', help='assume all interfaces in down at this moment should be down and create a filter to filter out all of them for use with the -f on subequent checks')
    args = parser.parse_args()
    return args

def process_result(result, args):
    exitstat = 0
    exitmsg = ''
    filterstring = ''
    if args.filter:
        idxfilter = args.filter.split(',')
    for iface in result:
        if args.createfilter:
            if iface[2] != '1':
                filterstring += iface[0] + ','
        if args.filter:
            if iface[0] in idxfilter:
                continue
        if iface[3] == '1': # Admin status is up
            if iface[2] == '1':
                exitmsg += 'interface %s: UP\n' % iface[1]
            if iface[2] != '1':
                exitmsg += 'interface %s: DOWN!\n' % iface[1]
                exitstat = 2
    if args.createfilter:
        print 'Use the filter string with arg -f ' + '"' + filterstring.rstrip(',') + '"'
        sys.exit(0)
    print exitmsg
    sys.exit(exitstat)

def get_data(args):
    ifaces = []
    session = netsnmp.client.Session(Community=args.community, Version=2, DestHost=args.host)
    #result = session.getbulk(0, 1000, oidvars)
    result = session.walk(oidvars)
    for i in range(0, len(result), 4):
        ifaces.append((result[i], result[i+1], result[i+2], result[i+3] ))
    if not ifaces:
        print '\nError getting data from %s' % (args.host)
        sys.exit(2)
    return ifaces

def main():
    args = parseargs()
    data = get_data(args)
    process_result(data,args)
    print "unknown error"
    sys.exit(2)

if __name__ in '__main__':
    main()
