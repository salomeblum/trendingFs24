import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
#from statsmodels.formula.api import ols
#from statsmodels.stats.anova import anova_lm

from sorted_data import bereinigteDaten, gemittelteAchse, deviceNames_failures, datenKeys

#Funktionen

#Pandas Dataframe mit nach Messerien erstellen
def data_messserie(data:list, sensor: int, messserie:int, betriebspunkt:str, schaden:str):
    
    #Filtert Daten nach Betriebspunkt und Schaden --> deviceNames_failures berücksichtigt nur Pumpen mit einem einzigen Schaden
    data_with_failure = deviceNames_failures(data, betriebspunkt, schaden) #Liste mit den Pumpen_IDs nach Betriebspunkt und Schaden
    print(data_with_failure)
    y_values = pd.DataFrame()

    #erstellt ein Pandas Dataframe mit je einer Spalte Messwerte pro Pumpe
    for pump in data_with_failure:
        daten_dict = bereinigteDaten(pump, sensor) #Dictionary mit den bereinigten Daten
        y_gemittelt = gemittelteAchse(daten_dict, messserie)
        y_values[pump] = y_gemittelt
    
    return y_values #Pandas Dataframe mit je einer Spalte pro Pumpen für einen spezifischen Sensor, abhängig von Messserie 
                    #--> Bug: Nicht alle Pumpen haben dieselbe Anzahl Messerien, wird nicht berücksichtigt...


#Mittelwerte eines Pandas-Dataframe berechnen
def messserie_gemittelt(data:pd.DataFrame, schaden:str):
    y_gemittelt = []
    for index, row in data.iterrows():
        y_gemittelt.append(row.mean())
        
    data[f"Mean {schaden}"] = y_gemittelt
    
    return data


#Boxplots für Pandas Dataframe
def plot_messserie(data:pd.DataFrame, sensor:int, messserie:int, schaden:str): 
    sns.boxplot(data=data)
    plt.ylabel(f"Sensor {sensor_dict[sensor]}")
    plt.xlabel(f"Pumpen")
    plt.title(f"Boxplot für die Mess-Serie {messserie} mit Schaden {schaden}")
    plt.show()


#Daten einlesen
metadata = np.load('metadata.pkl', allow_pickle=True)


# Variablen für Boxplots
sensor_type  = 0         # 0   = Beschleunigung_Horizontal_58
                        # 1   = Beschleunigung_Vertikal_60
                        # 2   = CAN_Flow
                        # 3   = Druck_DS_P2
                        # 4   = Druck_SS_P1
                        # 5   = Strom           
sensor_dict = {0:"Beschleunigung Horizontal", 1:"Beschleunigung Vertikal", 2: "CAN_Flow", 3: "Druck_DS P2", 4: "Druck_SS P1", 5: "Strom"}

betriebs_punkt = "air/water"


#Messerie 1 für alle Pumpen mit failure "bearing"

"""messung = 1
failure = "bearing"

messung_1_bearing = data_messserie(metadata, sensor_type, messung, betriebs_punkt, failure)
messung_1_bearing_gemittelt = messserie_gemittelt(messung_1_bearing, failure)


plot_messserie(messung_1_bearing_gemittelt, sensor_type, messung, failure)"""


#Messerie 1 für alle Pumpen mit failure "brushes"

"""messung = 1
failure = "brushes"

messung_1_brushes = data_messserie(metadata, sensor_type, messung, betriebs_punkt, failure)
messung_1_brushes_gemittelt = messserie_gemittelt(messung_1_brushes, failure)

plot_messserie(messung_1_brushes_gemittelt, sensor_type, messung, failure)"""


#Messerie 1 für alle Pumpen mit failure "leakage"

"""messung = 1
failure = "leakage"

messung_1_leakage = data_messserie(metadata, sensor_type, messung, betriebs_punkt, failure)
messung_1_leakage_gemittelt = messserie_gemittelt(messung_1_leakage, failure)

plot_messserie(messung_1_leakage_gemittelt, sensor_type, messung, failure)"""


#alle Messerien 1 in einem Boxplot

"""messserie_1_gemittelt = pd.DataFrame()
messserie_1_gemittelt["bearing"] = messung_1_bearing_gemittelt.iloc[:,-1]
messserie_1_gemittelt["brushes"] = messung_1_brushes_gemittelt.iloc[:,-1]
messserie_1_gemittelt["leakage"] = messung_1_leakage_gemittelt.iloc[:,-1]

plot_messserie(messserie_1_gemittelt, sensor_type, messung, schaden="alle Schadenstypen")"""

#Überprüfen ob Mittelwerte signifikant voneinander abweichen
"""f_statistic, p_value = stats.f_oneway(messserie_1_gemittelt["bearing"], messserie_1_gemittelt["brushes"], messserie_1_gemittelt["leakage"])"""

#--> F-Statistik: 9.567399882309363, P-Wert: 0.0001284881233282819 --> deutet auf signifikante Unterschiede in den Mittelwerten hin, müsste genauer angeschaut werden

"""f_statistic, p_value = stats.f_oneway(messserie_1_gemittelt["bearing"], messserie_1_gemittelt["brushes"])"""

#--> F-Statistik: 9.060631650029844, P-Wert: 0.0033703528493578975 --> deutet auf signifikante Unterschiede in den Mittelwerten von bearing und brushes hin, müsste genauer angeschaut werden

"""f_statistic, p_value = stats.f_oneway(messserie_1_gemittelt["bearing"], messserie_1_gemittelt["leakage"])"""

#--> F-Statistik: 0.2796091950686821, P-Wert: 0.5982308993100722 --> zwischen bearing und leakage scheinen keine signifikanten Unterschiede zu bestehen

"""f_statistic, p_value = stats.f_oneway(messserie_1_gemittelt["leakage"], messserie_1_gemittelt["brushes"])"""

#--> F-Statistik: 50.82270610205475, P-Wert: 2.2325409470825159e-10 --> zwischen leakage und brushes scheinen extrem signifikane Unterschiede zu bestehen --> sollte genauer untersucht werden

    
#Messerie 2 für alle Pumpen mit failure "bearing"

messung_last = 2
failure = "bearing"

messung_last_bearing = data_messserie(metadata, sensor_type, messung_last, betriebs_punkt, failure)
messung_last_bearing_gemittelt = messserie_gemittelt(messung_last_bearing, failure)

print()

#plot_messserie(messung_last_bearing, sensor_type, messung, failure)


#Messerie 5 für alle Pumpen mit failure "brushes"

#Messerie 5 für alle Pumpen mit failure "leakage"

#alle Messerien 5 in einem Boxplot

#Messerie 1 vs 5 mit failure "bearing"

#Messerie 1 vs 5 mit failure "brushes"

#Messerie 1 vs 5 mit failure "leakage"