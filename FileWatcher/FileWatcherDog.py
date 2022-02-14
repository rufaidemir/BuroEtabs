import watchdog.events
import watchdog.observers
import time, os
import datetime
from multiprocessing import Process

import pandas
pandas.options.mode.chained_assignment = None

db_path = 'C:\\Projeler\\PythonP\\BuroEtabs\\Scraw_Folder_to_DF.csv'
db_excel_path = 'C:\\Projeler\\PythonP\\BuroEtabs\\Scraw_Folder_to_DF.xlsx'
project_name_start_index=2
sleepTime=5

extention_software_match_dict =  {
    'xlsx':'Excel',
    'xls':'Excel',
    'doc':'Word',
    'EDB':'Etaps',
    'FBD':'Safe',
    'dwg':'AutoCAD',
    'rvt':'Revit',
    'lir':'Lira-Sapr',
    'spf':'Lira-Sapfire',
    'dyn':'Dynamo',
    'nwd':'Navisworks',
    'ide10':'IdeCAD10',
    'ide85':'IdeCAD85',

}

def total_second_from_datetime(date:datetime.datetime) ->datetime.datetime:
    return (date-datetime.datetime(1970,1,1)).total_seconds()


def ModificationTotalSecondsFromLastScrawledTime(filePath, last_scrawled_time):
    modified_timestamp_value = 0
    file_is_exists=os.path.exists(filePath)
    if file_is_exists:
        new_modification_time=datetime.datetime.fromtimestamp((os.path.getmtime(filePath)))
        if total_second_from_datetime(new_modification_time)>=total_second_from_datetime(last_scrawled_time):
            modified_timestamp_value += (new_modification_time-last_scrawled_time).total_seconds()
    return modified_timestamp_value

def GetFilePrams(full_path):
    mainData = {}
    extention = full_path[len(full_path)-(full_path[::-1].index(".")):]
    mainData['filePath'] = (full_path)
    mainData['root'] = ((full_path[::-1])[full_path[::-1].index('\\')+1:len(full_path)][::-1])
    mainData['file'] = ((full_path[::-1])[0:full_path[::-1].index('\\')][::-1])
    mainData['project_name'] = (full_path.split('\\')[project_name_start_index])
    mainData['extension'] = (extention)
    mainData['software'] ='Application'
    # check if extension has soft name in math dict
    if extention in extention_software_match_dict:
        mainData['software'] = (extention_software_match_dict[extention])
    mainData['ctime'] = (datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
    mainData['mtime'] = (datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
    mainData['existing_status'] = (True)
    mainData['last_scrawled_time'] = datetime.datetime.now()
    mainData['total_time'] = 0
    return mainData

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


def Check_File_Exists_UpdateDB(full_path):
    old_db_frame=pandas.read_csv(db_path, index_col=False)
    db_frame=old_db_frame
    file_in_db = full_path in list(db_frame['filePath'])
    total_time = 0
    if file_in_db:
        db_index = list(db_frame['filePath']).index(full_path)
        db_total_time = db_frame['total_time'][db_index]
        db_last_scrawled_time = db_frame['last_scrawled_time'][db_index]
        modified_time = ModificationTotalSecondsFromLastScrawledTime(full_path, datetime.datetime.fromisoformat(db_last_scrawled_time))
        total_time += modified_time + db_total_time

        db_frame['total_time'][db_index] = total_time
        db_frame['mtime'][db_index] = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
        db_frame['last_scrawled_time'][db_index]=datetime.datetime.now()
        
        print(total_time)
        # save 
        db_frame.to_csv(db_path, index=False)
        db_frame.to_excel(db_excel_path, index=False)
    else:
        # if file not exists in db
        file_params = GetFilePrams(full_path)
        add_db_row = pandas.DataFrame(file_params, index=[0])

        # concat new data
        new_df = pandas.concat([db_frame, add_db_row], ignore_index=True, axis=0)

        # save
        new_df.to_csv(db_path, index=False)
        new_df.to_excel(db_excel_path, index=False)


class Handler(watchdog.events.PatternMatchingEventHandler):
	def __init__(self):
		# Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.csv', '*.xls', '*.xlsx','*.dwg','*.rvt','*.EDB','*.nwd','*.pbix','*.FBD','*.doc','*.lir','*.spf'],
															ignore_directories=True, case_sensitive=False)

	def on_created(self, event):
		print("Watchdog received created event - % s" % event.src_path)
		# Event is created, you can process it now

	def on_modified(self, event):
		print("Watchdog received modified event - % s" % event.src_path)
		# Event is modified, you can process it now
		Check_File_Exists_UpdateDB(event.src_path)

	def on_deleted(self, event):
	    print("Watchdog received deleted event - % s" % event.src_path)

def WatchdogMain():
	src_path = "C:\\users\\rufai.demir\\Desktop"
	event_handler = Handler()
	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, path=src_path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

if __name__ == "__main__":

    p1 = Process(name='watchdog',target=WatchdogMain)
    p2 = Process(name='watchdog',target=UpdateScrawledTimeDBMain)

    p1.start()
    p2.start()