#!/usr/bin/python
# -*- encoding: utf-8 -*-
# A script applying Benford's Law to the investigation of datasets for potential of fraud.
# Usage: e.g. >>> 'python benford.py 1 mydata.csv'
#                 '1', '2', '3' can be passed to perform a fit to the first, second and third digit Benford distributions
#                 '12' or '123' can be passed to perform a fit to the first two or first three digits Benford joint distributions 
# Note: reads UTF-8 encoded csv file as input 
import sys
import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Read single column csv text file into a dataframe object. Return dataframe 
def load_data(filename):
        return pd.DataFrame(np.genfromtxt(filename, dtype=str)[0:], columns=['data'])

# Count of the first, second or third digits in a list of numerical data. Return dataframe of counts
def get_digit_counts(data, order):
        count_data = pd.DataFrame()

        # Clean input and strip out all non-numerical chars. Select significant (non-zero) digits, assign to seperate col in dataframe
        data['digits'] = ((data['data'].replace(to_replace='[^0-9]+', value='', regex=True)).replace(to_replace='(^0+)', value='', regex=True))

        # Select the first, second, third, first two or three digit combinations for each datapoint in the dataset
        if len(order) == 2:
                data = data.loc[data['digits'].str.len() > 1]
                data['digits'] = data['digits'].str[0:len(order)]
                count_data['digits'] = range(10, 100)
        elif len(order) == 3:
                data = data.loc[data['digits'].str.len() > 2]
                data['digits'] = data['digits'].str[0:len(order)]
                count_data['digits'] = range(100, 1000)
        elif len(order) == 1:
                data['digits'] = data['digits'].str[int(order)-1]
                if order == '1': count_data['digits'] = range(0, 10)
                else: count_data['digits'] = range(0, 10)

        # Convert string values to int/float data types
        data['digits'] = pd.to_numeric(data['digits'])

        # Calculate count data for selected digits or digit combinations
        counts = data.groupby(['digits']).size().reset_index(name='digit_count')
        count_data = pd.merge(count_data, counts, on='digits', how='outer')

        return count_data

# Generate values for Benford distributions. Single-digit distributions as well as first two and first three digit joint distributions. Return dataframe of probabilities.
def benford_function(order):
    if order == '12':
        # Calculate Benford values for first two significant digits: P(d1,d2) = log10( 1 + ( 1 / ( 10*d1 + d2 ) ) )
        benford_values = [math.log10(1 + (1 / (10*float(str(d)[0]) + float(str(d)[1]) ))) for d in range(10, 100)]
        benford = pd.DataFrame(data = { 'digits': range(10, 100), 'benford' : benford_values })   
            
    elif order == '123':
        # Calculate Benford values for first three significant digit: P(d1,d2,d3) = log10( 1 + ( 1 / ( 100*d1 + 10*d2 + d3 ) ) )
        benford_values = [math.log10(1 + (1 / (100*float(str(d)[0]) + 10*float(str(d)[1]) + float(str(d)[2]) ))) for d in range(100, 1000)]
        benford = pd.DataFrame(data = { 'digits': range(100, 1000), 'benford' : benford_values })  

    elif order == '1':
        # Calculate Benford values for first significant digit: P(d1) = log10( 1 + ( 1 / d1 ) )
        benford_values = [math.log10(1 + (1 / float(d1))) for d1 in range(1, 10)]
        benford = pd.DataFrame(data = { 'digits': range(0, 10), 'benford' : [None] + benford_values })                                               

    elif order == '2': 
        # Calculate Benford values for second significant digit: P(d2) = Simga_d1 { log10( 1 + ( 1 / ( 10*d1 + d2 ) ) ) }
        benford_values = [0] * 10
        for d1 in range(1, 10): benford_values = [x + y for x, y in zip(benford_values, [math.log10(1 + (1 / (10*float(d1) + float(d2) ))) for d2 in range(0, 10)])]
        benford = pd.DataFrame(data = { 'digits': range(0, 10), 'benford' : benford_values })    

    elif order == '3':
        # Calculate Benford values for third significant digit: P(d3) = Simga_d1_d2 { log10( 1 + ( 1 / ( 100*d1 + 10*d2 + d3 ) ) ) }
        benford_values = [0] * 10
        for d1 in range(1, 10): 
            for d2 in range(0, 10):
                benford_values = [x + y for x, y in zip(benford_values, [math.log10(1 + (1 / (100*float(d1) + 10*float(d2) + float(d3) ))) for d3 in range(0, 10)])]
        benford = pd.DataFrame(data = { 'digits': range(0, 10), 'benford' : benford_values })      

    else: return None
        
    return benford

