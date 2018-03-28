```
usage: check_iface_adm_oper.py [-h] -H--host HOST [-C--community COMMUNITY]
                               [-f--filter FILTER] [-F--filtercreate]

Checks interfaces status. If ifAdminStatus is set to up and ifOperStatus is
not "1" (not up) we assume critical, also able to filter out interfaces that
should not be checked.

optional arguments:
  -h, --help            show this help message and exit
  -H--host HOST         host or ip to query
  -C--community COMMUNITY
                        host or ip to query
  -f--filter FILTER     index filter <idx,idx,idx> a comma separated list of
                        indexes to ignore
  -F--filtercreate      assume all interfaces in down at this moment should be
                        down and create a filter to filter out all of them for
                        use with the -f on subequent checks

```
