from flask import Flask
from flask import request
import sys
import csv

#Création de notre application flask
app = Flask(__nom__)


#classe Personne qui prend en compte deux attributs nom et balance. 2 methodes sont mises en place
#debit et credit
class Personne:
    def __init__(self, nom, balance):
        self.nom = nom
        self.balance = balance
        
    def __str__(self):
        return f"Personne({self.nom}, {self.balance})"
    
    def debit(self, montant):
        self.balance -= montant
  
        
    def credit(self, montant):
        self.balance += montant
  

#classe transaction qui a 3 attributs expediteur, recipent et monta 
class Transaction:
    def __init__(self, expediteur, beneficaire, montant):
        self.expediteur = expediteur
        self.beneficaire = beneficaire
        self.montant = montant
  
    
    def __str__(self):
        return f"Transaction({self.expediteur}, {self.beneficaire}, {self.montant})"
    
#Création des comptes
p1=Personne("Mouad",2000)
p2=Personne("Mohammed",6000)
p3=Personne("Sami",2500)
p4=Personne("Nicolas",3500)


#création des transactions
t1=Transaction(p1,p2,100)
t2=Transaction(p2,p3,200)
t3=Transaction(p4,p3,200)

   
#creation des deux tables Personnes et transactions qui seront remplies des infos recupérées du fichier csv fourni
Personnes=[p1,p2,p3,p4,p5,p6]
transactions = []

#recupérer les infos du fichiers csv
def load_data_from_csv(file_path):
    #ouvrir le fichier en mode lecture
    with open(file_path, "r") as f:
        #creation d'un objet csv pour lire le fichier
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            # Déballer les valeurs de chaque ligne dans des variables 
            expediteur, beneficaire, montant= row
            # Vérifier si un objet Personne avec le nom de l'expéditeur existe dans la liste Personnes
            expediteur_Personne = next((p for p in personnes if p.nom == expediteur), None)
            # Si non, créer un nouvel objet Personne et l'ajouter à la liste Personnes
            if not expediteur_personne:
                expediteur_personne = Personne(expediteur, 0)
                personnes.append(expediteur_personne)
            # Vérifier si un objet Personne avec le nom du destinataire existe dans la liste Personnes
            beneficaire_personne = next((p for p in personnes if p.nom == beneficaire), None)
            # Si non, créer un nouvel objet Personne et l'ajouter à la liste Personnes
            if not beneficaire_personne:
                beneficaire_Personne = Personne(beneficaire, 0)
                personnes.append(beneficaire_personne)
            # Créer un nouvel objet Transaction avec les informations d'expéditeur, de destinataire et de montant   
            transaction = Transaction(expediteur, beneficaire, int(montant))
            transactions.append(transaction)
            expediteur_personne.debit(int(montant))
            beneficaire_personne.credit(int(montant))
            
            


#Création des listes : "Personnene" contenant des objets de type "Personnene" et "transaction" contenant des objets de type "Transaction" 
_transactions=[t1,t2,t3]

#Définition de la route principale de l'application, uniquement accessible via une requête HTTP GET pour récupérer des données.
@app.route("/", methods=['GET'])
def printAll():
    if request.method == 'GET':
        res = "<h1>Liste des Personnenes :</h1><ul>"
        for personne in personnes:
            res += "<li>NOM : " + personne.nom  + " / SOLDE COMPTE : " + '%.2f' % personne.balance + "€</li>"
        res += "</ul><h1>Liste des transactions :</h1><ul>"
        #for transaction in _transactions:
        res += "<li>P1 : " + p1.nom +  " / P2 : " + p2.nom+  ":   Montant de la transaction : 100€  : " 
        res += "<li>P1 : " + p2.nom +  " / P2 : " + p5.nom+  ":   Montant de la transaction : 200€  : " 
        res += "<li>P1 : " + p4.nom +  " / P2 : " + p3.nom+  ":   Montant de la transaction : 200€  : " 

        return res+"</ul>"
    else:
        return "methode invalide"
    
    
 #endpoint transactions qui affiche les transactions entre 2 Personnenes depuis le fichier csv.
@app.route("/transactions", methods=["GET"]) 
def get_transactions():
    load_data_from_csv('transactions.csv')
    return "\n".join(str(t) for t in transactions)

#endpoint Personnes qui affiche les Personnenes ayant deja effectué une transaction depuis le fichier csv.
@app.route("/personnes", methods=["GET"]) 
def get_Personnes():
    load_data_from_csv('transactions.csv')
    #print(Personnes)
    return "\n".join(str(p) for p in personnes)



#endpoint Personne qui permet d'ajouter une Personnene de type Personne ayant nom et balance.
@app.route("/personne", methods=["POST"])
def add_Personne():
    nom = request.form.get("nom")
    balance = request.form.get("balance")
    personne = Personne(nom, balance)
    personnes.append(personne)
    return "Personne ajoutée."

#endpoint Personne/id qui permet de supprimer une Personnene de la liste Personnes
@app.route('/personne/<int:Personne_id>', methods=['DELETE'])
def delete_Personne(Personne_id):
    personne = next((personne for Personne in Personnes if personne['id'] == personne_id), None)
    if Personne:
        personnes.remove(personne)
        return {"message": "Personne supprimée"}, 200
    else:
        return {"erreur": "Personne introuvable"}, 404
 
#endpoint /transaction qui sert a ajouter une transaction en prenant en argument l'emetteur, le recepteur et la somme de l'envoi
@app.route('/transaction', methods=['POST'])
def add_transaction():
    expediteur_nom = request.form['expediteur']
    recepteur_nom = request.form['recepteur']
    montant = int(request.form['montant'])
    
    expediteur = next((personne for personne in personnes if personne.nom == expediteur_nom), None)
    recepteur = next((personne for personne in personnes if personne.nom == recepteur_nom), None)
    
    if expediteur is None or recepteur is None:
        return {"erreur": "expediteur ou recepteur introuvable"}, 400
    
    expediteur.balance -= montant
    recepteur.balance += montant
    
    transactions.append(Transaction(expediteur_nom, recepteur_nom, montant))
    
    return {"message": "Transaction ajouté"}, 200

#donner le solde de la Personnene prise en compte
@app.route('/balance/<nom>', methods=['GET'])
def get_balance(nom):
    personne = next((p for p in personnes if p.nom == nom), None)
    if Personne:
        balance = personne.balance
        return jsonify({"nom": personne.nom, "balance": balance})
    return jsonify({"erreur": "Personne introuvable"}), 404


#lister l'ensemble des transactions par Personnene 
@app.route('/transactions/<personne>', methods=['GET'])
def getTransactions(personne):
    personne_transactions = [t for t in _transactions if t.expediteur == personne or t.beneficaire == personne]
    return jsonify([{'expediteur': t.expediteur, 'recepteur': t.beneficaire, 'montant': t.montant} for t in personne_transactions])
    
    
if __nom__ == "__main__":
    print(transactions)
    if len(sys.argv) > 1 :
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
