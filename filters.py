import os
import urllib2

import numpy as np
import pylab as pl
from matplotlib.patches import Arrow

REFSPEC_URL = 'ftp://ftp.stsci.edu/cdbs/current_calspec/1732526_nic_002.ascii'
URL = 'http://www.sdss.org/dr7/instruments/imager/filters/%s.dat'

def fetch_filter(filt):
    assert filt in 'ugriz'
    url = URL % filt
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    loc = os.path.join('downloads', '%s.dat' % filt)
    if not os.path.exists(loc):
        print "downloading from %s" % url
        F = urllib2.urlopen(url)
        open(loc, 'w').write(F.read())

    F = open(loc)
        
    data = np.loadtxt(F)
    return data

def fetch_vega_spectrum():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    refspec_file = os.path.join('downloads', REFSPEC_URL.split('/')[-1])

    if  not os.path.exists(refspec_file):
        print "downloading from %s" % REFSPEC_URL
        F = urllib2.urlopen(REFSPEC_URL)
        open(refspec_file, 'w').write(F.read())

    F = open(refspec_file)

    data = np.loadtxt(F)
    return data


Xref = fetch_vega_spectrum()
Xref[:, 1] /= 2.1 * Xref[:, 1].max()

#----------------------------------------------------------------------
# Plot filters in color with a single spectrum
pl.figure()
pl.plot(Xref[:, 0], Xref[:, 1], '-k', lw=2)

for f,c in zip('ugriz', 'bgrmk'):
    X = fetch_filter(f)
    pl.fill(X[:, 0], X[:, 1], ec=c, fc=c, alpha=0.4)

kwargs = dict(fontsize=20, ha='center', va='center', alpha=0.5)
pl.text(3500, 0.02, 'u', color='b', **kwargs)
pl.text(4600, 0.02, 'g', color='g', **kwargs)
pl.text(6100, 0.02, 'r', color='r', **kwargs)
pl.text(7500, 0.02, 'i', color='m', **kwargs)
pl.text(8800, 0.02, 'z', color='k', **kwargs)

pl.xlim(3000, 11000)

pl.title('SDSS Filters and Reference Spectrum')
pl.xlabel('Wavelength (Angstroms)')
pl.ylabel('normalized flux / filter transmission')


pl.show()
