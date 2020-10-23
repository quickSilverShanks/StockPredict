import requests, zipfile, io, logging
import pandas as pd
from datetime import datetime, timedelta

Start_date = "2020SEP20"
End_date = "2020OCT01"

d_path='R:\DataScience\Python\I-Neuron\Internship\StockAnalysis\Data.'

global No_of_download, Working_day, Non_Work_day
No_of_download = 0
Working_day = 0
Non_Work_day = 0


# Def for downloading and Unzipping the File
def req(zip_file_url):
    global No_of_download
    r = requests.post(zip_file_url)
    status_code = r.status_code
    # print(status_code)
    # If status code is <> 200, it indicates that no data is present for that date. For example, week-end, or trading holiday.
    if status_code == 200:
        No_of_download = No_of_download + 1
        logger.info("File Available.Downloading")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=d_path)
    else:
        logger.info("******File Not Available.Moving to next date.")


# Main Program
today_date = datetime.now().strftime("%Y%b%d")
logging.basicConfig(filename="Log_" + today_date + ".log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


daterange = pd.date_range(datetime.strptime(Start_date, "%Y%b%d"), datetime.strptime(End_date, "%Y%b%d"))
print(daterange)

# Looping through each date, and downloading the file.
for single_date in daterange:
    loop_date = single_date.strftime("%Y-%b-%d")
    year, month, date = loop_date.split('-')
    month = month.upper()
    weekday = single_date.weekday()
    # If day is not Saturday or Sunday,then proceed to download the file.
    if weekday not in [5, 6]:
        Working_day = Working_day + 1
        logger.info("Trying to download File of :" + loop_date)
        temp_zip_file_url = 'https://www1.nseindia.com/content/historical/EQUITIES/' + year + '/' + month + '/cm' + date + month + year + 'bhav.csv.zip'
        req(zip_file_url=temp_zip_file_url)
        # print(temp_zip_file_url)
    else:
        Non_Work_day = Non_Work_day + 1

# print("Number of files downloaded:"+str(No_of_download))
logger.info("****************************************************************************************")
logger.info("No. of files downloaded=" + str(No_of_download))
logger.info("Span= " + Start_date + " to " + End_date)
logger.info("No. of weekdays in the given time span=" + str(Working_day))
logger.info("****************************************************************************************")
logging.shutdown()


# Reading all CSV files from downloaded location and appending to form single data

import glob

df = pd.concat(map(pd.read_csv, glob.glob('R:\DataScience\Python\I-Neuron\Internship\StockAnalysis\Data\*.csv')))
print(df.shape)