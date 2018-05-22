import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
x = np.linspace(0, 1, 5)
y = np.linspace(0, 1, 7)
z = np.linspace(0, 1, 9)

path="orgData.xls"
df=pd.read_excel(path)

heatingPower=df["Power (kW)"]
inTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
[X,Y,Z]=np.meshgrid(heatingPower,inTemp,z)