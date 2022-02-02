#!/usr/bin/env python3
from email.mime import image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import threading
import ipaddress
import socket
import os, sys

import ssh_comms

class heliumUpdateGUI(tk.Tk):
    colors = {
        'light gray' : '#d4d6d9',
        'black' : '#1a1a1a',
        'dark gray' : '#262626',
        'white' : '#edeff2',
        'highlight' : '#ddeaed',
        'graph' : '#175dcf',
        'but' : '#e6e6e6'
    }

    def __init__(self):
        super().__init__()
        self.title('Milesight Fast Sync Tool')
        self.iconbitmap(default='assets/helium.ico')
        self.optionspath = 'config/options.config'
        self.savepath = 'log.txt'
        self.WIDTH = 900
        self.HEIGHT = 500 
        self.s = ssh_comms.ssh_comms()
        self.gui()


    #*************************** DRAW GUI *********************************
    def gui(self):
        self.font = {
            'bold' : tkFont.Font(family='Open Sans', size=11, weight='bold'),
            'bold big' : tkFont.Font(family='Open Sans', size=15, weight='bold'),
            'cmd txt' : tkFont.Font(family='Consolas', size=13, weight='normal')
        }
        canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg=self.colors['light gray'])
        canvas.pack(fill='both', expand=True)

        self.fbdata = tk.Text(canvas, bg=self.colors['white'], font=self.font['cmd txt'], relief='groove')
        self.fbdata.insert('end', '   Version: 1.2 | Built 01.02.22\n\n')
        self.fbdata.configure(state='disabled')
        self.fbdata.place(anchor='n', relx=0.5, rely=0.07, relwidth=0.98, relheight=0.84)

        self.scrollb = ttk.Scrollbar(self.fbdata, command=self.fbdata.yview)
        self.scrollb.place(relx=0.98, rely=0, relheight=1, relwidth=0.02)
        self.fbdata['yscrollcommand'] = self.scrollb.set

        self.update_but = tk.Button(canvas,  text='1. Fast Sync', font=self.font['bold'], bg=self.colors['but'], fg=self.colors['black'],
                                    relief='groove', activebackground=self.colors['light gray'], command=self.update_but_func)
        self.update_but.bind('<Enter>', lambda event, x=self.update_but:self.on_hover(x))
        self.update_but.bind('<Leave>', lambda event, x=self.update_but, y=self.colors['but']:self.on_hover_leave(x, y))
        self.update_but.place(anchor='n', relx=0.14, rely=0.92, relwidth=0.17, relheight=0.07)
        
        self.quagga_but = tk.Button(canvas,  text='2. Quagga Restart', font=self.font['bold'], bg=self.colors['but'], fg=self.colors['black'],
                                    relief='groove', activebackground=self.colors['light gray'], command=self.quagga_but_func)
        self.quagga_but.bind('<Enter>', lambda event, x=self.quagga_but:self.on_hover(x))
        self.quagga_but.bind('<Leave>', lambda event, x=self.quagga_but, y=self.colors['but']:self.on_hover_leave(x, y))
        self.quagga_but.place(anchor='n', relx=0.32, rely=0.92, relwidth=0.17, relheight=0.07)

        self.status_but = tk.Button(canvas,  text='3. Status', font=self.font['bold'], bg=self.colors['but'], fg=self.colors['black'],
                                    relief='groove', activebackground=self.colors['light gray'], command=self.status_but_func)
        self.status_but.bind('<Enter>', lambda event, x=self.status_but:self.on_hover(x))
        self.status_but.bind('<Leave>', lambda event, x=self.status_but, y=self.colors['but']:self.on_hover_leave(x, y))
        self.status_but.place(anchor='n', relx=0.5, rely=0.92, relwidth=0.17, relheight=0.07)

        self.status_but = tk.Button(canvas,  text='4. Miner Info', font=self.font['bold'], bg=self.colors['but'], fg=self.colors['black'],
                                    relief='groove', activebackground=self.colors['light gray'], command=self.miner_info_func)
        self.status_but.bind('<Enter>', lambda event, x=self.status_but:self.on_hover(x))
        self.status_but.bind('<Leave>', lambda event, x=self.status_but, y=self.colors['but']:self.on_hover_leave(x, y))
        self.status_but.place(anchor='n', relx=0.68, rely=0.92, relwidth=0.17, relheight=0.07)

        self.status_but = tk.Button(canvas,  text='5. Peer Book', font=self.font['bold'], bg=self.colors['but'], fg=self.colors['black'],
                                    relief='groove', activebackground=self.colors['light gray'], command=self.run_peer_book_func)
        self.status_but.bind('<Enter>', lambda event, x=self.status_but:self.on_hover(x))
        self.status_but.bind('<Leave>', lambda event, x=self.status_but, y=self.colors['but']:self.on_hover_leave(x, y))
        self.status_but.place(anchor='n', relx=0.86, rely=0.92, relwidth=0.17, relheight=0.07)

        iplb = tk.Label(canvas, text='IP :', font=self.font['bold'], bg=self.colors['light gray'])
        iplb.place(anchor='n', relx=0.03, rely=0.005, relwidth=0.03, relheight=0.06)

        init_ip = '192.168.1.X'
        self.ipEntry = tk.Entry(canvas, font=self.font['bold'], justify='center', bg=self.colors['white'])
        self.ipEntry.insert('end', init_ip)
        self.ipEntry.place(anchor='n', relx=0.12, rely=0.012, relwidth=0.13, relheight=0.05)

        separator = ttk.Separator(canvas, orient='vertical')
        separator.place(relx=0.2, rely=0.003, relwidth=0.001, relheight=0.06)

        portlb = tk.Label(canvas, text='SSH port :', font=self.font['bold'], bg=self.colors['light gray'])
        portlb.place(anchor='n', relx=0.255, rely=0.005, relwidth=0.08, relheight=0.06)

        init_port = '22'
        self.portEntry = tk.Entry(canvas, font=self.font['bold'], justify='center', bg=self.colors['white'])
        self.portEntry.insert('end', init_port)
        self.portEntry.place(anchor='n', relx=0.345, rely=0.012, relwidth=0.07, relheight=0.05)

        # add logo img
        logo = Image.open('assets/invibit.png')
        logo = logo.resize((82, 30), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logolb = tk.Label(canvas, image=logo, bg=self.colors['light gray'])
        logolb.image = logo
        logolb.place(anchor='n', relx=0.77, rely=0.004, relwidth=0.11, relheight=0.058)

        separator2 = ttk.Separator(canvas, orient='vertical')
        separator2.place(relx=0.83, rely=0.003, relwidth=0.001, relheight=0.06)

        mlogo = Image.open('assets/milesight.png')
        mlogo = mlogo.resize((130, 95), Image.ANTIALIAS)
        mlogo = ImageTk.PhotoImage(mlogo)
        mlogolb = tk.Label(canvas, image=mlogo, bg=self.colors['light gray'])
        mlogolb.image = mlogo
        mlogolb.place(anchor='n', relx=0.9, rely=0.004, relwidth=0.13, relheight=0.065)

    #*************************** DRAW GUI **********************************

    #*************************** BUTTON FUNCTIONS ***************************
    def update_but_func(self):
        if not self.s.is_alive():
            if self.conn_sequence() == None:
                return
            self.tmpthread = threading.Thread(target=self.run_sync_commands)
            self.tmpthread.daemon = True
            self.tmpthread.start()
        else:
            self.throw_custom_error(title='Error', message='Another function already in progress. Please be patient.')

    def quagga_but_func(self):
        if not self.s.is_alive():
            if self.conn_sequence() == None:
                return
            self.tmpthread = threading.Thread(target=self.run_quagga_cmd)
            self.tmpthread.daemon = True
            self.tmpthread.start()
        else:
            self.throw_custom_error(title='Error', message='Another function already in progress. Please be patient.')
    
    def status_but_func(self):
        if not self.s.is_alive():
            if self.conn_sequence() == None:
                return
            self.tmpthread = threading.Thread(target=self.run_status_cmd)
            self.tmpthread.daemon = True
            self.tmpthread.start()
        else:
            self.throw_custom_error(title='Error', message='Another function already in progress. Please be patient.')

    def miner_info_func(self):
        if not self.s.is_alive():
            if self.conn_sequence() == None:
                return
            self.tmpthread = threading.Thread(target=self.run_miner_info_cmd)
            self.tmpthread.daemon = True
            self.tmpthread.start()
        else:
            self.throw_custom_error(title='Error', message='Another function already in progress. Please be patient.')

    def run_peer_book_func(self):
        if not self.s.is_alive():
            if self.conn_sequence() == None:
                return
            self.tmpthread = threading.Thread(target=self.run_peer_book_cmd)
            self.tmpthread.daemon = True
            self.tmpthread.start()
        else:
            self.throw_custom_error(title='Error', message='Another function already in progress. Please be patient.')

    # button highlighting on hover
    def on_hover(self, button, color=colors['highlight']):
        button.configure(bg=color)
    
    def on_hover_leave(self, button, color):
        button.configure(bg=color)

    #*************************** BUTTON FUNCTIONS ***************************

    def run_sync_commands(self):
        self.update_fbdata('Syncing . . . This might take a minute . . .\n')
        self.log = ''
        height = '** ERROR WHILE EXECUTING CURL CMD **'
        cmds = ['docker exec miner miner repair sync_pause',
                'docker exec miner miner repair sync_cancel',
                'curl https://helium-snapshots.nebra.com/latest.json',
                'cd /mnt/mmcblk0p1/miner_data/snap && rm snap-*',
                'cd /mnt/mmcblk0p1/miner_data/snap && wget https://helium-snapshots.nebra.com/snap-',
                'docker exec miner miner snapshot load /var/data/snap/snap- &',
                'docker exec miner miner repair sync_state',
                'docker exec miner miner repair sync_resume']
        do_sync_resume = False
        for idx, cmd in enumerate(cmds):
            if idx == 7 and do_sync_resume: # sync resume
                chk = True
                while chk:
                    self.update_fbdata(f'${cmd}\n')
                    out, stderr = self.s.exec_cmd(cmd=cmd)
                    self.update_fbdata(out)
                    if stderr != '': self.update_fbdata(f'STDERR: {stderr}')
                    self.log += f'#{cmd}\n{out}'
                    if stderr != '': self.log += f'STDERR: {stderr}'
                    chk = 'failed' in out
            else:
                if idx == 4: # wget
                    cmd += height
                elif idx == 5: # snapshot load
                    cmd = f"{cmd.split(' &')[0]}{height}{cmd.split('snap-')[1]}"
                self.update_fbdata(f'${cmd}\n')
                out, stderr = self.s.exec_cmd(cmd=cmd)
                self.update_fbdata(out)
                if stderr != '':
                    if idx == 4: stderr = '\n'.join(stderr.split('\n')[:13])+'\n'+' '*30+'..........\n'+'\n'.join(stderr.split('\n')[-10:])
                    self.update_fbdata(f'STDERR: {stderr}')
                if idx == 2: # curl
                    height = out.split('height": ')[1].split(',')[0]
                elif idx == 6: # sync_state
                    do_sync_resume = 'sync active' not in out

                self.log += f'#{cmd}\n{out}'
                if stderr != '': self.log += f'STDERR: {stderr}'
        self.update_fbdata('*** DONE ***\n')
        self.save()
        self.s.disconnect()


    def run_quagga_cmd(self):
        cmd = '/etc/init.d/quagga restart'
        self.update_fbdata(f'${cmd}\n')
        out, stderr = self.s.exec_cmd(cmd=cmd)
        self.update_fbdata(out)
        if stderr != '': self.update_fbdata(f'STDERR: {stderr}')
        self.update_fbdata(f'*** DONE ***\n')
        self.s.disconnect()


    def run_status_cmd(self):
        cmd = 'docker exec miner miner info p2p_status'
        self.update_fbdata(f'${cmd}\n')
        out, stderr = self.s.exec_cmd(cmd=cmd)
        self.update_fbdata(out)
        if stderr != '': self.update_fbdata(f'STDERR: {stderr}')
        self.update_fbdata(f'*** DONE ***\n')
        self.s.disconnect()

    def run_miner_info_cmd(self):
        cmd = 'docker exec miner miner info summary'
        self.update_fbdata(f'${cmd}\n')
        out, stderr = self.s.exec_cmd(cmd=cmd)
        self.update_fbdata(out)
        if stderr != '': self.update_fbdata(f'STDERR: {stderr}')
        self.update_fbdata(f'*** DONE ***\n')
        self.s.disconnect()

    def run_peer_book_cmd(self):
        cmd = 'docker exec miner miner peer book -s'
        self.update_fbdata(f'${cmd}\n')
        out, stderr = self.s.exec_cmd(cmd=cmd)
        self.update_fbdata(out)
        if stderr != '': self.update_fbdata(f'STDERR: {stderr}')
        self.update_fbdata(f'*** DONE ***\n')
        self.s.disconnect()

    def conn_sequence(self):
        addr = self.ipEntry.get()
        port = self.portEntry.get()
        if not self.valid_port(port):
            self.throw_custom_error(title='Error', message='Invalid SSH port. Range : [0, 65535].')
            return None
        if addr[-1] == 'X':
            self.throw_custom_error(title='Error', message='Enter device IP address.')
            return None
        if not self.validate_ip_address(addr):
            self.throw_custom_error(title='Error', message='Invalid IP address.')
            return None
        opts = self.read_config()
        user, passwd = [opts[key] for key in ['username', 'password']]
        if any([x==None for x in [user, passwd]]):
            self.throw_custom_error(title='Error', message='Error reading options.config file.')
            return None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((addr, int(port))) != 0:
            sock.close()
            self.throw_trouble_connecting_error()
            return None
        sock.close()
        self.s.set_config(addr=addr, user=user, port=port, password=passwd)
        connection = self.s.connect()
        self.clear_fbdata()
        if not self.s.is_alive() or connection == None:
            self.update_fbdata('Connection Error.\nCheck username and password in options.config in config/ folder.')
            return None
        return True


    def update_fbdata(self, d):
        self.fbdata.configure(state='normal')
        self.fbdata.insert('end', d)
        self.fbdata.update()
        self.fbdata.configure(state='disabled')
        self.fbdata.see('end')
    
    def clear_fbdata(self):
        self.fbdata.configure(state='normal')
        self.fbdata.delete('3.0', 'end')
        self.fbdata.insert('end', '\n')
        self.fbdata.configure(state='disabled')

    def validate_ip_address(self, address):
        try:
            ip = ipaddress.ip_address(address)
            return True
        except ValueError:
            return False
    
    def valid_port(self, port):
        try:
            port = int(port)
            return (port >= 0 and port <=65535)
        except:
            return False

    def read_config(self):
        if os.path.isfile(self.optionspath) and os.path.getsize(self.optionspath) > 0:
            with open(self.optionspath, 'r') as f:
                lines = f.readlines()
            opts = {key:'' for key in ['username', 'password']}
            for line in lines:
                if any([x in line for x in opts.keys()]):
                    key, val = line.split('=')
                    opts[key] = val.strip()
            return opts
        else:
            return {key:None for key in ['username', 'password']}

    def save(self):
        try:
            with open(self.savepath, 'w') as f:
                f.write(self.log)
        except Exception as e:
            self.throw_custom_error('ERROR', 'Error trying to save log file.')
            print(f'e : {e}')


    #**************************** THROW ERROR ****************************
    def throw_trouble_connecting_error(self):
        messagebox.showwarning(title='ERROR', message='Having trouble connecting to device.')

    def throw_custom_error(self, title, message):
        messagebox.showwarning(title=title, message=message)
    #**************************** THROW ERROR ****************************

    def exit(self):
        self.quit()
        self.destroy()


if __name__ == '__main__':
    gui = heliumUpdateGUI()
    gui.resizable(True, True)
    gui.minsize(900, 500)
    gui.protocol('WM_DELETE_WINDOW', gui.exit)
    gui.mainloop()
