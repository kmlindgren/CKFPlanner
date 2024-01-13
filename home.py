import tkinter as tk
import future
import past
import musicians
import songs
import sqlite3 as lite
from tkinter import *
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

    welcomelbl = Label(welcomeframe, text='Welcome to the CKF planner! What would you like to do?',
                       height=15, font=('Calibri light', 13, 'bold'))
    planbtn = Button(planframe, bg='#5F388C', fg='white', text='Plan for the upcoming weeks',
                     command=future.Future)
    pastbtn = Button(pastframe, bg='#5F388C', fg='white', text='Look at past schedules', command=past.Past)
    musicianbtn = Button(musicianframe, bg='#5F388C', fg='white', text='Look at musicians', command=musicians.Musicians)
    songbtn = Button(songframe, bg='#5F388C', fg='white', text='Look at songs', command=songs.Songs)

    welcomelbl.grid(row=1, padx=10, pady=10)
    planbtn.grid(row=2, padx=10, pady=10)
    pastbtn.grid(row=3, padx=10, pady=10)
    musicianbtn.grid(row=4, padx=10, pady=10)
    songbtn.grid(row=5, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    Home()
