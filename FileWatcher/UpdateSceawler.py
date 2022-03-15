import os, sys, time, logging
import datetime, pandas
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Settings import *





def UpdateScrawledTimeDBMain():
    while True:
        now =datetime.datetime.now()
        old_db_frame=pandas.read_csv(db_path, index_col=False)
        db_frame=old_db_frame
        db_frame['last_scrawled_time'] = now
        db_frame.to_csv(db_path, index=False)
        db_frame.to_excel(db_excel_path, index=False)
        print('Last Scrawled Time Updated : ', now)
        time.sleep(sleepTime)



if __name__ == "__main__":
    UpdateScrawledTimeDBMain()