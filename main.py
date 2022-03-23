##################
#### Packages ####
##################

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#####################################################
#### change working directory to script location ####
#####################################################

os.chdir(os.path.dirname(sys.argv[0]))

###############################
#### Import and clean data ####
###############################

df_raw = pd.read_csv('2022-03-21_Data_Bewerbungsaufgabe.csv', sep = ';')
#   df_raw.info()                                               #   get basic information on dataframe structure

data_header_old = list(df_raw.columns)                      #   get column names from original data
data_header_new = ['Energiequelle', 'Leistung in kW']       #   define name of renamed columns

df_clean = df_raw.drop(columns = data_header_old[0])        #   drop first row of dataframe
df_clean.rename(columns = {data_header_old[1] : data_header_new[0], data_header_old[2] : data_header_new[1]}, inplace = True)   # rename rows of dataframe

df_clean.sort_values(data_header_new[0], axis = 0, inplace = True)  #   sorting values by 'Energiequelle'

df_clean.loc[df_clean[data_header_new[1]] == 'yes', data_header_new[1]] = 600   #   replace 'yes'-values with 600 kW

df_clean.dropna(inplace = True)                             #   drop all rows with any empty, NaN, NaT - values

df_clean = df_clean[pd.to_numeric(df_clean[data_header_new[1]], errors='coerce').notnull()]     #   drop all rows with non-numerical entry values in 'Leistung in kW'

df_clean[data_header_new[1]] = df_clean[data_header_new[1]].astype(float)

##################################################################
#### check if all data is numerical value in 'Leistung in kW' ####
##################################################################

if pd.to_numeric(df_clean[data_header_new[1]], errors = 'coerce').notnull().all():
    print('All values are numerical')
else:
    print('Not all values are numerical')

###########################################################################
#### seperate data by 'Energiequelle' entry and calculate distribution ####
###########################################################################

energy_source = df_clean[data_header_new[0]].unique()   #   write all different energy sources into list

for i in energy_source:                                 
    globals()['df_%s' % i] = df_clean[df_clean[data_header_new[0]] == i]                #   generate dynamic variable name for pandas dataframe
    globals()['distribution_%s' % i] = pd.DataFrame(globals()['df_%s' % i].pivot_table(columns = ['Leistung in kW'], aggfunc = 'size'))   #   generate dynamic variable for distribution dataframe

############################
#### plot gas dataframe ####
############################

# open figure box with specified attributes
fig = plt.figure(figsize = (2, 2), facecolor = 'w', edgecolor = 'k', dpi = 600)
ax = fig.gca()

# generating bar plot for gas distribution
plt.bar([str(x) for x in distribution_gas.index], distribution_gas[0])

# setting title and labels
plt.title('Energieanlagen: Gas', fontsize = 3, fontweight = 'bold')
plt.xlabel('Leistung in kW', fontsize = 3)
plt.ylabel('Anzahl der Energieanlangen', fontsize = 3)

# setting line and tick-size
plt.yticks(np.arange(0, 12, step = 1), fontsize = 3)
plt.xticks([str(x) for x in distribution_gas.index], fontsize = 3, rotation = 45)
ax.xaxis.set_tick_params(width = 0.5)
ax.yaxis.set_tick_params(width = 0.5)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)

# adding vertical grid
plt.grid(axis = 'y', color = 'gray', linestyle = '-.', linewidth = 0.2)

# option so that plot fits tightly in generated frame
plt.tight_layout()

# saving image to png-file
plt.savefig('distribution_gas.png')




