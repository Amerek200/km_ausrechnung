from main import TourAverage
from tkinter import *
from tkinter import messagebox, filedialog


#TODO: Error handling. (correct .csv, check for viable out_file path, catch keyerror) ?
#TODO: remove ugly delimiter dictonary and use if - elif for space and tab?
#TODO: Output .csv got blank lines in between the data lines?
#QUESTION: Initialdir set correctly? Dont think so
#QUESTION: Best way to check/validate path?


class GUI():
    def __init__(self):
        self.averager = TourAverage()
        self.root = Tk()
        self.in_file = None
        self.out_file = None
        self.min_km = None
        self.max_km = None
        self.km_keyword = None
        self.date_keyword = None
        self.delimiter = None

    def main_window(self):
        #root = Tk()
        self.root.title("Kilometer Auswertung")
        #disable button until all parameters are correct.
        run_btn = Button(self.root, text="Start", command=self.run, width=20, borderwidth=5, pady=5)
        run_btn.grid(row=1, column=0)
        self.param_frame()
        self.root.mainloop()
        pass

    def param_frame(self):
        frame = LabelFrame(self.root, text="placeholder", padx=5, pady=5)
        frame.grid(row=0, column=0, padx=5, pady=5)
        #get input file
        label_in = Label(frame, text="Opheo Datei: (.csv)")
        label_in.grid(row=0, column=0, sticky=W)
        select_btn = Button(frame, text="Durchsuchen", command=self.filemanager)
        select_btn.grid(row=0, column=3, sticky=E)
        self.in_file_display = Entry(frame, width=60, borderwidth=5)
        self.in_file_display.grid(row=1, column=0, columnspan=4)
        #get output file name
        label_out_name = Label(frame, text="Dateiname Ergebnis:")
        label_out_name.grid(row=2, column=0, sticky=W)
        self.out_name_display = Entry(frame, width=25, borderwidth=5)
        self.out_name_display.grid(row=2, column=1, sticky=E, columnspan=2)
        Label(frame, text=".csv").grid(row=2, column=3, sticky=W)
        #get output file path
        label_out = Label(frame, text="Ergebnis speichern unter:")
        label_out.grid(row=3, column=0, sticky=W, columnspan=2)
        out_btn = Button(frame, text="Durchsuchen", command=self.out_dir_manager)
        out_btn.grid(row=3, column=3, sticky=E)
        self.out_file_display = Entry(frame, width=60, borderwidth=5)
        self.out_file_display.grid(row=4, column=0, columnspan=4)
        #get min/max day values to filter.
        filter_frame = LabelFrame(frame, borderwidth=0)
        filter_frame.grid(row=6, column=0, columnspan=4, sticky=W)
        label_km_filter = Label(frame, text="Km / Tag Filter:").grid(row=5, column=0, sticky=W)
        label_min_km = Label(filter_frame, text="Min Km:").grid(row=0, column=0, sticky=E)
        #w = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        #taken from https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget &
        #http://stupidpythonideas.blogspot.com/2013/12/tkinter-validation.html, basically validatecommand gets called
        #with a (tcl function id, argument) tuple. function id is the return value of .register(),
        #argument %P gets replaced/substituted with the (proposed) new Entry value.
        valcmd = frame.register(self.validate_int_entry)
        self.input_min_km = Entry(filter_frame, width=10, borderwidth=5, validate="all", validatecommand=(valcmd, '%P'))
        self.input_min_km.grid(row=0, column=1, sticky=W)
        self.input_min_km.insert(0, 5)
        label_max_km = Label(filter_frame, text="Max Km:").grid(row=0, column=2, sticky=E)
        self.input_max_km = Entry(filter_frame, width=10, borderwidth=5, validate="all", validatecommand=(valcmd, '%P'))
        self.input_max_km.grid(row=0, column=3, sticky=W)
        self.input_max_km.insert(0, 600)
        #get header of the km & date column.
        label_km_name = Label(frame, text="Kopfzeile Km:").grid(row=7, column=0, sticky=W)
        self.km_name = Entry(frame, width=20, borderwidth=5)
        self.km_name.grid(row=7, column=1, sticky=W, columnspan=2)
        self.km_name.insert(0, "Strecke (Plan) [Km]")
        label_date_name = Label(frame, text="Kopfzeile Datum:").grid(row=8, column=0, sticky=W)
        self.date_name = Entry(frame, width=20, borderwidth=5)
        self.date_name.grid(row=8, column=1, sticky=W, columnspan=2)
        self.date_name.insert(0, "Start")
        #get delimiter
        delimiter_label = Label(frame, text="Trennzeichen:").grid(row=9, column=0, sticky=W)
        self.del_selected = StringVar()
        self.del_selected.set(";")
        self.delimiter_options = {",": ",", ";": ";", ":": ":", "Tab": "\\t", "Space": " "}
        del_menu = OptionMenu(frame, self.del_selected, *[k for k in self.delimiter_options])
        del_menu.config(width=5)
        del_menu.grid(row=9, column=1, sticky=W)

    #used to prevent letters etc. in the min/max km Entry fields.
    def validate_int_entry(self, n):
        if str.isdigit(n) or n == "":
            return True
        else:
            return False

    #opens input file dialog, writes path to entry field and creates suggestions for output name/path if not set.
    def filemanager(self):
        self.in_file = filedialog.askopenfilename(title="Fahrzeugdaten auswählen", initialdir="/User/Desktop", filetypes=[(".csv Dateien", "*.csv")])
        self.in_file_display.delete(0, END)
        self.in_file_display.insert(0, self.in_file)
        self.out_suggestions()

    #open output file dialog
    def out_dir_manager(self):
        self.out_dir = filedialog.askdirectory(title="Zielordner auswählen", initialdir="/User/Desktop", mustexist=True)
        self.out_file_display.delete(0, END)
        self.out_file_display.insert(0, self.out_dir)

    #creates and fills output name & path Entry fields with suggestions taken from input file.
    def out_suggestions(self):
        #rsplit starts right, returns maxsplit +1 items
        path_splitted = self.in_file.rsplit("/", 1)
        if self.out_name_display.get() == "":
            suggestion = path_splitted[1].rsplit(".", 1)
            suggestion = suggestion[0] + "_kmSchnitt"
            self.out_name_display.insert(0, suggestion)
        if self.out_file_display.get() == "":
            self.out_file_display.insert(0, path_splitted[0])

    #sets values and checks if all fields are filled out.
    def set_values(self):
        self.in_file = self.in_file_display.get()
        out_path = self.out_file_display.get()
        out_name = self.out_name_display.get()
        self.out_file = out_path + "/" + out_name + ".csv"
        self.km_keyword = self.km_name.get()
        self.date_keyword = self.date_name.get()
        self.min_km = int(self.input_min_km.get())
        self.max_km = int(self.input_max_km.get())
        strs = [self.in_file, out_path, out_name, self.date_keyword, self.km_keyword]
        self.delimiter = self.delimiter_options.get(self.del_selected.get())
        if all(s != "" for s in strs) and (self.min_km < self.max_km):
            return True
        else:
            return False

    #feeds values into & runs the main script, prints out error if keyError or PermissionError arises.
    def run(self):
        if self.set_values():
            E = TourAverage()
            E.min_km = self.min_km
            E.max_km = self.max_km
            E.in_file = self.in_file
            E.out_file = self.out_file
            E.km_keyword = self.km_keyword
            E.date_keyword = self.date_keyword
            E.delimiter = self.delimiter
            e = E.run()
            if e != True:
                messagebox.showwarning("Fehler", f"Fehler bei Auswertung. \n {e}")
            else:
                messagebox.showinfo("", "Datei erfolgreich ausgewertet.")
        else:
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")


if __name__ == "__main__":
    g = GUI()
    g.main_window()
