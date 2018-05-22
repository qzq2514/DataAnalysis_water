import tkinter as tk
from tkinter import messagebox
from SortHeat import handle

window=tk.Tk()
window.title("供热水力分析")
window.geometry('400x350')

lab_Heat=tk.Label(window,text="热指标q: ",font=("Arial",12),width=15,height=2)
lab_Give=tk.Label(window,text="供水温度tg:",font=("Arial",12),width=15,height=2)
lab_Hui=tk.Label(window,text="回水温度th:",font=("Arial",12),width=15,height=2)
lab_Heat.place(x=10,y=50,anchor="nw")
lab_Give.place(x=10,y=100,anchor="nw")
lab_Hui.place(x=10,y=150,anchor="nw")

tail_Heat=tk.Label(window,text="(w/m²)",font=("Arial",12),width=15,height=2)
tail_Give=tk.Label(window,text="(°C)",font=("Arial",12),width=15,height=2)
tail_Hui=tk.Label(window,text="(°C)",font=("Arial",12),width=15,height=2)
tail_Heat.place(x=215,y=50,anchor="nw")
tail_Give.place(x=210,y=100,anchor="nw")
tail_Hui.place(x=210,y=150,anchor="nw")



heatEntry=tk.Entry(window,show=None)
giveEntry=tk.Entry(window,show=None)
huiEntry=tk.Entry(window,show=None)

heatEntry.place(x=125,y=62,anchor="nw",width=140)
giveEntry.place(x=125,y=112,anchor="nw",width=140)
huiEntry.place(x=125,y=162,anchor="nw",width=140)

def calcu():
    heatData=heatEntry.get()
    giveData = giveEntry.get()
    huiData = huiEntry.get()

    try:
        heatData = float(heatData)
        giveData = float(giveData)
        huiData = float(huiData)
        handle(heatData, giveData, huiData)
        tk.messagebox.showinfo(title="成功", message="计算成功，新文件已导出!")
    except Exception as e:
        ans=tk.messagebox.askyesno(title="数据错误", message="数据错误,请重新输入(Y)，或退出计算(N)")
        print(e)
        if(ans==False) :
            window.quit()
        #tk.messagebox.showinfo(title="数据错误", message="数据错误,请重新输入(Y)，或退出计算(N)")

btn_Calcu=tk.Button(window,text="计算",bg="#ffff99",width=15,height=2,command=calcu)
btn_Calcu.place(x=140,y=220,anchor="nw")
window.mainloop()