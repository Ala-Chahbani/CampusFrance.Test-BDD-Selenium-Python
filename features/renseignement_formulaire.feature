Feature: Renseignement du formulaire de création de compte
ETQ utilisateur
Je veux renseigner le formulaire de création de compte
Afin de créer un compte Campus France

Critères d'acceptance:
- Le formulaire de création de compte contient un bouton "Créer un compte"
- L'utilisateur peut cocher la profession "étudiant", "chercheur" ou "institutionnel" dans le formulaire
- L'utilisateur peut renseigner son domaine d'étude et son niveau d'étude s'il a choisi la profession "étudiant" ou "chercheur"
- L'utilisateur peut renseigner sa fonction, le type de l'organisme et le nom de l'organisme s'il a choisi la profession "institutionnel"

Scenario Outline: Renseignement d'un formulaire étudiant
    Given l'utilisateur est sur la page de création de compte
    When l'utilisateur renseigne les champs "<email>" "<mdp>" "<confirmation_mdp>" "<civilite>" "<nom>" "<prenom>" "<pays_residence>" "<pays_nationalite>" "<code_postal>" "<ville>" "<tel>" "<profession>" "<domaine_etude>" "<niveau_etude>" "<consentement>" 
    Then le formulaire contient un bouton "Créer un compte"
    And le champ "<profession>" est sélectionné
    And le formulaire contient "<domaine_etude>" et "<niveau_etude>" dans leurs champs appropriés
    Examples:
    | email | mdp | confirmation_mdp | civilite | nom | prenom | pays_residence | pays_nationalite | code_postal | ville | tel | profession | domaine_etude | niveau_etude | consentement |
    |salah.ouartani@gmail.com|Ouartani--18|Ouartani--18|Mr|Ouartani|Salah|-France|Tunisie,France,Algérie|75005|Paris|0033612345678|etudiant|Mathématiques|Licence 3|true|
    |manel.sakli@gmail.com|Sakli-Manel1|Sakli-Manel1|Mme|Sakli|Manel|-France|Maroc|38000|Grenoble|0033687654321|etudiant|Sciences économiques et politiques|Master 2|false|
 
