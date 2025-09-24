from selenium.webdriver import Chrome 

class TestCreationEtudiant:
    url = "https://www.campusfrance.org/fr/user/register"

    def setup_method(self):
        self.driver = Chrome()
        self.driver.maximize_window()

    def test_renseignement_etudiant_mathemathiques_licence_3(self):
        self.driver.get(self.url)
        assert True

    def teardown_method(self):
        self.driver.delete_all_cookies()
        self.driver.quit()