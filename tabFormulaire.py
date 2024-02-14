import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from FormulationProbleme import FormulationProbleme

class TabFormulaire(ttk.Frame):

    @staticmethod
    def is_decimal(text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def __init__(self, master=None):
        super().__init__(master)
        
        self.labelNombreClients = tk.Label(self, text="Nombre de clients :")
        self.labelNombreClients.grid(row=0, column=0, padx=5, pady=5)
        self.entryNombreClients = tk.Entry(self)
        self.entryNombreClients.grid(row=0, column=1, padx=5, pady=5)

        self.labelNombreVehicules = tk.Label(self, text="Nombre de véhicules :")
        self.labelNombreVehicules.grid(row=0, column=2, padx=5, pady=5)
        self.entryNombreVehicules = tk.Entry(self)
        self.entryNombreVehicules.grid(row=0, column=3, padx=5, pady=5)

        self.labelNombreDepots = tk.Label(self, text="Nombre de dépôts :")
        self.labelNombreDepots.grid(row=0, column=4, padx=5, pady=5)
        self.entryNombreDepots = tk.Entry(self)
        self.entryNombreDepots.grid(row=0, column=5, padx=5, pady=5)

        self.labelCapaciteMaxVehicule = tk.Label(self, text="Capacité max véhicule :")
        self.labelCapaciteMaxVehicule.grid(row=1, column=2, padx=5, pady=5)
        self.entryCapaciteMaxVehicule = tk.Entry(self)
        self.entryCapaciteMaxVehicule.grid(row=1, column=3, padx=5, pady=5)

        self.labelDemandeClients = tk.Label(self, text="Demande des clients :")
        self.labelDemandeClients.grid(row=2, column=0, padx=1, pady=1)
        self.entryDemandeClients = tk.Entry(self)
        self.entryDemandeClients.grid(row=2, column=1, columnspan=5, sticky="ew", padx=1, pady=1)

        self.labelMatriceDistances = tk.Label(self, text="Matrice des distances :")
        self.labelMatriceDistances.grid(row=4, column=2, sticky='ew', columnspan=2, padx=1, pady=1)
        self.entryMatriceDistances = tk.Text(self)
        self.entryMatriceDistances.grid(row=5, column=0, columnspan=6, sticky="ew", padx=1, pady=1)

        self.entryValidation = tk.Button(self, text="Valider formulaire", command=self.generer_fichier_texte)
        self.entryValidation.grid(row=6, column=0, columnspan=6, sticky="ew", padx=1, pady=1)

    def generer_fichier_texte(self):
        nombre_clients = self.entryNombreClients.get()
        nombre_vehicules = self.entryNombreVehicules.get()
        nombre_depots = self.entryNombreDepots.get()
        capacite_max_vehicule = self.entryCapaciteMaxVehicule.get()
        demande_clients = self.entryDemandeClients.get()
        matrice_distances = self.entryMatriceDistances.get("1.0", tk.END)

        # Validation des entrées numériques
        if not (self.is_decimal(nombre_clients) and
                self.is_decimal(nombre_vehicules) and
                self.is_decimal(nombre_depots) and
                self.is_decimal(capacite_max_vehicule)):
            messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques.")
            return
        
        # Instanciation de l'objet FormulationProbleme
        formulation_probleme = FormulationProbleme()
        if not (formulation_probleme.calcul(nombre_depots,nombre_clients,nombre_vehicules,capacite_max_vehicule,demande_clients,matrice_distances)) :
            messagebox.showerror("Erreur", "Résolution impossible !")


      
