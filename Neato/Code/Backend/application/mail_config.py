"""
Module for sending emails using SMTP.
"""

import os
import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "21f3002511@ds.study.iitm.ac.in"
SENDER_PASSWORD = ''

def send_email(to, subject, msg, attachment=None):
    """
    Send an email with optional attachment using SMTP.
    """
    try:
        mail = MIMEMultipart()
        mail["From"] = SENDER_ADDRESS
        mail["Subject"] = subject
        mail["To"] = to

        # Add HTML content
        mail.attach(MIMEText(msg, "html"))

        if attachment is not None:
            # Check file size
            file_size = os.path.getsize(attachment)
            max_size = 10 * 1024 * 1024  # 10MB limit
            
            if file_size > max_size:
                print(f"Warning: File size ({file_size} bytes) exceeds 10MB limit")
                # You might want to implement file compression here
            
            # Add attachment with chunked reading
            with open(attachment, "rb") as attachment_file:
                part = MIMEBase("application", "pdf")
                
                # Read file in chunks to handle large files
                chunk_size = 1024 * 1024  # 1MB chunks
                file_data = b""
                while True:
                    chunk = attachment_file.read(chunk_size)
                    if not chunk:
                        break
                    file_data += chunk
                
                part.set_payload(file_data)
                encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment)}"
            )
            mail.attach(part)

        # Connect with timeout
        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT, timeout=30)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(mail)
        s.quit()

        # Remove the file after successful sending
        if attachment is not None:
            os.remove(attachment)

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise