import tkinter as tk
import sqlite3 as lite
from tkinter import ttk
from tkinter import *
from datetime import date, timedelta
from tkinter import messagebox
import functools
#  bg='#5F388C', fg='white',


def Home():
    conn = lite.connect("CKF.db")
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS "Musician" ( "MusicianID" INTEGER NOT NULL, "FirstName" TEXT NOT NULL, "LastName" TEXT NOT NULL, "Email" TEXT NOT NULL, "Phone" TEXT, PRIMARY KEY("MusicianID") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "Instrument" ( "InstrumentID" INTEGER NOT NULL, "Instrument" TEXT NOT NULL UNIQUE, PRIMARY KEY("InstrumentID" AUTOINCREMENT) )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "MusicianInstruments" ( "MusicianID" INTEGER NOT NULL, "InstrumentID" INTEGER NOT NULL, FOREIGN KEY("InstrumentID") REFERENCES "Instrument"("InstrumentID"), FOREIGN KEY("MusicianID") REFERENCES "Musician"("MusicianID"), PRIMARY KEY("InstrumentID","MusicianID") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "Song" ( "SongID" INTEGER NOT NULL, "Title" TEXT NOT NULL, "Songwriter" TEXT, "Pages" INTEGER, "KeySig" BLOB, "TimeSig" TEXT, PRIMARY KEY("SongID" AUTOINCREMENT) )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "Theme" ( "ThemeID" INTEGER NOT NULL, "Theme" TEXT NOT NULL, PRIMARY KEY("ThemeID" AUTOINCREMENT) )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "SongScripture" ( "SongID" INTEGER, "Book" TEXT, "ChapVerse" TEXT, FOREIGN KEY("SongID") REFERENCES "Song"("SongID"), PRIMARY KEY("SongID","Book","ChapVerse") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "SongTheme" ( "SongID" INTEGER NOT NULL, "ThemeID" INTEGER NOT NULL, FOREIGN KEY("SongID") REFERENCES "Song"("SongID"), PRIMARY KEY("SongID","ThemeID"), FOREIGN KEY("ThemeID") REFERENCES "Theme"("ThemeID") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "InstrumentReq" ( "SongID" INTEGER, "InstrumentID" INTEGER, PRIMARY KEY("SongID","InstrumentID"), FOREIGN KEY("SongID") REFERENCES "Song"("SongID") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "MusicianSchedule" ( "MusicianID" INTEGER, "InstrumentID" INTEGER, "Sunday" TEXT, FOREIGN KEY("InstrumentID") REFERENCES "Instrument"("InstrumentID"), FOREIGN KEY("MusicianID") REFERENCES "Musician"("MusicianID"), PRIMARY KEY("MusicianID","Sunday","InstrumentID") )')
    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS "SongSchedule" ( "SongID" INTEGER, "Sunday" TEXT, PRIMARY KEY("SongID","Sunday"), FOREIGN KEY("SongID") REFERENCES "Song"("SongID") )')
    conn.commit()

    root = tk.Tk()

    root.state('zoomed')
    root.geometry('800x600')
    root.title('Home')
    # root.iconbitmap('CKF_image.ico')

    welcomeframe = Frame(root)
    planframe = Frame(root)
    pastframe = Frame(root)
    musicianframe = Frame(root)
    songframe = Frame(root)

    welcomeframe.pack()
    planframe.pack()
    pastframe.pack()
    musicianframe.pack()
    songframe.pack()

    # FUTURE MODULE
    #
    #
    #
    #
    #
    def Future():
        conn = lite.connect("CKF.db")
        cur = conn.cursor()

        future_root = tk.Tk()

        future_root.state('zoomed')
        future_root.geometry('800x600')
        future_root.title('Plan')
        # future_root.iconbitmap('CKF_image.ico')

        lblframe = Frame(future_root)
        tableframe = Frame(future_root)
        btnframe = Frame(future_root)

        lblframe.pack()
        tableframe.pack()
        btnframe.pack()

        sundaylbl = Label(lblframe, text='Which Sunday would you like to plan?',
                          height=15, font=('Calibri light', 13, 'bold'))
        sundaylbl.grid(row=1, column=1)

        scroll_vert = Scrollbar(tableframe)
        scroll_vert.pack(side=RIGHT, fill=Y)

        scroll_horizon = Scrollbar(tableframe, orient='horizontal')
        scroll_horizon.pack(side=BOTTOM, fill=X)

        # Create table frame
        table = ttk.Treeview(tableframe, yscrollcommand=scroll_vert.set,
                             xscrollcommand=scroll_horizon.set)

        table.pack()

        scroll_vert.config(command=table.yview)
        scroll_horizon.config(command=table.xview)

        # define columns
        table['columns'] = ('month', 'day', 'year')

        # Format columns
        table.column("#0", width=0, stretch=NO)
        table.column("month", anchor=CENTER, width=80)
        table.column("day", anchor=CENTER, width=80)
        table.column("year", anchor=CENTER, width=80)

        # Create Headings
        table.heading("#0", text="", anchor=CENTER)
        table.heading("month", text="Month", anchor=CENTER)
        table.heading("day", text="Day", anchor=CENTER)
        table.heading("year", text="Year", anchor=CENTER)

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

        def sundays():
            def allsundays(year):
                d = date(year, 1, 1)
                d += timedelta(days=6 - d.weekday())
                while d.year == year or d.year == year + 1:
                    yield d
                    d += timedelta(days=7)

            sundaylist = []

            current_year = int(date.today().strftime("%Y"))

            for d in allsundays(current_year):
                sundaylist.append(d)

            for i in sundaylist:
                today = date.today()
                y = i.strftime('%Y')
                m = i.strftime('%B')
                d = i.strftime('%d')
                if i > today:
                    dates = (m, d, y)
                    table.insert("", tk.END, values=dates)

        sundays()

        def get_values():
            selected = table.focus()
            values = table.item(selected, 'values')
            return values

        def tup_to_str():
            tupledate = get_values()
            month = tupledate[0]
            day = tupledate[1]
            year = tupledate[2]

            date = f'{month} {day}, {year}'
            return date

        def new_schedule():
            if table.focus() != '':
                tupledate = get_values()
                scheduledate = date(int(tupledate[2]), int(month_to_num(tupledate[0])), int(tupledate[1]))
                cur.execute(
                    'SELECT MusicianSchedule.Sunday FROM MusicianSchedule INTERSECT SELECT SongSchedule.Sunday FROM SongSchedule')
                results = cur.fetchall()
                sundays = str(results)

                def new_schedule_plan():
                    new_schedule_root = tk.Tk()

                    new_schedule_root.state('zoomed')
                    new_schedule_root.geometry('800x600')
                    new_schedule_root.title('Plan')
                    # new_schedule_root.iconbitmap('CKF_image.ico')

                    infoframe = Frame(new_schedule_root)
                    tablesframe = Frame(new_schedule_root)
                    mustableframe = Frame(tablesframe)
                    songtableframe = Frame(tablesframe)
                    btnframe = Frame(new_schedule_root)
                    exitframe = Frame(new_schedule_root)

                    infoframe.pack()
                    tablesframe.pack()
                    mustableframe.pack(side='left')
                    songtableframe.pack(side='right')
                    btnframe.pack()
                    exitframe.pack()

                    infolbl = Label(infoframe, text=f'Create a schedule for {tup_to_str()}', height=5,
                                    font=('Calibri light', 13, 'bold'))
                    infolbl.pack()

                    def mus_table():
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
                        musiciantable['columns'] = ('id', 'fname', 'lname', 'email')

                        # Format columns
                        musiciantable.column("#0", width=0, stretch=NO)
                        musiciantable.column("id", anchor=CENTER, width=80)
                        musiciantable.column("fname", anchor=CENTER, width=100)
                        musiciantable.column("lname", anchor=CENTER, width=125)
                        musiciantable.column("email", anchor=CENTER, width=200)

                        # Create Headings
                        musiciantable.heading("#0", text="", anchor=CENTER)
                        musiciantable.heading("id", text="ID", anchor=CENTER)
                        musiciantable.heading("fname", text="First Name", anchor=CENTER)
                        musiciantable.heading("lname", text="Last Name", anchor=CENTER)
                        musiciantable.heading("email", text="Email", anchor=CENTER)

                        def update_musician_table():
                            musiciantable.delete(*musiciantable.get_children())

                            cur.execute(
                                'SELECT DISTINCT Musician.MusicianID, FirstName, LastName, Email FROM Musician INNER JOIN MusicianSchedule ON Musician.MusicianID '
                                '= MusicianSchedule.MusicianID WHERE Sunday = ?', (str(scheduledate),))
                            results = cur.fetchall()

                            for row in results:
                                musiciantable.insert("", tk.END, values=row)

                        def view_mus_instr():
                            try:
                                selected = musiciantable.focus()
                                values = musiciantable.item(selected, 'values')
                                fname = values[1]
                                lname = values[2]
                                email = values[3]
                                cur.execute(
                                    'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ? AND Email = ?',
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
                                        instr = str(item).replace('(', '').replace(')', '').replace(',', '').replace(
                                            "'", '')
                                        string += f'\n{instr}'
                                    return string

                                messagebox.showinfo("Musician's Instruments",
                                                    f"Musician's Instruments:{list_to_string(instrlist)}",
                                                    parent=new_schedule_root)

                            except IndexError:
                                messagebox.showinfo('', 'Please select a musician to view their instruments.',
                                                    parent=new_schedule_root)

                        def del_mus():
                            selected = musiciantable.focus()
                            if selected != '':
                                sure = messagebox.askyesno('',
                                                           "This action will remove this musician from this schedule. "
                                                           "Are you sure you'd like to continue?",
                                                           parent=new_schedule_root)
                                if sure:
                                    values = musiciantable.item(selected, 'values')
                                    musiciantable.delete(selected)
                                    # Delete From Database
                                    cur.execute("DELETE from MusicianSchedule WHERE MusicianID = ? AND Sunday = ?",
                                                (values[0], scheduledate))

                                    # Commit changes
                                    conn.commit()

                                    update_musician_table()

                                    messagebox.showinfo('Successfully Completed', 'Musician was successfully deleted.',
                                                        parent=new_schedule_root)
                            else:
                                messagebox.showinfo('',
                                                    'Please select a musician to delete from the schedule, and then click the "Delete Musician" button.')

                        viewmusinstrbtn = Button(btnframe, bg='#5F388C', fg='white', text='View Musician Instrument(s)',
                                                 command=view_mus_instr)
                        viewmusinstrbtn.grid(column=2, row=0, padx=5, pady=10)

                        delmusicianbtn = Button(btnframe, bg='#5F388C', fg='white', text='Delete Musician',
                                                command=del_mus)
                        delmusicianbtn.grid(column=3, row=0, padx=(5, 125), pady=10)

                        def musician():
                            add_musician_root = tk.Tk()

                            add_musician_root.geometry('300x200')
                            add_musician_root.title('Add Musician')
                            # add_musician_root.iconbitmap('CKF_image.ico')

                            musicianframe = Frame(add_musician_root)
                            instrframe = Frame(add_musician_root)
                            addbtnframe = Frame(add_musician_root)
                            cancelsavebtnframe = Frame(add_musician_root)

                            musicianframe.pack()
                            instrframe.pack()
                            addbtnframe.pack()
                            cancelsavebtnframe.pack()

                            def mus_combo():
                                musinstrlist = ['Pick an instrument']
                                muslist = ['Pick a musician']

                                cur.execute('SELECT FirstName, LastName FROM Musician')
                                results = cur.fetchall()

                                for i in results:
                                    muslist.append(i)

                                musinstrbox = ttk.Combobox(instrframe, values=musinstrlist)
                                musinstrbox.set(musinstrlist[0])

                                musbox = ttk.Combobox(musicianframe, values=muslist)
                                musbox.pack(pady=5)

                                musinstrbox.pack(padx=5, pady=3)

                                def update_instr(event):
                                    name = musbox.get()
                                    musinstrlist = ['Pick an instrument']
                                    if name != 'Pick a musician' and name != '':
                                        nametuple = tuple(name.split(' '))
                                        fname = str(nametuple[0])
                                        lname = str(nametuple[1])
                                        cur.execute(
                                            'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ?',
                                            (fname, lname))
                                        musid = cur.fetchone()

                                        cur.execute(
                                            'SELECT Instrument FROM Instrument INNER JOIN MusicianInstruments ON MusicianInstruments.InstrumentID = Instrument.InstrumentID '
                                            'INNER JOIN Musician ON Musician.MusicianID = MusicianInstruments.MusicianID WHERE MusicianInstruments.MusicianID = ?',
                                            musid)

                                        musinstr = cur.fetchall()

                                        for instrument in musinstr:
                                            strinstr = str(instrument).replace('{', '').replace('}', '').replace('(',
                                                                                                                 '').replace(
                                                ')', '').replace(',', '').replace("'", '')
                                            musinstrlist.append(strinstr)

                                        musinstrbox.config(values=musinstrlist)
                                        musinstrbox.set(value=musinstrlist[0])

                                musbox.current(0)
                                musbox.bind("<<ComboboxSelected>>", update_instr)

                                def add_instr():
                                    name = musbox.get()
                                    musinstrlist = ['Pick an instrument']
                                    if name != 'Pick a musician' and name != '':
                                        nametuple = tuple(name.split(' '))
                                        fname = str(nametuple[0])
                                        lname = str(nametuple[1])
                                        cur.execute(
                                            'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ?',
                                            (fname, lname))
                                        musid = cur.fetchone()

                                        cur.execute(
                                            'SELECT Instrument FROM Instrument INNER JOIN MusicianInstruments ON MusicianInstruments.InstrumentID = Instrument.InstrumentID '
                                            'INNER JOIN Musician ON Musician.MusicianID = MusicianInstruments.MusicianID WHERE MusicianInstruments.MusicianID = ?',
                                            musid)

                                        musinstr = cur.fetchall()

                                        for instrument in musinstr:
                                            strinstr = str(instrument).replace('{', '').replace('}', '').replace('(',
                                                                                                                 '').replace(
                                                ')', '').replace(',', '').replace("'", '')
                                            musinstrlist.append(strinstr)

                                        newmusinstrbox = ttk.Combobox(instrframe, values=musinstrlist)
                                        newmusinstrbox.set(value=musinstrlist[0])
                                        newmusinstrbox.pack(pady=3)

                                def add_mus():
                                    muswidget = musicianframe.winfo_children()
                                    instrwidgets = instrframe.winfo_children()

                                    for mwidget in muswidget:
                                        if isinstance(mwidget, ttk.Combobox):
                                            if mwidget.get() != 'Pick a musician':
                                                nametuple = tuple(mwidget.get().split(' '))
                                                fname = str(nametuple[0])
                                                lname = str(nametuple[1])
                                                cur.execute(
                                                    'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ?',
                                                    (fname, lname))
                                                musid = cur.fetchone()
                                                for iwidget in instrwidgets:
                                                    if isinstance(iwidget, ttk.Combobox):
                                                        if iwidget.get() != 'Pick an instrument':
                                                            cur.execute(
                                                                'SELECT InstrumentID FROM Instrument WHERE Instrument = ?',
                                                                (iwidget.get(),))
                                                            instrid = cur.fetchone()
                                                            strmusid = ''.join([str(id) for id in musid])
                                                            strinstrid = ''.join([str(id) for id in instrid])
                                                            cur.execute(
                                                                'SELECT * FROM MusicianSchedule WHERE Sunday = ?',
                                                                (scheduledate,))
                                                            this_schedule = cur.fetchall()
                                                            check_if_in = (
                                                            int(strmusid), int(strinstrid), str(scheduledate))
                                                            if check_if_in not in this_schedule:
                                                                cur.execute(
                                                                    'INSERT INTO MusicianSchedule VALUES (?, ?, ?)',
                                                                    (int(strmusid), int(strinstrid), str(scheduledate)))
                                                                conn.commit()
                                                update_musician_table()
                                                messagebox.showinfo('Successfully Completed',
                                                                    'Musician was successfully added to the schedule.',
                                                                    parent=add_musician_root)
                                                add_musician_root.destroy()
                                            else:
                                                messagebox.showinfo('',
                                                                    'Musician and Instrument must be selected to add a musician to the schedule.',
                                                                    parent=add_musician_root)

                                addinstrbtn = Button(addbtnframe, bg='#5F388C', fg='white', text='Add Instrument',
                                                     command=add_instr)
                                cancelmusbtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Cancel',
                                                      command=add_musician_root.destroy)
                                savemusbtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Save',
                                                    command=add_mus)

                                addinstrbtn.pack(pady=10)
                                cancelmusbtn.grid(column=0, row=0, padx=5)
                                savemusbtn.grid(column=1, row=0, padx=5)

                            mus_combo()

                        addmusicianbtn = Button(btnframe, bg='#5F388C', fg='white', text='Add Musician',
                                                command=musician)
                        addmusicianbtn.grid(column=1, row=0, padx=5, pady=10)

                        fillerlbl = Label(btnframe, text='')
                        fillerlbl.grid(column=0, row=0, padx=50)

                        def song_table():
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
                            songtable['columns'] = ('id', 'title')

                            # Format columns
                            songtable.column("#0", width=0, stretch=NO)
                            songtable.column("id", anchor=CENTER, width=80)
                            songtable.column("title", anchor=CENTER, width=200)

                            # Create Headings
                            songtable.heading("#0", text="", anchor=CENTER)
                            songtable.heading("id", text="ID", anchor=CENTER)
                            songtable.heading("title", text="Title", anchor=CENTER)

                            def update_song_table():
                                songtable.delete(*songtable.get_children())

                                cur.execute(
                                    'SELECT Song.SongID, Title FROM Song INNER JOIN SongSchedule ON Song.SongID '
                                    '= SongSchedule.SongID WHERE Sunday = ?', (str(scheduledate),))
                                results = cur.fetchall()

                                for row in results:
                                    songtable.insert("", tk.END, values=row)

                            update_song_table()

                            def del_song():
                                selected = songtable.focus()
                                if selected != '':
                                    sure = messagebox.askyesno('',
                                                               "This action will remove this song from this schedule. "
                                                               "Are you sure you'd like to continue?",
                                                               parent=new_schedule_root)
                                    if sure:
                                        values = songtable.item(selected, 'values')
                                        songtable.delete(selected)
                                        # Delete From Database
                                        cur.execute("DELETE from SongSchedule WHERE SongID = ? AND Sunday = ?",
                                                    (values[0], scheduledate))

                                        # Commit changes
                                        conn.commit()

                                        update_song_table()

                                        messagebox.showinfo('Successfully Completed', 'Song was successfully deleted.',
                                                            parent=new_schedule_root)
                                else:
                                    messagebox.showinfo('', 'Please select a song to delete from the schedule, '
                                                            'then click the "Delete Song" button.')

                            def song():
                                add_song_root = tk.Tk()

                                add_song_root.geometry('1400x700')
                                add_song_root.title('Add Song')
                                # add_song_root.iconbitmap('CKF_image.ico')

                                searchframe = Frame(add_song_root)
                                searchbtnframe = Frame(add_song_root)
                                songtableframe = Frame(add_song_root)
                                cancelsavebtnframe = Frame(add_song_root)
                                instrtableframe = Frame(add_song_root)
                                themetableframe = Frame(add_song_root)

                                searchframe.pack()
                                searchbtnframe.pack()
                                songtableframe.pack()
                                cancelsavebtnframe.pack()
                                instrtableframe.pack(side='left', padx=(400, 0), pady=(0, 100))
                                themetableframe.pack(side='right', padx=(0, 400), pady=(0, 100))

                                song_scroll_vert = Scrollbar(songtableframe)
                                song_scroll_vert.pack(side=RIGHT, fill=Y, pady=(20))

                                song_scroll_horizon = Scrollbar(songtableframe, orient='horizontal')
                                song_scroll_horizon.pack(side=BOTTOM, fill=X)

                                # Create table frame
                                songtable = ttk.Treeview(songtableframe, yscrollcommand=song_scroll_vert.set,
                                                         xscrollcommand=song_scroll_horizon.set)

                                songtable.pack(pady=(20, 0))

                                song_scroll_vert.config(command=songtable.yview)
                                song_scroll_horizon.config(command=songtable.xview)

                                # define columns
                                songtable['columns'] = ('songid', 'title', 'songwriter', 'pages', 'key', 'time')

                                # Format columns
                                songtable.column("#0", width=0, stretch=NO)
                                songtable.column("songid", anchor=CENTER, width=80)
                                songtable.column("title", anchor=CENTER, width=200)
                                songtable.column("songwriter", anchor=CENTER, width=200)
                                songtable.column("pages", anchor=CENTER, width=80)
                                songtable.column("key", anchor=CENTER, width=80)
                                songtable.column("time", anchor=CENTER, width=100)

                                # Create Headings
                                songtable.heading("#0", text="", anchor=CENTER)
                                songtable.heading("songid", text="Song ID", anchor=CENTER)
                                songtable.heading("title", text="Title", anchor=CENTER)
                                songtable.heading("songwriter", text="Songwriter", anchor=CENTER)
                                songtable.heading("pages", text="# of pages", anchor=CENTER)
                                songtable.heading("key", text="Key", anchor=CENTER)
                                songtable.heading("time", text="Time Signature", anchor=CENTER)

                                instr_scroll_vert = Scrollbar(instrtableframe)
                                instr_scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 0))

                                instr_scroll_horizon = Scrollbar(instrtableframe, orient='horizontal')
                                instr_scroll_horizon.pack(side=BOTTOM, fill=X, pady=(0, 10))

                                # Create table frame
                                instrtable = ttk.Treeview(instrtableframe, yscrollcommand=instr_scroll_vert.set,
                                                          xscrollcommand=instr_scroll_horizon.set)

                                instrtable.pack(pady=(30, 0))

                                instr_scroll_vert.config(command=instrtable.yview)
                                instr_scroll_horizon.config(command=instrtable.xview)

                                # define columns
                                instrtable['columns'] = ('id', 'title')

                                # Format columns
                                instrtable.column("#0", width=0, stretch=NO)
                                instrtable.column("id", anchor=CENTER, width=50)
                                instrtable.column("title", anchor=CENTER, width=200)

                                # Create Headings
                                instrtable.heading("#0", text="", anchor=CENTER)
                                instrtable.heading("id", text="ID", anchor=CENTER)
                                instrtable.heading("title", text="Title", anchor=CENTER)

                                theme_scroll_vert = Scrollbar(themetableframe)
                                theme_scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 0))

                                theme_scroll_horizon = Scrollbar(themetableframe, orient='horizontal')
                                theme_scroll_horizon.pack(side=BOTTOM, fill=X, pady=(0, 10))

                                # Create table frame
                                themetable = ttk.Treeview(themetableframe, yscrollcommand=theme_scroll_vert.set,
                                                          xscrollcommand=theme_scroll_horizon.set)

                                themetable.pack(pady=(30, 0))

                                theme_scroll_vert.config(command=themetable.yview)
                                theme_scroll_horizon.config(command=themetable.xview)

                                # define columns
                                themetable['columns'] = ('id', 'theme')

                                # Format columns
                                themetable.column("#0", width=0, stretch=NO)
                                themetable.column("id", anchor=CENTER, width=50)
                                themetable.column("theme", anchor=CENTER, width=200)

                                # Create Headings
                                themetable.heading("#0", text="", anchor=CENTER)
                                themetable.heading("id", text="ID", anchor=CENTER)
                                themetable.heading("theme", text="Theme", anchor=CENTER)

                                def update_song_table():
                                    songtable.delete(*songtable.get_children())

                                    cur.execute('SELECT * FROM Song ORDER BY Title')
                                    results = cur.fetchall()

                                    for row in results:
                                        songtable.insert("", tk.END, values=row)

                                def update_instr_table():
                                    instrtable.delete(*instrtable.get_children())

                                    cur.execute('SELECT * FROM Instrument')
                                    results = cur.fetchall()

                                    for row in results:
                                        instrtable.insert("", tk.END, values=row)

                                def update_theme_table():
                                    themetable.delete(*themetable.get_children())

                                    cur.execute('SELECT * FROM Theme')
                                    results = cur.fetchall()

                                    for row in results:
                                        themetable.insert("", tk.END, values=row)

                                update_song_table()
                                update_instr_table()
                                update_theme_table()

                                idlbl = Label(searchframe, text='ID:')
                                titlelbl = Label(searchframe, text='Title:')
                                songwriterlbl = Label(searchframe, text='Songwriter:')
                                pageslbl = Label(searchframe, text='# of pages:')
                                keylbl = Label(searchframe, text='Key:')
                                timelbl = Label(searchframe, text='Time Signature:')
                                instrlbl = Label(searchframe, text='Instrument Recommendation (ID):')
                                themelbl = Label(searchframe, text='Song Theme (ID):')

                                identry = Entry(searchframe, width=5)
                                titleentry = Entry(searchframe)
                                songwriterentry = Entry(searchframe)
                                pagesentry = Entry(searchframe, width=5)
                                keyentry = Entry(searchframe, width=5)
                                timeentry = Entry(searchframe, width=5)
                                instrentry = Entry(searchframe, width=5)
                                themeentry = Entry(searchframe, width=5)

                                idlbl.pack(side='left', padx=0, pady=(20, 0))
                                identry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                titlelbl.pack(side='left', padx=0, pady=(20, 0))
                                titleentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                songwriterlbl.pack(side='left', padx=0, pady=(20, 0))
                                songwriterentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                pageslbl.pack(side='left', padx=0, pady=(20, 0))
                                pagesentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                keylbl.pack(side='left', padx=0, pady=(20, 0))
                                keyentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                timelbl.pack(side='left', padx=0, pady=(20, 0))
                                timeentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                instrlbl.pack(side='left', padx=0, pady=(20, 0))
                                instrentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                themelbl.pack(side='left', padx=0, pady=(20, 0))
                                themeentry.pack(side='left', padx=(0, 5), pady=(20, 0))

                                def search_songs():
                                    id = identry.get()
                                    title = titleentry.get()
                                    songwriter = songwriterentry.get()
                                    pages = pagesentry.get()
                                    key = keyentry.get()
                                    time = timeentry.get()
                                    instr = instrentry.get()
                                    theme = themeentry.get()

                                    title = title.rstrip().upper()
                                    songwriter = songwriter.rstrip().upper()
                                    key = key.rstrip().upper()
                                    time = time.rstrip().upper()

                                    cur.execute(
                                        "SELECT DISTINCT Song.SongID, Title, Songwriter, Pages, KeySig, TimeSig "
                                        "FROM Song "
                                        "LEFT OUTER JOIN InstrumentReq ON Song.SongID = InstrumentReq.SongID "
                                        "LEFT OUTER JOIN SongTheme ON Song.SongID = SongTheme.SongID "
                                        "WHERE 1 "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Song.SongID) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Title) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Songwriter) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Pages) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(KeySig) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(TimeSig) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(InstrumentID) = ? END "
                                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(ThemeID) = ? END "
                                        "ORDER BY Title", (
                                            id, id, title, title, songwriter, songwriter, pages, pages, key, key, time,
                                            time, instr, instr, theme, theme))

                                    rows = cur.fetchall()

                                    songtable.delete(*songtable.get_children())

                                    for row in rows:
                                        songtable.insert(parent='', index='end', text='',
                                                         values=row)

                                searchbtn = Button(searchbtnframe, bg='#5F388C', fg='white', text='Search', width=5,
                                                   height=1,
                                                   command=search_songs)
                                searchbtn.pack(pady=10)

                                def add_song():
                                    selected = songtable.focus()
                                    if selected != '':
                                        values = songtable.item(selected, 'values')
                                        songid = values[0]
                                        cur.execute('SELECT SongID FROM SongSchedule WHERE Sunday = ?', (scheduledate,))
                                        results = cur.fetchall()
                                        songs = ''.join(str(results))

                                        def addsong():
                                            cur.execute('INSERT INTO SongSchedule VALUES (?, ?)',
                                                        (songid, str(scheduledate)))
                                            conn.commit()
                                            messagebox.showinfo('Successfully Completed',
                                                                'Song was successfully added to the schedule.',
                                                                parent=new_schedule_root)
                                            update_tables()
                                            add_song_root.destroy()

                                        def add():
                                            cur.execute(
                                                'SELECT Sunday FROM SongSchedule WHERE SongID = ? ORDER BY Sunday DESC',
                                                (songid,))
                                            sundaysplayed = cur.fetchone()
                                            if sundaysplayed != None:
                                                for sunday in sundaysplayed:
                                                    sunday = ''.join(sunday)
                                                    sundaylist = sunday.split('-')
                                                    y = int(sundaylist[0])
                                                    m = int(sundaylist[1])
                                                    d = int(sundaylist[2])
                                                    if date(y, m, d) + timedelta(days=90) > scheduledate:
                                                        stilladd = messagebox.askyesno('',
                                                                                       'This song has already been/will be played recently. '
                                                                                       'Would you still like to add it to the schedule?',
                                                                                       parent=add_song_root)
                                                        if stilladd:
                                                            addsong()
                                                    else:
                                                        addsong()
                                            else:
                                                addsong()

                                        if songid not in songs:
                                            # cur.execute('SELECT InstrumentID FROM MusicianSchedule WHERE Sunday = ?', (scheduledate,))
                                            # cur.execute('SELECT InstrumentID FROM InstrumentReq WHERE SongID = ?', (songid,))
                                            # instrreq = cur.fetchall()

                                            cur.execute(
                                                'SELECT DISTINCT InstrumentReq.InstrumentID FROM InstrumentReq WHERE InstrumentReq.SongID = ? '
                                                'AND InstrumentReq.InstrumentID NOT IN (SELECT MusicianSchedule.InstrumentID FROM MusicianSchedule '
                                                'WHERE MusicianSchedule.Sunday = ?)',
                                                (songid, str(scheduledate)))

                                            notintersect = cur.fetchall()

                                            if len(notintersect) == 0:
                                                add()
                                            else:
                                                cur.execute(
                                                    'SELECT Instrument FROM Instrument INNER JOIN InstrumentReq ON Instrument.InstrumentID = InstrumentReq.InstrumentID '
                                                    'WHERE SongID = ?', (songid,))
                                                instrname = cur.fetchall()
                                                instrname = ''.join(str(instrname))
                                                instrname = instrname.replace("'", '').replace('(', '').replace(')',
                                                                                                                '').replace(
                                                    '[', '').replace(']', '').replace(',', '')
                                                print(instrname)
                                                addanyway = messagebox.askyesno('',
                                                                                f'There are currently no musicians playing a recommended instrument for this song ({instrname}). '
                                                                                f'Would you still like to add this song to the schedule?',
                                                                                parent=add_song_root)
                                                if addanyway:
                                                    add()



                                        else:
                                            messagebox.showinfo('Song Already Exists',
                                                                'This song already exists in this schedule.',
                                                                parent=add_song_root)
                                    else:
                                        messagebox.showinfo('',
                                                            'Select a song, then click the "Add to Schedule" button.',
                                                            parent=add_song_root)

                                cancelbtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Cancel',
                                                   command=add_song_root.destroy)
                                savebtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Add to Schedule',
                                                 command=add_song)

                                cancelbtn.grid(column=0, row=0, padx=5, pady=5)
                                savebtn.grid(column=1, row=0, padx=5, pady=5)

                            def view_instr():
                                try:
                                    conn = lite.connect("CKF.db")
                                    cur = conn.cursor()

                                    selected = songtable.focus()
                                    values = songtable.item(selected, 'values')
                                    songid = values[0]

                                    cur.execute(
                                        'SELECT Instrument FROM InstrumentReq INNER JOIN Instrument ON Instrument.InstrumentID = '
                                        'InstrumentReq.InstrumentID WHERE SongID = ?', (songid,))
                                    results = cur.fetchall()

                                    instrlist = []
                                    for instrument in results:
                                        instrlist.append(instrument)

                                    def list_to_string(list):
                                        string = ''
                                        for item in list:
                                            instr = str(item).replace('(', '').replace(')', '').replace(',',
                                                                                                        '').replace("'",
                                                                                                                    '')
                                            string += f'\n{instr}'
                                        return string

                                    messagebox.showinfo("Musician's Instruments",
                                                        f"Song's Recommended Instruments:{list_to_string(instrlist)}",
                                                        parent=new_schedule_root)

                                except IndexError:
                                    messagebox.showinfo('',
                                                        'Please select a song to view its instrument recommendation.',
                                                        parent=new_schedule_root)

                            addsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Add Song', command=song)
                            delsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Delete Song',
                                                command=del_song)
                            viewsonginstrbtn = Button(btnframe, bg='#5F388C', fg='white',
                                                      text='View Song Instrument Recommendation', command=view_instr)

                            addsongbtn.grid(column=4, row=0, padx=(25, 5), pady=10)
                            delsongbtn.grid(column=5, row=0, padx=5, pady=10)
                            viewsonginstrbtn.grid(column=6, row=0, padx=5, pady=10)

                            exitbtn = Button(exitframe, bg='#5F388C', fg='white', text='Exit', width=5,
                                             command=new_schedule_root.destroy)

                            exitbtn.grid(column=1, row=1, padx=5, pady=10)

                            def update_tables():
                                musiciantable.delete(*musiciantable.get_children())

                                cur.execute(
                                    'SELECT DISTINCT Musician.MusicianID, FirstName, LastName, Email FROM Musician INNER JOIN MusicianSchedule ON Musician.MusicianID '
                                    '= MusicianSchedule.MusicianID WHERE Sunday = ?', (str(scheduledate),))

                                results = cur.fetchall()

                                for row in results:
                                    musiciantable.insert("", tk.END, values=row)

                                songtable.delete(*songtable.get_children())

                                cur.execute(
                                    'SELECT Song.SongID, Title FROM Song INNER JOIN SongSchedule ON Song.SongID '
                                    '= SongSchedule.SongID WHERE Sunday = ?', (str(scheduledate),))
                                results = cur.fetchall()

                                for row in results:
                                    songtable.insert("", tk.END, values=row)

                            update_tables()

                            def clear_schedule():
                                sure = messagebox.askyesno('',
                                                           "This action will remove all songs and musicians from this schedule. "
                                                           "Are you sure you'd like to continue?",
                                                           parent=new_schedule_root)
                                if sure:
                                    cur.execute('DELETE FROM MusicianSchedule WHERE Sunday = ?', (str(scheduledate),))
                                    cur.execute('DELETE FROM SongSchedule WHERE Sunday = ?', (str(scheduledate),))
                                    conn.commit()
                                    update_tables()
                                    messagebox.showinfo('Successfully Completed', 'Schedule was successfully cleared.',
                                                        parent=new_schedule_root)

                            clearschedulebtn = Button(exitframe, bg='#5F388C', fg='white', text='Clear Schedule',
                                                      command=clear_schedule)
                            clearschedulebtn.grid(column=2, row=1, padx=5, pady=5)

                            schedulefillerlbl = Label(exitframe, text='')
                            schedulefillerlbl.grid(column=0, row=1, padx=40)

                        song_table()

                    mus_table()

                if str(scheduledate) in sundays:
                    proceed = messagebox.askyesno('Schedule Already Exists',
                                                  'There is already a schedule for this Sunday. '
                                                  'Would you like to continue?', parent=future_root)
                    if not proceed:
                        pass
                    else:
                        new_schedule_plan()
                        pass
                elif str(scheduledate) not in sundays:
                    new_schedule_plan()

            else:
                messagebox.showinfo('', 'Please select a date, and then click the "Create Schedule" button.',
                                    parent=future_root)

        homebtn = Button(btnframe, bg='#5F388C', fg='white', text='Home', command=future_root.destroy)
        schedulebtn = Button(btnframe, bg='#5F388C', fg='white', text='Create/Edit Schedule', command=new_schedule)

        homebtn.pack(side='left', padx=10)
        schedulebtn.pack(side='left', padx=10)

        future_root.mainloop()

    # PAST MODULE
    #
    #
    #
    #
    #
    #
    #
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
                        cur.execute(
                            'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ? AND Email = ?',
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
        schedulebtn = Button(homescheduleframe, bg='#5F388C', fg='white', text='View Schedule',
                             command=view_past_schedule)

        homebtn.pack(side='left', padx=10)
        schedulebtn.pack(side='left', padx=10)

        past_root.mainloop()

    # MUSICIANS MODULE
    #
    #
    #
    #
    #
    #
    #
    def Musicians():
        conn = lite.connect("CKF.db")
        cur = conn.cursor()

        musicians_root = tk.Tk()

        musicians_root.state('zoomed')
        musicians_root.geometry('800x600')
        musicians_root.title('Musicians')
        # musicians_root.iconbitmap('CKF_image.ico')

        searchframe = Frame(musicians_root)
        searchbtnframe = Frame(musicians_root)
        musiciantableframe = Frame(musicians_root)
        instrtableframe = Frame(musicians_root)
        musbtnframe = Frame(musicians_root)
        instrbtnframe = Frame(musicians_root)

        searchframe.pack()
        searchbtnframe.pack()
        musiciantableframe.pack()
        musbtnframe.pack()
        instrtableframe.pack()
        instrbtnframe.pack()

        scroll_vert = Scrollbar(musiciantableframe)
        scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 0))

        scroll_horizon = Scrollbar(musiciantableframe, orient='horizontal')
        scroll_horizon.pack(side=BOTTOM, fill=X, pady=(0, 10))

        # Create table frame
        musiciantable = ttk.Treeview(musiciantableframe, yscrollcommand=scroll_vert.set,
                                     xscrollcommand=scroll_horizon.set)

        musiciantable.pack(pady=(30, 0))

        scroll_vert.config(command=musiciantable.yview)
        scroll_horizon.config(command=musiciantable.xview)

        # define columns
        musiciantable['columns'] = ('id', 'first_name', 'last_name', 'email', 'phone')

        # Format columns
        musiciantable.column("#0", width=0, stretch=NO)
        musiciantable.column("id", anchor=CENTER, width=50)
        musiciantable.column("first_name", anchor=CENTER, width=200)
        musiciantable.column("last_name", anchor=CENTER, width=200)
        musiciantable.column("email", anchor=CENTER, width=300)
        musiciantable.column("phone", anchor=CENTER, width=200)

        # Create Headings
        musiciantable.heading("#0", text="", anchor=CENTER)
        musiciantable.heading("id", text="ID", anchor=CENTER)
        musiciantable.heading("first_name", text="First Name", anchor=CENTER)
        musiciantable.heading("last_name", text="Last Name", anchor=CENTER)
        musiciantable.heading("email", text="Email", anchor=CENTER)
        musiciantable.heading("phone", text="Phone", anchor=CENTER)

        instr_scroll_vert = Scrollbar(instrtableframe)
        instr_scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 0))

        instr_scroll_horizon = Scrollbar(instrtableframe, orient='horizontal')
        instr_scroll_horizon.pack(side=BOTTOM, fill=X, pady=(0, 10))

        # Create table frame
        instrtable = ttk.Treeview(instrtableframe, yscrollcommand=instr_scroll_vert.set,
                                  xscrollcommand=instr_scroll_horizon.set)

        instrtable.pack(pady=(30, 0))

        instr_scroll_vert.config(command=instrtable.yview)
        instr_scroll_horizon.config(command=instrtable.xview)

        # define columns
        instrtable['columns'] = ('id', 'title')

        # Format columns
        instrtable.column("#0", width=0, stretch=NO)
        instrtable.column("id", anchor=CENTER, width=50)
        instrtable.column("title", anchor=CENTER, width=200)

        # Create Headings
        instrtable.heading("#0", text="", anchor=CENTER)
        instrtable.heading("id", text="ID", anchor=CENTER)
        instrtable.heading("title", text="Title", anchor=CENTER)

        def update_musician_table():
            musiciantable.delete(*musiciantable.get_children())

            cur.execute('SELECT * FROM Musician ORDER BY FirstName')
            results = cur.fetchall()

            for row in results:
                musiciantable.insert("", tk.END, values=row)

        def update_instr_table():
            instrtable.delete(*instrtable.get_children())

            cur.execute('SELECT * FROM Instrument')
            results = cur.fetchall()

            for row in results:
                instrtable.insert("", tk.END, values=row)

        update_musician_table()
        update_instr_table()

        idlbl = Label(searchframe, text='ID:')
        fnamelbl = Label(searchframe, text='First Name:')
        lnamelbl = Label(searchframe, text='Last Name:')
        emaillbl = Label(searchframe, text='Email:')
        phonelbl = Label(searchframe, text='Phone:')
        instrlbl = Label(searchframe, text='Instrument ID:')

        identry = Entry(searchframe)
        fnameentry = Entry(searchframe)
        lnameentry = Entry(searchframe)
        emailentry = Entry(searchframe)
        phoneentry = Entry(searchframe)
        instrentry = Entry(searchframe)

        idlbl.pack(side='left', padx=0, pady=(20, 0))
        identry.pack(side='left', padx=(0, 5), pady=(20, 0))

        fnamelbl.pack(side='left', padx=0, pady=(20, 0))
        fnameentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        lnamelbl.pack(side='left', padx=0, pady=(20, 0))
        lnameentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        emaillbl.pack(side='left', padx=0, pady=(20, 0))
        emailentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        phonelbl.pack(side='left', padx=0, pady=(20, 0))
        phoneentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        instrlbl.pack(side='left', padx=0, pady=(20, 0))
        instrentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        def search_musicians():
            id = identry.get()
            fname = fnameentry.get()
            lname = lnameentry.get()
            email = emailentry.get()
            phone = phoneentry.get()
            instr = instrentry.get()

            fname = fname.rstrip().upper()
            lname = lname.rstrip().upper()
            email = email.rstrip().upper()
            phone = phone.rstrip().upper()
            instr = instr.rstrip().upper()

            cur.execute("SELECT DISTINCT Musician.MusicianID, FirstName, LastName, Email, Phone "
                        "FROM Musician "
                        "LEFT OUTER JOIN MusicianInstruments ON Musician.MusicianID = MusicianInstruments.MusicianID "
                        "WHERE 1 "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Musician.MusicianID) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(FirstName) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(LastName) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Email) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Phone) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(InstrumentID) = ? END "
                        "ORDER BY FirstName",
                        (id, id, fname, fname, lname, lname, email, email, phone, phone, instr, instr))

            rows = cur.fetchall()

            musiciantable.delete(*musiciantable.get_children())

            for row in rows:
                musiciantable.insert(parent='', index='end', text='',
                                     values=row)

        searchbtn = Button(searchbtnframe, bg='#5F388C', fg='white', text='Search', width=5, height=1,
                           command=search_musicians)
        searchbtn.pack(pady=10, side='bottom')

        def new_musicians():
            new_musicians_root = tk.Tk()

            new_musicians_root.state('zoomed')
            new_musicians_root.geometry('800x600')
            new_musicians_root.title('Musicians')

            # new_musicians_root.iconbitmap('CKF_image.ico')

            def add_musician():
                fname = fnameentry.get()
                lname = lnameentry.get()
                email = emailentry.get()
                phone = phoneentry.get()

                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                try:
                    if fname != '' and lname != '' and email != '':
                        cur.execute('INSERT INTO Musician (FirstName, LastName, Email, Phone) VALUES (?, ?, ?, ?)',
                                    (fname, lname, email, phone))
                        conn.commit()
                        widgets = instrframe.winfo_children()

                        for widget in widgets:
                            if isinstance(widget, ttk.Combobox):
                                if widget.get() != 'Pick an instrument':
                                    conn = lite.connect("CKF.db")
                                    cur = conn.cursor()
                                    instr = widget.get()
                                    cur.execute('SELECT InstrumentID FROM Instrument WHERE Instrument = ?', (instr,))
                                    instrument = cur.fetchone()
                                    instrid = functools.reduce(lambda sub, ele: sub * 10 + ele, instrument)
                                    cur.execute(
                                        'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ? AND Email = ? AND Phone = ?',
                                        (fname, lname, email, phone))
                                    musician = cur.fetchone()
                                    musicianid = functools.reduce(lambda sub, ele: sub * 10 + ele, musician)
                                    cur.execute('SELECT InstrumentID FROM MusicianInstruments WHERE MusicianID = ?',
                                                musician)
                                    results = cur.fetchall()
                                    if instrument not in results:
                                        cur.execute('INSERT INTO MusicianInstruments VALUES (?, ?)',
                                                    (int(musicianid), int(instrid)))
                                        conn.commit()

                        messagebox.showinfo('Successfully Completed', 'Musician was successfully added.',
                                            parent=new_musicians_root)

                        new_musicians_root.destroy()

                        update_musician_table()

                    else:
                        messagebox.showinfo('Error Adding Musician',
                                            'First Name, Last Name, and Email must be filled out in order to add a musician.',
                                            parent=new_musicians_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error adding this musician.',
                                         parent=new_musicians_root)

            fnameframe = Frame(new_musicians_root)
            lnameframe = Frame(new_musicians_root)
            emailframe = Frame(new_musicians_root)
            phoneframe = Frame(new_musicians_root)
            addinstrframe = Frame(new_musicians_root)
            instrframe = Frame(new_musicians_root)
            saveframe = Frame(new_musicians_root)
            cancelframe = Frame(new_musicians_root)

            fnameframe.pack()
            lnameframe.pack()
            emailframe.pack()
            phoneframe.pack()
            addinstrframe.pack()
            instrframe.pack()
            saveframe.pack()
            cancelframe.pack()

            fnamelbl = Label(fnameframe, text='First Name:')
            fnameentry = Entry(fnameframe, width=25)

            lnamelbl = Label(lnameframe, text='Last Name:')
            lnameentry = Entry(lnameframe, width=25)

            emaillbl = Label(emailframe, text='Email:')
            emailentry = Entry(emailframe, width=30)

            phonelbl = Label(phoneframe, text='Phone (optional):')
            phoneentry = Entry(phoneframe, width=10)

            def instrument_selection():
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                          '').replace(
                        ',', '').replace(
                        "'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(value=instrlist[0])
                instrbox.pack(padx=5, pady=5)

            addinstrbtn = Button(addinstrframe, bg='#5F388C', fg='white', text='Add an Instrument',
                                 command=instrument_selection)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=add_musician)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=new_musicians_root.destroy)

            fnamelbl.grid(column=1, row=1, padx=5, pady=10)
            fnameentry.grid(column=2, row=1, padx=5, pady=10)

            lnamelbl.grid(column=1, row=2, padx=5, pady=10)
            lnameentry.grid(column=2, row=2, padx=5, pady=10)

            emaillbl.grid(column=1, row=3, padx=5, pady=10)
            emailentry.grid(column=2, row=3, padx=5, pady=10)

            phonelbl.grid(column=1, row=4, padx=5, pady=10)
            phoneentry.grid(column=2, row=4, padx=5, pady=10)

            addinstrbtn.grid(column=2, row=6, padx=5, pady=5)

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        def are_you_sure():
            if musiciantable.focus() == '':
                messagebox.showinfo('',
                                    'Please select a musician to delete, and then click the "Delete Musician" button.',
                                    parent=musicians_root)
            else:
                delete = messagebox.askyesno('Warning',
                                             "This action will permanently delete this musician. Are you sure you'd like to continue?",
                                             parent=musicians_root)
                if delete:
                    del_musician()

        def del_musician():
            conn = lite.connect("CKF.db")
            cur = conn.cursor()

            selected = musiciantable.focus()
            values = musiciantable.item(selected, 'values')
            musiciantable.delete(selected)
            # Delete From Database
            cur.execute("DELETE from Musician WHERE MusicianID = ?", (values[0],))
            cur.execute('DELETE FROM MusicianInstruments WHERE MusicianID = ?', (values[0],))

            # Commit changes
            conn.commit()

            update_musician_table()

            messagebox.showinfo('Successfully Completed', 'Musician was successfully deleted.', parent=musicians_root)

        def view_instr():
            try:
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                selected = musiciantable.focus()
                values = musiciantable.item(selected, 'values')
                cur.execute(
                    'SELECT Instrument FROM MusicianInstruments INNER JOIN Instrument ON Instrument.InstrumentID = '
                    'MusicianInstruments.InstrumentID WHERE MusicianID = ?', (values[0],))
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

                messagebox.showinfo("Musician's Instruments", f"Musician's Instruments:{list_to_string(instrlist)}",
                                    parent=musicians_root)

            except IndexError:
                messagebox.showinfo('', 'Please select a musician to view their instruments.', parent=musicians_root)

        def get_values():
            selected = musiciantable.focus()
            values = musiciantable.item(selected, 'values')
            return values

        def edit_musicians():
            if musiciantable.focus() != '':
                edit_musicians_root = tk.Tk()

                edit_musicians_root.state('zoomed')
                edit_musicians_root.geometry('800x600')
                edit_musicians_root.title('Musicians')
                # edit_musicians_root.iconbitmap('CKF_image.ico')

                musicianinfo = get_values()
                musicianid = musicianinfo[0]

                fnameframe = Frame(edit_musicians_root)
                lnameframe = Frame(edit_musicians_root)
                emailframe = Frame(edit_musicians_root)
                phoneframe = Frame(edit_musicians_root)
                noteframe = Frame(edit_musicians_root)
                addinstrframe = Frame(edit_musicians_root)
                instrframe = Frame(edit_musicians_root)
                saveframe = Frame(edit_musicians_root)
                cancelframe = Frame(edit_musicians_root)

                fnameframe.pack()
                lnameframe.pack()
                emailframe.pack()
                phoneframe.pack()
                noteframe.pack()
                addinstrframe.pack()
                instrframe.pack()
                saveframe.pack()
                cancelframe.pack()

                cur.execute('SELECT FirstName FROM Musician WHERE MusicianID = ?', (musicianid,))
                firstname = cur.fetchone()
                fnamelbl = Label(fnameframe, text='First Name:')
                fnameentry = Entry(fnameframe, width=25)
                fnameentry.insert(0, firstname)

                cur.execute('SELECT LastName FROM Musician WHERE MusicianID = ?', (musicianid,))
                lastname = cur.fetchone()
                lnamelbl = Label(lnameframe, text='Last Name:')
                lnameentry = Entry(lnameframe, width=25)
                lnameentry.insert(0, lastname)

                cur.execute('SELECT Email FROM Musician WHERE MusicianID = ?', (musicianid,))
                email = cur.fetchone()
                emaillbl = Label(emailframe, text='Email:')
                emailentry = Entry(emailframe, width=30)
                emailentry.insert(0, email)

                cur.execute('SELECT Phone FROM Musician WHERE MusicianID = ?', (musicianid,))
                phone = cur.fetchone()
                phonelbl = Label(phoneframe, text='Phone (optional):')
                phoneentry = Entry(phoneframe, width=10)
                phoneentry.insert(0, phone)
                if phoneentry.get() == '{}':
                    phoneentry.delete(0, 'end')

                cur.execute(
                    'SELECT Instrument FROM MusicianInstruments INNER JOIN Instrument ON Instrument.InstrumentID = MusicianInstruments.InstrumentID WHERE MusicianID = ?',
                    (musicianid,))
                results = cur.fetchall()

                for i in results:
                    instrlist = ['Pick an instrument']
                    cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                    instruments = cur.fetchall()

                    for instrument in instruments:
                        strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                              '').replace(
                            ',', '').replace("'", '')
                        instrlist.append(strinstr)

                    instrbox = ttk.Combobox(instrframe, values=instrlist)
                    instrbox.set(
                        value=str(i).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                 '').replace(
                            "'", ''))
                    instrbox.pack(padx=5, pady=5)

                def edit_musician():
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    fname = fnameentry.get()
                    lname = lnameentry.get()
                    email = emailentry.get()
                    phone = phoneentry.get()
                    musicianinfo = get_values()
                    musicianid = musicianinfo[0]

                    try:
                        if fname != '' and lname != '' and email != '':
                            cur.execute(
                                'UPDATE Musician SET FirstName = ?, LastName = ?, Email = ?, Phone = ? WHERE MusicianID = ?',
                                (fname, lname, email, phone, musicianid))
                            cur.execute('DELETE FROM MusicianInstruments WHERE MusicianID = ?', (musicianid,))
                            conn.commit()
                            widgets = instrframe.winfo_children()

                            for widget in widgets:
                                if isinstance(widget, ttk.Combobox):
                                    if widget.get() != 'Pick an instrument':
                                        conn = lite.connect("CKF.db")
                                        cur = conn.cursor()
                                        instr = widget.get()
                                        cur.execute('SELECT InstrumentID FROM Instrument WHERE Instrument = ?',
                                                    (instr,))
                                        instrument = cur.fetchone()
                                        instrid = functools.reduce(lambda sub, ele: sub * 10 + ele, instrument)
                                        cur.execute(
                                            'SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ? AND Email = ?',
                                            (fname, lname, email))
                                        musician = cur.fetchone()
                                        musicianid = functools.reduce(lambda sub, ele: sub * 10 + ele, musician)
                                        cur.execute('SELECT InstrumentID FROM MusicianInstruments WHERE MusicianID = ?',
                                                    musician)
                                        results = cur.fetchall()
                                        if instrument not in results:
                                            cur.execute('INSERT INTO MusicianInstruments VALUES (?, ?)',
                                                        (int(musicianid), int(instrid)))
                                            conn.commit()

                            messagebox.showinfo('Successfully Completed', 'Musician was successfully edited.',
                                                parent=edit_musicians_root)

                            edit_musicians_root.destroy()

                            update_musician_table()

                        else:
                            messagebox.showinfo('Error Editing Musician',
                                                'First Name, Last Name, and Email must be filled out in order to edit a musician.',
                                                parent=edit_musicians_root)
                    except:
                        messagebox.showerror('Error', 'Sorry, there was an error editing this musician.',
                                             parent=edit_musicians_root)
            else:
                messagebox.showinfo('', 'Select a musician, then click the "Edit Musician" button.',
                                    parent=musicians_root)

            def instrument_selection():
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                          '').replace(
                        ',', '').replace("'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(value=instrlist[0])
                instrbox.pack(padx=5, pady=5)
                return instrbox

            notelbl = Label(noteframe, text='Note: Set instrument to "Pick an instrument" to remove')
            addinstrbtn = Button(addinstrframe, bg='#5F388C', fg='white', text='Add an Instrument',
                                 command=instrument_selection)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=edit_musician)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=edit_musicians_root.destroy)

            fnamelbl.grid(column=1, row=1, padx=5, pady=10)
            fnameentry.grid(column=2, row=1, padx=5, pady=10)

            lnamelbl.grid(column=1, row=2, padx=5, pady=10)
            lnameentry.grid(column=2, row=2, padx=5, pady=10)

            emaillbl.grid(column=1, row=3, padx=5, pady=10)
            emailentry.grid(column=2, row=3, padx=5, pady=10)

            phonelbl.grid(column=1, row=4, padx=5, pady=10)
            phoneentry.grid(column=2, row=4, padx=5, pady=10)

            notelbl.grid(column=2, row=6, padx=5, pady=5)
            addinstrbtn.grid(column=2, row=7, padx=5, pady=5)

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        def new_instr():
            new_instr_root = tk.Tk()

            new_instr_root.state('zoomed')
            new_instr_root.geometry('800x600')
            new_instr_root.title('Musicians')

            # new_instr_root.iconbitmap('CKF_image.ico')

            def add_instr():
                instr = instrentry.get()

                try:
                    if instr != '':
                        cur.execute('INSERT INTO Instrument (Instrument) VALUES (?)',
                                    (instr,))
                        conn.commit()

                        messagebox.showinfo('Successfully Completed', 'Instrument was successfully added.',
                                            parent=new_instr_root)

                        new_instr_root.destroy()

                        update_instr_table()

                    else:
                        messagebox.showinfo('Error Adding Instrument',
                                            'Title must be filled out in order to add an intsrument.',
                                            parent=new_instr_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error adding this instrument.',
                                         parent=new_instr_root)

            instrframe = Frame(new_instr_root)
            saveframe = Frame(new_instr_root)

            instrframe.pack()
            saveframe.pack()

            instrlbl = Label(instrframe, text='Instrument:')
            instrentry = Entry(instrframe, width=25)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=add_instr)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=new_instr_root.destroy)

            instrlbl.grid(column=1, row=1, padx=5, pady=30)
            instrentry.grid(column=2, row=1, padx=5, pady=30)

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        def edit_instruments():
            if instrtable.focus() != '':
                edit_instr_root = tk.Tk()

                edit_instr_root.state('zoomed')
                edit_instr_root.geometry('800x600')
                edit_instr_root.title('Instruments')
                # edit_instr_root.iconbitmap('CKF_image.ico')

                selected = instrtable.focus()
                instrinfo = instrtable.item(selected, 'values')
                instrid = instrinfo[0]

                instrframe = Frame(edit_instr_root)
                btnframe = Frame(edit_instr_root)

                instrframe.pack()
                btnframe.pack()

                cur.execute('SELECT Instrument FROM Instrument WHERE InstrumentID = ?', (instrid,))
                instrument = cur.fetchone()
                instrument = ''.join(instrument).replace('{', '').replace('}', '')
                instrlbl = Label(instrframe, text='Instrument:')
                instrentry = Entry(instrframe, width=25)
                instrentry.insert(0, instrument)

                def edit_instr():
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    instr = instrentry.get()

                    selected = instrtable.focus()
                    instrinfo = instrtable.item(selected, 'values')
                    instrid = instrinfo[0]

                    try:
                        if instr != '':
                            cur.execute('UPDATE Instrument SET Instrument = ? WHERE InstrumentID = ?',
                                        (instr, instrid))
                            conn.commit()

                            messagebox.showinfo('Successfully Completed', 'Instrument was successfully edited.',
                                                parent=edit_instr_root)

                            edit_instr_root.destroy()

                            update_instr_table()

                        else:
                            messagebox.showinfo('Error Editing Instrument',
                                                'Instrument must be filled out in order to edit an instrument.',
                                                parent=edit_instr_root)
                    except:
                        messagebox.showerror('Error', 'Sorry, there was an error editing this musician.',
                                             parent=edit_instr_root)

                savebtn = Button(btnframe, bg='#5F388C', fg='white', text='Save', command=edit_instr)
                cancelbtn = Button(btnframe, bg='#5F388C', fg='white', text='Cancel', command=edit_instr_root.destroy)

                instrlbl.grid(column=1, row=1, padx=5, pady=30)
                instrentry.grid(column=2, row=1, padx=5, pady=30)

                savebtn.grid(column=2, row=8, padx=5, pady=5)
                cancelbtn.grid(column=1, row=8, padx=5, pady=5)

            else:
                messagebox.showinfo('', 'Please select an instrument, then click the "Edit Instrument" button.',
                                    parent=musicians_root)

        def del_instr():
            if instrtable.focus() == '':
                messagebox.showinfo('',
                                    'Please select an instrument to delete, and then click the "Delete Instrument" button.',
                                    parent=musicians_root)
            else:
                delete = messagebox.askyesno('Warning',
                                             "This action will permanently delete this instrument. Are you sure you'd like to continue?",
                                             parent=musicians_root)
                if delete:
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    selected = instrtable.focus()
                    values = instrtable.item(selected, 'values')
                    instrid = values[0]
                    instrtable.delete(selected)
                    # Delete From Database
                    cur.execute("DELETE from Instrument WHERE InstrumentID = ?", (instrid,))
                    cur.execute('DELETE FROM MusicianInstrument WHERE InstrumentID = ?', (instrid,))

                    # Commit changes
                    conn.commit()

                    update_instr_table()

                    messagebox.showinfo('Successfully Completed', 'Instrument was successfully deleted.',
                                        parent=musicians_root)

        homebtn = Button(musbtnframe, bg='#5F388C', fg='white', text='Home', command=musicians_root.destroy)
        viewinstrumentsbtn = Button(musbtnframe, bg='#5F388C', fg='white', text="View Musician's Instrument(s)",
                                    command=view_instr)
        addmusicianbtn = Button(musbtnframe, bg='#5F388C', fg='white', text='Add Musician', command=new_musicians)
        editmusicianbtn = Button(musbtnframe, bg='#5F388C', fg='white', text='Edit Musician', command=edit_musicians)
        delmusicianbtn = Button(musbtnframe, bg='#5F388C', fg='white', text='Delete Musician', command=are_you_sure)
        addinstrbtn = Button(instrbtnframe, bg='#5F388C', fg='white', text='Add Instrument', command=new_instr)
        editinstrbtn = Button(instrbtnframe, bg='#5F388C', fg='white', text='Edit Instrument', command=edit_instruments)
        delinstrbtn = Button(instrbtnframe, bg='#5F388C', fg='white', text='Delete Instrument', command=del_instr)

        homebtn.pack(side='left', padx=10)
        viewinstrumentsbtn.pack(side='left', padx=10)
        addmusicianbtn.pack(side='left', padx=10)
        editmusicianbtn.pack(side='left', padx=10)
        delmusicianbtn.pack(side='left', padx=10)
        addinstrbtn.pack(side='left', padx=10)
        editinstrbtn.pack(side='left', padx=10)
        delinstrbtn.pack(side='left', padx=10)

        musicians_root.mainloop()

    # SONGS MODULE
    #
    #
    #
    #
    #
    #
    #
    #
    def Songs():
        conn = lite.connect("CKF.db")
        cur = conn.cursor()

        songs_root = tk.Tk()

        songs_root.state('zoomed')
        songs_root.geometry('800x600')
        songs_root.title('Songs')
        # songs_root.iconbitmap('CKF_image.ico')

        searchframe = Frame(songs_root)
        searchbtnframe = Frame(songs_root)
        mustableframe = Frame(songs_root)
        btnframe = Frame(songs_root)
        instrtableframe = Frame(songs_root)
        themetableframe = Frame(songs_root)
        fillerframe = Frame(songs_root)

        searchframe.pack()
        searchbtnframe.pack()
        mustableframe.pack()
        btnframe.pack()
        instrtableframe.pack(side='left', padx=(450, 0))
        themetableframe.pack(side='right', padx=(0, 450))
        fillerframe.pack(pady=50, side='bottom')

        scroll_vert = Scrollbar(mustableframe)
        scroll_vert.pack(side=RIGHT, fill=Y, pady=(20, 0))

        scroll_horizon = Scrollbar(mustableframe, orient='horizontal')
        scroll_horizon.pack(side=BOTTOM, fill=X)

        # Create table frame
        songtable = ttk.Treeview(mustableframe, yscrollcommand=scroll_vert.set,
                                 xscrollcommand=scroll_horizon.set)

        songtable.pack(pady=(20, 0))

        scroll_vert.config(command=songtable.yview)
        scroll_horizon.config(command=songtable.xview)

        # define columns
        songtable['columns'] = ('id', 'title', 'songwriter', 'pages', 'key', 'time')

        # Format columns
        songtable.column("#0", width=0, stretch=NO)
        songtable.column("id", anchor=CENTER, width=50)
        songtable.column("title", anchor=CENTER, width=200)
        songtable.column("songwriter", anchor=CENTER, width=200)
        songtable.column("pages", anchor=CENTER, width=80)
        songtable.column("key", anchor=CENTER, width=80)
        songtable.column("time", anchor=CENTER, width=100)

        # Create Headings
        songtable.heading("#0", text="", anchor=CENTER)
        songtable.heading("id", text="ID", anchor=CENTER)
        songtable.heading("title", text="Title", anchor=CENTER)
        songtable.heading("songwriter", text="Songwriter", anchor=CENTER)
        songtable.heading("pages", text="# of Pages", anchor=CENTER)
        songtable.heading("key", text="Key", anchor=CENTER)
        songtable.heading("time", text="Time Signature", anchor=CENTER)

        instr_scroll_vert = Scrollbar(instrtableframe)
        instr_scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 50))

        instr_scroll_horizon = Scrollbar(instrtableframe, orient='horizontal')
        instr_scroll_horizon.pack(side=BOTTOM, fill=X, pady=(0, 50))

        # Create table frame
        instrtable = ttk.Treeview(instrtableframe, yscrollcommand=instr_scroll_vert.set,
                                  xscrollcommand=instr_scroll_horizon.set)

        instrtable.pack(pady=(30, 0))

        instr_scroll_vert.config(command=instrtable.yview)
        instr_scroll_horizon.config(command=instrtable.xview)

        # define columns
        instrtable['columns'] = ('id', 'instr')

        # Format columns
        instrtable.column("#0", width=0, stretch=NO)
        instrtable.column("id", anchor=CENTER, width=50)
        instrtable.column("instr", anchor=CENTER, width=200)

        # Create Headings
        instrtable.heading("#0", text="", anchor=CENTER)
        instrtable.heading("id", text="ID", anchor=CENTER)
        instrtable.heading("instr", text="Instrument", anchor=CENTER)

        theme_scroll_vert = Scrollbar(themetableframe)
        theme_scroll_vert.pack(side=RIGHT, fill=Y, pady=(30, 50))

        # Create table frame
        themetable = ttk.Treeview(themetableframe, yscrollcommand=theme_scroll_vert.set)

        themetable.pack(pady=(30, 0))

        theme_scroll_vert.config(command=themetable.yview)

        # define columns
        themetable['columns'] = ('id', 'theme')

        # Format columns
        themetable.column("#0", width=0, stretch=NO)
        themetable.column("id", anchor=CENTER, width=50)
        themetable.column("theme", anchor=CENTER, width=200)

        # Create Headings
        themetable.heading("#0", text="", anchor=CENTER)
        themetable.heading("id", text="ID", anchor=CENTER)
        themetable.heading("theme", text="Theme", anchor=CENTER)

        def update_song_table():
            songtable.delete(*songtable.get_children())

            cur.execute('SELECT * FROM Song ORDER BY Title')
            results = cur.fetchall()

            for row in results:
                songtable.insert("", tk.END, values=row)

        def update_instr_table():
            instrtable.delete(*instrtable.get_children())

            cur.execute('SELECT * FROM Instrument')
            results = cur.fetchall()

            for row in results:
                instrtable.insert("", tk.END, values=row)

        def update_theme_table():
            themetable.delete(*themetable.get_children())

            cur.execute('SELECT * FROM Theme')
            results = cur.fetchall()

            for row in results:
                themetable.insert("", tk.END, values=row)

        update_song_table()
        update_instr_table()
        update_theme_table()

        idlbl = Label(searchframe, text='ID:')
        titlelbl = Label(searchframe, text='Title:')
        songwriterlbl = Label(searchframe, text='Songwriter:')
        pageslbl = Label(searchframe, text='# of pages:')
        keylbl = Label(searchframe, text='Key:')
        timelbl = Label(searchframe, text='Time Signature:')
        instrlbl = Label(searchframe, text='Instrument Recommendation (ID):')
        themelbl = Label(searchframe, text='Song Theme (ID):')

        identry = Entry(searchframe, width=5)
        titleentry = Entry(searchframe)
        songwriterentry = Entry(searchframe)
        pagesentry = Entry(searchframe, width=5)
        keyentry = Entry(searchframe, width=5)
        timeentry = Entry(searchframe, width=5)
        instrentry = Entry(searchframe, width=5)
        themeentry = Entry(searchframe, width=5)

        idlbl.pack(side='left', padx=0, pady=(20, 0))
        identry.pack(side='left', padx=(0, 5), pady=(20, 0))

        titlelbl.pack(side='left', padx=0, pady=(20, 0))
        titleentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        songwriterlbl.pack(side='left', padx=0, pady=(20, 0))
        songwriterentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        pageslbl.pack(side='left', padx=0, pady=(20, 0))
        pagesentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        keylbl.pack(side='left', padx=0, pady=(20, 0))
        keyentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        timelbl.pack(side='left', padx=0, pady=(20, 0))
        timeentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        instrlbl.pack(side='left', padx=0, pady=(20, 0))
        instrentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        themelbl.pack(side='left', padx=0, pady=(20, 0))
        themeentry.pack(side='left', padx=(0, 5), pady=(20, 0))

        def search_songs():
            id = identry.get()
            title = titleentry.get()
            songwriter = songwriterentry.get()
            pages = pagesentry.get()
            key = keyentry.get()
            time = timeentry.get()
            instr = instrentry.get()
            theme = themeentry.get()

            title = title.rstrip().upper()
            songwriter = songwriter.rstrip().upper()
            key = key.rstrip().upper()
            time = time.rstrip().upper()

            cur.execute("SELECT DISTINCT Song.SongID, Title, Songwriter, Pages, KeySig, TimeSig "
                        "FROM Song "
                        "LEFT OUTER JOIN InstrumentReq ON Song.SongID = InstrumentReq.SongID "
                        "LEFT OUTER JOIN SongTheme ON Song.SongID = SongTheme.SongID "
                        "WHERE 1 "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Song.SongID) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Title) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Songwriter) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(Pages) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(KeySig) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(TimeSig) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(InstrumentID) = ? END "
                        "AND CASE WHEN ? = '' THEN 1 ELSE UPPER(ThemeID) = ? END "
                        "ORDER BY Title", (
                            id, id, title, title, songwriter, songwriter, pages, pages, key, key, time,
                            time, instr, instr, theme, theme))

            rows = cur.fetchall()

            songtable.delete(*songtable.get_children())

            for row in rows:
                songtable.insert(parent='', index='end', text='',
                                 values=row)

        searchbtn = Button(searchbtnframe, bg='#5F388C', fg='white', text='Search', width=5, height=1,
                           command=search_songs)
        searchbtn.pack(pady=10)

        def new_songs():
            new_songs_root = tk.Tk()

            new_songs_root.state('zoomed')
            new_songs_root.geometry('800x600')
            new_songs_root.title('Songs')
            # new_songs_root.iconbitmap('CKF_image.ico')

            def add_song():
                title = titleentry.get()
                songwriter = songwriterentry.get()
                pages = pagesentry.get()
                keysig = keysigentry.get()
                timesig = timesigentry.get()

                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                try:
                    if title != '' and songwriter != '':
                        cur.execute(
                            'INSERT INTO Song (Title, Songwriter, Pages, KeySig, TimeSig) VALUES (?, ?, ?, ?, ?)',
                            (title, songwriter, pages, keysig, timesig))
                        conn.commit()

                        reqinstrwidgets = instrframe.winfo_children()
                        for widget in reqinstrwidgets:
                            if isinstance(widget, ttk.Combobox):
                                if widget.get() != 'Pick an instrument':
                                    conn = lite.connect("CKF.db")
                                    cur = conn.cursor()
                                    instr = widget.get()
                                    cur.execute('SELECT InstrumentID FROM Instrument WHERE Instrument = ?', (instr,))
                                    instrument = cur.fetchone()
                                    instrid = functools.reduce(lambda sub, ele: sub * 10 + ele, instrument)
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                    cur.execute('SELECT InstrumentID FROM InstrumentReq WHERE SongID = ?', (songid,))
                                    results = cur.fetchall()
                                    if instrument not in results:
                                        cur.execute('INSERT INTO InstrumentReq VALUES (?, ?)',
                                                    (int(songid), int(instrid)))
                                        conn.commit()

                        themewidgets = themeframe.winfo_children()
                        for widget in themewidgets:
                            if isinstance(widget, ttk.Combobox):
                                if widget.get() != 'Pick a theme':
                                    conn = lite.connect("CKF.db")
                                    cur = conn.cursor()
                                    theme = widget.get()
                                    cur.execute('SELECT ThemeID FROM Theme WHERE Theme = ?', (theme,))
                                    my_theme = cur.fetchone()
                                    themeid = functools.reduce(lambda sub, ele: sub * 10 + ele, my_theme, )
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song, )
                                    cur.execute('SELECT ThemeID FROM SongTheme WHERE SongID = ?', song)
                                    results = cur.fetchall()
                                    if my_theme not in results:
                                        cur.execute('INSERT INTO SongTheme VALUES (?, ?)',
                                                    (int(songid), int(themeid)))
                                        conn.commit()

                        oldtestwidgets = oldtestframe.winfo_children()
                        for oldcombowidget in oldtestwidgets:
                            if isinstance(oldcombowidget, ttk.Combobox):
                                conn = lite.connect("CKF.db")
                                cur = conn.cursor()
                                book = oldcombowidget.get()
                                if oldcombowidget.get() != 'Pick a book':
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                    cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?',
                                                song)
                                    results = cur.fetchall()
                                    if book not in results:
                                        cur.execute('INSERT INTO SongScripture (SongID, Book) VALUES (?, ?)',
                                                    (int(songid), book))
                                        conn.commit()
                                else:
                                    # cur.execute('DELETE FROM SongScripture WHERE SongID = ?', (songid,))
                                    pass

                            elif isinstance(oldcombowidget, Entry):
                                cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                            (title, songwriter))
                                song = cur.fetchone()
                                songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                cur.execute('SELECT ChapVerse FROM SongScripture WHERE SongID = ? AND Book = ?',
                                            (songid, book))
                                reference = cur.fetchall()
                                if oldcombowidget.get() == '':
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                elif oldcombowidget.get() not in reference:
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                    cur.execute('INSERT INTO SongScripture VALUES (?, ?, ?)',
                                                (songid, book, oldcombowidget.get()))

                                conn.commit()

                        newtestwidgets = newtestframe.winfo_children()
                        for newcombowidget in newtestwidgets:
                            if isinstance(newcombowidget, ttk.Combobox):
                                book = newcombowidget.get()
                                if newcombowidget.get() != 'Pick a book':
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                    cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?',
                                                song)
                                    results = cur.fetchall()
                                    if book not in results:
                                        cur.execute('INSERT INTO SongScripture (SongID, Book) VALUES (?, ?)',
                                                    (int(songid), book))
                                        conn.commit()
                            if isinstance(newcombowidget, Entry):
                                cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                            (title, songwriter))
                                song = cur.fetchone()
                                songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                cur.execute('SELECT ChapVerse FROM SongScripture WHERE SongID = ? AND Book = ?',
                                            (songid, book))
                                reference = cur.fetchall()
                                if newcombowidget.get() == '':
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                if newcombowidget.get() not in reference:
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                    cur.execute('INSERT INTO SongScripture VALUES (?, ?, ?)',
                                                (songid, book, newcombowidget.get()))

                                conn.commit()

                        messagebox.showinfo('Successfully Completed', 'Song was successfully added.',
                                            parent=new_songs_root)

                        new_songs_root.destroy()

                        update_song_table()

                    else:
                        messagebox.showinfo('Error Adding Song',
                                            'Title and Songwriter must be filled out in order to add a song.',
                                            parent=new_songs_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error adding this song.',
                                         parent=new_songs_root)

            titleframe = Frame(new_songs_root)
            songwriterframe = Frame(new_songs_root)
            pagesframe = Frame(new_songs_root)
            keysigframe = Frame(new_songs_root)
            timesigframe = Frame(new_songs_root)
            addinstrframe = Frame(new_songs_root)
            instrframe = Frame(new_songs_root)
            addoldtestframe = Frame(new_songs_root)
            oldtestframe = Frame(new_songs_root)
            addnewtestframe = Frame(new_songs_root)
            newtestframe = Frame(new_songs_root)
            addthemeframe = Frame(new_songs_root)
            themeframe = Frame(new_songs_root)
            saveframe = Frame(new_songs_root)
            cancelframe = Frame(new_songs_root)

            titleframe.pack()
            songwriterframe.pack()
            pagesframe.pack()
            keysigframe.pack()
            timesigframe.pack()
            addinstrframe.pack()
            instrframe.pack()
            addoldtestframe.pack()
            oldtestframe.pack()
            addnewtestframe.pack()
            newtestframe.pack()
            addthemeframe.pack()
            themeframe.pack()
            saveframe.pack()
            cancelframe.pack()

            titlelbl = Label(titleframe, text='Title:')
            titleentry = Entry(titleframe, width=25)

            songwriterlbl = Label(songwriterframe, text='Songwriter:')
            songwriterentry = Entry(songwriterframe, width=25)

            pageslbl = Label(pagesframe, text='# of Pages (optional):')
            pagesentry = Entry(pagesframe, width=30)

            keysiglbl = Label(keysigframe, text='Key Signature (optional):')
            keysigentry = Entry(keysigframe, width=10)

            timesiglbl = Label(timesigframe, text='Time Signature (optional):')
            timesigentry = Entry(timesigframe, width=10)

            def instrument_selection():
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                          '').replace(
                        ',', '').replace("'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(value=instrlist[0])
                instrbox.pack(padx=5, pady=5)

            oldtestbooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
                            '1 Samuel',
                            '2 Samuel', '1 Kings',
                            '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm',
                            'Proverbs',
                            'Ecclesiastes',
                            'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea',
                            'Joel',
                            'Amos', 'Obadiah', 'Jonah',
                            'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

            newtestbooks = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
                            'Galatians',
                            'Ephesians',
                            'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy',
                            'Titus', 'Philemon',
                            'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude',
                            'Revelation']

            def new_scripture_selection():
                scripturelist = ['Pick a book']

                for book in newtestbooks:
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                    '').replace(
                        "'", '')
                    scripturelist.append(strbook)

                bookbox = ttk.Combobox(newtestframe, values=scripturelist)
                bookbox.set(value=scripturelist[0])
                bookbox.pack(padx=5, pady=5)
                bookentry = Entry(newtestframe, width=10)
                bookentry.pack(padx=5, pady=5)

            def old_scripture_selection():
                scripturelist = ['Pick a book']

                for book in oldtestbooks:
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                    '').replace(
                        "'", '')
                    scripturelist.append(strbook)

                bookbox = ttk.Combobox(oldtestframe, values=scripturelist)
                bookbox.set(value=scripturelist[0])
                bookbox.pack(padx=5, pady=5)
                bookentry = Entry(oldtestframe, width=10)
                bookentry.pack(padx=5, pady=5)

            def theme_selection():
                themelist = ['Pick a theme']
                cur.execute('SELECT Theme FROM Theme')
                themes = cur.fetchall()

                for theme in themes:
                    strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(
                        ',', '').replace("'", '')
                    themelist.append(strtheme)

                themebox = ttk.Combobox(themeframe, values=themelist)
                themebox.set(value=themelist[0])
                themebox.pack(padx=5, pady=5)
                return themebox

            addinstrbtn = Button(addinstrframe, bg='#5F388C', fg='white', text='Add Instrument Recommendation',
                                 command=instrument_selection)
            addnewtestbtn = Button(addnewtestframe, bg='#5F388C', fg='white', text='Add New Testament Reference',
                                   command=new_scripture_selection)
            addoldtestbtn = Button(addoldtestframe, bg='#5F388C', fg='white', text='Add Old Testament Reference',
                                   command=old_scripture_selection)
            addthemebtn = Button(addthemeframe, bg='#5F388C', fg='white', text='Add a Theme', command=theme_selection)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=add_song)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=new_songs_root.destroy)

            titlelbl.grid(column=1, row=1, padx=5, pady=10)
            titleentry.grid(column=2, row=1, padx=5, pady=10)

            songwriterlbl.grid(column=1, row=2, padx=5, pady=10)
            songwriterentry.grid(column=2, row=2, padx=5, pady=10)

            pageslbl.grid(column=1, row=3, padx=5, pady=10)
            pagesentry.grid(column=2, row=3, padx=5, pady=10)

            keysiglbl.grid(column=1, row=4, padx=5, pady=10)
            keysigentry.grid(column=2, row=4, padx=5, pady=10)

            timesiglbl.grid(column=1, row=5, padx=5, pady=10)
            timesigentry.grid(column=2, row=5, padx=5, pady=10)

            addinstrbtn.grid(column=2, row=6, padx=5, pady=5)
            addnewtestbtn.grid(column=2, row=7, padx=5, pady=5)
            addoldtestbtn.grid(column=2, row=8, padx=5, pady=5)
            addthemebtn.grid(column=2, row=9, padx=5, pady=5)

            savebtn.grid(column=2, row=10, padx=5, pady=5)
            cancelbtn.grid(column=1, row=10, padx=5, pady=5)

        def are_you_sure():
            if songtable.focus() == '':
                messagebox.showinfo('', 'Please select a song to delete, and then click the "Delete Song" button.',
                                    parent=songs_root)
            else:
                delete = messagebox.askyesno('Warning',
                                             "This action will permanently delete this song. Are you sure you'd like to continue?",
                                             parent=songs_root)
                if delete:
                    del_song()

        def del_song():
            conn = lite.connect("CKF.db")
            cur = conn.cursor()

            selected = songtable.focus()
            values = songtable.item(selected, 'values')
            songtable.delete(selected)
            # Delete From Database
            cur.execute("DELETE from Song WHERE SongID = ?", (values[0],))

            # Commit changes
            conn.commit()

            update_song_table()

            messagebox.showinfo('Successfully Completed', 'Song was successfully deleted.', parent=songs_root)

        def view_instr():
            try:
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                selected = songtable.focus()
                values = songtable.item(selected, 'values')
                songid = values[0]

                cur.execute('SELECT Instrument FROM InstrumentReq INNER JOIN Instrument ON Instrument.InstrumentID = '
                            'InstrumentReq.InstrumentID WHERE SongID = ?', (songid,))
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
                                    f"Song's Recommended Instruments:{list_to_string(instrlist)}", parent=songs_root)

            except IndexError:
                messagebox.showinfo('', 'Please select a song to view its instrument recommendation.',
                                    parent=songs_root)

        def view_reference():
            try:
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                selected = songtable.focus()
                values = songtable.item(selected, 'values')
                cur.execute('SELECT Book, ChapVerse FROM SongScripture WHERE SongID = ?', (values[0],))
                results = cur.fetchall()

                referencelist = []
                for reference in results:
                    referencelist.append(reference)

                def list_to_string(list):
                    string = ''
                    for item in list:
                        reference = str(item).replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                        string += f'\n{reference}'
                    return string

                messagebox.showinfo("Song's Scripture References",
                                    f"Song's Scripture References:{list_to_string(referencelist)}", parent=songs_root)

            except IndexError:
                messagebox.showinfo('', 'Please select a song to view its scripture references.', parent=songs_root)

        def view_theme():
            try:
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                selected = songtable.focus()
                values = songtable.item(selected, 'values')
                cur.execute('SELECT Theme FROM SongTheme INNER JOIN Theme ON Theme.ThemeID = '
                            'SongTheme.ThemeID WHERE SongID = ?', (values[0],))
                results = cur.fetchall()

                themelist = []
                for theme in results:
                    themelist.append(theme)

                def list_to_string(list):
                    string = ''
                    for item in list:
                        theme = str(item).replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                        string += f'\n{theme}'
                    return string

                messagebox.showinfo("Song's Themes", f"Song's Themes:{list_to_string(themelist)}", parent=songs_root)

            except IndexError:
                messagebox.showinfo('', 'Please select a song to view its themes.', parent=songs_root)

        def get_values():
            selected = songtable.focus()
            values = songtable.item(selected, 'values')
            return values

        def edit_songs():
            if songtable.focus() != '':
                edit_songs_root = tk.Tk()

                edit_songs_root.state('zoomed')
                edit_songs_root.geometry('800x600')
                edit_songs_root.title('Musicians')
                # edit_songs_root.iconbitmap('CKF_image.ico')

                songinfo = get_values()
                songid = songinfo[0]

                titleframe = Frame(edit_songs_root)
                songwriterframe = Frame(edit_songs_root)
                pagesframe = Frame(edit_songs_root)
                keysigframe = Frame(edit_songs_root)
                timesigframe = Frame(edit_songs_root)
                addinstrframe = Frame(edit_songs_root)
                instrframe = Frame(edit_songs_root)
                addoldtestframe = Frame(edit_songs_root)
                oldtestframe = Frame(edit_songs_root)
                addnewtestframe = Frame(edit_songs_root)
                newtestframe = Frame(edit_songs_root)
                noteframe = Frame(edit_songs_root)
                addthemeframe = Frame(edit_songs_root)
                themeframe = Frame(edit_songs_root)
                saveframe = Frame(edit_songs_root)
                cancelframe = Frame(edit_songs_root)

                titleframe.pack()
                songwriterframe.pack()
                pagesframe.pack()
                keysigframe.pack()
                timesigframe.pack()
                addinstrframe.pack()
                instrframe.pack()
                addoldtestframe.pack()
                oldtestframe.pack()
                addnewtestframe.pack()
                newtestframe.pack()
                noteframe.pack()
                addthemeframe.pack()
                themeframe.pack()
                saveframe.pack()
                cancelframe.pack()

                def format_entry(row):
                    strrow = ''.join(str(row))
                    formatted = strrow.replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                   '').replace(
                        "'", '')
                    return formatted

                cur.execute('SELECT Title FROM Song WHERE SongID = ?', (songid,))
                title = cur.fetchone()
                titlelbl = Label(titleframe, text='Title:')
                titleentry = Entry(titleframe, width=25)
                titleentry.insert(0, format_entry(title))

                cur.execute('SELECT Songwriter FROM Song WHERE SongID = ?', (songid,))
                songwriter = cur.fetchone()
                writerlbl = Label(songwriterframe, text='Songwriter:')
                writerentry = Entry(songwriterframe, width=25)
                writerentry.insert(0, format_entry(songwriter))

                cur.execute('SELECT Pages FROM Song WHERE SongID = ?', (songid,))
                pages = cur.fetchone()
                pageslbl = Label(pagesframe, text='# of Pages (optional):')
                pagesentry = Entry(pagesframe, width=30)
                pagesentry.insert(0, format_entry(pages))

                cur.execute('SELECT KeySig FROM Song WHERE SongID = ?', (songid,))
                keysig = cur.fetchone()
                keylbl = Label(keysigframe, text='Key Signature (optional):')
                keyentry = Entry(keysigframe, width=10)
                keyentry.insert(0, format_entry(keysig))

                cur.execute('SELECT TimeSig FROM Song WHERE SongID = ?', (songid,))
                timesig = cur.fetchone()
                timelbl = Label(timesigframe, text='Time Signature (optional):')
                timeentry = Entry(timesigframe, width=10)
                timeentry.insert(0, format_entry(timesig))

                cur.execute(
                    'SELECT Instrument FROM InstrumentReq INNER JOIN Instrument ON Instrument.InstrumentID = InstrumentReq.InstrumentID WHERE SongID = ?',
                    (songid,))
                results = cur.fetchall()

                for i in results:
                    instrlist = ['Pick an instrument']
                    cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                    instruments = cur.fetchall()

                    for instrument in instruments:
                        strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                              '').replace(
                            ',', '').replace("'", '')
                        instrlist.append(strinstr)

                    instrbox = ttk.Combobox(instrframe, values=instrlist)
                    instrbox.set(
                        value=str(i).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                 '').replace(
                            "'", ''))
                    instrbox.pack(padx=5, pady=5)

                cur.execute('SELECT Theme FROM SongTheme INNER JOIN Theme ON Theme.ThemeID = '
                            'SongTheme.ThemeID WHERE SongID = ?', (songid,))
                results = cur.fetchall()

                for i in results:
                    themelist = ['Pick a theme']
                    cur.execute('SELECT Theme FROM Theme')
                    themes = cur.fetchall()

                    for theme in themes:
                        strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                         '').replace(
                            ',', '').replace("'", '')
                        themelist.append(strtheme)

                    themebox = ttk.Combobox(themeframe, values=themelist)
                    themebox.set(value=format_entry(i))
                    themebox.pack(padx=5, pady=5)

                cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?', (songid,))
                book_results = cur.fetchall()


                oldtestbooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
                                '1 Samuel',
                                '2 Samuel', '1 Kings',
                                '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm',
                                'Proverbs',
                                'Ecclesiastes',
                                'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea',
                                'Joel',
                                'Amos', 'Obadiah', 'Jonah',
                                'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

                newtestbooks = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
                                'Galatians',
                                'Ephesians',
                                'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy',
                                '2 Timothy',
                                'Titus', 'Philemon',
                                'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude',
                                'Revelation']

                new = []
                old = []

                for book in book_results:
                    book = format_entry(book)
                    if book in newtestbooks:
                        if book not in new:
                            new.append(book)
                    elif book in oldtestbooks:
                        if book not in old:
                            old.append(book)

                def edit_new_scripture_selection():
                    scripturelist = ['Pick a book']

                    for book in newtestbooks:
                        strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(
                            ',', '').replace("'", '')
                        scripturelist.append(strbook)

                    for newbook in new:
                        bookbox = ttk.Combobox(newtestframe, values=scripturelist)
                        bookbox.set(value=newbook)
                        bookbox.pack(padx=5, pady=5)
                        cur.execute('SELECT ChapVerse FROM SongScripture WHERE Book = ? AND SongID = ?',
                                    (newbook, songid))
                        chapverse = cur.fetchone()
                        bookentry = Entry(newtestframe, width=10)
                        bookentry.insert(0, format_entry(chapverse))
                        bookentry.pack(padx=5, pady=5)

                def edit_old_scripture_selection():
                    scripturelist = ['Pick a book']

                    for book in oldtestbooks:
                        strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(
                            ',', '').replace("'", '')
                        scripturelist.append(strbook)

                    for oldbook in old:
                        bookbox = ttk.Combobox(oldtestframe, values=scripturelist)
                        bookbox.set(value=oldbook)
                        bookbox.pack(padx=5, pady=5)
                        cur.execute('SELECT ChapVerse FROM SongScripture WHERE Book = ? AND SongID = ?',
                                    (oldbook, songid))
                        chapverse = cur.fetchone()
                        bookentry = Entry(oldtestframe, width=10)
                        bookentry.insert(0, format_entry(chapverse))
                        bookentry.pack(padx=5, pady=5)

                edit_new_scripture_selection()
                edit_old_scripture_selection()

                def edit_song():
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    title = titleentry.get()
                    songwriter = writerentry.get()
                    pages = pagesentry.get()
                    keysig = keyentry.get()
                    timesig = timeentry.get()
                    songinfo = get_values()
                    songid = songinfo[0]

                    try:
                        if title != '' and songwriter != '':
                            conn = lite.connect("CKF.db")
                            cur = conn.cursor()

                            cur.execute(
                                'UPDATE Song SET Title = ?, Songwriter = ?, Pages = ?, KeySig = ?, TimeSig = ? WHERE SongID = ?',
                                (title, songwriter, pages, keysig, timesig, songid))
                            conn.commit()

                            cur.execute('DELETE FROM SongTheme WHERE SongID = ?', (songid,))
                            cur.execute('DELETE FROM InstrumentReq WHERE SongID = ?', (songid,))
                            conn.commit()

                            reqinstrwidgets = instrframe.winfo_children()
                            for widget in reqinstrwidgets:
                                if isinstance(widget, ttk.Combobox):
                                    if widget.get() != 'Pick an instrument':
                                        conn = lite.connect("CKF.db")
                                        cur = conn.cursor()
                                        instr = widget.get()
                                        cur.execute('SELECT InstrumentID FROM Instrument WHERE Instrument = ?',
                                                    (instr,))
                                        instrument = cur.fetchone()
                                        instrid = functools.reduce(lambda sub, ele: sub * 10 + ele, instrument)
                                        cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                    (title, songwriter))
                                        song = cur.fetchone()
                                        songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                        cur.execute('SELECT InstrumentID FROM InstrumentReq WHERE SongID = ?',
                                                    (songid,))
                                        results = cur.fetchall()
                                        if instrument not in results:
                                            cur.execute('INSERT INTO InstrumentReq VALUES (?, ?)',
                                                        (int(songid), int(instrid)))
                                            conn.commit()

                            themewidgets = themeframe.winfo_children()
                            for widget in themewidgets:
                                if isinstance(widget, ttk.Combobox):
                                    if widget.get() != 'Pick a theme':
                                        conn = lite.connect("CKF.db")
                                        cur = conn.cursor()
                                        theme = widget.get()
                                        cur.execute('SELECT ThemeID FROM Theme WHERE Theme = ?', (theme,))
                                        my_theme = cur.fetchone()
                                        themeid = functools.reduce(lambda sub, ele: sub * 10 + ele, my_theme)
                                        cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                    (title, songwriter))
                                        song = cur.fetchone()
                                        songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                        cur.execute('SELECT ThemeID FROM SongTheme WHERE SongID = ?',
                                                    song)
                                        results = cur.fetchall()
                                        if my_theme not in results:
                                            cur.execute('INSERT INTO SongTheme VALUES (?, ?)',
                                                        (int(songid), int(themeid)))
                                            conn.commit()

                            oldtestwidgets = oldtestframe.winfo_children()
                            for oldcombowidget in oldtestwidgets:
                                if isinstance(oldcombowidget, ttk.Combobox):
                                    book = oldcombowidget.get()
                                    if oldcombowidget.get() != 'Pick a book':
                                        cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                    (title, songwriter))
                                        song = cur.fetchone()
                                        songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                        cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?',
                                                    song)
                                        results = cur.fetchall()
                                        if book not in results:
                                            cur.execute('INSERT INTO SongScripture (SongID, Book) VALUES (?, ?)',
                                                        (int(songid), book))
                                            conn.commit()
                                    else:
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ?', (songid,))
                                        pass

                                elif isinstance(oldcombowidget, Entry):
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                    cur.execute('SELECT ChapVerse FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                    reference = cur.fetchall()
                                    if oldcombowidget.get() == '':
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                    (songid, book))
                                    elif oldcombowidget.get() not in reference:
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                    (songid, book))
                                        cur.execute('INSERT INTO SongScripture VALUES (?, ?, ?)',
                                                    (songid, book, oldcombowidget.get()))

                                    conn.commit()

                            newtestwidgets = newtestframe.winfo_children()
                            for newcombowidget in newtestwidgets:
                                if isinstance(newcombowidget, ttk.Combobox):
                                    book = newcombowidget.get()
                                    if book != 'Pick a book':
                                        cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                    (title, songwriter))
                                        song = cur.fetchone()
                                        songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                        cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?',
                                                    song)
                                        results = cur.fetchall()
                                        if book not in results:
                                            cur.execute('INSERT INTO SongScripture (SongID, Book) VALUES (?, ?)',
                                                        (int(songid), book))
                                            conn.commit()
                                    else:
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ?', (songid,))
                                        pass

                                if isinstance(newcombowidget, Entry):
                                    cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                                (title, songwriter))
                                    song = cur.fetchone()
                                    songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song)
                                    cur.execute('SELECT ChapVerse FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                (songid, book))
                                    reference = cur.fetchall()
                                    if newcombowidget.get() == '':
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                    (songid, book))
                                    if newcombowidget.get() not in reference:
                                        cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?',
                                                    (songid, book))
                                        cur.execute('INSERT INTO SongScripture VALUES (?, ?, ?)',
                                                    (songid, book, newcombowidget.get()))

                                    conn.commit()

                            messagebox.showinfo('Successfully Completed', 'Song was successfully edited.',
                                                parent=edit_songs_root)

                            edit_songs_root.destroy()

                            update_song_table()
                        else:
                            messagebox.showinfo('Error Editing Song',
                                                'Title and Songwriter must be filled out in order to add a musician.',
                                                parent=edit_songs_root)
                    except:
                        messagebox.showerror('Error', 'Sorry, there was an error editing this song.',
                                             parent=edit_songs_root)
            else:
                messagebox.showinfo('', 'Select a song, then click the "Edit Song" button.',
                                    parent=songs_root)

            def instrument_selection():
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')',
                                                                                                          '').replace(
                        ',', '').replace("'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(value=instrlist[0])
                instrbox.pack(padx=5, pady=5)

            def new_scripture_selection():
                scripturelist = ['Pick a book']

                for book in newtestbooks:
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                    '').replace(
                        "'", '')
                    scripturelist.append(strbook)

                bookbox = ttk.Combobox(newtestframe, values=scripturelist)
                bookbox.set(value=scripturelist[0])
                bookbox.pack(padx=5, pady=5)
                bookentry = Entry(newtestframe, width=10)
                bookentry.pack(padx=5, pady=5)

            def old_scripture_selection():
                scripturelist = ['Pick a book']

                for book in oldtestbooks:
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',',
                                                                                                                    '').replace(
                        "'", '')
                    scripturelist.append(strbook)

                bookbox = ttk.Combobox(oldtestframe, values=scripturelist)
                bookbox.set(value=scripturelist[0])
                bookbox.pack(padx=5, pady=5)
                bookentry = Entry(oldtestframe, width=10)
                bookentry.pack(padx=5, pady=5)

            def theme_selection():
                conn = lite.connect("CKF.db")
                cur = conn.cursor()

                themelist = ['Pick a theme']
                cur.execute('SELECT Theme FROM Theme')
                themes = cur.fetchall()

                for theme in themes:
                    strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(
                        ',', '').replace("'", '')
                    themelist.append(strtheme)

                themebox = ttk.Combobox(themeframe, values=themelist)
                themebox.set(value=themelist[0])
                themebox.pack(padx=5, pady=5)
                return themebox

            instrnotelbl = Label(addinstrframe,
                                 text='Note: Set Instrument Recommendation to "Pick an instrument" to remove.')
            addinstrbtn = Button(addinstrframe, bg='#5F388C', fg='white', text='Add Instrument Recommendation',
                                 command=instrument_selection)

            scripturenotelbl = Label(addoldtestframe,
                                     text='Note: Set book to "Pick a book" and clear the chapter/verse entry to remove a reference.')

            addnewtestbtn = Button(addnewtestframe, bg='#5F388C', fg='white', text='Add New Testament reference',
                                   command=new_scripture_selection)
            addoldtestbtn = Button(addoldtestframe, bg='#5F388C', fg='white', text='Add Old Testament reference',
                                   command=old_scripture_selection)
            notelbl = Label(noteframe, text='Note: Set theme to "Pick a theme" to remove')
            addthemebtn = Button(addthemeframe, bg='#5F388C', fg='white', text='Add a theme',
                                 command=theme_selection)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=edit_song)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=edit_songs_root.destroy)

            titlelbl.grid(column=1, row=1, padx=5, pady=10)
            titleentry.grid(column=2, row=1, padx=5, pady=10)

            writerlbl.grid(column=1, row=2, padx=5, pady=10)
            writerentry.grid(column=2, row=2, padx=5, pady=10)

            pageslbl.grid(column=1, row=3, padx=5, pady=10)
            pagesentry.grid(column=2, row=3, padx=5, pady=10)

            keylbl.grid(column=1, row=4, padx=5, pady=10)
            keyentry.grid(column=2, row=4, padx=5, pady=10)

            timelbl.grid(column=1, row=5, padx=5, pady=10)
            timeentry.grid(column=2, row=5, padx=5, pady=10)

            instrnotelbl.pack()
            addinstrbtn.pack()

            notelbl.grid(column=2, row=6, padx=5, pady=5)
            addthemebtn.pack()

            scripturenotelbl.pack()
            addnewtestbtn.pack()
            addoldtestbtn.pack()

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        def new_theme():
            new_theme_root = tk.Tk()

            new_theme_root.state('zoomed')
            new_theme_root.geometry('800x600')
            new_theme_root.title('Themes')
            # new_theme_root.iconbitmap('CKF_image.ico')

            def add_theme():
                theme = themeentry.get()

                try:
                    if theme != '':
                        cur.execute('INSERT INTO Theme (Theme) VALUES (?)',
                                    (theme,))
                        conn.commit()

                        messagebox.showinfo('Successfully Completed', 'Theme was successfully added.',
                                            parent=new_theme_root)

                        new_theme_root.destroy()

                        update_theme_table()

                    else:
                        messagebox.showinfo('Error Adding Theme',
                                            'Theme must be filled out in order to add a theme.',
                                            parent=new_theme_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error adding this theme.',
                                         parent=new_theme_root)

            themeframe = Frame(new_theme_root)
            saveframe = Frame(new_theme_root)

            themeframe.pack()
            saveframe.pack()

            themelbl = Label(themeframe, text='Theme:')
            themeentry = Entry(themeframe, width=25)

            savebtn = Button(saveframe, bg='#5F388C', fg='white', text='Save', command=add_theme)
            cancelbtn = Button(saveframe, bg='#5F388C', fg='white', text='Cancel', command=new_theme_root.destroy)

            themelbl.grid(column=1, row=1, padx=5, pady=30)
            themeentry.grid(column=2, row=1, padx=5, pady=30)

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        def edit_themes():
            if themetable.focus() != '':
                edit_theme_root = tk.Tk()

                edit_theme_root.state('zoomed')
                edit_theme_root.geometry('800x600')
                edit_theme_root.title('Themes')
                # edit_theme_root.iconbitmap('CKF_image.ico')

                selected = themetable.focus()
                themeinfo = themetable.item(selected, 'values')
                themeid = themeinfo[0]

                themeframe = Frame(edit_theme_root)
                btnframe = Frame(edit_theme_root)

                themeframe.pack()
                btnframe.pack()

                cur.execute('SELECT Theme FROM Theme WHERE ThemeID = ?', (themeid,))
                my_theme = cur.fetchone()
                my_theme = ''.join(my_theme).replace('{', '').replace('}', '')
                themelbl = Label(themeframe, text='Theme:')
                themeentry = Entry(themeframe, width=25)
                themeentry.insert(0, my_theme)

                def edit_theme():
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    themename = themeentry.get()

                    selected = themetable.focus()
                    themeinfo = themetable.item(selected, 'values')
                    themeid = themeinfo[0]

                    try:
                        if themename != '':
                            cur.execute('UPDATE Theme SET Theme = ? WHERE ThemeID = ?',
                                        (themename, themeid))
                            conn.commit()

                            messagebox.showinfo('Successfully Completed', 'Theme was successfully edited.',
                                                parent=edit_theme_root)

                            edit_theme_root.destroy()

                            update_theme_table()

                        else:
                            messagebox.showinfo('Error Editing Theme',
                                                'Theme must be filled out in order to edit a theme.',
                                                parent=edit_theme_root)
                    except:
                        messagebox.showerror('Error', 'Sorry, there was an error editing this theme.',
                                             parent=edit_theme_root)

                savebtn = Button(btnframe, bg='#5F388C', fg='white', text='Save', command=edit_theme)
                cancelbtn = Button(btnframe, bg='#5F388C', fg='white', text='Cancel', command=edit_theme_root.destroy)

                themelbl.grid(column=1, row=1, padx=5, pady=30)
                themeentry.grid(column=2, row=1, padx=5, pady=30)

                savebtn.grid(column=2, row=8, padx=5, pady=5)
                cancelbtn.grid(column=1, row=8, padx=5, pady=5)

            else:
                messagebox.showinfo('', 'Please select a theme, then click the "Edit Theme" button.',
                                    parent=songs_root)

        def del_theme():
            if themetable.focus() == '':
                messagebox.showinfo('',
                                    'Please select a theme to delete, and then click the "Delete Theme" button.',
                                    parent=songs_root)
            else:
                delete = messagebox.askyesno('Warning',
                                             "This action will permanently delete this theme. Are you sure you'd like to continue?",
                                             parent=songs_root)
                if delete:
                    conn = lite.connect("CKF.db")
                    cur = conn.cursor()

                    selected = themetable.focus()
                    values = themetable.item(selected, 'values')
                    themeid = values[0]
                    themetable.delete(selected)
                    # Delete From Database
                    cur.execute("DELETE from Theme WHERE ThemeID = ?", (themeid,))
                    cur.execute('DELETE FROM SongTheme WHERE ThemeID = ?', (themeid,))

                    # Commit changes
                    conn.commit()

                    update_theme_table()

                    messagebox.showinfo('Successfully Completed', 'Theme was successfully deleted.',
                                        parent=songs_root)

        homebtn = Button(btnframe, bg='#5F388C', fg='white', text='Home', command=songs_root.destroy)
        viewinstrbtn = Button(btnframe, bg='#5F388C', fg='white', text="View Song's Instrument Recommendation",
                              command=view_instr)
        viewreferencesbtn = Button(btnframe, bg='#5F388C', fg='white', text="View Song's Scripture Reference(s)",
                                   command=view_reference)
        viewthemesbtn = Button(btnframe, bg='#5F388C', fg='white', text="View Song's Theme(s)", command=view_theme)
        addsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Add Song', command=new_songs)
        editsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Edit Song', command=edit_songs)
        delsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Delete Song', command=are_you_sure)
        addthemebtn = Button(themetableframe, bg='#5F388C', fg='white', text='Add Theme', command=new_theme)
        editthemebtn = Button(themetableframe, bg='#5F388C', fg='white', text='Edit Theme', command=edit_themes)
        delthemebtn = Button(themetableframe, bg='#5F388C', fg='white', text='Delete Theme', command=del_theme)
        fillerlbl = Label(fillerframe, text='')

        homebtn.pack(side='left', padx=10, pady=20)
        viewinstrbtn.pack(side='left', padx=10, pady=20)
        viewreferencesbtn.pack(side='left', padx=10, pady=20)
        viewthemesbtn.pack(side='left', padx=10, pady=20)
        addsongbtn.pack(side='left', padx=10, pady=20)
        editsongbtn.pack(side='left', padx=10, pady=20)
        delsongbtn.pack(side='left', padx=10, pady=20)
        delthemebtn.pack(side='right', padx=5, pady=(5, 50))
        editthemebtn.pack(side='right', padx=5, pady=(5, 50))
        addthemebtn.pack(side='right', padx=5, pady=(5, 50))
        fillerlbl.pack(pady=100)

        songs_root.mainloop()

    welcomelbl = Label(welcomeframe, text='Welcome to the CKF planner! What would you like to do?',
                       height=15, font=('Calibri light', 13, 'bold'))
    planbtn = Button(planframe, bg='#5F388C', fg='white', text='Plan for the upcoming weeks',
                     command=Future)
    pastbtn = Button(pastframe, bg='#5F388C', fg='white', text='Look at past schedules', command=Past)
    musicianbtn = Button(musicianframe, bg='#5F388C', fg='white', text='Look at musicians', command=Musicians)
    songbtn = Button(songframe, bg='#5F388C', fg='white', text='Look at songs', command=Songs)

    welcomelbl.grid(row=1, padx=10, pady=10)
    planbtn.grid(row=2, padx=10, pady=10)
    pastbtn.grid(row=3, padx=10, pady=10)
    musicianbtn.grid(row=4, padx=10, pady=10)
    songbtn.grid(row=5, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    Home()
