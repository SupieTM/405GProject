import mysql.connector
import tkinter as tk
from tkinter import ttk

# This is for the information for the dbConnection
import loginInfo as LI
from databaseInfo import DBHM


class App(tk.Tk):
    # dbConnection = mysql.connector.connect(
    #     host=LI.host,
    #     user=LI.user,
    #     password=LI.password,
    #     database=LI.database)

    dataBaseOptions = ["Faculty", "Student",
                       "Clubs", "Meeting", "Participation"]
    dataBaseManipulationOptions = ["View", "Add", "Delete", "Modify", "Join"]
    currentDBSelection = ""
    currentMSelection = ""

    def __init__(self):
        self.currentSelection = self.dataBaseOptions[0]
        super().__init__()

        # Configure the Windows
        self.title("Club database navigator")
        self.geometry("850x500+50+50")
        self.configure(background="lightgrey")

        # configure the grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Label
        # title_label = tk.Label(self, text="Club Navigator")
        # title_label.grid(row=0, column=1, columnspan=2, sticky='n')

        # comboBoxs
        comboBoxFrame = tk.Frame(self, bg="lightblue")
        comboBoxFrame.grid(row=0, column=0, sticky=tk.NSEW)

        comboBoxFrame.rowconfigure(0, weight=1)
        comboBoxFrame.rowconfigure(1, weight=1)
        comboBoxFrame.rowconfigure(2, weight=1)
        comboBoxFrame.columnconfigure(0, weight=1)

        selectionLabel = tk.Label(
            comboBoxFrame, text="Choose table and operation")
        selectionLabel.grid(row=0, column=0, sticky='s')

        comboBoxDB = ttk.Combobox(comboBoxFrame, values=self.dataBaseOptions)
        comboBoxDB.configure(justify="center", width=20)
        comboBoxDB.set("Select Database")
        comboBoxDB.bind("<<ComboboxSelected>>", self.changeDatabase)
        comboBoxDB.grid(row=1, column=0, padx=10)

        comboBoxM = ttk.Combobox(
            comboBoxFrame, values=self.dataBaseManipulationOptions)
        comboBoxM.configure(justify="center", width=20)
        comboBoxM.set("Select Operation")
        comboBoxM.bind("<<ComboboxSelected>>", self.changeManipulationOption)
        comboBoxM.grid(row=2, column=0, padx=10, sticky='n')

        self.tabs = {
            "View": None,
            "Add": None,
            "Delete": None,
            "Modify": None,
            "Join": None,
        }

        # Editing Tabs

        # view
        self.tabs["View"] = tk.Frame(self, bg="lightgreen")
        self.tabs["View"].grid(row=1, column=0, sticky='nsew')

        self.tabs["View"].rowconfigure(0, weight=1)
        self.tabs["View"].rowconfigure(1, weight=1)
        self.tabs["View"].rowconfigure(2, weight=1)
        self.tabs["View"].rowconfigure(3, weight=1)
        self.tabs["View"].rowconfigure(4, weight=1)
        self.tabs["View"].rowconfigure(5, weight=1)

        self.tabs["View"].columnconfigure(0, weight=1)
        self.tabs["View"].columnconfigure(1, weight=1)
        self.tabs["View"].columnconfigure(2, weight=1)

        viewTabTitle = tk.Label(self.tabs["View"], text="View")
        viewTabTitle.grid(row=0, column=1, columnspan=3, sticky='n')

        seletectTitle = tk.Label(self.tabs["View"], text="Select Columns: ")
        seletectTitle.grid(row=1, column=1, padx=10, sticky='w')

        selectEntry = tk.Entry(self.tabs["View"])
        selectEntry.grid(row=1, column=2, sticky='w')

        whereTitle = tk.Label(self.tabs["View"], text="Where: ")
        whereTitle.grid(row=2, column=1, padx=10, sticky='w')

        whereEntry = tk.Entry(self.tabs["View"])
        whereEntry.grid(row=2, column=2, sticky='w')

        joinTitle = tk.Label(self.tabs["View"], text="Joined with: ")
        joinTitle.grid(row=3, column=1, padx=10, sticky='w')

        joinEntry = tk.Entry(self.tabs["View"])
        joinEntry.grid(row=3, column=2, sticky='w')

        joinbyTitle = tk.Label(self.tabs["View"], text="on: ")
        joinbyTitle.grid(row=4, column=1, padx=10, sticky='w')

        joinbyEntry = tk.Entry(self.tabs["View"])
        joinbyEntry.grid(row=4, column=2, sticky='w')

        viewButton = tk.Button(
            self.tabs["View"], text="Select", command=self.buttonTest)
        viewButton.grid(row=5, column=0, columnspan=3, sticky='nsew')

        self.tabs["Add"] = tk.Frame(self, bg="lightgreen")
        self.tabs["Add"].grid(row=1, column=0, sticky='nsew')

        self.tabs["Add"].rowconfigure(0, weight=1)
        self.tabs["Add"].rowconfigure(1, weight=1)
        self.tabs["Add"].rowconfigure(2, weight=1)

        self.tabs["Add"].columnconfigure(0, weight=1)
        self.tabs["Add"].columnconfigure(1, weight=1)

        addTabTitle = tk.Label(self.tabs["Add"], text="Add")
        addTabTitle.grid(row=0, column=0, columnspan=3, sticky='n')

        addLabel = tk.Label(self.tabs["Add"], text="Insert")
        addLabel.grid(row=1, column=0, sticky='nw')

        addEntry = tk.Entry(self.tabs["Add"])
        addEntry.grid(row=1, column=1, sticky='nw')

        addButton = tk.Button(
            self.tabs["Add"], text="Select", command=self.buttonTest)
        addButton.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.tabs["Delete"] = tk.Frame(self, bg="lightgreen")
        self.tabs["Delete"].grid(row=1, column=0, sticky='nsew')

        self.tabs["Delete"].rowconfigure(0, weight=1)
        self.tabs["Delete"].rowconfigure(1, weight=1)
        self.tabs["Delete"].rowconfigure(2, weight=1)

        self.tabs["Delete"].columnconfigure(0, weight=1)
        self.tabs["Delete"].columnconfigure(1, weight=1)
        self.tabs["Delete"].columnconfigure(2, weight=1)

        deleteTabTitle = tk.Label(self.tabs["Delete"], text="Delete")
        deleteTabTitle.grid(row=0, column=0, columnspan=3, sticky='n')

        deleteButton = tk.Button(
            self.tabs["Delete"], text="Select", command=self.buttonTest)
        deleteButton.grid(row=2, column=2, sticky='nsew')

        self.tabs["Modify"] = tk.Frame(self, bg="lightgreen")
        self.tabs["Modify"].grid(row=1, column=0, sticky='nsew')

        self.tabs["Modify"].rowconfigure(0, weight=1)
        self.tabs["Modify"].rowconfigure(1, weight=1)
        self.tabs["Modify"].rowconfigure(2, weight=1)

        self.tabs["Modify"].columnconfigure(0, weight=1)
        self.tabs["Modify"].columnconfigure(1, weight=1)
        self.tabs["Modify"].columnconfigure(2, weight=1)

        modifyTabTitle = tk.Label(self.tabs["Modify"], text="Modify")
        modifyTabTitle.grid(row=0, column=0, columnspan=3, sticky='n')

        modifyButton = tk.Button(
            self.tabs["Modify"], text="Select", command=self.buttonTest)
        modifyButton.grid(row=2, column=2, sticky='nsew')

        self.tabs["Join"] = tk.Frame(self, bg="lightgreen")
        self.tabs["Join"].grid(row=1, column=0, sticky='nsew')

        self.tabs["Join"].rowconfigure(0, weight=1)
        self.tabs["Join"].rowconfigure(1, weight=1)
        self.tabs["Join"].rowconfigure(2, weight=1)

        self.tabs["Join"].columnconfigure(0, weight=1)
        self.tabs["Join"].columnconfigure(1, weight=1)
        self.tabs["Join"].columnconfigure(2, weight=1)

        joinTabTitle = tk.Label(self.tabs["Join"], text="Join")
        joinTabTitle.grid(row=0, column=0, columnspan=3, sticky='n')

        joinButton = tk.Button(
            self.tabs["Join"], text="Select", command=self.buttonTest)
        joinButton.grid(row=2, column=2, sticky='nsew')

        self.tabs["View"].tkraise()

        # display text
        self.displayTextFigure = tk.Frame(self, bg="white")
        self.displayTextFigure.grid(row=0, column=1, rowspan=2, sticky="nsew")

        testText = "hello\nThisistesttext"

        self.outputText = tk.Text(self.displayTextFigure)
        self.outputText.insert('1.0', testText)
        self.outputText.pack()

    def changeDatabase(self, event):
        self.currentDBSelection = event.widget.get()
        print(self.currentDBSelection)

    def changeManipulationOption(self, event):
        self.currentMSelection = event.widget.get()
        self.tabs[self.currentMSelection].tkraise()

    def changeCheckBoxes(DBE, MS):
        print(DBE, MS)

    def buttonTest(self):
        print("click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
