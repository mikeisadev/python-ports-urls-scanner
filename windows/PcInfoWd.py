import tkinter as tk
from tkinter import ttk, messagebox
from customtkinter import CTkScrollableFrame
import platform
import psutil
from utils.memory import get_size

class PcInfoWd:

    def __init__(self, root) -> None:
        self.root = root

    def pc_info_window(self):
        '''
        Get PC Infos.
        '''
        self.pcinfo_wd = tk.Toplevel(self.root)
        self.pcinfo_wd.title('Informazioni sul tuo PC')
        self.pcinfo_wd.geometry('720x600')

        info_frame = CTkScrollableFrame(
            self.pcinfo_wd,
            orientation='vertical'
        )
        info_frame.pack(side='top', fill='both', expand=True)

        #  [TITLE] - OS info title
        tk.Label(info_frame, text='Informazioni sul sistema operativo', font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky='wn')

        # OS - Operative system
        tk.Label(info_frame, text='Sistema operativo:', font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_os = tk.Label(info_frame, text=platform.system(), font=('Arial', 10))
        self.pc_info_os.grid(row=1, column=1, padx=10, pady=5, sticky="w") 

        # OS - Current info
        tk.Label(info_frame, text='Utente corrente:', font=('Arial', 10, 'bold')).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_node = tk.Label(info_frame, text=platform.node(), font=('Arial', 10))
        self.pc_info_node.grid(row=2, column=1, padx=10, pady=5, sticky="w") 

        # OS - Release
        tk.Label(info_frame, text='Release:', font=('Arial', 10, 'bold')).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_os_release = tk.Label(info_frame, text=platform.release(), font=('Arial', 10))
        self.pc_info_os_release.grid(row=3, column=1, padx=10, pady=5, sticky="w") 

        # OS - Version
        tk.Label(info_frame, text='Versione sistema operativo:', font=('Arial', 10, 'bold')).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_os_ver = tk.Label(info_frame, text=platform.version(), font=('Arial', 10))
        self.pc_info_os_ver.grid(row=4, column=1, padx=10, pady=5, sticky="w") 

        # OS - Machine
        tk.Label(info_frame, text='Macchina:', font=('Arial', 10, 'bold')).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_os_mach = tk.Label(info_frame, text=platform.machine(), font=('Arial', 10))
        self.pc_info_os_mach.grid(row=5, column=1, padx=10, pady=5, sticky="w") 

        # OS - Architecture
        tk.Label(info_frame, text='Architettura:', font=('Arial', 10, 'bold')).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_os_arch = tk.Label(info_frame, text=' '.join(platform.architecture()), font=('Arial', 10))
        self.pc_info_os_arch.grid(row=6, column=1, padx=10, pady=5, sticky="w") 

        #  [TITLE] - Python info
        tk.Label(info_frame, text='Informazioni su Python', font=('Arial', 12, 'bold')).grid(row=7, column=0, padx=10, pady=10, sticky='w')

        # PY - Version
        tk.Label(info_frame, text='Versione Python:', font=('Arial', 10, 'bold')).grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_python_v = tk.Label(info_frame, text=' '.join(platform.python_version()), font=('Arial', 10))
        self.pc_info_python_v.grid(row=8, column=1, padx=10, pady=5, sticky="w") 

        # PY - Compiler
        tk.Label(info_frame, text='Compilatore:', font=('Arial', 10, 'bold')).grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_python_comp = tk.Label(info_frame, text=' '.join(platform.python_compiler()), font=('Arial', 10))
        self.pc_info_python_comp.grid(row=9, column=1, padx=10, pady=5, sticky="w") 

        # PY - Build
        tk.Label(info_frame, text='Build:', font=('Arial', 10, 'bold')).grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_python_build = tk.Label(info_frame, text=' '.join(platform.python_build()), font=('Arial', 10))
        self.pc_info_python_build.grid(row=10, column=1, padx=10, pady=5, sticky="w") 

        #  [TITLE] - CPU info
        tk.Label(info_frame, text='Informazioni CPU (processore)', font=('Arial', 12, 'bold')).grid(row=11, column=0, padx=10, pady=10, sticky='w')

        # CPU - Physical cores
        tk.Label(info_frame, text='Cores fisici:', font=('Arial', 10, 'bold')).grid(row=12, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_cpu_p = tk.Label(info_frame, text=psutil.cpu_count(logical=False), font=('Arial', 10))
        self.pc_info_cpu_p.grid(row=12, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Logical cores
        tk.Label(info_frame, text='Cores logici:', font=('Arial', 10, 'bold')).grid(row=13, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_cpu_l = tk.Label(info_frame, text=psutil.cpu_count(logical=True), font=('Arial', 10))
        self.pc_info_cpu_l.grid(row=13, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Max frequency
        tk.Label(info_frame, text='Frequenza massima:', font=('Arial', 10, 'bold')).grid(row=14, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_cpu_max_f = tk.Label(info_frame, text=f'{psutil.cpu_freq().max:.2f} MHz', font=('Arial', 10))
        self.pc_info_cpu_max_f.grid(row=14, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Min frequency
        tk.Label(info_frame, text='Frequenza minima:', font=('Arial', 10, 'bold')).grid(row=15, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_cpu_min_f = tk.Label(info_frame, text=f'{psutil.cpu_freq().min:.2f} MHz', font=('Arial', 10))
        self.pc_info_cpu_min_f.grid(row=15, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Current frequency
        tk.Label(info_frame, text='Frequenza corrente:', font=('Arial', 10, 'bold')).grid(row=16, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_cpu_curr_f = tk.Label(info_frame, text=f"{psutil.cpu_freq().current:.2f} Mhz", font=('Arial', 10))
        self.pc_info_cpu_curr_f.grid(row=16, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Percent per core percent usage
        tk.Label(info_frame, text='Utilizzo CPU per core:', font=('Arial', 10, 'bold')).grid(row=17, column=0, padx=10, pady=5, sticky="nw")

        self.pc_info_per_core_usage_frame = tk.Frame(info_frame)
        self.pc_info_per_core_usage_frame.grid(row=17, column=1, padx=10, pady=5, sticky='nw')

        r = 0
        for core_usage in psutil.cpu_percent(percpu=True):
            tk.Label(self.pc_info_per_core_usage_frame, text=f'Core {r+1} - {core_usage} %', font=("Arial", 10)).grid(row=r, column=0, padx=5 , pady=5, sticky="nw")

            r += 1

        # CPU - Total percent usage
        tk.Label(info_frame, text='Utilizzo CPU totale:', font=('Arial', 10, 'bold')).grid(row=18, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_tot_cpu_usage = tk.Label(info_frame, text=f'{psutil.cpu_percent(interval=0.5)} %', font=('Arial', 10))
        self.pc_info_tot_cpu_usage.grid(row=18, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Sys calls
        tk.Label(info_frame, text='System calls:', font=('Arial', 10, 'bold')).grid(row=19, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_sys_calls = tk.Label(info_frame, text=psutil.cpu_stats().syscalls, font=('Arial', 10))
        self.pc_info_sys_calls.grid(row=19, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Context switches
        tk.Label(info_frame, text='Context switches:', font=('Arial', 10, 'bold')).grid(row=20, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_ctx_switches = tk.Label(info_frame, text=psutil.cpu_stats().ctx_switches, font=('Arial', 10))
        self.pc_info_ctx_switches.grid(row=20, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Soft interrupts
        tk.Label(info_frame, text='Soft interrupts:', font=('Arial', 10, 'bold')).grid(row=21, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_soft_interrupts = tk.Label(info_frame, text=psutil.cpu_stats().soft_interrupts, font=('Arial', 10))
        self.pc_info_soft_interrupts.grid(row=21, column=1, padx=10, pady=5, sticky="w") 

        # CPU - Interrupts
        tk.Label(info_frame, text='Interrupts:', font=('Arial', 10, 'bold')).grid(row=22, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_sys_interrupts = tk.Label(info_frame, text=psutil.cpu_stats().interrupts, font=('Arial', 10))
        self.pc_info_sys_interrupts.grid(row=22, column=1, padx=10, pady=5, sticky="w") 

        # [TITLE] - RAM and Memory Info
        tk.Label(info_frame, text='Informazioni memoria RAM', font=('Arial', 12, 'bold')).grid(row=23, column=0, padx=10, pady=10, sticky='w')

        ram = psutil.virtual_memory()

        # RAM - Total
        tk.Label(info_frame, text='Memoria RAM totale:', font=('Arial', 10, 'bold')).grid(row=24, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_ram_tot = tk.Label(info_frame, text=get_size(ram.total), font=('Arial', 10))
        self.pc_info_ram_tot.grid(row=24, column=1, padx=10, pady=5, sticky="w") 

        # RAM - Available
        tk.Label(info_frame, text='Memoria RAM disponibile:', font=('Arial', 10, 'bold')).grid(row=25, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_ram_available = tk.Label(info_frame, text=get_size(ram.available), font=('Arial', 10))
        self.pc_info_ram_available.grid(row=25, column=1, padx=10, pady=5, sticky="w") 

        # RAM - Utilized
        tk.Label(info_frame, text='Memoria RAM utilizzata:', font=('Arial', 10, 'bold')).grid(row=26, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_ram_used = tk.Label(info_frame, text=get_size(ram.used), font=('Arial', 10))
        self.pc_info_ram_used.grid(row=26, column=1, padx=10, pady=5, sticky="w") 

        # RAM - Current usage
        tk.Label(info_frame, text='Utilizzo della RAM corrente:', font=('Arial', 10, 'bold')).grid(row=27, column=0, padx=10, pady=5, sticky="w")
        self.pc_info_ram_usage = tk.Label(info_frame, text=f'{ram.percent} %', font=('Arial', 10))
        self.pc_info_ram_usage.grid(row=27, column=1, padx=10, pady=5, sticky="w")  

        # Disk info
        tk.Label(info_frame, text='Informazioni memoria interna e esterna', font=('Arial', 12, 'bold')).grid(row=28, column=0, padx=10, pady=10, sticky='w')

        diskparts = psutil.disk_partitions()

        r = 29
        for disk in diskparts:
            disk_usage = psutil.disk_usage(disk.mountpoint)

            disk_info = [
                ('Mountpoint:', disk.mountpoint),
                ('Tipo di file system:', disk.fstype),
                ('Dimensione totale:', get_size(disk_usage.total)),
                ('Spazio usato:', get_size(disk_usage.used)),
                ('Spazio libero:', get_size(disk_usage.free)),
                ('Utilizzo (%):', f'{disk_usage.percent}%')
            ]
        
            tk.Label(info_frame, text=f'Disco {disk.device}', font=('Arial', 10, 'bold')).grid(row=r, column=0, padx=10, pady=5, sticky="nw")

            self.disk_info = tk.Frame(info_frame)
            self.disk_info.grid(row=r, column=1, padx=10, pady=5, sticky='nw')
            
            for i, (label, data) in enumerate(disk_info):
                tk.Label(self.disk_info, text=label, font=('Arial', 10)).grid(row=i, column=0, sticky='nw')
                tk.Label(self.disk_info, text=data, font=('Arial', 10)).grid(row=i, column=1, sticky='nw')

            r += 1
    

        # Network info

        self.pc_info_window_refresh()

    def pc_info_window_refresh(self):
        '''
        Refresh PC info.

        Refresh only changing data.
        '''

        # CPU
        # CPU - Current frequency
        self.pc_info_cpu_curr_f.config(text=f"{psutil.cpu_freq().current:.2f} Mhz")

        # CPU - Per CPU Core usage
        for core in self.pc_info_per_core_usage_frame.winfo_children():
            core.destroy()

        r = 0
        for core_usage in psutil.cpu_percent(percpu=True):
            tk.Label(self.pc_info_per_core_usage_frame, text=f'Core {r+1} - {core_usage} %', font=("Arial", 10)).grid(row=r, column=0, padx=10, pady=5, sticky="nw")

            r += 1

        # CPU - Total usage
        self.pc_info_tot_cpu_usage.config(text=f'{psutil.cpu_percent()} %')

        # CPU - Sys calls
        self.pc_info_sys_calls.config(text=psutil.cpu_stats().syscalls) 

        # CPU - Context switches
        self.pc_info_ctx_switches.config(text=psutil.cpu_stats().ctx_switches) 

        # CPU - Soft interrupts
        self.pc_info_soft_interrupts.config(text=psutil.cpu_stats().soft_interrupts) 

        # CPU - Interrupts
        self.pc_info_sys_interrupts.config(text=psutil.cpu_stats().interrupts) 

        # RAM
        ram = psutil.virtual_memory()

        # RAM - Available
        self.pc_info_ram_available.config(text=get_size(ram.available))

        # RAM - Used
        self.pc_info_ram_used.config(text=get_size(ram.used))

        # RAM - Usage
        self.pc_info_ram_usage.config(text=f'{ram.percent} %')

        # Refresh info
        self.pcinfo_wd.after(250, self.pc_info_window_refresh)