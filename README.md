# uRF_SDSS
## Applying an Unsupervised Machine-Learning Algorithm to a Large Dataset of Galaxy Spectra

This repository summarizes the work of Guy Goren, with Prof. Dovi Poznanski as the advisor, from the School of Physics & Astronomy at Tel Aviv University, as part of the Physics department's honor program. Please find below the research's abstract.

The repository includes:
* The research's summary: A pdf document summarizing the main methods of work and conclusions.
* A Demo: A Jupyter Notebook providing the relevant python code. It enables anyone with a basic knowledge in Python the ability to apply the main methods of work presented in the research: obtain the dataset, perform feature engineering, apply the unsupervised Random Forest (RF) algorithm, and analyze the results. In order to use the demo, it is highly recommended to download the entire repository, as it already includes the relevant data.

## Abstract
As large astronomical datasets become greater and more accessible, we must ask ourselves how we utilize them to their fullest – understanding both macroscopic trends, as well as more specific interesting objects.  Machine-learning (ML) based algorithms prove themselves as highly efficient in understanding complicated correlations among large datasets with dozens of features that characterize every object. By learning these correlations, we can detect trends, learn about the similarity and dissimilarity between objects, and detect specific outliers – objects that lack common correlations or that are characterized by new and unique correlations.
We present an unsupervised variation of the Random Forest (RF) algorithm, which provides us with a similarity measure between every pair of observations in our data set. We implement it over 150,000 spectra measurements of galaxies obtained from Sloan Digital Sky Survey (SDSS). By analyzing the similarity measures, we discover outlying observations, galaxies that are governed by unusual physical phenomena, as well as visualize the data to reveal underlying structures. As true for many ML algorithms, most of the methods discussed are generic and are suitable for a variety of domains and types of data.
The purpose of this document is to summarize the methods of work used, their advantages and disadvantages, as well as the unusual physical phenomena discovered, all in the purpose for an efficient future research. A demo which includes the relevant Python code is available upon demand. 
