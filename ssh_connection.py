import paramiko
from credentials_ssh import USERNAME, USERNAME_PASSWORD, HOST, SSH_PORT


class Ssh:
    """Class for SSH single use"""
    def __init__(self):
        self.client = None
        self.host = HOST
        self.username = USERNAME
        self.password = USERNAME_PASSWORD
        self.port = SSH_PORT
        self.ssh_out = None
        self.ssh_err = None

    def connect(self):
        """ Method for SSH connection"""
        try:
            self.client = paramiko.SSHClient()
            print(f"Connecting to {self.host} with user: '{self.username}'")
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, self.port, self.username, self.password)
            print("Connection established")
            response = True
        except paramiko.AuthenticationException:
            print("Authentication failed, please chez your credentials")
            response = False
        except paramiko.SSHException:
            print(f"Could not establish connection with {self.host}:")
            response = False
        return response

    def execute_command(self, command):
        """Method for the execution of one single command"""
        try:
            if self.connect():
                stdin, stdout, stderr = self.client.exec_command(command)
                self.ssh_out = stdout.read()
                self.ssh_err = stderr.read()
                if self.ssh_out:
                    print(f"command : '{command}' executed successfully")
                    response = True
                elif self.ssh_err:
                    print(f"Error while running command: '{command}'")
                    response = False
                self.client.close()
            else:
                response = False
                print(f"Could not establish connection with {self.host}:")
        except paramiko.SSHException:
            print(f"Failed to execute the command: '{command}'")
            response = False
        return response

    def upload_file(self, localfile, remote_location):
        """ Method to upload a file on the Server """
        try:
            if self.connect():
                ftp_session = self.client.open_sftp()
                ftp_session.put(localfile, remote_location)
                ftp_session.close()
                print(f"The file '{localfile}' has been correctly uploaded")
                response = True
            else:
                response = False
                print(f"Could not establish connection with {self.host}:")
            self.client.close()
        except paramiko.SSHException:
            print(f"Failed to transfert the file: '{localfile}' to {self.host}")
            response = False
        return response

ssh = Ssh()
ssh.execute_command('ls /home/seiph')
ssh.upload_file('fichier_test', '/home/seiph/fichier_test')