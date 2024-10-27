import tkinter as tk
import socket
from datetime import datetime
from tkinter import ttk, messagebox
from customtkinter import CTkScrollableFrame

class ScanUrlIPWd:
    
    # The entry to search for.
    ip: str = ''
    
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
        self.body_frame.pack(expand=True, side='bottom', fill='x', padx=0, pady=0)

        # Generate header and body
        self.generate_header()
        self.generate_body()

    def generate_header(self):
        '''
        Generate header
        '''
        tk.Label(
            self.header_frame, 
            text='Strumento di scansione delle porte di URL / Indirizzi IP', 
            font=('Arial', 12, 'bold'), 
            justify='center'
        ).pack(expand=False, side='top', fill='x', padx=0, pady=[0, 15])

        searchbox_wrap_frame = tk.Frame(self.header_frame)
        searchbox_wrap_frame.pack(expand=False, side='top', fill='x', padx=5, pady=5)

        tk.Label(
            searchbox_wrap_frame, 
            text='Inserisci URL/IP da scansionare:', 
            font=('Arial', 10, 'bold'), 
            justify='left'
        ).pack(expand=True, side='top', fill='none', anchor='w', padx=0, pady=[0, 5])

        searchbox_frame = tk.Frame(searchbox_wrap_frame)
        searchbox_frame.pack(expand=True, side='bottom', fill='both', anchor='nw', padx=0, pady=0)

        self.urlip_entry = tk.Entry(searchbox_frame, font=('Arial', 12))
        self.scan_button = tk.Button(
            searchbox_frame, 
            text='Scansiona', 
            font=('Arial', 10, 'bold'),
            command=self.scan_url_ip,
            cursor='hand2'
        )

        self.urlip_entry.pack(side='left', fill='x', expand=True, padx=0, pady=0)
        self.scan_button.pack(side='right', fill='x', expand=False, padx=[10, 0], pady=0)

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

        self.scan_results_table.insert('', 'end', values=('80', 'Aperta', 'HTTP'))


    def scan_url_ip(self):
        '''
        Scan URL/IP and fill the table with results
        '''
        self.ip = self.urlip_entry.get()

        if self.ip == '':
            messagebox.showerror('Errore', 'Inserire un URL/IP')
            self.scanurlip_wd.lift()

            return
        
        messagebox.showinfo('Scansione URL/IP', f'Scansione URL/IP {self.ip} in corso...')
        self.scanurlip_wd.lift()
