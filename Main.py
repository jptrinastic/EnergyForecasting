#Edited by jptrinastic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


#This function imports the two csv files for Round1 training, and merges them.  This outputs a Pandas DataFrame object that contains all of the input data from the files.

def Import(flag):
	flag = flag.lower()
	file2 = "2015_Round1_training_2of2.csv"
	file1 = "2015_Round1_training_1of2.csv"

	F1 = pd.read_csv(file1)
	F2 = pd.read_csv(file2)
	Total = pd.merge(F2,F1,on='Date')
        return Total


#In the csv files, one column has a key for what type of day it is (Particular holidays, saturdays, sundays, etc.).  To facilitate plotting and running machine learning algorithms, these
#may need to be converted to an integer key code instead.  This function uses a dictionary from the documentation for the challenge to convert each element in the array to an integer.
#There are some key codes (SD was the one I'm aware of right now) that are not in the documentation.  For handle things that won't fit the key I've generated, I've built a try-except
#structure that will add a new integer to the key, beyond the 10 I've hard-coded into the method.

def ConvertDayToNumbers(data):
	copy = data.copy()
	key = {'WE' : 0, 'SA' : 1, 'SU' : 2, 'CD' : 3, 'BD' : 4, 'J1' : 5, 'GF' : 6, 'EM' : 7, 'M1' : 8, 'M2' : 9, 'A2' : 10}
	currentNumber = 11
	for i in xrange(0,len(data.index)):
		try:
			copy.at[i,'Day_type'] = key[copy.loc[i,'Day_type']]
		except KeyError:
			key[copy.loc[i,'Day_type']] = currentNumber
			copy.at[i,'Day_type'] = key[copy.loc[i,'Day_type']]
			currentNumber = currentNumber + 1
	copy['Day_type'] = copy['Day_type'].astype(int)
	return copy


#There are some difficulties in saving the figure when runinng Pandas DataFrame.hist() method, so I've written my own that uses matplotlib's subfigure routines and the DataFrame.hist() method
#only for individual plots.  Then, I save all of the histograms in the file "SimpleHistograms.png".  

def PlotHistograms(data):
	header = list(convertedSet.columns.values)

	#Some columns in the data structure aren't appropriate to plot.  For instance, the date doesn't make sense to make a histogram of.  And if the strings for Day_type haven't been converted,
	#that also can't be plotted.  This makes a list of all the things that will actually be plotted (ie, data types that are floats and integers).

	plotHeader = []
	for label in header:
		if((isinstance(data.loc[0,label],int)) or (isinstance(data.loc[0,label],float))):
			plotHeader.append(label)

	#Finds how to format the subfigures

	nColumns = 3
	nRows = math.ceil(len(plotHeader)/3.0)
	index = 1

	#For each subfigure, a title is generated and a histogram run.  The DataFrame.hist() output is then plotted on the matplotlib subfigure selected.  The index variable controls
	#which subfigure to use.

	for label in plotHeader:
		plt.subplot(nRows, nColumns, index)
		plotLabel=label.replace("_"," ")
		if(isinstance(data.loc[0,label],int)):
			nbins = data[label].max() + 1
			plt.title(plotLabel)
			data[label].hist()
		elif(isinstance(data.loc[0,label],float)):
			plt.title(plotLabel)
			data[label].hist(bins=18, xrot=30)
		index = index + 1
		plt.tick_params(axis='y',labelleft='off')
	plt.tight_layout()
	plt.savefig("SimpleHistograms.png")

# Since the desired forecasting data, volume of energy is used, is a daily variable, it may be helpful to compute a new set of data describing statistics within each day that can be used as features/predictors.
# To do this, I have used the groupby method to group data by 'Date' and then calculate statistics, which are outputted to a new DataFrame, one for each type of statistic (average, variance, etc.)
# Some of these variables don't make sense (e.g., average of 'school_holiday' variable), but I computed stats for all for now.  We can always change this later.
# Returns a list, where each element of list is the DataFrame corresponding to a different statistic:
#  [0] - Mean, [1] - Median, [2] - Variance, [3] - Minimum, [4] - Maximum
def WithinDayStatistics(data):
    meanData = data.groupby('Date').mean()
    medianData = data.groupby('Date').median()
    varData = data.groupby('Date').var()
    minData = data.groupby('Date').min()
    maxData = data.groupby('Date').max()
    return meanData, medianData, varData, minData, maxData

# Plot scatter plots of various within-day statistics with daily energy volume, output to png file
# Input: 1) data - input data, 2) stat - descriptive statistics to use for feature to scatter plot vs daily energy volume (options: mean,median,var,min,max)
def PlotScatterPlots(data,stat):

    # Convert choice of statistic ('stat') into integer to access element of within-day data to use for scatterplot
    statKey = {'mean' : 0, 'median' : 1, 'var' : 2, 'min' : 3, 'max' : 4}
    statIndex = statKey[stat]
    
    header = list(data[statIndex].columns.values)
    
    #Some columns in the data structure aren't appropriate to plot.  For instance, the date doesn't make sense to make a histogram of.  And if the strings for Day_type haven't been converted,
    #that also can't be plotted.  This makes a list of all the things that will actually be plotted (ie, data types that are floats and integers).
    #Based on 'stat' input, choose that particular descriptive variable to appen to 'plotHeader'
    
    plotHeader = []
    for label in header:
        if((isinstance(data[statIndex][label][0],int)) or (isinstance(data[statIndex][label][0],float))):
            plotHeader.append(label)
            
    #Finds how to format the subfigures

    nColumns = 3
    nRows = math.ceil(len(plotHeader)/3.0)
    index = 1

    #Plot scatter plots for chosen descriptive statistic and output to file.  The IV (y-axix) is always daily energy volume.
    plt.close
    for label in plotHeader:
        plt.subplot(nRows, nColumns, index)
        plotLabel=label.replace("_"," ")
        plt.title(plotLabel)
        plt.plot(data[statIndex][label],data[0]['Volume'],marker='o',ls='')
        index = index + 1
        plt.tick_params(axis='y',labelleft='off')
    plt.tight_layout()
    plt.savefig("WithinDayScatterPlots.png")

#Import the trainingSet
trainingSet = Import('N')

#Convert the Day_type strings into integer codes
convertedSet = ConvertDayToNumbers(trainingSet)

#Plots the histograms for each of the columns in the set
PlotHistograms(convertedSet)
plot.close()

#Create within-day data set and produce scatter plots
withinDay=WithinDayStatistics(convertedSet)
PlotScatterPlots(withinDay,'mean')
plt.close()
