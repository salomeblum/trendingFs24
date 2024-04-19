import pickle
import numpy as np
import matplotlib.pyplot as plt
import logging
import pandas as pd
import seaborn as sns

#Teil 0: Daten einlesen
y_data = np.load('y.pkl', allow_pickle=True)
metadata = np.load('metadata.pkl', allow_pickle=True)
x_data = np.load('x.pkl', allow_pickle=True)

#Teil 1: 
#List of all Pumps, exluding 31468, 31564, 31565 which have no values in Dataset
Pumps = [
    31424, 31426, 31427, 31428, 31429, 31430, 31431, 31432, 31433, 31434,
    31435, 31436, 31437, 31438, 31439, 31440, 31441, 31442, 31443, 31444,
    31445, 31446, 31447, 31448, 31449, 31450, 31451, 31452, 31453, 31454,
    31455, 31456, 31457, 31458, 31459, 31460, 31461, 31462, 31463, 31464,
    31465, 31466, 31467, 31469, 31470, 31471, 31485, 31486, 31487, 31488,
    31490, 31491, 31492, 31493, 31496, 31497, 31498, 31499, 31500, 31501,
    31502, 31503, 31504, 31560, 31572, 31579, 31923, 31924, 31925, 31926, 
    31927, 31928, 31929, 31931, 31932, 31933, 31934, 31935, 31936, 31937, 
    31938 ]

#Create callable function to retrieve max Elapsed time for any DeviceId
def getMaxElapsedTime(DeviceId):
    global MaxValue
    MaxValues = []
    for n in range(len(metadata)):
        if DeviceId == metadata[n]["device_id"]:
            MaxValues.append(metadata[n]["elapsed_time_h"])
    try: 
        MaxValue = max(MaxValues)
    except ValueError:
        print("There are no values for:",DeviceId)
        #break


PumpTests   = {}

for DeviceId in Pumps: 

    #Create Dictioary for specifc Pump
    PumpTests[DeviceId] = {}

    getMaxElapsedTime(DeviceId)

    #Write Values to Dict 
    for ElapsedTime in range(0,MaxValue+500,500):
        PumpTests[DeviceId][ElapsedTime] = {}

        #Get Individual Tests 
        for n in range(len(metadata)):
            if DeviceId == metadata[n]["device_id"] and ElapsedTime== metadata[n]["elapsed_time_h"] and round(metadata[n]["t_min"]) != round(metadata[n]["t_max"]):
                PumpTests[DeviceId][ElapsedTime][round(metadata[n]["t_min"])] = {
                    "TestId"        :   n,
                    "TimeStart"     :   round(metadata[n]["t_min"]),
                    "TimeEnd"       :   round(metadata[n]["t_max"])
                    }


#Teil 2: 
#Ermitteln der Pumpen_IDs für Air/Water und spezifische Failures von Air/Water-Pumpen

#Ermitteln Pumpen_ID nach Betriebspunkt
def deviceNames(data:np.array, condition:str):
    data_df = pd.DataFrame(data)
    data_select = data_df.loc[(data_df["device_infos/condition"]==condition)]
    devices = []
    for e in data_select["device_id"]:
        if e not in devices:
            devices.append(e)
        else:
            continue
    return devices

#Ermitteln Pumpen-ID nach Betriebspunkt und Failure
def deviceNames_failures(data:np.array, condition:str, failure:str):
    data_df = pd.DataFrame(data)
    data_select = data_df.loc[(data_df["device_infos/condition"]==condition)&
                              (data_df["device_infos/defect 1"]==failure) & 
                              (pd.isna(data_df["device_infos/defect 2"]))]
    devices = data_select["device_id"].unique().tolist()
    return devices #Liste mit den Pumpen_IDs die unter einem bestimmten Betriebspunkt und mit einem bestimmten Schaden laufen

