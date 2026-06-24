# streamlit_app.py

import streamlit as st
from back.main import app

st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="🎧"
)

st.title("🎧 Customer Support System")

message = st.text_area(
    "Describe your issue",
    height=150
)

if st.button("Submit Ticket"):

    with st.spinner("Processing..."):

        result = app.invoke({
            "ticket_id": "T-1001",
            "customer_id": "C-500",
            "message": message
        })

    st.success("Ticket Processed")

    st.subheader("Category")
    st.write(result["category"])

    st.subheader("Response")
    st.write(result["final_response"])