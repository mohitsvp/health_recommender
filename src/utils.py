import re
import smtplib
import os
import jwt
import datetime
from PyPDF2 import PdfReader
from langchain.tools import tool
from fpdf import FPDF
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import current_app

def fetch_pdf_content_from_url(pdf_url):
    @tool
    def fetch_pdf_content(url: str) -> str:
        """
        Fetches and preprocesses content from a PDF.
        Returns the text of the PDF.
        """
        #return url
        with open(pdf_url, "rb") as f:
            pdf = PdfReader(f)
            text = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )

        # Optional preprocessing of text
        processed_text = re.sub(r"\s+", " ", text).strip()

        return processed_text
    
    return fetch_pdf_content

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.write(5, text)
    pdf.output("output/health_recommendations.pdf")

def send_email(filePath, email):
    sender_email = os.environ.get("SENDER_EMAIL","your_email@gmail.com")
    password = os.environ.get("EMAIL_PASSWORD","secret") 
    subject = "Your health recommendations"
    body = "Please find attached the health recommendations based on your blood test report."
    pdf_filename = filePath

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with open(pdf_filename, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name="Health Recommendations.pdf")
    part['Content-Disposition'] = f'attachment; filename="Health Recommendations.pdf"'
    message.attach(part)
    context = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    context.login(sender_email, password)
    context.sendmail(sender_email, email, message.as_string())
    context.quit()

def generate_token(id):
    """
    Generates a JWT token for a given email.
    """
    try:
        token = jwt.encode(
            {'userId': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            current_app.config['SECRET_KEY'],
            algorithm="HS256" 
        )
        return token
    except Exception as e:
        return str(e)
    
def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload['userId']
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")