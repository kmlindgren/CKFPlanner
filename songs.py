import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3 as lite
import functools
from tkinter import messagebox

oldtestbooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings',
        '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs', 'Ecclesiastes',
        'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah',
        'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

newtestbooks = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
                'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
                'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']


def Songs():
    conn = lite.connect("CKF.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Song(SongID INTEGER PRIMARY KEY, Title TEXT, Pages INTEGER, KeySig TEXT, TimeSig TEXT, Songwriter TEXT)")
    conn.commit()

    songs_root = tk.Tk()

    songs_root.state('zoomed')
    songs_root.geometry('800x600')
    songs_root.title('Songs')
    songs_root.iconbitmap('CKF_image.ico')

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

    searchbtn = Button(searchbtnframe, bg='#5F388C', fg='white', text='Search', width=5, height=1, command=search_songs)
    searchbtn.pack(pady=10)

    def new_songs():
        new_songs_root = tk.Tk()

        new_songs_root.state('zoomed')
        new_songs_root.geometry('800x600')
        new_songs_root.title('Songs')
        new_songs_root.iconbitmap('CKF_image.ico')

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
                    cur.execute('INSERT INTO Song (Title, Songwriter, Pages, KeySig, TimeSig) VALUES (?, ?, ?, ?, ?)',
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
                                themeid = functools.reduce(lambda sub, ele: sub * 10 + ele, my_theme,)
                                cur.execute('SELECT SongID FROM Song WHERE Title = ? AND Songwriter = ?',
                                           (title, songwriter))
                                song = cur.fetchone()
                                songid = functools.reduce(lambda sub, ele: sub * 10 + ele, song,)
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
                                cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
                            elif oldcombowidget.get() not in reference:
                                cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
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
                                cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
                            if newcombowidget.get() not in reference:
                                cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
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
                strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                instrlist.append(strinstr)

            instrbox = ttk.Combobox(instrframe, values=instrlist)
            instrbox.set(value=instrlist[0])
            instrbox.pack(padx=5, pady=5)

        def new_scripture_selection():
            scripturelist = ['Pick a book']

            books = open('new_testament.txt', 'r')
            file_contents = books.read()
            bookslist = file_contents.split('\n')

            for book in bookslist:
                strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                scripturelist.append(strbook)

            bookbox = ttk.Combobox(newtestframe, values=scripturelist)
            bookbox.set(value=scripturelist[0])
            bookbox.pack(padx=5, pady=5)
            bookentry = Entry(newtestframe, width=10)
            bookentry.pack(padx=5, pady=5)

        def old_scripture_selection():
            scripturelist = ['Pick a book']

            books = open('old_testament.txt', 'r')
            file_contents = books.read()
            bookslist = file_contents.split('\n')

            for book in bookslist:
                strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
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
                strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
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
            messagebox.showinfo('', 'Please select a song to delete, and then click the "Delete Song" button.', parent=songs_root)
        else:
            delete = messagebox.askyesno('Warning', "This action will permanently delete this song. Are you sure you'd like to continue?", parent=songs_root)
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

            messagebox.showinfo("Musician's Instruments", f"Song's Recommended Instruments:{list_to_string(instrlist)}", parent=songs_root)

        except IndexError:
            messagebox.showinfo('', 'Please select a song to view its instrument recommendation.', parent=songs_root)

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

            messagebox.showinfo("Song's Scripture References", f"Song's Scripture References:{list_to_string(referencelist)}", parent=songs_root)

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
            edit_songs_root.iconbitmap('CKF_image.ico')

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
                formatted = strrow.replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
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

            cur.execute('SELECT Instrument FROM InstrumentReq INNER JOIN Instrument ON Instrument.InstrumentID = InstrumentReq.InstrumentID WHERE SongID = ?',
                        (songid,))
            results = cur.fetchall()

            for i in results:
                instrlist = ['Pick an instrument']
                cur.execute('SELECT Instrument FROM Instrument ORDER BY Instrument')
                instruments = cur.fetchall()

                for instrument in instruments:
                    strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                    instrlist.append(strinstr)

                instrbox = ttk.Combobox(instrframe, values=instrlist)
                instrbox.set(
                    value=str(i).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
                instrbox.pack(padx=5, pady=5)

            cur.execute('SELECT Theme FROM SongTheme INNER JOIN Theme ON Theme.ThemeID = '
                        'SongTheme.ThemeID WHERE SongID = ?', (songid,))
            results = cur.fetchall()

            for i in results:
                themelist = ['Pick a theme']
                cur.execute('SELECT Theme FROM Theme')
                themes = cur.fetchall()

                for theme in themes:
                    strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                    themelist.append(strtheme)

                themebox = ttk.Combobox(themeframe, values=themelist)
                themebox.set(value=format_entry(i))
                themebox.pack(padx=5, pady=5)

            cur.execute('SELECT Book FROM SongScripture WHERE SongID = ?', (songid,))
            book_results = cur.fetchall()

            # newbooks = open('new_testament.txt', 'r')
            # newfilecontents = newbooks.read()
            # newbookslist = newfilecontents.split('\n')
            #
            # oldbooks = open('old_testament.txt', 'r')
            # oldfilecontents = oldbooks.read()
            # oldbookslist = oldfilecontents.split('\n')

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
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                    scripturelist.append(strbook)

                for newbook in new:
                    bookbox = ttk.Combobox(newtestframe, values=scripturelist)
                    bookbox.set(value=newbook)
                    bookbox.pack(padx=5, pady=5)
                    cur.execute('SELECT ChapVerse FROM SongScripture WHERE Book = ? AND SongID = ?', (newbook, songid))
                    chapverse = cur.fetchone()
                    bookentry = Entry(newtestframe, width=10)
                    bookentry.insert(0, format_entry(chapverse))
                    bookentry.pack(padx=5, pady=5)

            def edit_old_scripture_selection():
                scripturelist = ['Pick a book']

                for book in oldtestbooks:
                    strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                    scripturelist.append(strbook)

                for oldbook in old:
                    bookbox = ttk.Combobox(oldtestframe, values=scripturelist)
                    bookbox.set(value=oldbook)
                    bookbox.pack(padx=5, pady=5)
                    cur.execute('SELECT ChapVerse FROM SongScripture WHERE Book = ? AND SongID = ?', (oldbook, songid))
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

                        cur.execute('UPDATE Song SET Title = ?, Songwriter = ?, Pages = ?, KeySig = ?, TimeSig = ? WHERE SongID = ?',
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
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
                                elif oldcombowidget.get() not in reference:
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
                                    cur.execute('INSERT INTO SongScripture VALUES (?, ?, ?)', (songid, book, oldcombowidget.get()))

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
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
                                if newcombowidget.get() not in reference:
                                    cur.execute('DELETE FROM SongScripture WHERE SongID = ? AND Book = ?', (songid, book))
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
                strinstr = str(instrument).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                instrlist.append(strinstr)

            instrbox = ttk.Combobox(instrframe, values=instrlist)
            instrbox.set(value=instrlist[0])
            instrbox.pack(padx=5, pady=5)

        def new_scripture_selection():
            scripturelist = ['Pick a book']

            books = open('new_testament.txt', 'r')
            file_contents = books.read()
            bookslist = file_contents.split('\n')

            for book in bookslist:
                strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace(
                    "'", '')
                scripturelist.append(strbook)

            bookbox = ttk.Combobox(newtestframe, values=scripturelist)
            bookbox.set(value=scripturelist[0])
            bookbox.pack(padx=5, pady=5)
            bookentry = Entry(newtestframe, width=10)
            bookentry.pack(padx=5, pady=5)

        def old_scripture_selection():
            scripturelist = ['Pick a book']

            books = open('old_testament.txt', 'r')
            file_contents = books.read()
            bookslist = file_contents.split('\n')

            for book in bookslist:
                strbook = str(book).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
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
                strtheme = str(theme).replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '')
                themelist.append(strtheme)

            themebox = ttk.Combobox(themeframe, values=themelist)
            themebox.set(value=themelist[0])
            themebox.pack(padx=5, pady=5)
            return themebox

        instrnotelbl = Label(addinstrframe, text='Note: Set Instrument Recommendation to "Pick an instrument" to remove.')
        addinstrbtn = Button(addinstrframe, bg='#5F388C', fg='white', text='Add Instrument Recommendation',
                               command=instrument_selection)

        scripturenotelbl = Label(addoldtestframe, text='Note: Set book to "Pick a book" and clear the chapter/verse entry to remove a reference.')

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
        new_theme_root.iconbitmap('CKF_image.ico')

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
            edit_theme_root.iconbitmap('CKF_image.ico')

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
    viewinstrbtn = Button(btnframe, bg='#5F388C', fg='white', text="View Song's Instrument Recommendation", command=view_instr)
    viewreferencesbtn = Button(btnframe, bg='#5F388C', fg='white', text="View Song's Scripture Reference(s)", command=view_reference)
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
