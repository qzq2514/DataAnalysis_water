import tkinter as tk
from tkinter import messagebox
from CurveFitting import handle

window=tk.Tk()
window.title("气候补偿拟合")
window.geometry('400x250')

lab_Hui=tk.Label(window,text="室内温度:",font=("Arial",12),width=15,height=2)
lab_Hui.place(x=10,y=70,anchor="nw")

tail_Hui=tk.Label(window,text="(°C)",font=("Arial",12),width=15,height=2)
tail_Hui.place(x=210,y=70,anchor="nw")

huiEntry=tk.Entry(window,show=None)

huiEntry.place(x=125,y=82,anchor="nw",width=140)

def calcu():
    huiData = huiEntry.get()
    try:
        huiData = float(huiData)
        handle( huiData)
    except Exception as e:
        pass

btn_Calcu=tk.Button(window,text="计算",bg="#ffff99",width=15,height=2,command=calcu)
btn_Calcu.place(x=140,y=140,anchor="nw")
window.mainloop()