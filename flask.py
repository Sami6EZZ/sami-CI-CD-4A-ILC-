from flask import Flask
from flask import request
import sys
import csv

#Création de notre application flask
app = Flask(__name__)


#classe Person qui prend en compte deux attributs name et balance. 2 methodes sont mises en place
#debit et credit
class Person:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        
    def __str__(self):
        return f"Person({self.name}, {self.balance})"
    
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
p1=Person("Mouad",2000)
p2=Person("Mohammed",6000)
p3=Person("Sami",2500)
p4=Person("Nicolas",3500)


#création des transactions
t1=Transaction(p1,p2,100)
t2=Transaction(p2,p3,200)
t3=Transaction(p4,p3,200)

   
#creation des deux tables persons et transactions qui seront remplies des infos recupérées du fichier csv fourni
persons=[p1,p2,p3,p4,p5,p6]
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
            # Vérifier si un objet Person avec le nom de l'expéditeur existe dans la liste persons
            sender_person = next((p for p in persons if p.name == sender), None)
            # Si non, créer un nouvel objet Person et l'ajouter à la liste persons
            if not sender_person:
                sender_person = Person(sender, 0)
                persons.append(sender_person)
            # Vérifier si un objet Person avec le nom du destinataire existe dans la liste persons
            recipient_person = next((p for p in persons if p.name == recipient), None)
            # Si non, créer un nouvel objet Person et l'ajouter à la liste persons
            if not recipient_person:
                recipient_person = Person(recipient, 0)
                persons.append(recipient_person)
            # Créer un nouvel objet Transaction avec les informations d'expéditeur, de destinataire et de montant   
            transaction = Transaction(sender, recipient, int(amount))
            transactions.append(transaction)
            sender_person.debit(int(amount))
            recipient_person.credit(int(amount))
            
            


#Création des listes : "personne" contenant des objets de type "Personne" et "transaction" contenant des objets de type "Transaction" 
_transactions=[t1,t2,t3]

#Définition de la route principale de l'application, uniquement accessible via une requête HTTP GET pour récupérer des données.
@app.route("/", methods=['GET'])
def printAll():
    if request.method == 'GET':
        res = "<h1>Liste des personnes :</h1><ul>"
        for person in personnes:
            res += "<li>NOM : " + person.name  + " / SOLDE COMPTE : " + '%.2f' % person.balance + "€</li>"
        res += "</ul><h1>Liste des transactions :</h1><ul>"
        #for transaction in _transactions:
        res += "<li>P1 : " + p1.name +  " / P2 : " + p2.name+  ":   Montant de la transaction : 100€  : " 
        res += "<li>P1 : " + p2.name +  " / P2 : " + p5.name+  ":   Montant de la transaction : 200€  : " 
        res += "<li>P1 : " + p4.name +  " / P2 : " + p3.name+  ":   Montant de la transaction : 200€  : " 

        return res+"</ul>"
    else:
        return "Invalid request method"
    
    
 #endpoint transactions qui affiche les transactions entre 2 personnes depuis le fichier csv.
@app.route("/transactions", methods=["GET"]) 
def get_transactions():
    load_data_from_csv('transactions.csv')
    return "\n".join(str(t) for t in transactions)

#endpoint persons qui affiche les personnes ayant deja effectué une transaction depuis le fichier csv.
@app.route("/persons", methods=["GET"]) 
def get_persons():
    load_data_from_csv('transactions.csv')
    #print(persons)
    return "\n".join(str(p) for p in persons)



#endpoint person qui permet d'ajouter une personne de type Person ayant name et balance.
@app.route("/person", methods=["POST"])
def add_person():
    name = request.form.get("name")
    balance = request.form.get("balance")
    person = Person(name, balance)
    persons.append(person)
    return "Person added."

#endpoint person/id qui permet de supprimer une personne de la liste persons
@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = next((person for person in persons if person['id'] == person_id), None)
    if person:
        persons.remove(person)
        return {"message": "Person deleted successfully"}, 200
    else:
        return {"error": "Person not found"}, 404
 
#endpoint /transaction qui sert a ajouter une transaction en prenant en argument l'emetteur, le recepteur et la somme de l'envoi
@app.route('/transaction', methods=['POST'])
def add_transaction():
    sender_name = request.form['sender']
    receiver_name = request.form['receiver']
    amount = int(request.form['amount'])
    
    sender = next((person for person in persons if person.name == sender_name), None)
    receiver = next((person for person in persons if person.name == receiver_name), None)
    
    if sender is None or receiver is None:
        return {"error": "Sender or receiver not found"}, 400
    
    sender.balance -= amount
    receiver.balance += amount
    
    transactions.append(Transaction(sender_name, receiver_name, amount))
    
    return {"message": "Transaction added successfully"}, 200

#donner le solde de la personne prise en compte
@app.route('/balance/<name>', methods=['GET'])
def get_balance(name):
    person = next((p for p in persons if p.name == name), None)
    if person:
        balance = person.balance
        return jsonify({"name": person.name, "balance": balance})
    return jsonify({"error": "Person not found"}), 404


#lister l'ensemble des transactions par personne 
@app.route('/transactions/<person>', methods=['GET'])
def getTransactions(person):
    person_transactions = [t for t in _transactions if t.sender == person or t.recipient == person]
    return jsonify([{'sender': t.sender, 'receiver': t.recipient, 'amount': t.amount} for t in person_transactions])
    
    
if __name__ == "__main__":
    print(transactions)
    if len(sys.argv) > 1 :
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)
