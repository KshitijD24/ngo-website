import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

def get_gspread_client():
    # Load credentials from environment variable
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def save_to_google_sheet(name, email, phone, message):
    client = get_gspread_client()
    sheet = client.open("NGO_Contact_Data").sheet1

    sheet.append_row([
        name,
        email,
        phone,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

def get_all_contacts():
    client = get_gspread_client()
    sheet = client.open("NGO_Contact_Data").sheet1

    return sheet.get_all_records()

