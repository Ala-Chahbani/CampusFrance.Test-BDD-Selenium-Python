from selenium import webdriver

def before_scenario(context, scenario):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

def after_scenario(context, scenario):
    context.driver.delete_all_cookies()
    context.driver.quit()
