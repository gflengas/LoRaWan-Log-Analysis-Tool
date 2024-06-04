import log_parsing as LP
import pandas as pd
import json, os
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '\\'.join([ROOT_DIR, 'config.json'])

# read config file
with open(config_path) as config_file:
    config = json.load(config_file)
    server_config = config['server_credentials']
    file_config = config['local_files']

# Server details
SERVER_ADDRESS = server_config['SERVER_ADDRESS']
SERVER_PORT = server_config['SERVER_PORT']
SERVER_USERNAME = server_config['SERVER_USERNAME']
SERVER_PASSWORD = server_config['SERVER_PASSWORD']
REMOTE_FILE_PATH = server_config['REMOTE_FILE_PATH']
LOCAL_DESTINATION = file_config['LOCAL_DESTINATION']
# Open an empty txt file to save the report messages
report_file = file_config['report_file']
folder_path = file_config['logs_folder']
webhook = file_config['webhook']
with open(report_file, "w") as file:
    pass 
# Calculate the date one month ago from the current date
current_date = datetime.now()
one_month_ago = (current_date - timedelta(days=30)).strftime("%Y-%m-%d")
report_message = "Data since %s"%(one_month_ago)
with open(report_file, "a") as file:
    file.write(report_message + "\n")  
# parse the txt file
LP.downloadlog(SERVER_ADDRESS, SERVER_PORT, SERVER_USERNAME, SERVER_PASSWORD, 
                REMOTE_FILE_PATH,LOCAL_DESTINATION)
print("-----------------------------------------------")
print('Parsing the log file in progress...')
data = LP.txt_to_df('log_file.txt') 
review = pd.read_excel('sensor_list.xlsx')
print("-----------------------------------------------")
print('Analysing and creating the files...')
LP.analysis(review,data,report_file,folder_path)
print("-----------------------------------------------")
print('Starting uploading files to Sharepoint folder!')
LP.uploadFiles(folder_path,report_file)
LP.sendReport(report_file,webhook)
# Delete the report file
if os.path.exists(report_file):
    os.remove(report_file)
print("-----------------------------------------------")
print('Task finished...')