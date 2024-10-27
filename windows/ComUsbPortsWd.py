import tkinter as tk
import serial
import esptool
import io
import sys
from tkinter import ttk, messagebox
from customtkinter import CTkScrollableFrame
from time import sleep

class ComUsbPortsWd:

    baud_rates: tuple = [
        110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600,
        115200, 128000, 256000, 512000, 1000000, 2000000, 4000000
    ]

    sel_baud_rate: int = 9600

    def __init__(self, root) -> None:
        self.def_baudrate = self.sel_baud_rate

        self.root = root

    def port_info_window(self, port_data):
        # Add port data to current obj
        self.port_name = port_data['port']
        self.port_desc = port_data['desc']
        self.port_hwid = port_data['hwid']

        # Define window
        self.portinfo_wd = tk.Toplevel(self.root)
        self.portinfo_wd.title(f'Porta {self.port_name}')
        self.portinfo_wd.geometry('720x600')

        # Add scrollable frame
        self.frame = CTkScrollableFrame(
            self.portinfo_wd,
            orientation='vertical'
        )
        self.frame.pack(side='top', fill='both', expand=True)

        # Info port title
        tk.Label(self.frame, text=f'Informazioni porta {self.port_name}', font=('Arial', 12, 'bold'), justify='left').grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Port name
        tk.Label(self.frame, text='Nome porta:', font=('Arial', 10, 'bold'), justify='left').grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        tk.Label(self.frame, text=self.port_name, font=('Arial', 10), justify='left').grid(row=1, column=1, padx=10, pady=5, sticky="nw") 

        # Port description
        tk.Label(self.frame, text='Descrizione porta:', font=('Arial', 10, 'bold'), justify='left').grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        tk.Label(self.frame, text=self.port_desc, font=('Arial', 10), justify='left').grid(row=2, column=1, padx=10, pady=5, sticky="nw") 

        # Port HWID
        tk.Label(self.frame, text='HWID (Identificatore porta):', font=('Arial', 10, 'bold'), justify='left').grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        tk.Label(self.frame, text=f'{self.port_hwid}', font=('Arial', 10), wraplength=400, justify='left').grid(row=3, column=1, padx=10, pady=5, sticky="nw") 

        # Test port connection title
        tk.Label(self.frame, text=f'Esegui test connessione porta {self.port_name}', font=('Arial', 12, 'bold'), justify='left').grid(row=4, column=0, padx=10, pady=10, sticky='nw')

        # Test section frame
        self.port_test_frame = tk.Frame(self.frame)
        self.port_test_frame.grid(row=5, column=0, sticky='nw', padx=10, pady=10)

        # Baud rates
        tk.Label(self.port_test_frame, text="Baud rate", font=('Arial', 10), justify='left').grid(row=0, column=0, sticky='nw', pady=0, padx=[0, 20])

        self.baudrates_combo_box = ttk.Combobox(self.port_test_frame, values=self.baud_rates)
        self.baudrates_combo_box.grid(row=0, column=1, sticky='nw', pady=0)
        self.baudrates_combo_box.set(self.def_baudrate)
        self.baudrates_combo_box.bind("<<ComboboxSelected>>", self.on_baudrate_select)

        # Buttons to init connection tests. One is made via Serial library, the other with esptool library
        # Init connection test with Serial library
        tk.Button(
            self.port_test_frame, 
            text='Avvia test di connessione con libreria Serial', 
            font=('Arial', 10), 
            command=self.serial_test_com_port,
            justify='left'
        ).grid(row=1, column=0, sticky='nw', pady=[40, 0])

        # Init connection test with esptool library
        tk.Button(
            self.port_test_frame, 
            text='Avvia test di connessione con ESPTOOL', 
            font=('Arial', 10), 
            command=self.esptool_test_com_port,
            justify='left'
        ).grid(row=2, column=0, sticky='nw', pady=[20, 0])

        # Testing log
        self.test_log_frame = tk.Frame(self.frame)
        self.test_log_frame.grid(row=6, column=0, sticky='nw', padx=10, pady=10)

        tk.Label(self.test_log_frame, text="Log del test", font=('Arial', 12, 'bold'), justify='left').grid(row=0, column=0, sticky='nw', pady=0, padx=0)

        self.test_log = tk.Label(self.test_log_frame, text='Avvia un test (Serial o Esptool) per visualizzare i risultati di log in questo box', font=('Arial', 10), wraplength=400, justify='left')
        self.test_log.grid(row=1, column=0, sticky='e', padx=0, pady=0)

    def serial_test_com_port(self):
        '''
        Test the COM port using the Serial library
        '''
        self.test_log.config(text='0 - Test della porta in corso usando la libreria Python Serial...\n')
        self.test_log.config(text=f'{self.test_log.cget('text')}\n1 - Caricamento in corso...\n')
        sleep(1.5)
        self.test_log.config(text=f'{self.test_log.cget('text')}\n2 - Baud rate selezionato: {self.sel_baud_rate}\n')

        try:
            # Open the COM port
            ser = serial.Serial(port=self.port_name, baudrate=int(self.sel_baud_rate), timeout=5)

            if ser.is_open:
                self.test_log.config(
                    text=f'{self.test_log.cget('text')}\n3 - La porta {self.port_name} è aperta e sta funzionando!\n'
                )
                print(f"{self.port_name} è aperta e sta funzionando!")
            
                # Optionally, write or read some data to test
                ser.write(b'Test data\n')
                data = ser.readline().decode('utf-8').strip()

                self.test_log.config(text=f'{self.test_log.cget('text')}\n4 - Dati ricevuti: {data}\n', sticky='nw')

                print(f"Dati ricevuti: {data}")
                
                # Close the port after testing
                ser.close()
            else:
                self.test_log.config(text=f'{self.test_log.cget('text')}\n3 - Impossibile aprire la porta: {self.port_name}')
                print(f"Impossibile aprire la porta: {self.port_name}")

        except Exception as e:
            error = f'\n3 - Si è verificato un errore durante il testing della porta: {self.port_name} - {e}\n'

            self.test_log.config(text= f'{self.test_log.cget('text')}{error}')

            messagebox.showerror('Si è verificato un errore', error)

            print(f"Si è verificato un errore durante il testing della porta: {self.port_name} - {e}")

    def esptool_test_com_port(self):
        '''
        Test the COM port using the esptool library
        '''
        self.test_log.config(text='0 - Test della porta in corso usando la libreria Python ESPTOOL...\n')
        self.test_log.config(text=f'{self.test_log.cget('text')}\n1 - Caricamento in corso...\n')
        sleep(1.5)
        self.test_log.config(text=f'{self.test_log.cget('text')}\n2 - Baud rate selezionato: {self.sel_baud_rate}\n')

        try:
            # Test the COM port using the esptool library
            esptool_log = self.init_esptool_log()
        
            self.test_log.config(
                text=f'{self.test_log.cget('text')}\n3 - La porta {self.port_name} è aperta e sta funzionando!\n\n4 - ESPTOOL log completo:\n{esptool_log}\n'
            )

        except Exception as e:
            error = f'\n3 - Si è verificato un errore durante il testing della porta: {self.port_name} - {e}'

            self.test_log.config(text=f'{self.test_log.cget('text')}{error}')

            messagebox.showerror('Si è verificato un errore', error)

            print(f"Si è verificato un errore durante il testing della porta: {self.port_name} - {e}")

    def init_esptool_log(self) -> str:
        '''
        Get the log from the esptool library
        '''
        cap_output = io.StringIO()
        sys.stdout = cap_output

        try:
            esptool.main([
                '--port', self.port_name,
                'flash_id'
            ])

            log = cap_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        return str(log)

    def on_baudrate_select(self, e):
        '''
        Event to select the baudrate from the combobox
        '''
        self.sel_baud_rate = self.baudrates_combo_box.get()