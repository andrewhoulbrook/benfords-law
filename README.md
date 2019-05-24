# Benford's Law

A script to compare a given dataset to Benford's Law and its generalised form.

## Getting Started

This script is written largely as the product of my learning about and experimenting with Benford's Law, especially its application to fraud detection tasks.  

I'd strongly recommend checking out [Marcel Milcent's](https://github.com/milcent/benford_py/blob/master/Demo.ipynb) excellent Python package, which is a far more professional offering than my humble effort. Marcel's work is also now available as a PyPi Package!  

### Benford's Law

Benford's Law, also known as the Law of First Digits, is the finding that for certain types of datasets, the first digits (or numerals) of numbers contained within a series do not display a uniform distribution, but rather follow a distribution shown below:

<p align="center">
  <img src="/doc/benford_dist.png"/>
</p>

A more detailed overview of Benford's Law can be [found here](http://mathworld.wolfram.com/BenfordsLaw.html) and [here](http://www.nigrini.com/ForensicAnalytics.htm).

Benford's Law is known to apply across a diverse range of datasets, for example: census data, street addresses, stock prices, house prices, population data, death rates, lengths of rivers, areas of land masses and lottery numbers. 

In general, Benford's Law usually holds when a series of numerical data has some (or most) of the following characteristics:

* Data values have varying degrees of magnitude
* Data values formed through mathematical combination of numbers from several distributions 
* Data with no pre-determined minimum or maximum limits
* A relatively large number of records 
* Data doesn't contain identifier/index-type numbers (e.g. SSINs, account numbers, phone numbers etc...) 
* Data is right-skewed, mean is less than the median

Data that conforms to the above characteristics is common in accounting which has lead to Benford's Law being used as a heuristic tool to detect the potential of fraud. 

### Breaking the Law - Fraud Detection

Benford's Law can also be generalised beyond the first digit to consider probability distributions for the first two and first three digits, for example. Distribution of the last two digits has also been suggested for identifying artificially rounded or fabricated data and flag data that could warrant further investigation. 

[This report](https://www.acfe.com/uploadedFiles/Shared_Content/Products/Self-Study_CPE/Using%20Benford's%20Law_2018_final_extract.pdf) by the Association of Certified Fraud Examiner's (ACFE) provides much more background on the application of Benford's Law to fraud detection and generalising Benford's Law to include analysis of second and third digit distributions. 

The first digit distribution alone doesn't help narrow the data into a subset of potential fraudulent data. It also doesn't necessarily help generate specific leads for investigators (sample sizes for first digit tests often impractical to manage). Tests for conformity to Benford's Law are often described as indicating the *possibility* of the presence of fraud.

Worth nothing that if, for example, certain accounts data are expected to conform to Benford’s law but doesn't, it doesn’t necessarily mean the data is fraudulent. It could however offer reason for further investigation.  
  
### Prerequisites

The script is written in Python 2.7.

Requires the following Python modules installed too if you don't already have them:

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

### Installing

Required modules are available from PyPI and can easily be installed as follows:

```
pip install numpy
pip install pandas
pip install matplotlib
```

Note: these are not minor installs! Read more about [NumPy](http://www.numpy.org/) and [Pandas](https://pandas.pydata.org/). 

## Running the Script

Usage Example: 

```>>> python benford.py 1 data/fibonacci.csv```

The first parameter denotes the type of Benford test to be performed. Options are:

* '1' = First digit distribution test
* '2' = Second digit distribution test
* '3' = Third digit distribution test
* '12' = First two digits joint distribution test
* '123' = First three digits joint distribution test

The second parameter is the file path to the user's dataset.

The script's file handling is a bit rudimentary. It reads csv text file formatted as a one-column data file, with no header row.

## Other Usage Information

It is left to the user to control and normalise the dataset that the script will run on. For example, the user should control for negative numbers in the dataset prior to running the script. This will most likely be a common pre-processing task for accountancy data.  

## Test Data

I've included some test datasets in the ```/data``` repo, which include: 

* The first 500 Fibonacci numbers - [data source](http://home.hiwaay.net/~jalison/Fib500.html). An almost perfect fit for the Benford Distribution. 

First Digit Distribution                      | First Two Digits Joint Distribution
:--------------------------------------------:|:-----------------------------------------------:
![Fibonacci Distribution](/doc/fibonacci.png) | ![Fibonacci Distribution](/doc/fibonacci_12.png)

* World population by country in 2017 - [data source](https://data.worldbank.org/indicator/SP.POP.TOTL?end=2017&start=1960). A statistically significant fit for the Benford Distribution.

First Digit Distribution                      | First Two Digits Joint Distribution
:--------------------------------------------:|:-----------------------------------------------:
![World Population](/doc/world_pop_2017.png)  | ![World Population](/doc/world_pop_2017_12.png)

* Monthly returns (Dec 1990 - May 2005) from Fairfield Sentry Ltd (a former Bernie Madoff fund) - [data source](https://www.sec.gov/news/studies/2009/oig-509/exhibit-0293.pdf). Visible deviations from  expected Benford distributions, but notably *not* statistically significant under Chi-Squared test. [Read more here](https://seekingalpha.com/article/173294-madoffs-results-really-were-random) about whether Madoff may have evaded detection via Benford analysis. 

First Digit Distribution                             | First Two Digits Joint Distribution
:---------------------------------------------------:|:------------------------------------------------------:
![Fairfield Sentry Monthly Returns](/doc/madoff.png) | ![Fairfield Sentry Monthly Returns](/doc/madoff_12.png)

* China 2010 Census, urban area populations - [data source](https://en.wikipedia.org/wiki/Sixth_National_Population_Census_of_the_People%27s_Republic_of_China). The data is not a fit for the first digit Benford distribution under the Chi-Squared test but does fit other digit distributions. 

First Digit Distribution                             | First Two Digits Joint Distribution
:---------------------------------------------------:|:-------------------------------------------------------:
![Urban Populations in China](/doc/china_cities.png) | ![Urban Populations in China](/doc/china_cities_12.png)

Plenty more examples at the fantastic [testingbenford.com](http://testingbenfordslaw.com)

## To Do

* Implement last two digits test (detect artificial rounding)
* Add error handling
* Improve input file handling and reading data from multiple file formats
* Sampling issues with Chi-Squared can make it less than ideal. Implement alternative test statistics (e.g. Z tests, MAD, Komologrov-Smirnov etc...)

## Built With

* [Python](http://www.python.org)
* [NumPy](http://www.numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)

## Authors

* **Andrew Houlbrook** - *Initial work* - [andrewhoulbrook](https://github.com/andrewhoulbrook)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details