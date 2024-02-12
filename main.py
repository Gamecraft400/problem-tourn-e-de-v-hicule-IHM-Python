import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk

from tabFichier import TabFichier
from tabFormulaire import TabFormulaire

def main():
    # Création de la fenêtre principale
    root = ThemedTk(theme='adapta')
    root.title("Interface Graphique")

    # Empêcher le redimensionnement de la fenêtre
    root.resizable(False, False)

    labelTitreApp = tk.Label(root, text="VRI_CPLEX")
    tabControl = ttk.Notebook(root)
    tabFormulaire = TabFormulaire(tabControl)
    tabFichier = TabFichier(tabControl)

    tabControl.add(tabFormulaire, text='Formulaire')
    tabControl.add(tabFichier, text='Fichier')

    labelTitreApp.pack(expand=0)
    tabControl.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
