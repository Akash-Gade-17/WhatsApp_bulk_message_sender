import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import streamlit as st
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Function to create customized messages
def create_customized_message(name, customer):
    if customer == "Recently added customer":
        message = f"Hello {name}, welcome to our service!"
    else:
        message = f"Hello {name}, thanks for being a loyal customer!"
    return message

# Function to send a WhatsApp message
def send_whatsapp_message(name, phone_number, customer, message):
    # Load the Chrome driver
    chrome_driver_path = r"C:\new driver\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("https://web.whatsapp.com")
    time.sleep(10)  # Wait for the user to log in using QR code

    # Replace placeholders with customer information
    message = message.replace('{name}', name)

    # Locate the search box
    search_box = wait.until(lambda driver: driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]'))

    # Clear the search box
    search_box.clear()

    # Send the phone number to the search box
    search_box.send_keys(phone_number)

    # Wait for 2 seconds to search for the contact
    time.sleep(2)

    # Send the message
    search_box.send_keys(Keys.ENTER)
    actions = ActionChains(driver)
    actions.send_keys(message)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # Close the browser
    driver.quit()

# Streamlit UI
st.title("WhatsApp Bulk Message Sender")
st.write("Scan the QR code and log in to WhatsApp Web.")

if st.button("Connect to Database"):
    try:
        # Connect to the MySQL database
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="SQLuser",
            password="Akash@1234",
            database="customer_data",
            connect_timeout=30
        )

        # Create a cursor
        cursor = db.cursor()

        # Query the database to fetch customer data
        cursor.execute("SELECT name, phone_number, customer FROM customers")
        results = cursor.fetchall()

        st.success("Connected to the database")

        # Loop through the database results and send messages
        for name, phone_number, customer in results:
            message = create_customized_message(name, customer)
            send_whatsapp_message(name, phone_number, customer, message)

    except Exception as e:
        st.error(f"Error: {str(e)}")
