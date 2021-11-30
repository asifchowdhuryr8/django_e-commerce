# start server from vs code and run this file from another vs code
from selenium import webdriver
import time

firefox_driver_path = "S:/software_install_package/Firefox Web Driver/geckodriver"
driver = webdriver.Firefox(executable_path=firefox_driver_path)


driver.get("http://127.0.0.1:8000/account/register")


first_name = driver.find_element_by_name("first_name")
first_name.send_keys("blah blah")

last_name = driver.find_element_by_name("last_name")
last_name.send_keys("blah")

phone_number = driver.find_element_by_name("phone_number")
phone_number.send_keys("01777765656")

email = driver.find_element_by_name("email")
email.send_keys("asifchowdhuryrafi143@yahoo.com")

password = driver.find_element_by_name("password")
password.send_keys("My_Password_123")

confirm_password = driver.find_element_by_name("confirm_password")
confirm_password.send_keys("My_Password_123")
# My_Password_123

add = driver.find_element_by_id("register")
add.click()

time.sleep(5)
driver.close()
