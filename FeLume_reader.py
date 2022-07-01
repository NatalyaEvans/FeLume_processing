# -*- coding: utf-8 -*-
"""
Initial version of this script created on Fri Jan  3 13:31:35 2020
Last updated 2021 Sept 10 to work with the FeLume

@author: Talia Evans

This script is designed to average measurements from the FeLume, as stored in csv files, into an Excel sheet, which this script writes.
This script reads through all files that contain ".csv" in the folder that this script sits in, so you must organize this folder to concatenate the files you desire.
If this library cannot read the csv, this script does not concatenate that file and reports that it failed


"""
# %% 1. Load relevant libraries
#This chunk gets all the pre-requisites out of the way for you
#Note that this code will overwrite the output file, so if there is already a file with output_name in the folder, it will be replaced

output_name='out.xlsx' #This is the name of the file that this code outputs. The default is output_name='out.xlsx'

import csv
import numpy as np
import numpy.ma as ma
import os
import pandas as pd

#If chunk 2 does not populate a listofout, it is likely that the current working directory is not in the correct location. The following three lines of code in this chunk could help.
#Alternatively, running the entire script at once, rather than chunks, fixed this issue for me every time I tried it.

#print(os.getcwd)
#ROOT_PATH = os.path.dirname(os.path.abspath('cnv to csv_backup.py')) # #https://stackoverflow.com/questions/21934731/how-to-set-current-working-directory-in-python-in-a-automatic-way
#myfile_path = os.path.join(ROOT_PATH, "cnv to csv_backup.py")

#%% 2. Create a list of csv files to iterate through
#This chunk identifies all the csv files in a folder then fills their names into a list, listofout

listoffiles = os.listdir('.') #creates the list, taken from listing 3 on https://stackabuse.com/python-list-files-in-a-directory/
pattern = "*.py" #I don't know what this does
 
listofout_temp=[0]*len(listoffiles) #creates a blank list to get filled with the filenames of files that worked
for name in listoffiles: #iterate through all files
    if '.csv' in listoffiles[listoffiles.index(name)]: #select only the .cnv files
        listofout_temp[listoffiles.index(name)]=name   #create a temporary list with empty space and only cnv files
listofout=list(filter(lambda a: a != 0, listofout_temp))  #removes the file name of the csv output from the files that get searched for energies https://www.geeksforgeeks.org/lambda-filter-python-examples/



# %% 3. Generate the output list of lists and print which files don't work
fail=list() #create a list of file names that the cnv reader couldn't read

if 'data' in globals(): #data is the object that concatenates all of the cnv values. We clear it before concatenation in case this code is ran multiple times.
    del data

for entry in listofout: #loop through all the files
        run=pd.read_csv(entry, sep=',',header=None) # read the csv
        check=run>1E8 # create a dataframe that's for finding the timestamp
        # timestamp=np.nonzero(check[0]) # find the timestamp
        timestamp=np.flatnonzero(check[0])
        # now average 50 time points before the time stamp, and find the stdev for fun too
        temp=np.array([np.mean(run[timestamp[0]-51:timestamp[0]-1])[0],np.std(run[timestamp[0]-51:timestamp[0]-1])[0]])        
        if not 'data' in globals(): #this is the base case to generate the object that will be concatenated
            data=temp #defines the concatenation variable
        else:
            data=np.vstack([data, temp]) #if the concatentation variable exists, concatenate to it

 # %% 6. Output the data file  
data2=pd.DataFrame(data,columns=['Mean','Stdev']) #converts your data into a panda dataframe to make the output xlsx file easier to generate
data2.insert(0, "file", listofout) # add the file names
data2.to_excel(output_name,index=False) #outputs the concatenated data. Change the file name by adjusting "ouput_name" at the top. Index referes to unique numbers on the left side of the xlsx sheet, these aren't really needed.  

print('')
print("You have successfully written "+str(len(listofout)) +" cnv files into a single xlsx file named " +str(output_name))

