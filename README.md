# Rendu Vue.js Quiz

## Équipe
- Devers--Doré Lucas
- Kerguen Tony

## Contexte
Nous devons construire une application Vue sur le même modèle pour notre questionnaire. Cette application doit se connecter à notre serveur REST précédemment mis en place. Il doit nous permettre de récupérer, modifier, créer et supprimer des questionnaires ainsi que des questions.

## Lancement et arrêt de l'application
1) Sur Linux  
    Pour lancer le serveur REST  
        ```$ source ./lancementServeur.bash```  
    Pour lancer le client node  
        ```$ source ./lancementClient.bash```  
    Le serveur et le client sont à lancer dans 2 terminaux différents à la racine du rendu.
1) Sur Windows  
    Pour lancer le serveur REST  
        ```$ ./lancementServeur.ps1```  
    Pour lancer le client node  
        ```$ ./lancementClient.ps1```  
    Le serveur et le client sont à lancer dans 2 terminaux différents à la racine du rendu.

Pour revenir à l'état initial, il suffit pour le terminal serveur de faire :  
    ```CTRL+C```  
    ```deactivate ; cd ..```  
Pour revenir à l'état initial, il suffit pour le terminal client de faire :  
    ```CTRL+C```  
    ```O```  
    ```cd ..```  

## Analyse des choix de modélisation
Nous avons choisi de modéliser notre application avec seulement 2 composants, car nos questionnaires ont un accès direct dans leurs attributs à leurs questions. Le composant principal App.vue gère l'affichage de tous les questionnaires. Pour chaque questionnaire, il crée un composant QuestionnaireItem. Et dans ce composant QuestionnaireItem, l'affichage des questions est géré.

Nous ne pouvions pas créer de composants QuestionItem car les questionnaires ont déjà accès à leurs questions. Il aurait fallu modifier complètement l'API REST dès le début.
