#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
from time import time
import matplotlib
import matplotlib.pyplot as plt
from uRF_SDSS import getFitsFiles
from uRF_SDSS import calcEbv
t_i = time()
#### Obtain the spectra from SDSS DR14

## The sample
dbPath= os.getcwd()+ '/db/'
gs = pd.read_csv(dbPath+'demo.test', header=0)

# Replacing z by z_noqso when possible

n0_rows = len(gs.index)
idx = (gs['z_noqso'] != 0)
n_z_noqso = len(gs.loc[idx,'z_noqso'].index)
#n_z_noqso = len(gs.loc[idx,'z_noqso'].shape[0])
print(f'There are {n0_rows} objects')
print(f'{n_z_noqso} redshifts were replaced by the z_noqso value')
print(f'{n0_rows - n_z_noqso} redshifts remained the same')

gs.loc[idx,'z'] = gs.loc[idx,'z_noqso'].values

# Remove galaxies with redshift z<=0.01

gs = gs[gs.z > 0.01]
n1_rows = len(gs.index)

print(f'{n0_rows - n1_rows} galaxies with z <= 0.01 removed')

gs.index = np.arange(n1_rows)

# Choose the top n_obs median SNR objects
# It is supposed to be already ordered, but it isn't
gs.sort_values(by=['snMedian'], ascending=False, inplace=True)
n_obs = 1000
gs = gs[:n_obs]

gs.index = np.arange(n_obs)

# Create links for the Download

url_head = 'http://skyserver.sdss.org/dr14/en/tools/explore/summary.aspx?plate='

gs['url'] = url_head + gs['plate'].map('{:04}'.format) + '&mjd='\
            + gs['mjd'].astype(str) \
            + '&fiber=' + gs['fiberid'].map('{:04}'.format)


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

# Downloading the data

getFitsFiles(gs,dbPath)

# Calculate E(B-V) values for each galaxy (parallelly)
gs['ebv'] = calcEbv(gs, dbPath)

## Obtaining spectra and feature engineering

t_f = time()
print(f'Time elapsed: {t_f-t_i:2}')
