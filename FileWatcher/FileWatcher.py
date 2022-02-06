import os, sys, time, logging
import datetime
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas
pandas.options.mode.chained_assignment = None

extention_software_match_dict =  {
    'xlsx':'Excel',
    'xls':'Excel',
    'EDB':'Etaps',
    'dwg':'AutoCAD',
    'rvt':'Revit',
    'lir':'Lira-Sapr',
    'spf':'Lira-Sapfire',
    'dyn':'Dynamo',
    'nwd':'Navisworks'

}

exclude_folders = []
root_path='C:\\Users\\RUFAI.DEMIR\\Desktop'

db_path = 'C:\\Projeler\\PythonP\\BuroEtabs\\Scraw_Folder_to_DF.csv'

now = datetime.datetime.now().timestamp()

 
# convert unix time to datetime object
def unix_time_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time)

# convert datime object to unix time
def datetime_to_unix_time(datetime_obj):
    c_d_time=datetime_obj
    if type(datetime_obj)==str:
        c_d_time = datetime.datetime.strptime(datetime_obj)
    return int(time.mktime(c_d_time.timetuple()))
 

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


def Scraw_Folder_to_DF(folder_path):
    try:
        suppprted_file_extensions = list(extention_software_match_dict.keys())
        mainData ={
            "filePath":[],
            "root":[],
            "file":[],
            "extension":[],
            "software":[],
            "ctime":[],
            "mtime":[],
            "existing_status":[],
        }
        for (root,dirs,files) in os.walk(folder_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude_folders]
            # print ('--------------------------------')
            for file in files:
                if len(str(file))>0 and "." in file:
                    extention = file[len(file)-(file[::-1].index(".")):]
                    if extention in suppprted_file_extensions:
                        full_path = root+'\\'+file
                        mainData['filePath'].append(full_path)
                        mainData['root'].append(root)
                        mainData['file'].append(file)
                        mainData['extension'].append(extention)
                        # check if extension has soft name in math dict
                        mainData['software'].append(extention_software_match_dict[extention]) if extention in extention_software_match_dict else mainData['software'].append('Application')
                        mainData['ctime'].append(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
                        mainData['mtime'].append(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
                        mainData['existing_status'].append(True)

        df = pandas.DataFrame(mainData)
        df['last_scrawled_time'] = unix_time_to_datetime(now)
        df['total_time'] =0.0
        return df
    except Exception as hata:
        print('Bir hata alindi, HATA ', hata)
        raise hata

 
def Main_Scraw_Directory():
    new_df = Scraw_Folder_to_DF(root_path)
    db_frame=pandas.read_csv(db_path, index_col=False)

    for i in range(0,new_df.shape[0]):
        full_path = new_df['filePath'][i]
        file_in_db = full_path in list(db_frame['filePath'])
        total_time = 0
        if file_in_db:
            db_index = list(db_frame['filePath']).index(full_path)
            db_total_time = db_frame['total_time'][db_index]
            db_last_scrawled_time = db_frame['last_scrawled_time'][db_index]
            modified_time = ModificationTotalSecondsFromLastScrawledTime(full_path, datetime.datetime.fromisoformat(db_last_scrawled_time))
            total_time += modified_time + db_total_time
        new_df['total_time'][i]=total_time
    
    # this area for files that deleted or excluded until a certain time
    # TODO will be added a function change db file status for this area
    old_data={
            'filePath': [],
            'root': [],
            'file': [],
            'extension': [],
            'software': [],
            'ctime': [],
            'mtime': [],
            'last_scrawled_time': [],
            'total_time':[],
            'existing_status':[]
        }
    for j in range(len(db_frame)):
        if db_frame['filePath'][j] not in list(new_df['filePath']):
            old_data['filePath'].append(db_frame['filePath'][j])
            old_data['root'].append(db_frame['root'][j])
            old_data['file'].append(db_frame['file'][j])
            old_data['extension'].append(db_frame['extension'][j])
            old_data['software'].append(db_frame['software'][j])
            old_data['ctime'].append(db_frame['ctime'][j])
            old_data['mtime'].append(db_frame['mtime'][j])
            old_data['last_scrawled_time'].append(db_frame['last_scrawled_time'][j])
            old_data['total_time'].append(db_frame['total_time'][j])
            old_data['existing_status'].append(False)

    to_db_result_frame=new_df.append(pandas.DataFrame(old_data), ignore_index=True)
    to_db_result_frame.to_csv(db_path, index=False)



# ================================================================================================= MAIN STARTS HERE =================================================================================================
def Main():
    root_path_is_exists = os.path.exists(root_path)
    if not root_path_is_exists:
        raise Exception('\033[91m'+' HATA: root_path degiskenini kontrol edin'+'\033[0m')
    db_exists =  os.path.exists(db_path)
    start_time = datetime.datetime.now()
    if db_exists:
        print('\033[95m'+'DB EXISTS SCRAWLING...'+'\033[0m')
        Main_Scraw_Directory()
    else:
        print('\033[95m'+'DB DOES NOT EXISTS INITIALIZING...'+'\033[0m')
        initial_df = Scraw_Folder_to_DF(root_path)
        initial_df.to_csv(db_path)
    
    end_time = datetime.datetime.now()
    loop_time =  ((end_time-start_time).total_seconds()/60)



    print('\033[93m'+'SCRAWLING COMPLETED IN '+'\033[0m')
    print('                                                        START TIME  : ', start_time)
    print('                                                        FINISH TIME : ', end_time)
    print('                                                      TOTAL SECONDS : '+str(" %.3f"%loop_time))

    logging.info('SCRAWLING COMPLETED IN')
    logging.info('                                                        START TIME  : '+ start_time.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info('                                                        FINISH TIME : '+ end_time.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info('                                                      TOTAL SECONDS : '+str(" %.3f"%loop_time))


while True:
    Main()
    time.sleep(10)


