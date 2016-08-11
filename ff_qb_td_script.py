import pandas as pd
import numpy as np
import html5lib

df = pd.DataFrame(dtype=float)

i = 1990
while i<2016:
    singleYear = pd.read_html('http://www.pro-football-reference.com/years/' + str(i) + '/passing.htm')
    singleYearDF = pd.DataFrame(singleYear[0])
    singleYearDF['TD'] = pd.to_numeric(singleYearDF['TD'],errors='coerce')
    singleYearDF['GS'] = pd.to_numeric(singleYearDF['GS'],errors='coerce')
    singleYearDF = singleYearDF.query('TD != "TD"')
    singleYearDF = singleYearDF.query('GS >= 12')
    singleYearDF.rename(columns={'Unnamed: 1': 'name','TD':str(i)}, inplace=True)
    df = df.append(singleYearDF[['name',str(i)]])
    df.fillna(value=0,inplace=True)
    i += 1
    
df['name'] = df['name'].str.replace('+', '')
df['name'] = df['name'].str.replace('*', '')

df = df.groupby(['name']).sum()
df = df.reset_index()

tdJumps = []
qbList = []
rowKeys = list(df.columns.values)
del rowKeys[0]

for index,row in df.iterrows():
    for index,key in enumerate(rowKeys):
        newQBObj1 = {'name':row['name'],'occasion':1}
        newQBObj2 = {'name':row['name'],'occasion':1}
        newQBObj3 = {'name':row['name'],'occasion':1}
        prevKey = rowKeys[index-1]
        if index != len(rowKeys)-1:
            nextKey = rowKeys[index+1]
        else:
            nextKey = False
        tdChange = row[key] - row[prevKey]
        if row[prevKey] > 0 and tdChange >= 15:
            newQBObj1['tds'] = row[prevKey]
            newQBObj1['year'] = prevKey
            newQBObj2['tds'] = row[key]
            newQBObj2['year'] = key
            if nextKey:
                newQBObj3['tds'] = row[nextKey]
                newQBObj3['year'] = nextKey
            if nextKey and row[nextKey] != 0:
                if row['name'] in qbList:
                    newQBObj1['occasion'] += 1
                    newQBObj2['occasion'] += 1
                    newQBObj3['occasion'] += 1
                tdJumps.append(newQBObj1)
                tdJumps.append(newQBObj2)
                tdJumps.append(newQBObj3)
                qbList.append(row['name'])
            elif not nextKey:
                tdJumps.append(newQBObj1)
                tdJumps.append(newQBObj2)
                qbList.append(row['name'])
                

tdJumpsDF = pd.DataFrame(tdJumps)
tdJumpsDF.set_index('name',inplace=True)
tdJumpsDF.to_csv('qb_td_jumps.csv')