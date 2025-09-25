from selenium.webdriver import Chrome

def before_scenario(context, scenario):
    context.driver = Chrome()
    context.driver.maximize_window()

def after_scenario(context, scenario):
    context.driver.delete_all_cookies()
    context.driver.quit()