# Return list of expected counts under Benford's law. Return dataframe of expected counts
def get_expected_counts(total, order):
        # Calculate the expected counts under Benford's law using dataframes of Benford probabilities    
        expected = benford_function(order)
        expected['digit_count'] = expected['benford'] * total 

        return expected

# Calculate Chi-squared function. Return test statistic
def get_chi2_stat(data, expected):
        chi2_stat = (((data['digit_count'] - expected['digit_count'])**2) / expected['digit_count']).sum().sum()

        return chi2_stat

def main():
        # Load dataset from filepath passed by user
        filename = sys.argv[2].strip()
        data_df = load_data(filename)
        order = sys.argv[1]

        # Set variables for chart display labels
        if order == '1': chart_label = "First"
        elif order == '2': chart_label = "Second"
        elif order == '3': chart_label = "Third"
        elif order == '12': chart_label = "First Two"
        elif order == '123': chart_label = "First Three"
        else: print "Error: select a digit distribution to test against."; sys.exit(1)

        # Calculate the digit counts in the user's dataset
        count_data_df = get_digit_counts(data_df, order)

        # Calculate the counts expected under Benford's law
        count_expected_df = get_expected_counts(count_data_df['digit_count'].sum(), order)

        # Print observed and expected counts to the CLI
        print("observed counts = {}\n".format(list(count_data_df['digit_count'].values)))
        print("expected counts = {}\n".format(list(count_expected_df['digit_count'].round(2).values)))

        # Calculate Chi-Squared value
        chi2 = round(get_chi2_stat(count_data_df.astype('float64'), count_expected_df.astype('float64')), 2)
        
        # Degrees of freedom and Chi-Squared critical values (at P=0.05) for significance testing
        c_values = { '1': [8, 15.51], '2': [9, 16.92], '3': [9, 16.92], '12': [89, 111.02], '123': [899, 969.86] }

        # Perform Chi-Squared significance test
        if chi2 < c_values[order][1]: signf = True 
        else: signf = False
        
        # Print Chi-Squared significance result to CLI
        if signf: print("Observed distribution matches expected distribution.")
        else: print("Observed distribution does not match expected.")

        # Create chart object to display observed and expected counts
        fig, ax1 = plt.subplots()
        ax2 = ax1.twiny()

        # Add observed count data to chart with chart formatting
        count_data_df.plot(x='digits', y='digit_count', kind='bar', color='LightBlue', ax=ax1, legend=None)

        # Overlay expected count data to the chart
        count_expected_df.plot(x='digits', y='digit_count', kind='line', color='DarkGreen', ax=ax2, legend=None)

        # Add title and labels to the chart with chart formatting
        ax1.set_title('{} - Benford\'s Distribution of {} Digits'.format(filename, chart_label))
        ax1.set_ylabel('Count - {} Digits'.format(chart_label))
        ax1.set_xlabel('Digits')
        plt.xlim(count_expected_df['digits'].min(), count_expected_df['digits'].max())
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)

        # Add Chi-Squared value and significance test information as chart annotation
        plt.annotate(xy=[count_data_df['digits'].max()*0.7,count_data_df['digit_count'].max()*0.8], s="dof={}\nChi2={}\nCritical Value={}\nalpha=0.05".format(c_values[order][0], chi2, c_values[order][1]))

        # Display chart
        plt.show()

if __name__ == '__main__':
        main()