#auslesen von Keys eines Dictionarys
def datenKeys(data:dict):
    keyList = []
    for keys in data:
        keyList.append(keys)

    return keyList


#Teil 3: 
#Setzen von Variablen - Betriebspunkt, PumpenIDs, SensorTyp
#Betriebspunkt
Condition = "air/water"

#ermittelte Pumpen-IDs in Listenform zur weiteren Verwendung
md_air_water = deviceNames(metadata, "air/water")
md_air_water_bearings = deviceNames_failures(metadata, Condition, "bearing")
#Devices: 31433, 31459

md_air_water_brushes = deviceNames_failures(metadata, Condition, "brushes")
#31432, 31434, 31448, 31449, 31450, 31451, 31456, 31470, 31501, 31502, 31503, 31504, 31927, 31928, 31929, 31935, 31937, 31938

md_air_water_leakage = deviceNames_failures(metadata, Condition, "leakage")
#31490, 31492

 
DeviceId    = 31434
SensorType  = 0         # 0   = Beschleunigung_Horizontal_58
                        # 1   = Beschleunigung_Vertikal_60
                        # 2   = CAN_Flow
                        # 3   = Druck_DS_P2
                        # 4   = Druck_SS_P1
                        # 5   = Strom           
SensorDict = {0:"Beschleunigung Horizontal", 1:"Beschleunigung Vertikal", 2: "CAN_Flow", 3: "Druck_DS P2", 4: "Druck_SS P1", 5: "Strom"}

Key = 1

#Dictionary Data: Elapsed Time -> TimeStart -> List with all Values
def bereinigteDaten(devID:int, sensor):
    Data        = {}

    getMaxElapsedTime(devID)

    for ElapsedTime in range(0,MaxValue+500,500):
        Data[ElapsedTime] = {}

        #Retrieve TestId and create new empty list for every Time period
        for TimeStart in PumpTests[devID][ElapsedTime]:
            TestId = (PumpTests[devID][ElapsedTime][TimeStart]["TestId"])
            Data[ElapsedTime][TimeStart]= []

            #add all 10'000 Entries for Time Period to ad List inside Dict
            for n in (x_data[TestId][sensor]):
                (Data[ElapsedTime][TimeStart]).append(n)
        
        #Keys ersetzen mit 1,2,3 usw., damit in Boxplots einfacher nach den Messserien gefiltert werden kann
        DataNewKey = {}
        NewKey = 1

        for key in Data:
            DataNewKey[NewKey] = Data[key]
            NewKey += 1
    
    return DataNewKey #Dictionary with key (Integer von 1 aufwärts als Indize für jede Messserie) and List (Data from x.pkl)

#dictionary mit bereinigten Daten zu Pumpe mit gewähltem SensorenTyp    
daten_test = bereinigteDaten(DeviceId, SensorType)


#Dictionary in eine 1d-Liste mit allen erfassten Daten umwandeln
def datenAchse(data:dict, key:int):
    y_axis = []
    for values in data[key].values():
        y_axis.extend(values)
    return y_axis

#Dictionary in eine 1d-Liste umwandeln, Werte pro 10000 Einträge mitteln
def gemittelteAchse(data:dict, key: int):
    axis = []
    if key in datenKeys(data):
        for values in data[key].values():
            mean = np.mean(values)
            axis.append(mean)
    else:
        print(f"Key {key} nicht im Dictionary enthalten ")
    return axis



"""y_axis = pd.DataFrame(gemittelteAchse(daten_test,Key), columns=[SensorDict[SensorType]])
x_axis = np.arange(0,len(y_axis))"""



"""sns.boxplot(y=y_axis[SensorDict[SensorType]])
plt.show()"""


"""plt.plot(x_axis,y_axis)
plt.xlabel("Zeit [s]")
plt.ylabel(f"{SensorDict[SensorType]}")
plt.title(f"Pumpe {DeviceId} - Messung {Key/500}")
plt.show()"""