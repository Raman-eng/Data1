import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from sklearn.svm import SVR

register_matplotlib_converters()

numeric_fields = ['Consump1 Rate (kg/h)', 'Aux Power1 (kW)']

def readAllFiles(extension):
  return [i for i in glob.glob('*.{}'.format(extension))]

def updateDateTimeField(all_filenames):
    for file_name in all_filenames:
        df = pd.read_excel(file_name)
        for col in df.select_dtypes([np.datetime64]):
            df.rename(columns={col:'Datetime'}, inplace=True)
            df.to_excel(file_name, sheet_name='Sheet1')

def getSortedCombinedData(all_filenames):
 df= pd.concat([pd.read_excel(f) for f in all_filenames], sort=True)
 df.sort_values('Datetime')
 return df

def badDataFiltering(df):
  df = df[~df['Consump1 Rate (kg/h)'].str.contains("W", na=False)]
  df = df[~df['Consump1 Rate (kg/h)'].str.contains("E", na=False)]
  return df

def convertVariableToNumeric(df):
  df[numeric_fields] = df[numeric_fields].apply(pd.to_numeric)
  return df

def plotData(df):
  for (column_name, column_data) in df.iteritems():
    if column_name not in ['Datetime']:
      sns.lineplot(x='Datetime', y=column_name, color='red', data=df)

def exportFinalData(df, file_name):
  df.to_excel(file_name, sheet_name='Sheet1')

if __name__ == "__main__":
    file_extensions = 'xlsx'
    file_name = 'final_out.xlsx'
    os.chdir("data/")
    all_filenames = readAllFiles(file_extensions)
    updateDateTimeField(all_filenames)
    df = getSortedCombinedData(all_filenames)
    df = badDataFiltering(df)
    df = convertVariableToNumeric(df)
    plotData(df)
    exportFinalData(df, file_name)


