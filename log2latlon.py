# This script turns the nginx log file into latitude/longitude.
# Reference: http://www.cnblogs.com/step1/archive/2009/01/07/1371402.html

import re
import os
import urllib2
import subprocess as sp

filename = 'access.log.2'
f = file(filename, 'r')
f_out = file('tmp.txt', 'w')

# read the file and get total line number
print('Parsing log file {0}...'.format(filename))
wc = sp.check_output(['wc', filename])
m = re.search('^ (\\d+) ', wc)
total_count = m.groups()[0]
print '{0} lines in total'.format(total_count)

count = 0
error_count = 0
while f:
    # update status
    count = count + 1
    print '\rprocessed/error/total: {0}/{1}/{2}'.format(count, error_count, total_count),

    # extract IP
    l = f.readline()
    m = re.search('^(.*?) ', l)
    if not m:
        error_count = error_count + 1
        continue
    ip = m.groups()[0]

    # invoke online service to turn IP into geolocation
    url = 'http://dituren-service.appspot.com/services/ip_lookup?c=onIpLookupLoaded&ip={0}'.format(ip)
    result = urllib2.urlopen(url).read()

    # parse the returned result
    m = re.search('"lat": ([\\d\\.]*),', result)
    if not m:
        error_count = error_count + 1
        continue
    lat = m.groups()[0]
    m = re.search('"lon": ([\\d\\.]*),', result)
    if not m:
        error_count = error_count + 1
        continue
    lon = m.groups()[0]

    # write the result to output file
    f_out.write('{0}, {1}{2}'.format(lat, lon, os.linesep))

f_out.close()
f.close()
