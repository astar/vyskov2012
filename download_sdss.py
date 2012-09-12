"""
This file fetches photometric observations associated with SDSS stars galaxies and qsos

"""

import os
import urllib, urllib2
import numpy as np

# Here's how the data can be downloaded directly from the SDSS server.
def fetch_data_sql(N = 100):
    URL = 'http://cas.sdss.org/public/en/tools/search/x_sql.asp'
    archive_file = 'sdss_colors.csv'

    DTYPE = [('mags', '5float32'),
             ('specClass', 'int8'),
             ('z', 'float32'),
             ('zerr', 'float32')]

    def sql_query(sql_str, url=URL, format='csv'):
        """Execute SQL query"""
        # remove comments from string
        sql_str = ' \n'.join(map(lambda x: x.split('--')[0],
                                 sql_str.split('\n')))
        params = urllib.urlencode(dict(cmd=sql_str, format=format))
        return urllib.urlopen(url + '?%s' % params)

    query_text = ('\n'.join(
            ("SELECT TOP %i" % N,
             " u-g,g-r,r-i,s.specClass",
             " FROM PhotoPrimary p join SpecPhotoAll s on p.objid=s.objid",
             " WHERE s.specClass in (1) AND u between 18 and 19",
             " UNION ALL",
             "SELECT TOP %i" % N,
             " u-g,g-r,r-i,s.specClass",
             " FROM PhotoPrimary p join SpecPhotoAll s on p.objid=s.objid",
             " WHERE s.specClass in (2) AND u between 18 and 19",
             " UNION ALL",
             "SELECT TOP %i" % N,
             " u-g,g-r,r-i,s.specClass",
             " FROM PhotoPrimary p join SpecPhotoAll s on p.objid=s.objid",
             " WHERE s.specClass in (3) AND u between 18 and 19"

         )))


#    if not os.path.exists(archive_file):
    print "querying for %i objects" % N
    print query_text
    output = sql_query(query_text)
    print "\n finished."
    try:
        data = np.loadtxt(output, delimiter=',', skiprows=1)
    except:
        raise ValueError(output.read())

    return data
    
        #np.save(archive_file, data)
#    else:
#        print "data already on disk"


