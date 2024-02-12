import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class TabFichier(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Ajuster la colonne pour centrer le bouton

        self.selected_file = None

        def select_file():
            filetypes = (('Text files', '*.txt'), ('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
            if filename:
                print(filename)
                self.selected_file = filename
        
        def validate_file():
            if self.selected_file:
                showinfo("Validation", f"Le fichier sélectionné est : {self.selected_file}")
            else:
                showinfo("Validation", "Aucun fichier sélectionné")

        # open button
        open_button = ttk.Button(self, text='Open a File', command=select_file)
        open_button.grid(row=2, column=0, columnspan=3, sticky="ew", padx=1, pady=1)  # Utiliser columnspan pour étendre sur 3 colonnes

        # validate button
        validate_button = ttk.Button(self, text='Validate', command=validate_file)
        validate_button.grid(row=3, column=0, columnspan=3, sticky="ew", padx=1, pady=1)  # Utiliser columnspan pour étendre sur 3 colonnes

        # placer le bouton en bas de la frame
        self.grid_rowconfigure(4, weight=1)
        validate_button.grid(row=6, column=0, columnspan=3, sticky="ew", padx=1, pady=10)

