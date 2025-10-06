from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator):
        self.find_element(locator).click()

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

class ContactPage(BasePage):
    NAME_FIELD = (By.ID, "name")
    EMAIL_FIELD = (By.ID, "email")
    MESSAGE_FIELD = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit")
    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")

    def fill_name(self, name):
        self.input_text(self.NAME_FIELD, name)

    def fill_email(self, email):
        self.input_text(self.EMAIL_FIELD, email)

    def fill_message(self, message):
        self.input_text(self.MESSAGE_FIELD, message)

    def submit_form(self):
        self.click_element(self.SUBMIT_BUTTON)

    def get_success_message(self):
        return self.find_element(self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        return self.find_element(self.ERROR_MESSAGE).text

# позитивный тест
def test_positive_contact_form_submission(driver):
    contact_page = ContactPage(driver)
    contact_page.fill_name("Филюшина Полина")
    contact_page.fill_email("polly@gmail.com")
    contact_page.fill_message("Привет!")
    contact_page.submit_form()
    assert "Форма успешно отправлена" in contact_page.get_success_message()

# негативный тест
def test_negative_contact_form_empty_name(driver):
    contact_page = ContactPage(driver)
    contact_page.fill_email("polly@gmail.com")
    contact_page.fill_message("Привет!")
    contact_page.submit_form()
    assert "ФИО слишком короткое" in contact_page.get_error_message()

@pytest.fixture
def driver():
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("file:///C:/Users/polly/Desktop/вуз/тестирование/лб4/код/lb4_ui-testing/form.html")
    yield driver
    driver.quit()