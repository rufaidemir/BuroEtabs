

import os, sys, time
import datetime
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas
pandas.options.mode.chained_assignment = None

suppprted_file_extensions = ['xlsx', 'xls', 'dwg', 'EDB']
root_path='C:\\Users\\RUFAI.DEMIR\\Desktop\\Rebar_Calc'

db_path = 'Scraw_Folder_to_DF.csv'

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
 

def total_second_from_datetime(date):
    return (date-datetime.datetime(1970,1,1)).total_seconds()


def Scraw_Folder_to_DF(folder_path):
    mainData ={
        "filePath":[],
        "root":[],
        "extension":[],
        "extension_exp":[],
        "ctime":[],
        "mtime":[],
    }
    for (root,dirs,files) in os.walk(folder_path):
        print (root)
        print (dirs)
        print (files)
        # print ('--------------------------------')
        for file in files:
            if len(str(file))>0 and "." in file:
                extention = file[len(file)-(file[::-1].index(".")):]
                print(root)
                if extention in suppprted_file_extensions:
                    full_path = root+'\\'+file
                    mainData['filePath'].append(full_path)
                    mainData['root'].append(root)
                    mainData['extension'].append(extention)
                    mainData['extension_exp'].append("will be added")
                    mainData['ctime'].append(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
                    mainData['mtime'].append(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
    df = pandas.DataFrame(mainData)
    return df



# ================================================================================================= MAIN STARTS HERE =================================================================================================
if __name__ == "__main__":
    db_exists= os.path.exists(db_path)
    if db_exists:
        # read db
        db_frame=pandas.read_csv(db_path, index_col=False)

        # swrawled frame
        # scraw_frame=Scraw_Folder_to_DF(root_path)

        for i in range(0,db_frame.shape[0]):
            mtime = db_frame['mtime'][i]
            full_path = db_frame['filePath'][i]
            file_is_exists=os.path.exists(full_path)
            if file_is_exists:
                last_scrawled_time = datetime.datetime.fromisoformat(db_frame['last_scrawled_time'][i])
                new_modification_time=datetime.datetime.fromtimestamp((os.path.getmtime(full_path)))
                modified_timestamp_value = 0
            
                # eger son modification time son tarama tarihinden buyuk ise farkini alaraak total sutunuxu gunceller, eger son tarama zamani lastmtime dan buyuk ise pass 
                if total_second_from_datetime(new_modification_time)>=total_second_from_datetime(last_scrawled_time):
                    modified_timestamp_value = (new_modification_time-datetime.datetime.fromisoformat(db_frame['mtime'][i])).total_seconds()
                db_frame['total_time'][i] = db_frame['total_time'][i]+ modified_timestamp_value
                db_frame['mtime'][i] = new_modification_time
            else:
                pass
        db_frame['last_scrawled_time'] = unix_time_to_datetime(now)
        db_frame.to_csv(db_path, index=False)
        print(db_frame)
        # print("============================================================================================== LOOP COMPLETED ====================================================================================================")

    else:
        first_db = Scraw_Folder_to_DF(root_path)
        first_db['last_scrawled_time'] = unix_time_to_datetime(now)
        first_db['total_time'] =0.0
        first_db.to_csv(db_path, index=False)
        print('-------------------------------- YENI DB OLUSTURULDU ----------------------------------------------------')
        print(first_db)

# print('=-=-today uniz', datetime.now())