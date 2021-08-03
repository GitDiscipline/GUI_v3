
import tkinter as tk

from tkinter import ttk
from tkinter import *
import tkinter.messagebox

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import asksaveasfile

import tkinter.filedialog

import pandas as pd
import pickle

import numpy as np
import seaborn as sb
import sklearn
from sklearn.multioutput import MultiOutputRegressor
from scipy import signal
import matplotlib.pyplot as plt


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

win = tk.Tk()
win.geometry('500x600')
win.title("Vibration Data Analysis GUI")



pickle_in = open('sensor.pkl', 'rb')
classifier = pickle.load(pickle_in)

pickle_in2 = open('sensor2.pkl', 'rb')
classifier2 = pickle.load(pickle_in2)




var = IntVar()

R1 = Radiobutton(win, text="Decision tree regression", variable=var, value=1
                  )
R1.place(x=0,y=130)
R2 = Radiobutton(win, text="Artificial neural network", variable=var, value=2
                  )
R2.place(x=180,y=130)



def download():
    global df1,df2
    a=df1
##    if len(a.columns)==8:
##        a=a.drop(['Unnamed: 0'],axis=1)
    a2=[]
    for i in range(len(a.index)):
        if var.get()==1:
            a1=classifier.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
        elif var.get()==2:
            a1=classifier2.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
            
        a1=a1.tolist()
        a1=sum(a1,[])
        a2.append(a1)
    df2=pd.DataFrame(a2, columns =["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"])

    fname = tkinter.filedialog.asksaveasfilename(title=u'Save file', filetypes=[("csv", ".CSV")])
    
    fname=fname+'.csv'
    
    df2.to_csv(fname)





def import_csv_data1():
    global v1,df1,df0
    csv_file_path1 = askopenfilename()
    print(csv_file_path1)
    df1 = pd.read_csv(csv_file_path1)
    v1.set(csv_file_path1)
    
    

    
##    df1=df1.drop(0)
##    df1=df1.reset_index()
##    

   


    #df1.columns = [''] * len(df1.columns)

    df1.columns=['INDEX', 'Time', 'V-INV', 'V-INT', 'V-ICV', 'V-ICT', 'V-TCV', 'V-TCT',
       'V-MRV', 'V-B1V', 'V-B2V', 'V-B3V', 'V-B5V', 'V-HCV', 'NH_Speed',
       'NL_Speed']
    #df1=df1.drop(0)
    df1=df1.reset_index()
    df0 =df1[['V-ICV','V-ICT','V-MRV', 'V-B1V', 'V-B2V', 'V-B3V', 'V-B5V']]
    #df0=df0.drop(0)
    df0=df0.reset_index()
    df1=df1[['V-INV','V-INT','V-TCV','V-TCT','V-HCV']]
    df1=df1.reset_index()




def correlmap():
    global df1, df0
    c1=df1
    c0=df0


        
##    if len(a.columns)==8:
##        a=a.drop(['Unnamed: 0'],axis=1)
##    c2=[]
##    for i in range(len(c.index)):
##        c1=classifier.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
##        c1=c1.tolist()
##        c1=sum(c1,[])
##        c2.append(c1)
##    df2=pd.DataFrame(c2, columns =["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"])
    new=pd.concat([df1, df0], axis=1, join='inner')
    new=new.drop(['index'], axis = 1)
    fig, ax = plt.subplots(figsize=(6, 5))
    sb.heatmap(new.corr())
    plt.show()
    


def ploting4():

    global df1,df4,df0
    f=df1
    f0=df0

    f2=[]
    for i in range(len(f.index)):
        if var.get()==1:
            f1=classifier.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
        elif var.get()==2:
            f1=classifier2.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
            
        
            
        f1=f1.tolist()
        f1=sum(f1,[])
        f2.append(f1)
    df4=pd.DataFrame(f2, columns =["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"])
    new2=pd.concat([df1, df4],axis=1, join='inner')
    new2=new2.drop(['index'], axis = 1)

    
    

    


    
    

    lis1=["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"]

    if n1.get() in lis1:
        yvalue=new2[n1.get()]
        yvalue=np.asfarray(yvalue,float)

        yvalue1=f0[n1.get()]
        yvalue1=np.asfarray(yvalue1,float)

        fig, (ax1,ax2) = plt.subplots(2)
        time=np.arange(0,len(yvalue))

        ax1.plot(time,yvalue1,label='actual',linewidth=1,color='black')
                   
        ax1.set_ylabel('vibration (in/s)')
        ax1.legend(prop={'size':6})

        ax2.plot(time,yvalue,label='predicted',linewidth=1,color='blue')
        ax2.set_xlabel('time')
        ax2.set_ylabel('vibration (in/s)')
        ax2.set_ylim([f0[n1.get()].min(), f0[n1.get()].max()])
        ax2.legend(prop={'size':6})

        
        plt.show()

    else:
        yvalue=new2[n1.get()]
        yvalue=np.asfarray(yvalue,float)

        fig, (ax1) = plt.subplots(1)
        time=np.arange(0,len(yvalue))


        ax1.plot(time,yvalue,label='actual',linewidth=1,color='black')
        ax1.set_xlabel('time')
                   
        ax1.set_ylabel('vibration (in/s)')
        ax1.legend(prop={'size':6})
    

        
        plt.show()

        
        

    

    


  

