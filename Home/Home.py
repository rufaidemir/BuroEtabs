import os, sys
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk





window = tk.Tk()
window.iconbitmap('C:\\Users\\rufai\\Projects\\pythonP\\BuroEtabs\\media\\bs_logo.ico')
window.geometry('800x400')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

def show_frame(frame):
    frame.tkraise()



homeFrame =  tk.Frame(window, bg='#404040')
frame2 =  tk.Frame(window, bg='blue')
frame3 =  tk.Frame(window, bg='green')


for frame in (homeFrame, frame2, frame3):
    frame.grid(row=0, column=0, sticky='nsew')



# example
# frame1_title=tk.Label(frame1, text="frame1")
# frame1_title.pack()

# =================================== Home Frame ==============================================
go_data_transfer_btn = tk.Button(homeFrame, text="VERI AKTARIMI", command= lambda: show_frame(frame2), pady=5, background="#505050", font=('Arial', 12 ), foreground='white', padx=10)
go_data_transfer_btn.grid(row=0, column=0, sticky='nsew')
# go_data_transfer_btn.pack()


go_columns_btn = tk.Button(homeFrame, text="KOLON",  command= lambda: show_frame(frame2), pady=5, background="#505050", font=('Arial', 12 ), foreground='white', padx=10).grid(row=0, column=1, sticky='sw')
# go_columns_btn.pack()


go_beams_btn = tk.Button(homeFrame, text="KIRIS",  command= lambda: show_frame(frame2), pady=5, background="#505050", font=('Arial', 12 ), foreground='white', padx=10).grid(row=0, column=2)
# go_beams_btn.pack()



go_wall_btn = tk.Button(homeFrame, text="PERDE",  command= lambda: show_frame(frame2), pady=5, background="#505050", font=('Arial', 12 ), foreground='white', padx=10).grid(row=0, column=3)
# go_wall_btn.pack()


show_frame(homeFrame)
window.mainloop()