import os, sys, time, logging
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas

class WatcherPropper:
    """ 
    This class scrawls the directori and returns pandas dataframe
    """
    def __init__(self, scrawling_directory, exlude_folders=[], exlude_extensions=[]):
        self.scrawle_directory = scrawling_directory
        self.exlude_folders =exlude_folders
        self.exlude_extensions =exlude_extensions
        
        if not os.path.isdir(scrawling_directory):
            raise ValueError(f"'{scrawling_directory}' is not a directory")

    def ScrawleDirectory(self):
        try:
            mainData ={
            "filePath":[],
            "root":[],
            "file":[],
            "extension":[],
            "ctime":[],
            "mtime":[],
            "size":[],
            "existing_status":[],
            }
            for (root,dirs,files) in os.walk(self.scrawle_directory, topdown=True):
                dirs[:] = [d for d in dirs if d not in self.exlude_folders]
                # print ('--------------------------------')
                for file in files:
                    if len(str(file))>0 and "." in file:
                        try:
                            extention = file[len(file)-(file[::-1].index(".")):]
                        except Exception as hata:
                            print('File has no extension')
                            extention=''

                        if extention not in self.exlude_extensions:
                            full_path = root+'\\'+file
                            mainData['filePath'].append(full_path)
                            mainData['root'].append(root)
                            mainData['file'].append(file)
                            mainData['extension'].append(extention)
                            # check if extension has soft name in math dict
                            mainData['ctime'].append(os.path.getctime(full_path))
                            mainData['mtime'].append(os.path.getmtime(full_path))
                            mainData['size'].append(os.path.getsize(full_path))
                            mainData['existing_status'].append(True)

            df = pandas.DataFrame(mainData)
            print(df)
            return df
        except Exception as hata:
            print('Bir hata alindi, HATA ', hata)
            raise hata



a = WatcherPropper(scrawling_directory='C:\\Users\\rufai\\Downloads')

df = a.ScrawleDirectory()
df.to_csv('Scraw_Folder_to_DF.csv')

import pprint


 