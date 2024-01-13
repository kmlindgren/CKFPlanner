import _tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3 as lite
import functools


def Musicians():
    conn = lite.connect("CKF.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Musician(MusicianID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Email TEXT, Phone TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Instrument(InstrumentID INTEGER PRIMARY KEY, Instrument TEXT)")

    conn.commit()

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
                    "ORDER BY FirstName", (id, id, fname, fname, lname, lname, email, email, phone, phone, instr, instr))

        rows = cur.fetchall()

        musiciantable.delete(*musiciantable.get_children())

        for row in rows:
            musiciantable.insert(parent='', index='end', text='',
                                 values=row)

    searchbtn = Button(searchbtnframe, bg='#5F388C', fg='white', text='Search', width=5, height=1, command=search_musicians)
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
                                cur.execute('SELECT InstrumentID FROM MusicianInstruments WHERE MusicianID = ?', musician)
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
                strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace(
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
            messagebox.showinfo('', 'Please select a musician to delete, and then click the "Delete Musician" button.', parent=musicians_root)
        else:
            delete = messagebox.askyesno('Warning', "This action will permanently delete this musician. Are you sure you'd like to continue?", parent=musicians_root)
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
            cur.execute('SELECT Instrument FROM MusicianInstruments INNER JOIN Instrument ON Instrument.InstrumentID = '
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

            messagebox.showinfo("Musician's Instruments", f"Musician's Instruments:{list_to_string(instrlist)}", parent=musicians_root)

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

            cur.execute('SELECT Instrument FROM MusicianInstruments INNER JOIN Instrument ON Instrument.InstrumentID = MusicianInstruments.InstrumentID WHERE MusicianID = ?',
                        (musicianid,))
            results = cur.fetchall()

            for i in results:
                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(value=str(i).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
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
                        cur.execute('UPDATE Musician SET FirstName = ?, LastName = ?, Email = ?, Phone = ? WHERE MusicianID = ?',
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
                                    cur.execute('SELECT InstrumentID FROM Instrument WHERE Instrument = ?', (instr,))
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
                                            'First Name, Last Name, and Email must be filled out in order to edit a musician.', parent=edit_musicians_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error editing this musician.', parent=edit_musicians_root)
        else:
            messagebox.showinfo('', 'Select a musician, then click the "Edit Musician" button.', parent=musicians_root)

        def instrument_selection():
            conn = lite.connect("CKF.db")
            cur = conn.cursor()

            instrlist = ['Pick an instrument']
            cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
            instruments = cur.fetchall()

            for instrument in instruments:
                strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
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
                                            'Instrument must be filled out in order to edit an instrument.', parent=edit_instr_root)
                except:
                    messagebox.showerror('Error', 'Sorry, there was an error editing this musician.', parent=edit_instr_root)

            savebtn = Button(btnframe, bg='#5F388C', fg='white', text='Save', command=edit_instr)
            cancelbtn = Button(btnframe, bg='#5F388C', fg='white', text='Cancel', command=edit_instr_root.destroy)

            instrlbl.grid(column=1, row=1, padx=5, pady=30)
            instrentry.grid(column=2, row=1, padx=5, pady=30)

            savebtn.grid(column=2, row=8, padx=5, pady=5)
            cancelbtn.grid(column=1, row=8, padx=5, pady=5)

        else:
            messagebox.showinfo('', 'Please select an instrument, then click the "Edit Instrument" button.', parent=musicians_root)

    def del_instr():
        if instrtable.focus() == '':
            messagebox.showinfo('', 'Please select an instrument to delete, and then click the "Delete Instrument" button.', parent=musicians_root)
        else:
            delete = messagebox.askyesno('Warning', "This action will permanently delete this instrument. Are you sure you'd like to continue?", parent=musicians_root)
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

                messagebox.showinfo('Successfully Completed', 'Instrument was successfully deleted.', parent=musicians_root)


    homebtn = Button(musbtnframe, bg='#5F388C', fg='white', text='Home', command=musicians_root.destroy)
    viewinstrumentsbtn = Button(musbtnframe, bg='#5F388C', fg='white', text="View Musician's Instrument(s)", command=view_instr)
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
