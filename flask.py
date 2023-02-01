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
    
    def debit(self, amount):
        self.balance -= amount
        
    def credit(self, amount):
        self.balance += amount

#classe transaction qui a 3 attributs sender, recipent et amount 
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
    
    def __str__(self):
        return f"Transaction({self.sender}, {self.recipient}, {self.amount})"
    
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
            sender, recipient, amount = row
            # Vérifier si un objet Personne avec le nom de l'expéditeur existe dans la liste Personnes
            sender_Personne = next((p for p in Personnes if p.nom == sender), None)
            # Si non, créer un nouvel objet Personne et l'ajouter à la liste Personnes
            if not sender_Personne:
                sender_Personne = Personne(sender, 0)
                Personnes.append(sender_Personne)
            # Vérifier si un objet Personne avec le nom du destinataire existe dans la liste Personnes
            recipient_Personne = next((p for p in Personnes if p.nom == recipient), None)
            # Si non, créer un nouvel objet Personne et l'ajouter à la liste Personnes
            if not recipient_Personne:
                recipient_Personne = Personne(recipient, 0)
                Personnes.append(recipient_Personne)
            # Créer un nouvel objet Transaction avec les informations d'expéditeur, de destinataire et de montant   
            transaction = Transaction(sender, recipient, int(amount))
            transactions.append(transaction)
            sender_Personne.debit(int(amount))
            recipient_Personne.credit(int(amount))
            
            


#Création des listes : "Personnene" contenant des objets de type "Personnene" et "transaction" contenant des objets de type "Transaction" 
_transactions=[t1,t2,t3]

#Définition de la route principale de l'application, uniquement accessible via une requête HTTP GET pour récupérer des données.
@app.route("/", methods=['GET'])
def printAll():
    if request.method == 'GET':
        res = "<h1>Liste des Personnenes :</h1><ul>"
        for Personne in Personnenes:
            res += "<li>NOM : " + Personne.nom  + " / SOLDE COMPTE : " + '%.2f' % Personne.balance + "€</li>"
        res += "</ul><h1>Liste des transactions :</h1><ul>"
        #for transaction in _transactions:
        res += "<li>P1 : " + p1.nom +  " / P2 : " + p2.nom+  ":   Montant de la transaction : 100€  : " 
        res += "<li>P1 : " + p2.nom +  " / P2 : " + p5.nom+  ":   Montant de la transaction : 200€  : " 
        res += "<li>P1 : " + p4.nom +  " / P2 : " + p3.nom+  ":   Montant de la transaction : 200€  : " 

        return res+"</ul>"
    else:
        return "Invalid request method"
    
    
 #endpoint transactions qui affiche les transactions entre 2 Personnenes depuis le fichier csv.
@app.route("/transactions", methods=["GET"]) 
def get_transactions():
    load_data_from_csv('transactions.csv')
    return "\n".join(str(t) for t in transactions)

#endpoint Personnes qui affiche les Personnenes ayant deja effectué une transaction depuis le fichier csv.
@app.route("/Personnes", methods=["GET"]) 
def get_Personnes():
    load_data_from_csv('transactions.csv')
    #print(Personnes)
    return "\n".join(str(p) for p in Personnes)



#endpoint Personne qui permet d'ajouter une Personnene de type Personne ayant nom et balance.
@app.route("/Personne", methods=["POST"])
def add_Personne():
    nom = request.form.get("nom")
    balance = request.form.get("balance")
    Personne = Personne(nom, balance)
    Personnes.append(Personne)
    return "Personne added."

#endpoint Personne/id qui permet de supprimer une Personnene de la liste Personnes
@app.route('/Personne/<int:Personne_id>', methods=['DELETE'])
def delete_Personne(Personne_id):
    Personne = next((Personne for Personne in Personnes if Personne['id'] == Personne_id), None)
    if Personne:
        Personnes.remove(Personne)
        return {"message": "Personne deleted successfully"}, 200
    else:
        return {"error": "Personne not found"}, 404
 
#endpoint /transaction qui sert a ajouter une transaction en prenant en argument l'emetteur, le recepteur et la somme de l'envoi
@app.route('/transaction', methods=['POST'])
def add_transaction():
    sender_nom = request.form['sender']
    receiver_nom = request.form['receiver']
    amount = int(request.form['amount'])
    
    sender = next((Personne for Personne in Personnes if Personne.nom == sender_nom), None)
    receiver = next((Personne for Personne in Personnes if Personne.nom == receiver_nom), None)
    
    if sender is None or receiver is None:
        return {"error": "Sender or receiver not found"}, 400
    
    sender.balance -= amount
    receiver.balance += amount
    
    transactions.append(Transaction(sender_nom, receiver_nom, amount))
    
    return {"message": "Transaction added successfully"}, 200

#donner le solde de la Personnene prise en compte
@app.route('/balance/<nom>', methods=['GET'])
def get_balance(nom):
    Personne = next((p for p in Personnes if p.nom == nom), None)
    if Personne:
        balance = Personne.balance
        return jsonify({"nom": Personne.nom, "balance": balance})
    return jsonify({"error": "Personne not found"}), 404


#lister l'ensemble des transactions par Personnene 
@app.route('/transactions/<Personne>', methods=['GET'])
def getTransactions(Personne):
    Personne_transactions = [t for t in _transactions if t.sender == Personne or t.recipient == Personne]
    return jsonify([{'sender': t.sender, 'receiver': t.recipient, 'amount': t.amount} for t in Personne_transactions])
    
    
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
