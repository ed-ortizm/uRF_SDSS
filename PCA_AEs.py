#!/usr/bin/env python3

import os
import sys
from time import time

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

from PCA_AEs_lib import plot_2D
from PCA_AEs_lib import plt_spec_pca


ti = time()

## Loading the data

fname = sys.argv[1]#'flx_5000.npy'
dir = f'{os.getcwd()}/db/'
exist = os.path.exists(f'{dir}{fname}')
if exist:
    flx = np.load(f'{dir}{fname}')
else:
    print(f'There is no {fname} in {dir} directory!')

## Performing PCA

pca = PCA(n_components=2) #0.99999951 (100)

tr_flx= pca.fit_transform(flx)

print(f'N° of componets: {pca.n_components_}, {tr_flx.shape}')

# ## Inverse transform
#
# inv_tr= pca.inverse_transform(tr_flx)
#
# ## Checking the percentages of explained variance
#
# tot_var = sum(pca.explained_variance_)
#
# expl_var = [(i/tot_var)*100 for i in sorted(pca.explained_variance_, reverse=True)]

# plot_2D(tr_flx, 'PCA')

# n = 10
# for i in range(n):
#     print(f'Component N° {i} explains {expl_var[i]:.3}% of the vatiance')
#
# print(f'These first {n} components explain {sum(expl_var[:n]):.6}% of the variance')

# ## Ploting a spetrum
#
# plt_spec_pca(flx[0],inv_tr[0],pca.n_components_)
#

## Creating the AE
# I do create it in two parts because later on I'll need to acces the latent
# space. Therefore it is necessary to add the input and output shape


encoder = keras.models.Sequential([keras.layers.Dense(2, input_shape=(flx.shape[1],))])
decoder = keras.models.Sequential([keras.layers.Dense(flx.shape[1])])
autoencoder = keras.models.Sequential([encoder, decoder])

autoencoder.compile(loss="mse", optimizer=keras.optimizers.Adam(lr=5e-1, decay=1e-2/20))

## Normalizing the flux: removing the mean value and normalizing by the standard
# deviation. This is done because pca.fit_transform does the same on the data.
# Therefore if we want to compare we need to have the same data.

sc = StandardScaler()
flx = sc.fit_transform(flx)

## Fitting

history = autoencoder.fit(flx, flx, epochs=50, batch_size=400)
latent = encoder.predict(flx)

print(latent.shape)

plot_2D(latent, 'AE')

tf = time()
print(f'Running time: {tf-ti:.2f}')
