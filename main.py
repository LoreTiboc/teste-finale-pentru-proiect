import time  # Import pentru a folosi funcția sleep
import unittest  # Import pentru a utiliza framework-ul de testare unittest

from selenium import webdriver  # Import pentru a utiliza Selenium WebDriver
from selenium.webdriver.common.by import By  # Import pentru a utiliza selectoarele de elemente
from selenium.webdriver.support import expected_conditions as EC  #Import pentru a aștepta condiții specifice în Selenium
from selenium.webdriver.support.wait import WebDriverWait  # Import pentru a aștepta elemente în Selenium


class Test(unittest.TestCase):
    """Clasă pentru definirea testelor."""

    driver = None
    LOGIN_LINK = "https://the-internet.herokuapp.com/login"
    BUTTON_LOGIN = (By.CLASS_NAME, "fa-sign-in")
    MESSAGE_SUCCESS = (By.CLASS_NAME, "alert-success")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SECURE_AREA = (By.XPATH, "//div[@class='flash success']")

    def setUp(self):
        """Metodă de inițializare pentru a deschide browser-ul și a accesa pagina de login."""
        self.driver = webdriver.Chrome()
        self.driver.get(self.LOGIN_LINK)
        self.driver.maximize_window()
        time.sleep(1)

    def tearDown(self):
        """Metodă pentru a închide browser-ul după fiecare test."""
        self.driver.quit()

    if __name__ == "__main__":
        unittest.main()
    # Test 1

    def test_url(self):
        """Verifică dacă URL-ul curent este cel așteptat."""
        actual_url = self.driver.current_url
        self.assertEqual(self.LOGIN_LINK, actual_url, "Unexpected URL")

    # Test 2

    def test_title(self):
        """Verifică dacă titlul paginii este cel așteptat."""
        expected_title = "The Internet"
        actual_title = self.driver.title
        self.assertEqual(expected_title, actual_title, "Unexpected title")

    # Test 3

    def test_h2_text(self):
        """Verifică dacă textul de tip h2 de pe pagină este cel așteptat."""
        text_h2 = self.driver.find_element(By.XPATH, "//h2").text
        expected_text = "Login Page"
        self.assertEqual(expected_text, text_h2, "Textul h2 este incorrect")

    # Test 4

    def test_buton_login_display(self):
        """Verifică dacă butonul de login este afișat pe pagină."""
        login_button = self.driver.find_element(*self.BUTTON_LOGIN)
        assert login_button.is_displayed(), "Butonul de Login nu este afisat"

    # Test 5

    def test_atribut_href(self):
        """Verifică dacă atributul 'href' al unui link este cel așteptat."""
        expected_href = "http://elementalselenium.com/"
        actual_href = self.driver.find_element(By.XPATH, "//a[text()='Elemental Selenium']").get_attribute("href")
        self.assertEqual(expected_href, actual_href, "Link-ul 'href' este incorect")

    # Test 6

    def test_blank_login(self):
        """Verifică afișarea corectă a erorii în cazul unei autentificări fără username și password."""
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        eroare = self.driver.find_element(By.ID, "flash")
        assert eroare.is_displayed(), "Eroarea nu este afisata dupa logare fara Username/Password"

    # Test 7

    def test_invalid_login(self):
        """Verifică afișarea corectă a mesajului de eroare în cazul unei autentificări invalide."""
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys("wrong_user")
        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys("wrong_password")
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        expected_message = "Your username is invalid!"
        actual_message = self.driver.find_element(By.ID, "flash").text
        self.assertTrue(expected_message in actual_message, "Mesajul de eroare nu este corect")

    def wait_for_element_to_be_present(self, element_locator, seconds_to_wait):
        wait = WebDriverWait(self.driver, seconds_to_wait)
        return wait.until(EC.presence_of_element_located(element_locator))

    def wait_for_element_to_disappear(self, element, timp):
        wait = WebDriverWait(self.driver, timp)
        return wait.until(EC.none_of(EC.presence_of_element_located(element)))

    def is_element_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    # Test 8

    def test_eroare_message_disappears_on_click(self):
        """Verifică dacă mesajul de eroare dispare după ce utilizatorul face click pe el."""
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        self.driver.find_element(By.CLASS_NAME, "close").click()
        self.wait_for_element_to_disappear((By.ID, "flash"), 3)
        self.assertTrue(not self.is_element_present((By.ID, "flash")), "Mesajul de eroare nu a disparut")

    # Test 9

    def test_text_asteptat(self):
        """Verifică dacă textul de pe label-urile din pagină corespunde cu cel așteptat."""
        lista_label = self.driver.find_elements(By.XPATH, "//label")
        expected_label_text_1 = "Username"
        actual_label_text_1 = lista_label[0].text
        expected_label_text_2 = "Password"
        actual_label_text_2 = lista_label[1].text
        self.assertEqual(expected_label_text_1, actual_label_text_1, "Textul de pe label nu coincide")
        self.assertEqual(expected_label_text_2, actual_label_text_2, "Textul de pe label nu coincide")

    # Test 10

    def test_valid_login(self):
        """Verifică dacă se realizează cu succes o autentificare validă."""
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys("tomsmith")
        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys("SuperSecretPassword!")
        self.driver.find_element(*self.BUTTON_LOGIN).click()

        actual_url = self.driver.current_url
        self.assertIn("/secure", actual_url), "Noul URL nu contine '/secure'"
        element_flash_success = self.wait_for_element_to_be_present(self.SECURE_AREA, 3)
        self.assertTrue(element_flash_success.is_displayed(), "Elementul nu este afisat")
        mesaj = self.driver.find_element(*self.SECURE_AREA).text
        self.assertIn("secure area", mesaj, "Mesajul nu contine textul 'secure area!'")




