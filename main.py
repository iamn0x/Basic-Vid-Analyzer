import tkinter as tk
from tkinter import ttk,messagebox
import views.realtimeanalysis as rta
import views.options as opt
import views.make as md
import views.analysis as ad
from modules.Settings import Settings
from modules.TempReader import TempReader
#temperaturePort = '/dev/ttyACM0'
from tendo import singleton
me = singleton.SingleInstance()

class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.framesList = []
        self.RTopened = False
        self.OPTopened = False
        self.MDopened = False
        self.ADopened = False
        self.settings = Settings.getInstance()
        #style = ttk.Style()
        #print('Style themes on my system are ', style.theme_names())
        #style.theme_use('xpnative')
        #style.configure('TButton', background='white', padding=5)

        container = tk.Frame(self)
        container.grid(row=0, column=0)

        self.realTimeButton = ttk.Button(container, text='real time analysis', state='disabled', command=self.showRealTime)
        self.realTimeButton.grid(row=0, column=0, sticky='NEWS')

        self.optionButton = ttk.Button(container, text='options', command=self.showOptions)
        self.optionButton.grid(row=1, column=0, sticky='NEWS')

        self.makeDataButton = ttk.Button(container, text='make data', state='disabled', command=self.showMake)
        self.makeDataButton.grid(row=2, column=0, sticky='NEWS')

        self.analyzeButton = ttk.Button(container, text='analyze data', command=self.showAnalysis)
        self.analyzeButton.grid(row=3, column=0, sticky='NEWS')

        self.portTestButton = ttk.Button(container, text='test port', state='disabled', command=self.testPort)
        self.portTestButton.grid(row=4, column=0, sticky='NEWS')

    def testPort(self):
        if TempReader.testPort(self, self.settings.portName):
            self.portTestButton.config(text="It's okay")
        else:
            self.portTestButton.config(text="It's wrong")

    def showRealTime(self):
        #realtimeanalysis.show(self.childframes)
        if not self.RTopened:
            self.RTopened = True
            self.RTroot = tk.Tk()
            self.framesList.append(self.RTroot)
            #root.resizable(False, False)
            self.RTroot.title("Basic Video Analyzer")
            self.RTroot.configure()
            self.RTmain = rta.RealTimeAnalysis(self.RTroot)
            self.RTmain.pack()
            self.RTroot.protocol("WM_DELETE_WINDOW", self.RTon_closing)
            self.RTroot.mainloop()            
        else:
            return
    def RTon_closing(self):
        self.RTopened = False
        self.framesList.remove(self.RTroot)
        self.RTroot.destroy()
    
    def showOptions(self):
        self.portTestButton.config(state='normal')
        self.makeDataButton.config(state='normal')
        self.realTimeButton.config(state='normal')
        if not self.OPTopened:
            self.OPTopened = True
            self.OPTroot = tk.Tk()
            self.framesList.append(self.OPTroot)
            #self.OPTroot.resizable(False, False)
            self.OPTroot.title("Basic Video Analyzer - Options")
            self.OPTmain = opt.Options(self.OPTroot)
            self.OPTmain.pack()
            self.OPTroot.protocol("WM_DELETE_WINDOW", self.OPTon_closing)
            self.OPTmain.portLabel.config(text=str(self.settings.portName))
            self.OPTmain.mainloop()

        else:
            return
    def OPTon_closing(self):
        try: 
            del self.OPTmain.camera
        except:
            print("Problem z del")
            pass
        print(self.settings.portName)
        self.portTestButton.config(text='test port {}'.format(self.settings.portName))
        self.OPTopened = False
        self.framesList.remove(self.OPTroot)
        self.OPTroot.destroy()


    def showMake(self):
        if not self.MDopened:
            self.MDopened = True
            self.MDroot = tk.Tk()
            self.framesList.append(self.MDroot)
            self.MDroot.resizable(False, False)
            self.MDroot.title("Basic Video Analyzer - Make Data")
            self.MDmain = md.Make(self.MDroot)
            self.MDmain.pack()
            self.MDroot.protocol("WM_DELETE_WINDOW", self.MDon_closing)
            self.MDroot.mainloop()
        else:
            return
    def MDon_closing(self):
        try:
            del self.MDmain.camera
        except:
            print("Problem z del")
            pass
        self.MDopened = False
        self.framesList.remove(self.MDroot)
        self.MDroot.destroy()


    def showAnalysis(self):
        if not self.ADopened:
            self.ADopened = True
            self.ADroot = tk.Tk()
            self.framesList.append(self.ADroot)
            self.ADroot.resizable(False, False)
            self.ADroot.title("Basic Video Analyzer - Analyze Data")
            self.ADmain = ad.Analysis(self.ADroot)
            self.ADmain.pack()
            self.ADroot.protocol("WM_DELETE_WINDOW", self.ADon_closing)
        else:
            return
    def ADon_closing(self):
        self.ADopened = False
        self.framesList.remove(self.ADroot)
        self.ADroot.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Basic Video Analyzer")
    main = MainWindow(root)
    main.pack()
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to Quit?"):
            for i in main.framesList:
                i.destroy()
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
