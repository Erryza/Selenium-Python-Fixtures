import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()


data = [
    ("", "", "Epic sadface: Username is required"),
    ("standard_user", "", "Epic sadface: Password is required"),
    ("", "secret_sauce", "Epic sadface: Username is required"),
    ("standard", "secret_sauce",
     "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "secret",
     "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "secret_sauce", "Swag Labs")
]


@pytest.mark.login
@pytest.mark.parametrize("username, password, message", data)
def test_login(setup, username, password, message):
    setup.find_element(By.ID, "user-name").send_keys(username)
    setup.find_element(By.ID, "password").send_keys(password)
    setup.find_element(By.ID, "login-button").click()
    sleep(3)

    if message == "Swag Labs":
        successMessage = setup.find_element(
            By.XPATH, "//div[@class='app_logo']").text
        assert successMessage == message

        urlWebsite = setup.current_url
        assert urlWebsite == "https://www.saucedemo.com/inventory.html"

    else:
        errorMessage = setup.find_element(
            By.CSS_SELECTOR, "h3[data-test='error']").text
        assert errorMessage == message
    sleep(5)


@pytest.mark.logout
def test_logout(setup):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    sleep(3)

    successMessage = setup.find_element(
        By.XPATH, "//div[@class='app_logo']").text
    assert successMessage == "Swag Labs"

    if successMessage:
        urlWebsite = setup.current_url
        assert urlWebsite == "https://www.saucedemo.com/inventory.html"

        menuBurger = setup.find_element(
            By.XPATH, "//button[@id='react-burger-menu-btn']")
        menuBurger.click()

        btnLogout = WebDriverWait(setup, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='logout_sidebar_link']")))
        btnLogout.click()
        sleep(3)

        urlWebsite = setup.current_url
        assert urlWebsite == "https://www.saucedemo.com/"
        print(urlWebsite)
    else:
        print("Your username or password invalid!")


listDropdowns = [
    ("az", "za", "lohi", "hilo")
]


@pytest.mark.selectProduct
@pytest.mark.parametrize("value", listDropdowns)
def test_select_product(setup, value):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    sleep(3)

    successMessage = setup.find_element(
        By.XPATH, "//div[@class='app_logo']").text
    assert successMessage == "Swag Labs"

    for val in value:
        btn = WebDriverWait(setup, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//option[@value='{val}']")))
        btn.click()
        sleep(3)


@pytest.mark.checkout
def test_checkout(setup):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    sleep(3)

    successMessage = setup.find_element(
        By.XPATH, "//div[@class='app_logo']").text
    assert successMessage == "Swag Labs"

    if successMessage:
        urlWebsite = setup.current_url
        assert urlWebsite == "https://www.saucedemo.com/inventory.html"
    else:
        print("Your username or password invalid!")
    sleep(5)

    setup.find_element(
        By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']").click()

    setup.find_element(
        By.XPATH, "//div[@id='shopping_cart_container']").click()

    urlWebsite = setup.current_url
    assert urlWebsite == "https://www.saucedemo.com/cart.html"
    sleep(3)

    setup.find_element(By.XPATH, "//button[@id='checkout']").click()

    element = setup.find_element(By.XPATH, "//span[@class='title']").text
    assert element == "Checkout: Your Information"

    setup.find_element(By.ID, "first-name").send_keys("Erryza")
    setup.find_element(By.ID, "last-name").send_keys("Nur Alif")
    setup.find_element(By.ID, "postal-code").send_keys("1234")
    setup.find_element(By.ID, "continue").click()
