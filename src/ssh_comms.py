from paramiko import SSHClient, AutoAddPolicy

class ssh_comms():
    def __init__(self):
        try:
            self.ssh = SSHClient()
            self.ssh.set_missing_host_key_policy(AutoAddPolicy())
            print('Successful Initialization')
        except:
            return None

    def set_config(self, addr=None, user=None, port=22, password=None):
        args = [addr, user, int(port), password]
        if all([arg != None for arg in args]):
            self.addr, self.user, self.port, self.password = args
            print(f'args : {args}')
        else:
            print('One / Multiple options not set on options file.')

    def connect(self):
        print(f'** Connecting to {self.addr} on port {self.port}**')
        try:
            self.ssh.connect(self.addr, username=self.user, password=self.password)
            return 'Connected'
        except:
            self.disconnect()
            return None

    def disconnect(self):
        print(f'** Disconnecting from {self.addr} **')
        try:
            self.ssh.close()
        except:
            print('Error disconnecting')

    def exec_cmd(self, cmd=None):
        if cmd is not None:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            return [stdout.read().decode(), stderr.read().decode()]
        else:
            print('provide cmd to execute')

    def is_alive(self):
        if self.ssh.get_transport() is not None:
            return self.ssh.get_transport().is_active()
