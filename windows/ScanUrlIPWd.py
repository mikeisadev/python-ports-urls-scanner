import tkinter as tk
import socket
import threading
from datetime import datetime
from tkinter import ttk, messagebox
from customtkinter import CTkScrollableFrame
from time import sleep
from utils.url import remove_protocol_url, is_str_url_hname, is_str_ipv4, is_str_ipv6, resolve_hostname_ip

class ScanUrlIPWd:

    # The thread for the scanning process
    scanning_thread: threading.Thread = None
    
    # The entry to search for.
    host: str = ''

    # IPv4 and IPv6
    IPv4: str = None
    IPv6: str = None

    # Start and end port for scanning
    start_port: int = 18
    end_port: int = 443

    # Scan start and end time
    scan_start_time: datetime = None
    scan_end_time: datetime = None
    scan_total_time: datetime = None

    # Scanning progress bar
    scanning_progress_bar: ttk.Progressbar = None

    # Scanning progress labels
    scan_detail__progress: tk.Label = None

    # General scanning data
    opened_ports: int = 0
    closed_ports: int = 0
    port_errors: int = 0
    
    def __init__(self, root):
        self.root = root

    def scan_urlip_window(self):
        # Define window
        self.scanurlip_wd = tk.Toplevel(self.root)
        self.scanurlip_wd.title('Scansione URL/IP')
        self.scanurlip_wd.geometry('720x600')

        # Add main scrollable frame
        self.frame = CTkScrollableFrame(
            self.scanurlip_wd,
            orientation='vertical'
        )
        self.frame.pack(expand=True, side='left', fill='both', padx=0, pady=0)

        # Header frame
        self.header_frame = tk.Frame(self.frame)
        self.header_frame.pack(expand=True, side='top', fill='x', padx=0, pady=0)

        # Body frame
        self.body_frame = tk.Frame(self.frame)
        self.body_frame.pack(expand=True, side='bottom', fill='x', padx=0, pady=[10, 0])

        # Generate header and body
        self.generate_header()
        self.generate_body()

    def generate_header(self):
        '''
        Generate header
        '''

        # Header title
        tk.Label(
            self.header_frame, 
            text='Strumento di scansione delle porte di URL / Indirizzi IP', 
            font=('Arial', 12, 'bold'), 
            justify='center'
        ).pack(expand=False, side='top', fill='x', padx=0, pady=[0, 15])

        # Header wrap
        searchbox_wrap_frame = tk.Frame(self.header_frame)
        searchbox_wrap_frame.pack(expand=False, side='top', fill='x', padx=5, pady=5)

        tk.Label(
            searchbox_wrap_frame, 
            text='Inserisci URL/IP da scansionare:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).pack(expand=True, side='top', fill='none', anchor='w', padx=0, pady=[0, 5])

        # Search box frame
        searchbox_frame = tk.Frame(searchbox_wrap_frame)
        searchbox_frame.pack(expand=True, side='top', fill='both', anchor='nw', padx=0, pady=0)

        self.urlip_entry = tk.Entry(searchbox_frame, font=('Arial', 10))
        self.scan_button = tk.Button(
            searchbox_frame, 
            text='Scansiona', 
            font=('Arial', 10),
            command=self.start_scanning,
            cursor='hand2'
        )

        self.urlip_entry.pack(side='left', fill='x', expand=True, padx=0, pady=0)
        self.scan_button.pack(side='right', fill='x', expand=False, padx=[10, 0], pady=0)

        # Config fields network scan search frame
        tk.Label(
            searchbox_wrap_frame, 
            text='Opzioni per configurare la scansione:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).pack(expand=True, side='top', fill='none', anchor='w', padx=0, pady=[10, 5])

        config_scan_frame = tk.Frame(searchbox_wrap_frame)
        config_scan_frame.pack(expand=True, side='top', fill='x', anchor='nw', padx=0, pady=0)

        # Config fields
        # Start port
        tk.Label(
            config_scan_frame, 
            text='Porta iniziale:', 
            font=('Arial', 10), 
            justify='left'
        ).pack(expand=True, side='left', fill='none', anchor='w', padx=0, pady=0)

        self.scan_start_port_field = tk.Entry(config_scan_frame, font=('Arial', 10))
        self.scan_start_port_field.pack(side='left', fill='x', expand=True, padx=[5, 10], pady=0)

        # End port
        tk.Label(
            config_scan_frame, 
            text='Porta iniziale:', 
            font=('Arial', 10), 
            justify='left'
        ).pack(expand=True, side='left', fill='none', anchor='w', padx=0, pady=0)

        self.scan_end_port_field = tk.Entry(config_scan_frame, font=('Arial', 10))
        self.scan_end_port_field.pack(side='left', fill='x', expand=True, padx=[5, 0], pady=0)

        # default values
        self.scan_start_port_field.insert(0, self.start_port)
        self.scan_end_port_field.insert(0, self.end_port)

        '''
        Scanning progress box area.

        Add the box but do not show it.

        Add pack after while scanning. (start_scanning method)
        '''
        self.scanning_progress_box = tk.Frame(self.header_frame)
        self.generate_progress_box()

    def generate_progress_box(self):
        '''
        Generate progress box
        '''

        ttk.Separator(self.scanning_progress_box, orient='horizontal').pack(fill='x', pady=5)

        # Generate new progress box
        tk.Label(
            self.scanning_progress_box, 
            text='Scansione in corso...', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).pack(expand=True, side='top', fill='none', anchor='w', padx=0, pady=[0, 5])

        self.scanning_progress_bar = ttk.Progressbar(
            self.scanning_progress_box, 
            orient='horizontal', 
            length=200, 
            mode='determinate'
        )
        self.scanning_progress_bar.pack(expand=True, side='top', fill='x', padx=0, pady=0)
        self.scanning_progress_bar['value'] = 0

        '''
        Scanning progress details
        '''
        self.scanning_progress_details = tk.Frame(self.scanning_progress_box)
        self.scanning_progress_details.pack(expand=True, side='top', fill='x', padx=0, pady=[5, 0])

        # IP / Hostname
        tk.Label(
            self.scanning_progress_details, 
            text='IP:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=0, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__hostname = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__hostname.grid(row=0, column=1, sticky='w', padx=5, pady=0)

        # Start port
        tk.Label(
            self.scanning_progress_details, 
            text='Porta iniziale:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=1, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__start_port = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__start_port.grid(row=1, column=1, sticky='w', padx=5, pady=0)

        # End port
        tk.Label(
            self.scanning_progress_details, 
            text='Porta finale:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=2, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__end_port = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__end_port.grid(row=2, column=1, sticky='w', padx=5, pady=0)

        # Start time
        tk.Label(
            self.scanning_progress_details, 
            text='Inizio scansione:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=3, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__start_time = tk.Label(
            self.scanning_progress_details, 
            text='',
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__start_time.grid(row=3, column=1, sticky='w', padx=5, pady=0)

        # Scan end time
        tk.Label(
            self.scanning_progress_details, 
            text='Fine scansione:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=4, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__end_time = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__end_time.grid(row=4, column=1, sticky='w', padx=5, pady=0)

        # Elapsed time
        tk.Label(
            self.scanning_progress_details, 
            text='Tempo trascorso:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=5, column=0, sticky='w', padx=0, pady=0)

        self.scan_detail__elapsed_time = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__elapsed_time.grid(row=5, column=1, sticky='w', padx=5, pady=0)

        # Progress percentage
        tk.Label(
            self.scanning_progress_details, 
            text='Progresso:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=0, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__progress = tk.Label(
            self.scanning_progress_details, 
            text='0 %', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__progress.grid(row=0, column=3, sticky='w', padx=5, pady=0)

        # Current port
        tk.Label(
            self.scanning_progress_details, 
            text='Porta corrente:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=1, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__current_port = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__current_port.grid(row=1, column=3, sticky='w', padx=5, pady=0)

        # Remaining ports
        tk.Label(
            self.scanning_progress_details, 
            text='Porte rimanenti:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=2, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__remaining_ports = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__remaining_ports.grid(row=2, column=3, sticky='w', padx=5, pady=0)

        # Opened ports
        tk.Label(
            self.scanning_progress_details, 
            text='Porte aperte:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=3, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__opened_ports = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__opened_ports.grid(row=3, column=3, sticky='w', padx=5, pady=0)

        # Closed ports
        tk.Label(
            self.scanning_progress_details, 
            text='Porte chiuse:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=4, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__closed_ports = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__closed_ports.grid(row=4, column=3, sticky='w', padx=5, pady=0)

        # Ports with errors
        tk.Label(
            self.scanning_progress_details, 
            text='Porte con errori:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).grid(row=5, column=2, sticky='w', padx=0, pady=0)

        self.scan_detail__port_errors = tk.Label(
            self.scanning_progress_details, 
            text='', 
            font=('Arial', 10), 
            justify='left'
        )
        self.scan_detail__port_errors.grid(row=5, column=3, sticky='w', padx=5, pady=0)

    def generate_body(self):
        '''
        Generate body
        '''
        tk.Label(
            self.body_frame, 
            text='Risultati di scansione:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).pack(expand=True, side='top', fill='none', anchor='w', padx=0, pady=[0, 10])

        self.scan_results_table = ttk.Treeview(
            self.body_frame, 
            columns=('Porta', 'Stato', 'Servizio'), 
            show='headings'
        )
        self.scan_results_table.pack(expand=True, side='top', fill='both', anchor='nw', padx=0, pady=0)

        self.scan_results_table.heading('Porta', text='Porta', anchor='w')
        self.scan_results_table.heading('Stato', text='Stato', anchor='w')
        self.scan_results_table.heading('Servizio', text='Servizio', anchor='w')

        self.scan_results_table.column('Porta', width=100, anchor='w')
        self.scan_results_table.column('Stato', width=100, anchor='w')
        self.scan_results_table.column('Servizio', width=100, anchor='w')

    def start_scanning(self):
        '''
        Scan URL/IP and fill the table with results
        '''
        url_entry: str = str(self.urlip_entry.get().strip())

        self.start_port: int = int(self.scan_start_port_field.get())
        self.end_port: int = int(self.scan_end_port_field.get())

        # Validate IP address
        if url_entry == '':
            messagebox.showerror('Errore', 'Inserire un URL/IP')

            self.scanurlip_wd.lift()

            return
        
        # Validate start port
        if self.start_port < 0 or self.start_port > 65535:
            messagebox.showerror('Errore', 'Inserire una porta di inizio valida.\n\nLa porta di inizio deve essere compresa tra 0 e 65535.')

            self.scanurlip_wd.lift()

            return
        
        # Validate end port
        if self.end_port < 0 or self.end_port > 65535:
            messagebox.showerror('Errore', 'Inserire una porta finale valida\n\nLa porta finale deve essere compresa tra 0 e 65535.')

            self.scanurlip_wd.lift()

            return
        
        # Validate start port < end port
        if self.start_port > self.end_port:
            messagebox.showerror('Errore', 'La porta di inizio deve essere minore della porta finale')

            self.scanurlip_wd.lift()

            return

        # Lift up window
        self.scanurlip_wd.lift()

        # Save the HostName, URL or IP (v4/v6)
        if is_str_url_hname(url_entry):
            self.host: str = remove_protocol_url(url_entry)

            _addresses = resolve_hostname_ip(self.host)
            
            self.IPv4 = _addresses[0][0]
            # self.IPv6 = _addresses[0][1]

        elif is_str_ipv4(url_entry) or is_str_ipv6(url_entry):
            self.host: str = url_entry
            self.IPv4: str = url_entry

        # Reupdate the host entry field.
        self.urlip_entry.delete(0, tk.END)
        self.urlip_entry.insert(0, self.host)

        '''
        START SCANNING
        Delete previous results
        '''
        self.scan_results_table.delete(*self.scan_results_table.get_children())

        '''
        Set the start time
        '''
        self.scan_start_time = datetime.now()

        '''
        Show progress box and add details
        '''
        _hostname: str = self.host if self.host == self.IPv4 else f'{self.host} ({self.IPv4})'

        self.scanning_progress_box.pack(expand=True, side='top', fill='x', padx=10, pady=10)
        self.scan_detail__hostname.config(text=_hostname)
        self.scan_detail__start_port.config(text=self.start_port)
        self.scan_detail__end_port.config(text=self.end_port)
        self.scan_detail__start_time.config(text=self.scan_start_time.strftime('%Y %m %d %H:%M:%S'))

        self.scan_detail__remaining_ports.config(text=f'{self.end_port - self.start_port}')
        self.scan_detail__opened_ports.config(text='0')
        self.scan_detail__closed_ports.config(text='0')
        self.scan_detail__port_errors.config(text='0')

        '''
        Because I need to asynchrounosly updated the threeview (table)
        I use threading technique to scan the ports.
        '''
        self.scanning_thread = threading.Thread(target=self.scan_ports)
        self.scanning_thread.start()

        self.is_scan_completed() # Loop scan if the thread has completed its process

    def scan_ports(self):
        '''
        Scan a port
        '''
        status: bool = False # Initial status

        for port in range(self.start_port, self.end_port + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.5)                    

                response = sock.connect_ex((self.host, port))

                if response == 0:  
                    status = 'Aperta'
                    self.opened_ports += 1
                    self.scan_detail__opened_ports.config(text=self.opened_ports)

                else:
                    status = 'Chiusa'
                    self.closed_ports += 1
                    self.scan_detail__closed_ports.config(text=self.closed_ports)

            except Exception as e:
                status = f'Errore: {e}'
                self.port_errors += 1
                self.scan_detail__port_errors.config(text=self.port_errors)

            finally:
                '''
                Doesn't matter if the we got an error or not.

                Update the table.
                '''
                sock.close()

                self.scan_detail__current_port.config(text=port)
                self.scan_detail__remaining_ports.config(text=f'{(self.end_port - self.start_port) - (port - self.start_port)}')

            self.root.after(0, self.update_scanner_ui, port, status)

    def add_scanned_port_row(self, port: int, status: str):
        '''
        Add a row to the table
        '''
        self.scan_results_table.insert('', 'end', values=(port, status, ''))

    def update_progress_bar(self, progress: float):
        '''
        Update progress bar
        '''
        # print(f'Current scan progress: {value}%')

        self.scanning_progress_bar['value'] = progress
        self.scan_detail__progress.config(text=f'{progress} %')

    def update_scanner_ui(self, port: int, status: str):
        '''
        Update scanner UI
        '''
        progress: float = 0

        # Add row
        self.add_scanned_port_row(port, status)

        # Update progress bar
        if self.end_port != self.start_port:
            progress = ((port - self.start_port) / (self.end_port - self.start_port)) * 100  
            progress = round(progress, 2)

        else:
            progress = 100.00

        self.update_progress_bar(progress)

    def is_scan_completed(self):
        '''
        Check if the scan is completed
        '''
        if self.scanning_thread.is_alive():
            self.scan_detail__elapsed_time.config(text=f'{(datetime.now() - self.scan_start_time).seconds} secondi')

            self.root.after(250, self.is_scan_completed)

        else:
            self.scan_end_time = datetime.now()
            self.scan_detail__end_time.config(text=self.scan_end_time.strftime('%Y %m %d %H:%M:%S'))

            # self.scanning_progress_box.pack_forget()

            messagebox.showinfo('Scansione completata', 'Scansione completata con successo!')

            self.scanning_thread = None # Reset the thread

            self.scanurlip_wd.lift()