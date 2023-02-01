# sami-CI-CD-4A-ILC-
 
  <h1 align="center">PROJET API CI/CD  ESIREM 2023</h1>
  
  
Le projet consiste à contrôler la gestion CRUD d'un système de transaction.

   ![Badge1](https://i0.wp.com/datascientest.com/wp-content/uploads/2021/03/illu_devops_blog-119.png?resize=1024%2C562&ssl=1.png)



## Réalisé par : 
  Sami EZZAHID


## Langage utilisé :
  Python 
  
![Badge1](https://dz2cdn1.dzone.com/storage/temp/12886720-why-devops-and-python.png)

## Fonctionnalités :

-Initialisation de l'application Flask

-Création d'une classe Personne qui permet de créer des objets Personne avec un nom et un solde. Les objets Personne peuvent être converties en objets JSON, avoir des méthodes pour débiter ou créditer un compte, effectuer une transaction entre deux personnes.

-Méthode pour importer un fichier CSV de personnes

-Route pour afficher toutes les personnes et les transactions

-Route pour affichier les transactions sauvegargdées dans un fichier csv entre 2 personnes.

## Utilisation :

-Installation de flask avec :
    pip install flask
   
-Utilisez la route '/' pour afficher toutes les personnes et les transactions. 
    Dans un navigateur web : http://localhost:5000/ 
    Dans une commande CURL : ``curl -X GET "http://localhost:5000/"``
    
-Utilisez la route'/transactions' qui affiche la liste des transactions effectuées qui sont été lises du fichier transactions.csv.
    Dans un navigateur web : http://localhost:5000/transactions
    Dans une commande CURL : ``curl -X GET "http://localhost:5000/transactions"``
    
-Utilisez la route'/persons' qui affiche la liste des personnes crées et leurs soldes apres avoir chargé les transactions du fichier csv.
    Dans un navigateur web : http://localhost:5000/persons
    Dans une commande CURL : ``curl -X GET "http://localhost:5000/persons"``
    
     
-Utlisiez la route '/person' qui permet d'ajouter une personne de type Person ayant un nom: name et un solde: balance.
     Executez cette fonction avec la commande CURL suivante :
              ``curl -X POST -d "name=Jerome&balance=5" http://localhost:5000/person``
              
-Utilisez la route 'person/id' qui permet de supprimer une personne en donnant son id
     Executez cette fonction avec la commande CURL suivante :
          ``curl -X DELETE http://localhost:5000/person/1``

-Utlisiez la route '/transaction' qui permet de créer une nouvelle transaction en leur donnant un émetteur, un recepteur et le montant de la transaction.
    Executez cette fonction avec la commande CURL suivante :
                ``curl -X POST -d "sender=Simo&receiver=Mouad&amount=100" http://localhost:5000/transaction``
                !! attention, il faudra bien que le nom du sender our receiver soit dans la liste persons.

 -Utlisize la route '/balance/name' qui peremt d'afficher le solde de la personne donnée dans le parametre name.
    Executer cette fonction avec :
        Navigateur web : ``http://localhost:5000/balance/Mouad ``
        Commande CURL :  ``curl -X GET "http://localhost:5000/balance/Mouad"``
        !!Attention il faudra bien que le nom donné soit dans la liste persons.

## Vous trouverez ci-dessus les différentes actions utilisées dans ce projet : 

App build :
![Generic badge](https://github.com/mouadw/4A_ILC_CRUD_API_CI_CD/actions/workflows/appBuild.yml/badge.svg)

Build docker image :
![Generic badge](https://github.com/mouadw/4A_ILC_CRUD_API_CI_CD/actions/workflows/buildDockerImage.yml/badge.svg)

Build and push tag :
![Generic badge](https://github.com/mouadw/4A_ILC_CRUD_API_CI_CD/actions/workflows/build_push.yml/badge.svg)