def ploting5():



    global df1,df3
    e=df1
    e0=df0

    e2=[]
    for i in range(len(e.index)):

        if var.get()==1:
        
            e1=classifier.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
        elif var.get()==2:
            e1=classifier2.predict([[df1['V-INV'][i],df1['V-INT'][i],df1['V-TCV'][i],df1['V-TCT'][i],df1['V-HCV'][i]]])
            
        e1=e1.tolist()
        e1=sum(e1,[])
        e2.append(e1)
    df3=pd.DataFrame(e2, columns =["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"])
    new1=pd.concat([df1, df3],axis=1, join='inner')
    new1=new1.drop(['index'], axis = 1)
    
    

    val=new1[n1.get()].drop(0)
    val=val.to_numpy()
    val=np.asfarray(val,float)
    
    val1=e0[n1.get()].drop(0)
    val1=val1.to_numpy()
    val1=np.asfarray(val1,float)
    
    f1, t1, z1= signal.stft(val1,8823.5, nperseg=500)
    f, t, z= signal.stft(val,8823.5, nperseg=500)

    

    

    lis2=["V-ICV", "V-ICT","V-MRV","V-B1V","V-B2V","V-B3V","V-B5V"]
    if n1.get() in lis2:
    
    
        
        
        fig = plt.figure()
        #fig, (ax1) = plt.subplots(2,2,1)
        plt.subplot( 2,1,1)
       
        plt.pcolormesh(t1,f1,abs(z1), shading='gouraud')
        #plt.xlabel('time')
        plt.ylabel('frequency(Hz)')
        plt.title('actual')
        plt.colorbar()
       

        plt.subplot(2,1,2)
        plt.pcolormesh(t,f,abs(z), shading='gouraud')
        plt.xlabel('time')
        plt.ylabel('frequency(Hz)')
        plt.title('predicted')
        plt.colorbar()
        plt.show()

        

    else:
        

        fig, (ax) = plt.subplots(1)
       
        plt.pcolormesh(t,f,abs(z), shading='gouraud')
        plt.xlabel('time')
        plt.ylabel('frequency(Hz)')
        #plt.title(n1.get())
        plt.colorbar()
        plt.show()
        


    

    


tk02=ttk.Label(win, text='Predict and analyse virtual sensor data using your raw sensor data set'
                   ,foreground="blue")
tk02.place(x=0,y=10)

tk03=ttk.Label(win, text='Choose regression type to predict and plot'
                   ,foreground="red")
tk03.place(x=0,y=110)   


tk8=ttk.Label(win, text='File Path :')
tk8.place(x=0,y=40)
v1 = tk.StringVar()
entry2 = ttk.Entry(win, textvariable=v1)
entry2.place(x=60,y=40)
tk9=ttk.Button(win, text='Upload csv file',command=import_csv_data1)
tk9.place(x=200,y=40)

tk10=ttk.Button(win, text='Download prediction',command=download)
tk10.place(x=200,y=170)

tk11=ttk.Button(win, text='Show heatmap',command=correlmap)
tk11.place(x=200,y=70) 

tk12=ttk.Label(win, text = 'Select   :'
                        '\n' 'Sensor',
          font = ("Times New Roman", 10))

tk12.place(x=0,y=250)


# Combobox creation
n1 = tk.StringVar()
sensor = ttk.Combobox(win, width = 15, textvariable = n1)


# Adding combobox drop down list
sensor['values'] = ( 'V-INV','V-INT','V-ICV', 'V-ICT',
                       'V-TCV','V-TCT','V-MRV', 'V-B1V', 'V-B2V',
                                   'V-B3V', 'V-B5V','V-HCV')
  
sensor.place(x=60,y=250)
sensor.current()

tk13=ttk.Button(win, text='Plot time domain',command=ploting4)
tk13.place(x=200,y=250)

tk14=ttk.Button(win, text='Plot campbell diagram',command=ploting5)
tk14.place(x=200,y=290)











win.mainloop()

