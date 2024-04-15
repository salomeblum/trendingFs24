import pickle
import numpy as np
import matplotlib.pyplot as plt

y_data      = np.load('y.pkl', allow_pickle=True)
metadata    = np.load('metadata.pkl', allow_pickle=True)
x_data      = np.load('x.pkl', allow_pickle=True)

DeviceId    = 31424
Sensor      = "CAN_Flow" #Select from: Beschleunigung_Horizontal_58, Beschleunigung_Vertikal_60, CAN_Flow, Druck_DS_P2, Druck_SS_P1, Strom
FirstPump   = 31424
LastPump    = 31938

for DeviceId in range(FirstPump, LastPump+1):
    if DeviceId >= LastPump:
        break

    SensorTypes = {
        "Beschleunigung_Horizontal_58": 0,
        "Beschleunigung_Vertikal_60":   1,
        "CAN_Flow":                     2,
        "Druck_DS_P2":                  3,
        "Druck_SS_P1":                  4,
        "Strom":                        5
        }

    Measurements = {}

    #Write Start / End Id's to Dictionary for futre lookup
    for Id in range(len(metadata)):
        if (metadata[Id]["trigger_time"])[:10] != (metadata[Id-1]["trigger_time"])[:10]:                 
            DeviceIdTmp = (metadata[Id]["device_id"])
            ElapsedTime = (metadata[Id]["elapsed_time_h"])

            if DeviceIdTmp not in Measurements:
                Measurements[DeviceIdTmp] = {}             
                                                                    
            Measurements[DeviceIdTmp][ElapsedTime] = {                                                             
                                    "IdStart"     : Id,
                                    "IdEnd"       : Id+92}
        else:
            continue
    #Dictionary Measurements: {DeviceID: {ElapsedTime: {IdStart: IdStart, IdEnd: IdEnd}}}

    #get Number of Total Measurements 
    try:
        NumberOfMeasurements = (len(Measurements[DeviceId]))
            #extract Data&Plot from each Measurement

        for n in range(NumberOfMeasurements):
            ElapsedTime = n * 500
            IdStart = Measurements[DeviceId][ElapsedTime]["IdStart"]
            IdEnd   = Measurements[DeviceId][ElapsedTime]["IdEnd"] 

            x = range(0,93,1)
            y = []
            for IdStart in range(IdStart,IdEnd+1):
                y.append(np.mean(x_data[IdStart][SensorTypes[Sensor]]))
            plt.plot(x, y, label=str(ElapsedTime))

        #Setting Metadata for Plot & Plotting
        plt.xlabel('Time')
        plt.ylabel(Sensor)
        plt.legend()
        plt.title("Graph for Sensor: "+str(DeviceId))
        plt.grid()
        #plt.show()

        plt.savefig("./graphs/"+str(Sensor)+"-"+str(DeviceId)+".png")
        
        plt.clf
        y = []

    except KeyError:
        print("Pump with ID",DeviceId,"not found.")
        continue

            
    #extract Data&Plot from each Measurement
"""
    for n in range(NumberOfMeasurements):
        ElapsedTime = n * 500
        IdStart = Measurements[DeviceId][ElapsedTime]["IdStart"]
        IdEnd   = Measurements[DeviceId][ElapsedTime]["IdEnd"] 

        x = range(0,93,1)
        y = []
        for IdStart in range(IdStart,IdEnd+1):
            y.append(np.mean(x_data[IdStart][SensorTypes[Sensor]]))
        plt.plot(x, y, label=str(ElapsedTime))

    #Setting Metadata for Plot & Plotting
    plt.xlabel('Time')
    plt.ylabel(Sensor)
    plt.legend()
    plt.title("Graph for Sensor: "+str(DeviceId))
    plt.grid()
    #plt.show()

    plt.savefig("./graphs/"+str(Sensor)+"-"+str(DeviceId)+".png")
    
    y = []

"""