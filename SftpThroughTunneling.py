# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:53:50 2019

@author: tamjid.m.hossain
"""
import os
import pandas as pd
import timeit
from datetime import timedelta,date
import paramiko
from sshtunnel import SSHTunnelForwarder
#%%
start = timeit.default_timer() #Starting time to see the total execution time
tod = date.today() - timedelta(days=0) #taking current date as filename can contain Date
day_old=0 # 0 indicates the file of current date whereas changing the value of day_old to 1 will download the Yesterdays' file
#%%
# 1.Credential used for Logging into Local, Tunnel and SFTP
print('# 1.Credential used for Logging into Local, Tunnel and SFTP')

local_ip = '127.0.0.1'
local_port = 10022 # pick any logical port

credential = pd.DataFrame()
credential = pd.read_csv('C:/Users/tamjid.m.hossain/Documents/GitHub/SFTPthroughTunneling/credential.csv', delimiter = ',')
tunnel_ip = '10.10.0.0'
tunnel_username = credential.iloc[0,1]
tunnel_password = credential.iloc[0,2]

sftp_ip = '192.168.0.0'
sftp_port = 22
sftp_username = 'SFTPUserName'
sftp_password = 'SFTPUserPassword'
sftp_file_location = '/sftpFileLocation'

#%%
# 2. Assigning Variables
print('# 2. Assigning Variables')
      
fileType = ['testFile1','testFile2','testFile3'] #Test Files which will be downloaded
os.chdir('C:/Users/tamjid.m.hossain/Documents/GitHub/SFTPthroughTunneling/')
dump_file_path = 'Dump' #Dumping File Location

#%%
# 3. FTPying through Tunnel
print('# 3. FTPying through Tunnel')

with SSHTunnelForwarder(
    tunnel_ip, #Tunnel IP address
    ssh_username = tunnel_username, #Tunnel username
    ssh_password = tunnel_password, #Tunnel password
    remote_bind_address = (sftp_ip, sftp_port),  # SFTP IP address
    local_bind_address = (local_ip, local_port)
) as tunnel:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(local_ip, username = sftp_username, password = sftp_password, port = local_port)
    ftp = client.open_sftp()
    new_loc = (sftp_file_location)
    ftp.chdir(new_loc)
    print('Filename:\n')
    
    for file in ftp.listdir():
        for i in range(len(fileType)):
            dt = tod - timedelta(days=day_old)
            
            if((fileType[i] in file) and (dt.strftime('%Y_%m_%d') in file)):  #change the date format as per the date in your file name
                print(file)
                try:
                    ftp.get(file,os.path.join(dump_file_path,file))
                except:
                    pass
            elif((fileType[i] in file) and (dt.strftime('%Y%m%d') in file)): #change the date format as per the date in your file name
                print(file)
                try:
                    ftp.get(file,os.path.join(dump_file_path,file))
                except:
                    pass

    ftp.close()
    client.close()
#%%
#4. Printing Total Time
print('#4. Printing Total Time\n')
      
stop = timeit.default_timer() # Ending Timer
execution_time = stop - start # Calculating Execution Time
print('Total Execution Time : '+str(execution_time)) #Printing Execution Time
