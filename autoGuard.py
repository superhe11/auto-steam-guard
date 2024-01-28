import re
import pyperclip
import time
import imaplib
import email
from email.header import decode_header

import threading

exit_flag = threading.Event()

def check_input():
    input("Press Enter to exit the program...\n")
    exit_flag.set()

input_thread = threading.Thread(target=check_input)
input_thread.start()

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
CREDENTIALS_FILE = "credentials.txt"

def read_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            credentials = file.read().strip().split(":")
            email = credentials[0]
            password = credentials[1]
            print("Credentials retrieved, starting monitoring.")
            return email, password
    except FileNotFoundError:
        print(f"File {CREDENTIALS_FILE} not found.")
        return None, None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None, None

def decode_subject(encoded_subject):
    decoded_parts = decode_header(encoded_subject)
    decoded_subject = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_subject += part.decode(encoding if encoding else 'utf-8')
        else:
            decoded_subject += part
    return decoded_subject

def find_latest_email(email_address, password):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_address, password)

        mail.select("inbox")

        _, messages = mail.search(None, '(FROM "noreply@steampowered.com")')

        latest_email_id = messages[0].split()[-1]

        _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg.get("Subject")
        decoded_subject = decode_subject(subject)

        print(f"Latest email from noreply@steampowered.com:")
        print(f"Subject: {decoded_subject}")

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    break
        else:
            body = msg.get_payload(decode=True)

        code_match = re.search(r"\b(?:(?!Steam)(?!image)(?!Email)(?!gmail)(?!Guard)(?!https)(?!Valve)(?!email)[A-Za-z0-9]){5}\b", body.decode('utf-8'))

        if code_match:
            verification_code = code_match.group(0)
            current_clipboard = pyperclip.paste()

            if current_clipboard != verification_code:
                pyperclip.copy(verification_code)
                print(f"Code found: {verification_code}")
                print("Code copied to the clipboard.")
                print("==============================")
            else:
                print("Code unchanged since the last time.")
                print("==============================")
        else:
            print("Code not found in the email text.")
            print("==============================")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        mail.logout()

while not exit_flag.is_set():
    email_address, password = read_credentials()
    
    if email_address is not None and password is not None:
        find_latest_email(email_address, password)
    
    time.sleep(3)

print("Program terminated.")
