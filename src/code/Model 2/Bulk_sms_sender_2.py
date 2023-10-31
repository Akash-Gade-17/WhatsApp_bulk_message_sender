import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import streamlit as st

# Set your database connection parameters here
db_host = "localhost"
db_user = "SQLuser"
db_password = "Akash@1234"  # Hardcoded database password
db_name = "customer_data"

# Function to send a WhatsApp message
def send_whatsapp_message(name, phone_number, label):
    # Load the Chrome driver
    chrome_driver_path = r"C:\new driver\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get("https://web.whatsapp.com/")

    # Wait for user to scan the QR code manually
    st.info("Please scan the QR code manually in your browser to log in to WhatsApp.")

    wait = WebDriverWait(driver, 20)  # Use WebDriverWait for better handling of page load

    # Create a customized message based on the label
    if label == "Recently added customer":
        message = f"Hello {name}, welcome to our service!"
    else:
        message = f"Hello {name}, thanks for being a loyal customer!"

    # Locate the search box
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))

    # Clear the search box
    search_box.clear()

    # Send the phone number to the search box
    search_box.send_keys(phone_number)

    # Wait for 5 seconds for the contact to load
    time.sleep(20)

    try:
        # Check if the contact is unavailable
        driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/span')
    except NoSuchElementException:
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

try:
    # Connect to the database
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    # Query the database to fetch customer data
    cursor.execute("SELECT name, phone_number, customer FROM customers")
    customers = cursor.fetchall()

    st.success("Connected to the database")

    # Loop through the customers and send WhatsApp messages
    for customer in customers:
        name, phone_number, label = customer
        if label == "Recently added customer":
            send_whatsapp_message(name, phone_number, label)

    connection.close()
except Exception as e:
    st.error(f"Error: {str(e)}")
