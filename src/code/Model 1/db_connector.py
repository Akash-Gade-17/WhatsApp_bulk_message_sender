import mysql.connector
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="SQLuser",
    password="Akash@1234",
    database="customer_data"
)


# Create a cursor
cursor = db.cursor()

# Define messages and labels
new_customer_message = "Welcome to our service! Are you interested? (Yes/No)"
interested_message = "Great! How can we assist you?"
existing_customer_message = "Thank you for choosing us!"


# Create a function to send WhatsApp messages
def send_whatsapp_message(phone_number, message):
    chrome_driver_path = r"C:\new driver\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("https://web.whatsapp.com")
    time.sleep(300)  # Wait for the user to log in using QR code

    # Find all target div elements
    search_boxes = driver.find_elements_by_css_selector('div[data-ref^="2@e93H5FZs02h0b7Gfz8eWMQHVTZAz7iTZjMk6DXgFYD4Tr3zklLYYnqBdzkE8RmfsKD4IBfx5Zdx1+A==,5B1w6bEG0FmDUsK0zOAohRKhsIpyliDy+ym4UfNsxRU=,CNYtR52dS84jRin1fsv/y9EdAF1pN4pFYY7ioxhLHlI=,U5frIcF35uAlPbV1Pk4+xRHHR4pBB5tpHWYnEAdshH0=,1"][style^="flex"]')

    for search_box in search_boxes:
        search_box.click()  # Click on the target element

        # Locate the message input element and send the message
        message_box = driver.find_element_by_css_selector('div[data-tab="6"]')
        message_box.send_keys(message)
        message_box.send_keys(webdriver.common.keys.Keys.ENTER)

    driver.quit()


# Query the database
cursor.execute("SELECT name, phone_number, customer FROM data")
results = cursor.fetchall()

# Define a simple message
simple_message = "Thank you for being our valued customer!"

# Loop through the database results and send the simple message
for name, phone_number, customer in results:
    send_whatsapp_message(phone_number, simple_message)


# Close the database connection
cursor.close()
db.close()