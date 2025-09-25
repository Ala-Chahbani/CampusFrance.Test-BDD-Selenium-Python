from behave import given, when, then
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

@given(u'l\'utilisateur est sur la page de création de compte')
def step_impl(context):
    context.driver.get("https://www.campusfrance.org/fr/user/register")

def renseignement_formulaire(context, utilisateur):
    # attendre la disparition des cookies
    def cookies_disparus(_):
        try:
            bouton_refus_cookies = context.driver.find_element(By.ID, "tarteaucitronAllDenied2")
            bouton_refus_cookies.click()
            return not bouton_refus_cookies.is_displayed()
        except:
            return False

    wait = WebDriverWait(context.driver, 5)
    wait.until(cookies_disparus)

    context.driver.find_element(By.CSS_SELECTOR, ".username").send_keys(utilisateur["email"])
    context.driver.find_element(By.ID, "edit-pass-pass1").send_keys(utilisateur["mdp"])
    context.driver.find_element(By.ID, "edit-pass-pass2").send_keys(utilisateur["confirmation_mdp"])

    if utilisateur["civilite"] == "Mr":
        context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-civilite\"]/div[2]/label").click()
    elif utilisateur["civilite"] == "Mme":
        context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-civilite\"]/div[1]/label").click()

    context.driver.find_element(By.ID, "edit-field-nom-0-value").send_keys(utilisateur["nom"])
    context.driver.find_element(By.ID,"edit-field-prenom-0-value").send_keys(utilisateur["prenom"])

    champ_pays_residence = context.driver.find_element(By.ID, "edit-field-pays-concernes-selectized")
    champ_pays_residence.click()
    champ_pays_residence.send_keys(Keys.BACKSPACE)
    champ_pays_residence.send_keys(utilisateur["pays_residence"])
    champ_pays_residence.send_keys(Keys.ENTER)

    # ajout de champs pays de nationalité si nécessaire
    for i in range(1, len(utilisateur["pays_nationalite"])):
        bouton_ajout_nationalite = context.driver.find_element(By.CSS_SELECTOR, ".field-add-more-submit")
        bouton_ajout_nationalite.click()
        # attendre l'apparition du nouveau champ pays de nationalité créé
        def apparition_champ_pays_nationalite(_):
            try:
                context.driver.find_element(By.NAME, "field_nationalite[" + str(i) + "][target_id]")
                return True
            except:
                return False
        wait.until(apparition_champ_pays_nationalite)

    for i in range(len(utilisateur["pays_nationalite"])):
        champ_pays_nationalite = context.driver.find_element(By.NAME, "field_nationalite[" + str(i) + "][target_id]")
        champ_pays_nationalite.click()
        champ_pays_nationalite.send_keys(utilisateur["pays_nationalite"][i])
        # attendre l'apparition de la liste des options
        def apparition_liste_options(_):
            try:
                context.driver.find_element(By.XPATH, "/html/body/ul[" + str(i + 1) + "]/li[1]/a")
                return True
            except:
                return False
        wait.until(apparition_liste_options)
        # clic sur la première option proposée
        context.driver.find_element(By.XPATH, "/html/body/ul[" + str(i + 1) + "]/li[1]/a").click()
    
    context.driver.find_element(By.ID, "edit-field-code-postal-0-value").send_keys(utilisateur["code_postal"])
    context.driver.find_element(By.ID, "edit-field-ville-0-value").send_keys(utilisateur["ville"])
    context.driver.find_element(By.ID, "edit-field-telephone-0-value").send_keys(utilisateur["tel"])

    if utilisateur["profession"] == "etudiant":
        context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-publics-cibles\"]/div[1]/label").click()

        # attendre l'apparition du champ de domaine d'études
        def apparition_domaine_etude(_):
            try:
                context.driver.find_element(By.ID, "edit-field-domaine-etudes-selectized")
                return True
            except:
                return False
        wait.until(apparition_domaine_etude)

        domaine_etude = context.driver.find_element(By.ID, "edit-field-domaine-etudes-selectized")
        domaine_etude.click()
        domaine_etude.send_keys(Keys.BACKSPACE)
        domaine_etude.send_keys(utilisateur["domaine_etude"])
        domaine_etude.send_keys(Keys.ENTER)

        niveau_etude = context.driver.find_element(By.ID, "edit-field-niveaux-etude-selectized")
        niveau_etude.click()
        niveau_etude.send_keys(Keys.BACKSPACE)
        niveau_etude.send_keys(utilisateur["niveau_etude"])
        niveau_etude.send_keys(Keys.ENTER)

    if utilisateur["consentement"]:
        context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-accepte-communications-wrapper\"]/div/label").click()

@when(u'l\'utilisateur renseigne les champs "{email}" "{mdp}" "{confirmation_mdp}" "{civilite}" "{nom}" "{prenom}" "{pays_residence}" "{pays_nationalite}" "{code_postal}" "{ville}" "{tel}" "{profession}" "{domaine_etude}" "{niveau_etude}" "{consentement}"')
def step_impl(context, email, mdp, confirmation_mdp, civilite, nom, prenom, pays_residence, pays_nationalite, code_postal, ville, tel, profession, domaine_etude, niveau_etude, consentement):
    utilisateur = {
        'email':  email,
        'mdp' : mdp,
        'confirmation_mdp': confirmation_mdp,
        'civilite': civilite,
        'nom': nom, 
        'prenom': prenom, 
        'pays_residence': pays_residence,
        'pays_nationalite': pays_nationalite.split(sep = ','),
        'code_postal': code_postal,
        'ville': ville,
        'tel': tel,
        'profession': profession,
        'domaine_etude': domaine_etude,
        'niveau_etude': niveau_etude,
        'consentement': consentement.lower() == "true"
    }
    renseignement_formulaire(context, utilisateur)

@then(u'le formulaire contient un bouton "Créer un compte"')
def step_impl(context):
    assert context.driver.find_element(By.ID, "edit-submit").get_attribute("value") == "Créer un compte"

@then(u'le champ "{profession}" est sélectionné')
def step_impl(context, profession):
    if profession == "etudiant":
        assert context.driver.find_element(By.ID, "edit-field-publics-cibles-2").is_selected()
    else:
        assert False, "Mauvais jeu de données"

@then(u'le formulaire contient "{domaine_etude}" et "{niveau_etude}" dans leurs champs appropriés')
def step_impl(context, domaine_etude, niveau_etude):
    assert context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-domaine-etudes-wrapper\"]/div/div/div[1]/div").text == domaine_etude
    assert context.driver.find_element(By.XPATH, "//*[@id=\"edit-field-niveaux-etude-wrapper\"]/div/div/div[1]/div").text == niveau_etude
