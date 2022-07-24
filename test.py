import paramiko


def exec_remote_cmd(cmd, hostname, username='root', password='root',port=22):
    #设置客户端实例
    ssh_client = paramiko.SSHClient()
    #如果没有：连接重复的IP，会弹出yes or no
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #客户端连接
    ssh_client.connect(hostname, port, username, password)
    #执行命令
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read().decode('utf-8'))
    returncode = stdout.channel.recv_exit_status()
    print("returncode:", returncode)
    ssh_client.close()


def upload_file2remote(src, dest, username='root', password='root', port=22):
    #设置transfer实例
    trans = paramiko.Transport()
    trans.connect(username=username, password=password)
    #获取sftp实例
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.put(src, dest)
    trans.close()


def download_file2local(local, dest, hostname=None, username='root', password='root', port=22):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password, port=port)
    # 实例化transfers
    trans = ssh_client.get_transport()
    # 实例化sftp
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.get(dest, local)
    ssh_client.close()