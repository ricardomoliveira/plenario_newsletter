import os
from subscribers import get_subscription_list, get_formatted_date, send_email
import mail

def main():
    # Authenticate with HubSpot
    recipients = get_subscription_list()
    if len(recipients) == 0:
        print("No recipients found. Exiting.")
        exit()

    # Fetch new items from RSS feeds
    body = mail.generate_email_html()
    subject = formatted_date = "Resumo Diário - {}".format(get_formatted_date())

    # Get secrets from environment variables
    mailersend_api_key = os.getenv("MAILERSEND_API_KEY")
    mailersend_api_email = os.getenv("MAILERSEND_API_EMAIL")

    if not mailersend_api_key or not mailersend_api_email:
        print("Missing MAILERSEND_API_KEY or MAILERSEND_API_EMAIL. Exiting.")
        exit()

    # Send email
    response = send_email(mailersend_api_key, mailersend_api_email, recipients, subject, body)
    if response == 202:
        print("Email sent successfully.")
    else:
        print(f"Failed to send email: {response}")

if __name__ == "__main__":
    main()
