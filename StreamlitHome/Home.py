import streamlit as st

import datetime
import pandas
import time


st.write('Dosya İzleme')

df = pandas.read_csv('C:\\Projeler\\PythonProj\\BuroEtabs\\Scraw_Folder_to_DF.csv')



# c time filter
st.sidebar.title('Olusturulma')
start_date = datetime.datetime.fromtimestamp((df['ctime'].min()))
end_date = datetime.datetime.fromtimestamp((df['ctime'].max()))

s_time = st.sidebar.date_input(label='Start Date', value=start_date, key = 'cs')
f_time = st.sidebar.date_input(label='End Date', value=end_date, key = 'cer')

a= time.mktime(s_time.timetuple())
b= time.mktime(f_time.timetuple())
df = df[(df['ctime']>=a) & (df['ctime']<=b)]




# m time filter
st.sidebar.title('Guncellenme Tarihi')
start_date_m = datetime.datetime.fromtimestamp((df['mtime'].min()))
end_date_m = datetime.datetime.fromtimestamp((df['mtime'].max()))

s_time_m = st.sidebar.date_input(label='Start Date', value=start_date_m, key='ms')
f_time_m = st.sidebar.date_input(label='End Date', value=end_date_m, key='me')

a_m= time.mktime(s_time_m.timetuple())
b_m= time.mktime(f_time_m.timetuple())
df = df[(df['mtime']>=a_m) & (df['mtime']<=b_m)]



selected_extensitons = st.sidebar.multiselect(label='UZANTI', options=df['extension'].unique(), default=df['extension'].unique())
df = df[df['extension'].isin(selected_extensitons)]

print(selected_extensitons)



st.title('Toplam Boyut')
st.title(str(round(df['size'].sum()/(1024*1024),2))+' MB')
print(list(df))
