import os
import paramiko

LOCAL_ROOT = os.getcwd()
REMOTE_ROOT = '/home/pi/apollo'

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts')))

ssh.connect('rpi', username='pi', password='raspberry')
sftp = ssh.open_sftp()

for root, sub_folders, files in os.walk(LOCAL_ROOT):

    for f in files:
        local_path = os.path.join(root, f)
        remote_path = local_path.replace(LOCAL_ROOT, REMOTE_ROOT).replace('\\', '/')

        fname, fext = os.path.splitext(local_path)
        if fext in ['.py', '.js', '.html', '.css', '.md', '.gitignore']:
            try:
                sftp.put(local_path, remote_path)
                print 'File ' + remote_path + ' was updated on the server'
            except Exception as e:
                print e

sftp.close()
ssh.close()