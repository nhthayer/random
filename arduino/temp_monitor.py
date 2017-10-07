import serial
import time

class temperature_controller:
    def __init__(self, which_port, verbose=True):
        self.port = serial.Serial(which_port, baudrate=115200)
        self.verbose = verbose
        self.port.readline() # Blocks until start message is written
        self.temp = None
        self.mash_start_time = None
        self.boil_start_time = None
        self.sensors = {'HLT': 0, 'Mash': 1, 'Boil': 2}

    def get_temperature(self, which_sensor):
        if which_sensor not in self.sensors:
            raise UserWarning(f'{which_sensor} not in named sensors')
        sensor_index = self.sensors[which_sensor]
        if self.verbose:
            print(f'-> {sensor_index}')
        self.port.write(bytes('%s' % sensor_index, 'ascii'))
        reading = float(
            self.port.readline().decode('ascii').strip().split('=')[1])
        setattr(self, f'{which_sensor}_temp', reading)
        return reading

    def get_temperature_by_index(self, which_index):
        self.port.write(bytes('%s' % which_index, 'ascii'))
        reading = float(
            self.port.readline().decode('ascii').strip().split('=')[1])
        setattr(self, f'{which_index}_temp', reading)
        return reading

    def set_desired_temperature(self, which_sensor, desired_temp):
        setattr(self, f'{which_sensor}_setpoint', float(desired_temp))

    def close(self):
        self.port.close()

if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
    
    import tkinter as Tk
    import time

    ## Create tk root object
    root = Tk.Tk()
    
    ## Create plot fig, axis
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8), dpi=100)


    ## create tk.Drawing area
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    
    def _quit():
        root.quit()     # stops mainloop
        root.destroy()


    def update_temp():
        global hlt_temps, mash_temps, boil_temps
        print('Updating plot...')
        if len(hlt_temps)==0:
            hlt_temps = [(time.time(), sensor.get_temperature('HLT'))]*5
            mash_temps = [(time.time(), sensor.get_temperature('Mash'))]*5
            boil_temps = [(time.time(), sensor.get_temperature('Boil'))]*5
        hlt_current_temp = (time.time(), sensor.get_temperature('HLT'))
        mash_current_temp = (time.time(), sensor.get_temperature('Mash'))
        boil_current_temp = (time.time(), sensor.get_temperature('Boil'))
        hlt_temps.append(hlt_current_temp)
        mash_temps.append(mash_current_temp)
        boil_temps.append(boil_current_temp)

        ax[0, 0].cla()
        ax[0, 1].cla()
        ax[1, 0].cla()

        ax[0, 0].set_xlim(0, 120)
        ax[0, 1].set_xlim(0, 120)
        ax[1, 0].set_xlim(0, 120)

        ax[0, 0].set_xticks([])
        ax[0, 1].set_xticks([])
        ax[1, 0].set_xticks([])
        
        ax[0, 0].plot([i[1] for i in hlt_temps[-100:]])
        ax[0, 1].plot([i[1] for i in mash_temps[-100:]])
        ax[1, 0].plot([i[1] for i in boil_temps[-100:]])
        
        tmp_slope1 = (60*(hlt_temps[-1][1]-hlt_temps[-4][1])/
            (hlt_temps[-1][0]-hlt_temps[-4][0]))
        tmp_slope2 = (60*(mash_temps[-1][1]-mash_temps[-4][1])/
            (mash_temps[-1][0]-mash_temps[-4][0]))
        tmp_slope3 = (60*(boil_temps[-1][1]-boil_temps[-4][1])/
            (boil_temps[-1][0]-boil_temps[-4][0]))
        
        ax[0, 0].set_title('HLT %.2f C (%.2f F) ∆/T %.2f C/min'\
                % (hlt_temps[-1][1], (hlt_temps[-1][1]*9/5+32), tmp_slope1))
        ax[0, 1].set_title('Mash %.2f C (%.2f F) ∆/T %.2f C/min'\
                % (mash_temps[-1][1], (mash_temps[-1][1]*9/5+32), tmp_slope2))
        ax[1, 0].set_title('Boil %.2f C (%.2f F) ∆/T %.2f C/min'\
                % (boil_temps[-1][1], (boil_temps[-1][1]*9/5+32), tmp_slope3)) 
        canvas.show()
        root.after(10, update_temp)

    button = Tk.Button(master=root, text='Quit', command=_quit)
    button.pack(side=Tk.BOTTOM)

    sensor = temperature_controller('/dev/cu.usbmodem1411', verbose=False)
    hlt_temps = []
    mash_temps = []
    boil_temps = []

    root.after(10, update_temp)
    Tk.mainloop()
    sensor.close()
