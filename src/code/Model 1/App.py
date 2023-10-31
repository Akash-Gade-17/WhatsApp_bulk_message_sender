import streamlit as st
import subprocess 

st.title("WhatsApp Bulk Message Sender")
if st.button("Press Enter"):
    st.write("Messaging start")
    subprocess.run(["python", "new.py"])
    
st.write(" Scan the QR code and log in to WhatsApp Web.")