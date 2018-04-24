#!/usr/bin/env python

"""
A specter extraction benchmark wrapper
"""

import sys, os
import time
import multiprocessing
import numpy as np
from astropy.io import fits
from specter.psf import load_psf
from specter.extract import ex2d

import argparse

parser = argparse.ArgumentParser(usage = "{prog} [options]")
# parser.add_argument("-i", "--input", type=str,  help="input data")
parser.add_argument("-n", "--nproc", type=int,  help="number of parallel processes to use")
opts = parser.parse_args()

if opts.nproc is None:
    opts.nproc = multiprocessing.cpu_count() // 2
    print('Using nproc={}'.format(opts.nproc))

#- Load input data
t0 = time.time()
print('{} Reading input data'.format(time.asctime()))
psf = load_psf('psfmodel.fits')
image = fits.getdata('image.fits', 'IMAGE')
image_ivar = fits.getdata('image.fits', 'IVAR')

#- Split data into sub-regions to extract
t1 = time.time()
print('{} Splitting data into subregions'.format(time.asctime()))
wavelengths = np.arange(psf.wmin_all, psf.wmax_all)
nspec = 25
nwave = 200
args = list()
for specmin in range(0, 500, nspec):
    for i in range(0, len(wavelengths), nwave):
        ww = wavelengths[i:i+nwave]
        xyrange = psf.xyrange((specmin, specmin+nspec), ww)
        xmin, xmax, ymin, ymax = xyrange
        args.append( [specmin, nspec, ww, xyrange,] )

def wrap_ex2d(args):
    specmin, nspec, ww, xyrange = args
    xmin, xmax, ymin, ymax = xyrange
    return ex2d(image[ymin:ymax, xmin:xmax], image_ivar[ymin:ymax, xmin:xmax],
        psf, specmin, nspec, ww, xyrange)

t2 = time.time()
print('{} Extracting spectra in {} subregions'.format(time.asctime(), len(args)))
if opts.nproc < 1:
    print('Not using multiprocessing parallelism')
    for i, a in enumerate(args):
        results = wrap_ex2d(a)
else:
    p = multiprocessing.Pool(opts.nproc)
    results = p.map(wrap_ex2d, args)

print('{} Done'.format(time.asctime()))

t3 = time.time()
print('I/O time: {:.1f} sec'.format(t1-t0))
print('Prep time: {:.1f} sec'.format(t2-t1))
print('Extraction time: {:.1f} sec'.format(t3-t2))
print('Total time: {:.1f} sec'.format(t3-t0))



