import os
import paramiko

LOCAL_ROOT = os.getcwd()
REMOTE_ROOT = '/home/pi/apollo/'

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts')))

ssh.connect('192.168.1.10', username='pi', password='raspberry')
sftp = ssh.open_sftp()

for root, sub_folders, files in os.walk(LOCAL_ROOT):

    for file in files:
        local_path = LOCAL_ROOT + '/' + file
        remote_path = REMOTE_ROOT + '/' + file

        try:
            sftp.put(local_path, remote_path)
            print 'File ' + file + ' was sent to server'
        except Exception as e:
            print 'Error ' + e.message

sftp.close()
ssh.close()