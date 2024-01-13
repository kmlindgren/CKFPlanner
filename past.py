import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3 as lite
from datetime import date


def Past():
    conn = lite.connect("CKF.db")
    cur = conn.cursor()

    past_root = tk.Tk()

    past_root.state('zoomed')
    past_root.geometry('800x600')
    past_root.title('Past Schedules')
    # past_root.iconbitmap('CKF_image.ico')

    lblframe = Frame(past_root)
    tableframe = Frame(past_root)
    homescheduleframe = Frame(past_root)

    lblframe.pack()
    tableframe.pack()
    homescheduleframe.pack()

    sundaylbl = Label(lblframe, text='Which past schedule would you like to see?',
                      height=15, font=('Calibri light', 13, 'bold'))
    sundaylbl.grid(row=1, column=1)

    scroll_vert = Scrollbar(tableframe)
    scroll_vert.pack(side=RIGHT, fill=Y)

    scroll_horizon = Scrollbar(tableframe, orient='horizontal')
    scroll_horizon.pack(side=BOTTOM, fill=X)

    # Create table frame
    pasttable = ttk.Treeview(tableframe, yscrollcommand=scroll_vert.set,
                         xscrollcommand=scroll_horizon.set)

    pasttable.pack()

    scroll_vert.config(command=pasttable.yview)
    scroll_horizon.config(command=pasttable.xview)

    # define columns
    pasttable['columns'] = ('month', 'day', 'year')

    # Format columns
    pasttable.column("#0", width=0, stretch=NO)
    pasttable.column("month", anchor=CENTER, width=80)
    pasttable.column("day", anchor=CENTER, width=80)
    pasttable.column("year", anchor=CENTER, width=80)

    # Create Headings
    pasttable.heading("#0", text="", anchor=CENTER)
    pasttable.heading("month", text="Month", anchor=CENTER)
    pasttable.heading("day", text="Day", anchor=CENTER)
    pasttable.heading("year", text="Year", anchor=CENTER)

    def update_past_table():
        pasttable.delete(*pasttable.get_children())

        cur.execute('SELECT DISTINCT Sunday FROM MusicianSchedule')
        results = cur.fetchall()

        for row in results:
            strdate = ''.join(row)
            splitdate = strdate.split('-')
            m = int(splitdate[1])
            d = int(splitdate[2])
            y = int(splitdate[0])
            sundaydate = date(y, m, d)
            today = date.today()
            if sundaydate < today:
                if m == 1:
                    m = 'January'
                elif m == 2:
                    m = 'February'
                elif m == 3:
                    m = 'March'
                elif m == 4:
                    m = 'April'
                elif m == 5:
                    m = 'May'
                elif m == 6:
                    m = 'June'
                elif m == 7:
                    m = 'July'
                elif m == 8:
                    m = 'August'
                elif m == 9:
                    m = 'September'
                elif m == 10:
                    m = 'October'
                elif m == 11:
                    m = 'November'
                elif m == 12:
                    m = 'December'
                dates = (m, d, y)
                pasttable.insert("", tk.END, values=dates)

    update_past_table()

    def num_to_month(month):
        if month == '01':
            month = 'January'
        elif month == '02':
            month = 'February'
        elif month == '03':
            month = 'March'
        elif month == '04':
            month = 'April'
        elif month == '05':
            month = 'May'
        elif month == '06':
            month = 'June'
        elif month == '07':
            month = 'July'
        elif month == '08':
            month = 'August'
        elif month == '09':
            month = 'September'
        elif month == '10':
            month = 'October'
        elif month == '11':
            month = 'November'
        elif month == '12':
            month = 'December'
        return month

    def month_to_num(month):
        if month == 'January':
            month = '01'
        elif month == 'February':
            month = '02'
        elif month == 'March':
            month = '03'
        elif month == 'April':
            month = '04'
        elif month == 'May':
            month = '05'
        elif month == 'June':
            month = '06'
        elif month == 'July':
            month = '07'
        elif month == 'August':
            month = '08'
        elif month == 'September':
            month = '09'
        elif month == 'October':
            month = '10'
        elif month == 'November':
            month = '11'
        elif month == 'December':
            month = '12'
        return month

    def get_values():
        selected = pasttable.focus()
        values = pasttable.item(selected, 'values')
        return values

    def tup_to_str():
        tupledate = get_values()
        month = tupledate[0]
        day = tupledate[1]
        year = tupledate[2]

        num_to_month(month)

        date = f'{month} {day}, {year}'
        return date

    def view_past_schedule():
        past_schedule_root = tk.Tk()

        past_schedule_root.state('zoomed')
        past_schedule_root.geometry('800x600')
        past_schedule_root.title('Plan')
        # past_schedule_root.iconbitmap('CKF_image.ico')

        infoframe = Frame(past_schedule_root)
        tablesframe = Frame(past_schedule_root)
        mustableframe = Frame(tablesframe)
        songtableframe = Frame(tablesframe)
        viewbtnframe = Frame(past_schedule_root)
        exitframe = Frame(past_schedule_root)

        infoframe.pack()
        tablesframe.pack()
        mustableframe.pack(side='left')
        songtableframe.pack(side='right')
        viewbtnframe.pack()
        exitframe.pack()

        infolbl = Label(infoframe, text=f'Schedule for {tup_to_str()}', height=5,
                        font=('Calibri light', 13, 'bold'))
        infolbl.pack()

        def mus_table():
            tupledate = get_values()
            scheduledate = date(int(tupledate[2]), int(month_to_num(tupledate[0])), int(tupledate[1]))

            muslbl = Label(mustableframe, text='Musicians')
            muslbl.pack()

            mus_scroll_vert = Scrollbar(mustableframe)
            mus_scroll_vert.pack(side=RIGHT, fill=Y, padx=(0, 40))

            mus_scroll_horizon = Scrollbar(mustableframe, orient='horizontal')
            mus_scroll_horizon.pack(side=BOTTOM, fill=X)

            # Create table frame
            musiciantable = ttk.Treeview(mustableframe, yscrollcommand=scroll_vert.set,
                                         xscrollcommand=mus_scroll_horizon.set)

            musiciantable.pack()

            mus_scroll_vert.config(command=musiciantable.yview)
            mus_scroll_horizon.config(command=musiciantable.xview)

            # define columns
            musiciantable['columns'] = ('fname', 'lname', 'email')

            # Format columns
            musiciantable.column("#0", width=0, stretch=NO)
            musiciantable.column("fname", anchor=CENTER, width=100)
            musiciantable.column("lname", anchor=CENTER, width=125)
            musiciantable.column("email", anchor=CENTER, width=200)

            # Create Headings
            musiciantable.heading("#0", text="", anchor=CENTER)
            musiciantable.heading("fname", text="First Name", anchor=CENTER)
            musiciantable.heading("lname", text="Last Name", anchor=CENTER)
            musiciantable.heading("email", text="Email", anchor=CENTER)

            def update_musician_table():
                musiciantable.delete(*musiciantable.get_children())

                cur.execute(
                    'SELECT DISTINCT FirstName, LastName, Email FROM Musician INNER JOIN MusicianSchedule ON Musician.MusicianID '
                    '= MusicianSchedule.MusicianID WHERE Sunday = ?', (str(scheduledate),))
                results = cur.fetchall()

                for row in results:
                    musiciantable.insert("", tk.END, values=row)

            update_musician_table()

            def view_mus_instr():
                try:
                    selected = musiciantable.focus()
                    values = musiciantable.item(selected, 'values')
                    fname = values[0]
                    lname = values[1]
                    email = values[2]
                    cur.execute('SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ? AND Email = ?',
                                (fname, lname, email))
                    tuplemusid = cur.fetchone()
                    strmusid = ''.join([str(id) for id in tuplemusid])
                    cur.execute(
                        'SELECT Instrument FROM Instrument INNER JOIN MusicianSchedule ON Instrument.InstrumentID = '
                        'MusicianSchedule.InstrumentID WHERE MusicianID = ? AND Sunday = ?',
                        (int(strmusid), str(scheduledate)))
                    results = cur.fetchall()

                    instrlist = []
                    for instrument in results:
                        instrlist.append(instrument)

                    def list_to_string(list):
                        string = ''
                        for item in list:
                            instr = str(item).replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                            string += f'\n{instr}'
                        return string

                    messagebox.showinfo("Musician's Instruments",
                                        f"Instrument(s) that this musician played:{list_to_string(instrlist)}",
                                        parent=past_schedule_root)

                except IndexError:
                    messagebox.showinfo('', 'Please select a musician to view their instruments.',
                                        parent=past_schedule_root)

            viewmusinstrbtn = Button(viewbtnframe, bg='#5F388C', fg='white', text='View Musician Instrument(s)',
                                     command=view_mus_instr)
            viewmusinstrbtn.grid(column=0, row=0, padx=5, pady=5)

            fillerlbl = Label(viewbtnframe, text='')
            fillerlbl.grid(column=1, row=0, padx=225)

        def song_table():
            tupledate = get_values()
            scheduledate = date(int(tupledate[2]), int(month_to_num(tupledate[0])), int(tupledate[1]))

            songlbl = Label(songtableframe, text='Songs')
            songlbl.pack()

            song_scroll_vert = Scrollbar(songtableframe)
            song_scroll_vert.pack(side=RIGHT, fill=Y)

            song_scroll_horizon = Scrollbar(songtableframe, orient='horizontal')
            song_scroll_horizon.pack(side=BOTTOM, fill=X, padx=(20, 0))

            # Create table frame
            songtable = ttk.Treeview(songtableframe, yscrollcommand=scroll_vert.set,
                                     xscrollcommand=song_scroll_horizon.set)

            songtable.pack(padx=(20, 0))

            scroll_vert.config(command=songtable.yview)
            scroll_horizon.config(command=songtable.xview)

            # define columns
            songtable['columns'] = ('title')

            # Format columns
            songtable.column("#0", width=0, stretch=NO)
            songtable.column("title", anchor=CENTER, width=200)

            # Create Headings
            songtable.heading("#0", text="", anchor=CENTER)
            songtable.heading("title", text="Title", anchor=CENTER)

            def update_song_table():
                songtable.delete(*songtable.get_children())

                cur.execute(
                    'SELECT Title FROM Song INNER JOIN SongSchedule ON Song.SongID '
                    '= SongSchedule.SongID WHERE Sunday = ?', (str(scheduledate),))
                results = cur.fetchall()

                for row in results:
                    songtable.insert("", tk.END, values=row)

            update_song_table()


            exitbtn = Button(exitframe, bg='#5F388C', fg='white', text='Exit', width=5,
                                     command=past_schedule_root.destroy)


            exitbtn.grid(column=0, row=1, padx=5, pady=5)

        mus_table()
        song_table()


    homebtn = Button(homescheduleframe, bg='#5F388C', fg='white', text='Home', command=past_root.destroy)
    schedulebtn = Button(homescheduleframe, bg='#5F388C', fg='white', text='View Schedule', command=view_past_schedule)

    homebtn.pack(side='left', padx=10)
    schedulebtn.pack(side='left', padx=10)

    past_root.mainloop()
