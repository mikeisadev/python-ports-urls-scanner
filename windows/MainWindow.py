import tkinter as tk
from tkinter import ttk, messagebox
from customtkinter import CTkScrollableFrame

from windows.PcInfoWd import PcInfoWd
from windows.ComUsbPortsWd import ComUsbPortsWd
from windows.ScanUrlIPWd import ScanUrlIPWd

import serial.tools.list_ports
from utils.path import icons_dir
import serial.tools
import usb.core, usb.util
from bleak import BleakScanner
import asyncio
import threading
import psutil

class MainWindow:

    '''
    Main data storage of the index of the window.
    '''
    ports_data: dict = {
        'com_usb_ports': [],
        'bluetooth_connections': [],
        'lan_ports': []
    }

    '''
    Init
    '''
    def __init__(self) -> None:
        # main settings
        self.root = tk.Tk()

        # main window title
        self.root.title('Local and Network Ports Scanner - by Michele Mincone')

        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth() - 200
        self.screen_height = self.root.winfo_screenheight() - 200

        # set main window geometry
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        # Import other windows
        self.pcinfo_wd = PcInfoWd(self.root)
        self.comusbport_wd = ComUsbPortsWd(self.root)
        self.scan_urlip_wd = ScanUrlIPWd(self.root)

        # create a scrollable environment for the body
        self.body_scrollframe = CTkScrollableFrame(
            self.root,
            orientation='vertical'
        )

        # create a scrollable environment for the header
        self.header_scrollframe = CTkScrollableFrame(
            self.root,
            orientation='horizontal',
            height= 45
        )

        # Build the overall UI
        # Build Header UI
        self.header_scrollframe.pack(side="top", fill="x", anchor="nw", expand=False)
        self.ui_header()

        # Build Body UI
        self.body_scrollframe.pack(side="top", fill="both", anchor="nw", expand=True)
        self.ui_body()

    '''
    UI Builders
    '''

    def ui_header(self): 
        '''
        Build the UI of the header of the application.
        '''

        self.scanner_image = tk.PhotoImage(file=f'{icons_dir()}\\scanner.png', width=32, height=32)
        self.bluetooth_image = tk.PhotoImage(file=f'{icons_dir()}\\bluetooth.png', width=32, height=32)
        self.lan_image = tk.PhotoImage(file=f'{icons_dir()}\\lan.png', width=32, height=32)
        self.pcinfo_image = tk.PhotoImage(file=f'{icons_dir()}\\info.png', width=32, height=32)
        self.urlipscan_image = tk.PhotoImage(file=f'{icons_dir()}\\urlipscan.png', width=32, height=32)

        self.header_grid = tk.Frame(self.header_scrollframe)
        self.header_grid.pack(padx=0, pady=0, expand=False, fill='x', side='top', anchor='nw')

        self.scan_ports_btn = tk.Button(self.header_grid, text="Scansiona porte", font=('Arial', 10), command=self.scan_com_usb_ports, image=self.scanner_image, compound=tk.LEFT, cursor='hand2', padx=10)

        self.scan_bluetooth_btn = tk.Button(self.header_grid, text="Scansiona bluetooth", font=('Arial', 10), command=self.await_bluetooth_devices_scanning, image=self.bluetooth_image, compound=tk.LEFT, cursor='hand2', padx=10)

        self.scan_lan_btn = tk.Button(self.header_grid, text="Scansiona porte LAN", font=('Arial', 10), command=self.scan_lan_ports, image=self.lan_image, compound=tk.LEFT,cursor='hand2', padx=10)

        self.pcinfo_btn = tk.Button(self.header_grid, text="Info PC", font=('Arial', 10), command=self.pcinfo_wd.pc_info_window, image=self.pcinfo_image, compound=tk.LEFT, cursor='hand2', padx=10)

        self.urlipscan_btn = tk.Button(self.header_grid, text="Scansiona URL/IP", font=('Arial', 10), command=self.scan_urlip_wd.scan_urlip_window, image=self.urlipscan_image, compound=tk.LEFT, cursor='hand2', padx=10)

        self.scan_ports_btn.grid(row=0, column= 0, padx=0)
        self.scan_ports_btn.grid(row=0, column=1, padx=0)
        self.scan_bluetooth_btn.grid(row=0, column=2, padx=0)
        self.scan_lan_btn.grid(row=0, column=3, padx=0)
        self.pcinfo_btn.grid(row=0, column=4, padx=0)
        self.urlipscan_btn.grid(row=0, column=5, padx=0)

    def ui_body(self) -> None:
        '''
        Build the interface of the body of the application.
        '''

        '''
        List of scanned ports
        '''
        self.ports_label = tk.Label(self.body_scrollframe, text="Porte scansionate:", font=('Arial', 10))
        self.ports_label.pack(side='top', fill='y', anchor='w')

        self.ports_table = ttk.Treeview(
            self.body_scrollframe, 
            columns=("port", "desc", "hwid"), 
            show='headings', 
            height=8
        )
        self.ports_table.pack(side='top', fill='x')

        self.ports_table.heading("port", text="Porta", anchor='w')
        self.ports_table.heading("desc", text="Descrizione", anchor='w')
        self.ports_table.heading("hwid", text="HWID (identification hardware)", anchor='w')

        self.ports_table.column("port", anchor='w')
        self.ports_table.column("desc", anchor='w')
        self.ports_table.column("hwid", anchor='w')

        for row in self.ports_data['com_usb_ports']:
            self.ports_table.insert('', tk.END, values=row)

        self.ports_table.pack(pady=10)

        self.ports_table.bind('<Double-1>', func=self.usb_port_table_row_click)

        '''
        List of bluetooth connections (bluetooth devices)
        '''
        self.bluetooth_label = tk.Label(self.body_scrollframe, text="Dispositivi bluetooth:", font=('Arial', 10))
        self.bluetooth_label.pack(side='top', fill='y', anchor='w')

        self.bluetooth_table = ttk.Treeview(
            self.body_scrollframe, 
            columns=("device_name", "device_address"), 
            show='headings', 
            height=8
        )
        self.bluetooth_table.pack(side='top', fill='x')

        self.bluetooth_table.heading("device_name", text="Nome dispositivo", anchor='w')
        self.bluetooth_table.heading("device_address", text="Indirizzo MAC dispositivo", anchor='w')

        self.bluetooth_table.column("device_name", anchor='w')
        self.bluetooth_table.column("device_address", anchor='w')

        for row in self.ports_data['bluetooth_connections']:
            self.bluetooth_table.insert('', tk.END, values=row)

        self.bluetooth_table.pack(pady=10)

        '''
        List of LAN and ETHERNET ports
        '''
        self.laneth_label = tk.Label(self.body_scrollframe, text="Connessioni LAN e porte Ethernet:", font=('Arial', 10))
        self.laneth_label.pack(side='top', fill='y', anchor='w')

        self.lan_table = ttk.Treeview(
            self.body_scrollframe, 
            columns=("interface_name", "interface_address"), 
            show='headings', 
            height=8
        )
        self.lan_table.pack(side='top', fill='x')

        self.lan_table.heading("interface_name", text="Nome interfaccia", anchor='w')
        self.lan_table.heading("interface_address", text="Indirizzo MAC interfaccia", anchor='w')

        self.lan_table.column("interface_name", anchor='w')
        self.lan_table.column("interface_address", anchor='w')

        for row in self.ports_data['bluetooth_connections']:
            self.lan_table.insert('', tk.END, values=row)

        self.lan_table.pack(pady=10)

        '''
        Credits text
        '''
        self.credits_label = tk.Label(self.body_scrollframe, text="Software realizzato da Michele Mincone (tkinter/python) - Started to develop on 30 September 2024 - https://michelemincone.com - Made in Italy", font=('Arial', 8))
        self.credits_label.pack(side='top', fill='y', anchor='w')

    '''
    Main functions
    '''

    def scan_com_usb_ports(self):
        '''
        Scam COM and USB ports.
        '''

        # Find COM ports
        comPorts = serial.tools.list_ports.comports()
        devices = list(usb.core.find(find_all=True))

        # Print COM ports and USB devices FOR DEBUGGING
        # print(comPorts)
        # print(devices)

        # No COM PORTS found? Show a warning
        if not comPorts:
            print("No USB devices found.")

            messagebox.showwarning('Nessun dispositivo USB rilevato', 'Nessun dispositivo USB rilevato!\n\nNota generale: può capitare che se si ha la rilevazione dei dispositivi bluetooth disattivata, il programma non riesce a rilevare dispositivi USB. Quindi prova ad attivare la rilevazione dei dispositivi bluetooth sul tuo computer e ritenta per l\'ultima volta.')

        # USB DEVICES test (only terminal log for now)
        for device in devices:
            print(f"USB Device: ID {hex(device.idVendor)}:{hex(device.idProduct)}")

        # Clean COM USB ports data
        self.ports_data['com_usb_ports'] = []

        # Clean table
        for item in self.ports_table.get_children():
            self.ports_table.delete(item)

        # Re-add data
        for port, desc, hwid in sorted(comPorts):
            self.ports_data['com_usb_ports'].append([port, desc, hwid])

        # Populate the table.
        for row in self.ports_data['com_usb_ports']:
            self.ports_table.insert('', tk.END, values=row)

        # print(self.ports_data)

    def await_bluetooth_devices_scanning(self):
        '''
        Add a threading process to scan bluetooth devices.
        '''

        thread = threading.Thread(
            target=lambda: asyncio.run(self.scan_bluetooth_devices())
        )
        thread.start()

    async def scan_bluetooth_devices(self):
        '''
        Asynchronously scan bluetooth devices
        '''

        print("Scanning for Bluetooth devices...")

        # Clean Bluetooth connections data
        self.ports_data['bluetooth_connections'] = []

        # Clean bluetooth connections table
        for item in self.bluetooth_table.get_children():
            self.bluetooth_table.delete(item)
    
        # Scan for bluetooth devices
        try:
            devices = await BleakScanner.discover()
    
            devices = None
            # Verify if there are bluetooth devices
            if devices:

                # Add bluetooth devices to data
                for device in devices:
                    self.ports_data['bluetooth_connections'].append([device.name, device.address])

                    print(device)

                # Populate the table
                for row in self.ports_data['bluetooth_connections']:
                    self.bluetooth_table.insert('', tk.END, values=row)
            else:
                messagebox.showwarning('Nessun dispositivo Bluetooth trovato', 'Nessun dispositivo Bluetooth trovato attorno a te!')

        except Exception as e:
            messagebox.showerror('Errore scansione dispositivi Bluetooth',f'Si è verificato un errore durante la scansione dei dispositi Bluetooth. Potresti avere la funzionalità "Bluetooth" disabilitata sul tuo PC, prova ad attivarla e a effettuare di nuovo la scansione.\n\nCodice errore: {e}')

    def scan_lan_ports(self):
        '''
        Scan LAN ports and networking interface
        '''

        self.ports_data['lan_ports'] = []

        for item in self.lan_table.get_children():
            self.lan_table.delete(item)

        addrs = psutil.net_if_addrs()

        # populate data
        for interface, addr in addrs.items():
            self.ports_data['lan_ports'].append([interface, addr[0].address])
            #print(f"Interface: {interface} -")

        # rebuild table
        for row in self.ports_data['lan_ports']:
            self.lan_table.insert('', tk.END, values=row)

        for a in addr:
            print(f"  {a.family.name}: {a.address}")

        if not addrs:
            print("No network interfaces found.")

    '''
    Managing events
    '''

    def usb_port_table_row_click(self, event):
        '''
        Handle usb / com ports row double click
        '''

        selected_item = self.ports_table.selection()

        if selected_item:
            row = self.ports_table.item(selected_item)

            # destructure the row
            port, desc, hwid = row['values']

            port_info = {
                'port': port,
                'desc': desc,
                'hwid': hwid
            }

            # show port details
            self.comusbport_wd.port_info_window(port_info)
