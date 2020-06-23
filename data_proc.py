#!/usr/bin/env python3
import os
from time import time

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from uRF_SDSS import getFitsFiles
from uRF_SDSS import calcEbv
from uRF_SDSS import fitsToSpecs
from uRF_SDSS import remove_cont

t_i = time()

#### Obtain the spectra from SDSS DR16

## The sample
dbPath= f'{os.getcwd()}/db/'
gs = pd.read_csv(f'{dbPath}gals_DR16.csv', header=0)

# Replacing z by z_noqso when possible

n0_rows = len(gs.index)
idx = (gs['z_noqso'] != 0)
n_z_noqso = len(gs.loc[idx,'z_noqso'].index)
#n_z_noqso = len(gs.loc[idx,'z_noqso'].shape[0])
print(f'There are {n0_rows} objects')
print(f'{n_z_noqso} redshifts were replaced by the z_noqso value')
print(f'{n0_rows - n_z_noqso} redshifts remained the same')

#gs.loc[idx,'z'] = gs.loc[idx,'z_noqso'].values
# This one is slighly faster
gs.loc[idx,'z'] = gs.z_noqso.loc[idx].values

# Remove galaxies with redshift z<=0.01

gs = gs[gs.z > 0.01]
n1_rows = len(gs.index)

print(f'{n0_rows - n1_rows} galaxies with z <= 0.01 removed')

gs.index = np.arange(n1_rows)

# Choose the top n_obs median SNR objects
gs.sort_values(by=['snMedian'], ascending=False, inplace=True)

n_obs = 10
gs = gs[:n_obs]

gs.index = np.arange(n_obs)

# Create links for the Download

url_head = 'http://skyserver.sdss.org/dr16/en/tools/explore/summary.aspx?plate='

# It cannot be done with a big f string
gs['url'] = url_head + gs['plate'].map('{:04}'.format) + '&mjd='\
            + gs['mjd'].astype(str) \
            + '&fiber=' + gs['fiberid'].map('{:04}'.format)
gs.to_csv(f'{dbPath}gs.csv')

# Plotting the z and SNR distribution

# fig, axarr = plt.subplots(1, 2)
#
# fig.set_figheight(7)
# fig.set_figwidth(14)
#
# ax1 = axarr[0]
# ax1.hist(gs.z, bins=int(len(gs)/50))
# ax1.set_xlabel('z')
# ax1.set_ylabel('Count')
# ax1.set_title('Redshift Histogram')
#
# ax2 = axarr[1]
# ax2.hist(gs.snMedian, bins=int(len(gs)/50))
# ax2.set_xlabel('median SNR')
# ax2.set_ylabel('Count')
# ax2.set_title('Median SNR Histogram')
#
# plt.show()
# plt.close

# Downloading the data...

getFitsFiles(gs,dbPath)

# Calculate E(B-V) values for each galaxy (parallelly)
gs['ebv'] = calcEbv(gs, dbPath)

## Obtaining spectra and feature engineering
gs, specs, grid, specobjids = fitsToSpecs(gs, dbPath)

## Removing the continuum
print(f'The shape of specs is {specs.shape}')
# Calculate the spectrum after its continuum was removed and the polynomial coefficients used for the fit
specs_no_cont, poly_coefs = remove_cont(specs, grid)
np.save(f'{dbPath}flx_{n_obs}',specs_no_cont)
# ## A random spectrum before and after removing the continuum
# ix = np.random.randint(0, len(gs))
#
# fig, axarr = plt.subplots(1, 2)
#
# fig.set_figheight(7)
# fig.set_figwidth(14)
#
# ax1 = axarr[0]
# ax1.plot(grid, specs[ix], label='Flux')
# ax1.plot(grid, np.poly1d(poly_coefs[ix])(grid), label='Fit')
# ax1.set_xlabel('Wavelength [$\AA$]')
# ax1.set_ylabel('Normalized Flux [ul]')
# ax1.set_title('Before')
# ax1.legend()
#
# ax2 = axarr[1]
# ax2.plot(grid, specs_no_cont[ix])
# ax2.set_xlabel('Wavelength [$\AA$]')
# ax2.set_ylabel('Normalized Flux [ul]')
# ax2.set_title('After')
#
# plt.show()

t_f = time()
print(f'Time elapsed: {t_f-t_i:.2}')
