import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import date, timedelta
import sqlite3 as lite
from tkinter import messagebox


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
            cur.execute('SELECT MusicianSchedule.Sunday FROM MusicianSchedule INTERSECT SELECT SongSchedule.Sunday FROM SongSchedule')
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
                                                f"Musician's Instruments:{list_to_string(instrlist)}",
                                                parent=new_schedule_root)

                        except IndexError:
                            messagebox.showinfo('', 'Please select a musician to view their instruments.',
                                                parent=new_schedule_root)

                    def del_mus():
                        selected = musiciantable.focus()
                        if selected != '':
                            sure = messagebox.askyesno('', "This action will remove this musician from this schedule. "
                                                           "Are you sure you'd like to continue?", parent=new_schedule_root)
                            if sure:
                                values = musiciantable.item(selected, 'values')
                                musiciantable.delete(selected)
                                # Delete From Database
                                cur.execute("DELETE from MusicianSchedule WHERE MusicianID = ? AND Sunday = ?", (values[0], scheduledate))

                                # Commit changes
                                conn.commit()

                                update_musician_table()

                                messagebox.showinfo('Successfully Completed', 'Musician was successfully deleted.',
                                                    parent=new_schedule_root)
                        else:
                            messagebox.showinfo('', 'Please select a musician to delete from the schedule, and then click the "Delete Musician" button.')


                    viewmusinstrbtn = Button(btnframe, bg='#5F388C', fg='white', text='View Musician Instrument(s)',
                                             command=view_mus_instr)
                    viewmusinstrbtn.grid(column=2, row=0, padx=5, pady=10)

                    delmusicianbtn = Button(btnframe, bg='#5F388C', fg='white', text='Delete Musician', command=del_mus)
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
                                    cur.execute('SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ?',
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
                                    cur.execute('SELECT MusicianID FROM Musician WHERE FirstName = ? AND LastName = ?',
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
                                                        cur.execute('SELECT * FROM MusicianSchedule WHERE Sunday = ?', (scheduledate,))
                                                        this_schedule = cur.fetchall()
                                                        check_if_in = (int(strmusid), int(strinstrid), str(scheduledate))
                                                        if check_if_in not in this_schedule:
                                                            cur.execute('INSERT INTO MusicianSchedule VALUES (?, ?, ?)',
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
                            savemusbtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Save', command=add_mus)

                            addinstrbtn.pack(pady=10)
                            cancelmusbtn.grid(column=0, row=0, padx=5)
                            savemusbtn.grid(column=1, row=0, padx=5)

                        mus_combo()

                    addmusicianbtn = Button(btnframe, bg='#5F388C', fg='white', text='Add Musician', command=musician)
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

                            cur.execute('SELECT Song.SongID, Title FROM Song INNER JOIN SongSchedule ON Song.SongID '
                                '= SongSchedule.SongID WHERE Sunday = ?', (str(scheduledate),))
                            results = cur.fetchall()

                            for row in results:
                                songtable.insert("", tk.END, values=row)

                        update_song_table()

                        def del_song():
                            selected = songtable.focus()
                            if selected != '':
                                sure = messagebox.askyesno('', "This action will remove this song from this schedule. "
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
                                        cur.execute('SELECT Sunday FROM SongSchedule WHERE SongID = ? ORDER BY Sunday DESC',
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

                                        cur.execute('SELECT DISTINCT InstrumentReq.InstrumentID FROM InstrumentReq WHERE InstrumentReq.SongID = ? '
                                                    'AND InstrumentReq.InstrumentID NOT IN (SELECT MusicianSchedule.InstrumentID FROM MusicianSchedule '
                                                    'WHERE MusicianSchedule.Sunday = ?)',
                                                    (songid, str(scheduledate)))

                                        notintersect = cur.fetchall()

                                        if len(notintersect) == 0:
                                            add()
                                        else:
                                            cur.execute('SELECT Instrument FROM Instrument INNER JOIN InstrumentReq ON Instrument.InstrumentID = InstrumentReq.InstrumentID '
                                                        'WHERE SongID = ?', (songid,))
                                            instrname = cur.fetchall()
                                            instrname = ''.join(str(instrname))
                                            instrname = instrname.replace("'", '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '')
                                            print(instrname)
                                            addanyway = messagebox.askyesno('', f'There are currently no musicians playing a recommended instrument for this song ({instrname}). '
                                                                    f'Would you still like to add this song to the schedule?', parent=add_song_root)
                                            if addanyway:
                                                add()



                                    else:
                                        messagebox.showinfo('Song Already Exists', 'This song already exists in this schedule.', parent=add_song_root)
                                else:
                                    messagebox.showinfo('', 'Select a song, then click the "Add to Schedule" button.', parent=add_song_root)

                            cancelbtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Cancel', command=add_song_root.destroy)
                            savebtn = Button(cancelsavebtnframe, bg='#5F388C', fg='white', text='Add to Schedule', command=add_song)

                            cancelbtn.grid(column=0, row=0, padx=5, pady=5)
                            savebtn.grid(column=1, row=0, padx=5, pady=5)

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
                                                    f"Song's Recommended Instruments:{list_to_string(instrlist)}",
                                                    parent=new_schedule_root)

                            except IndexError:
                                messagebox.showinfo('', 'Please select a song to view its instrument recommendation.',
                                                    parent=new_schedule_root)

                        addsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Add Song', command=song)
                        delsongbtn = Button(btnframe, bg='#5F388C', fg='white', text='Delete Song', command=del_song)
                        viewsonginstrbtn = Button(btnframe, bg='#5F388C', fg='white', text='View Song Instrument Recommendation', command=view_instr)

                        addsongbtn.grid(column=4, row=0, padx=(25, 5), pady=10)
                        delsongbtn.grid(column=5, row=0, padx=5, pady=10)
                        viewsonginstrbtn.grid(column=6, row=0, padx=5, pady=10)

                        exitbtn = Button(exitframe, bg='#5F388C', fg='white', text='Exit', width=5,
                                         command=new_schedule_root.destroy)

                        exitbtn.grid(column=1, row=1, padx=5, pady=10)

                        def update_tables():
                            musiciantable.delete(*musiciantable.get_children())

                            cur.execute('SELECT DISTINCT Musician.MusicianID, FirstName, LastName, Email FROM Musician INNER JOIN MusicianSchedule ON Musician.MusicianID '
                                '= MusicianSchedule.MusicianID WHERE Sunday = ?', (str(scheduledate),))

                            results = cur.fetchall()

                            for row in results:
                                musiciantable.insert("", tk.END, values=row)

                            songtable.delete(*songtable.get_children())

                            cur.execute('SELECT Song.SongID, Title FROM Song INNER JOIN SongSchedule ON Song.SongID '
                                        '= SongSchedule.SongID WHERE Sunday = ?', (str(scheduledate),))
                            results = cur.fetchall()

                            for row in results:
                                songtable.insert("", tk.END, values=row)
                        update_tables()

                        def clear_schedule():
                            sure = messagebox.askyesno('',
                                                       "This action will remove all songs and musicians from this schedule. "
                                                       "Are you sure you'd like to continue?", parent=new_schedule_root)
                            if sure:
                                cur.execute('DELETE FROM MusicianSchedule WHERE Sunday = ?', (str(scheduledate),))
                                cur.execute('DELETE FROM SongSchedule WHERE Sunday = ?', (str(scheduledate),))
                                conn.commit()
                                update_tables()
                                messagebox.showinfo('Successfully Completed', 'Schedule was successfully cleared.', parent=new_schedule_root)

                        clearschedulebtn = Button(exitframe, bg='#5F388C', fg='white', text='Clear Schedule',
                                                  command=clear_schedule)
                        clearschedulebtn.grid(column=2, row=1, padx=5, pady=5)

                        schedulefillerlbl = Label(exitframe, text='')
                        schedulefillerlbl.grid(column=0, row=1, padx=40)

                    song_table()
                mus_table()

            if str(scheduledate) in sundays:
                proceed = messagebox.askyesno('Schedule Already Exists', 'There is already a schedule for this Sunday. '
                                                                         'Would you like to continue?', parent=future_root)
                if not proceed:
                    pass
                else:
                    new_schedule_plan()
                    pass
            elif str(scheduledate) not in sundays:
                new_schedule_plan()

        else:
            messagebox.showinfo('', 'Please select a date, and then click the "Create Schedule" button.', parent=future_root)

    homebtn = Button(btnframe, bg='#5F388C', fg='white', text='Home', command=future_root.destroy)
    schedulebtn = Button(btnframe, bg='#5F388C', fg='white', text='Create/Edit Schedule', command=new_schedule)

    homebtn.pack(side='left', padx=10)
    schedulebtn.pack(side='left', padx=10)

    future_root.mainloop()
