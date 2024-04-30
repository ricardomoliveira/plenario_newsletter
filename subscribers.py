import requests
import webbrowser
from mail import generate_email_html, get_formatted_date
from mailersend import emails
import os

# Access GitHub secrets
HUBSPOT_API_BASE_URL = 'https://api.hubapi.com'
MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
MAILERSEND_API_EMAIL = os.getenv('MAILERSEND_API_EMAIL')
HUBSPOT_ACCESS_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')

# Check if secrets are available
if None in [HUBSPOT_API_BASE_URL, MAILERSEND_API_KEY, MAILERSEND_API_EMAIL, HUBSPOT_ACCESS_TOKEN]:
    raise ValueError("One or more required secrets are missing.")

def authenticate_hubspot():
    headers = {
        'Authorization': f'Bearer {HUBSPOT_ACCESS_TOKEN}'
    }
    return headers

def get_subscription_list():
    # Fetch the subscription list from HubSpot
    headers = authenticate_hubspot()
    params = {
        'property': 'SubscriptionStatus',
        'value': 'Active'
    }
    response = requests.get(f'{HUBSPOT_API_BASE_URL}/contacts/v1/lists/all/contacts/all', headers=headers,
                            params=params)

    if response.status_code == 200:
        contacts = response.json()['contacts']
        subscribers = []

        # Get subscribers' email addresses
        for contact in contacts:
            if 'properties' in contact and 'subscriptionstatus' in contact['properties']:
                subscription_status = contact['properties']['subscriptionstatus']['value']
                if subscription_status == 'Active':
                    for identity_profile in contact['identity-profiles']:
                        for identity in identity_profile['identities']:
                            if identity['type'] == 'EMAIL':
                                subscribers.append((identity['value'], contact['vid']))

        return [email for email, _ in subscribers]
    else:
        print(f'Failed to get subscription list from HubSpot: {response.text}')
        return []

def send_email(api_key, sender_email, bcc_recipients, subject, body):
    try:
        # Initialize a NewEmail instance with your API key
        mailer = emails.NewEmail(api_key)

        # Define mail_from dictionary
        mail_from = {
            "email": sender_email,
            "name": "Your Name"  # Replace with sender's name if needed
        }

        # Define an empty dictionary to populate with mail values
        mail_body = {}

        # Set mail_from, subject, HTML content
        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(body, mail_body)

        # Send separate emails to each BCC recipient
        for recipient in bcc_recipients:
            # Define BCC recipient
            mail_to = {"email": recipient}

            # Set mail_to
            mailer.set_mail_to([mail_to], mail_body)

            # Send the email
            response = mailer.send(mail_body)
            print(response)

        return True  # Indicate success
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")
        return False  # Indicate failure

# Test the functions
if __name__ == "__main__":
    # Authenticate with HubSpot
    recipients = get_subscription_list()
    if len(recipients) == 0:
        exit()

    # Fetch new items from RSS feeds
    body = generate_email_html()
    subject = formatted_date = "Resumo Diário - {}".format(get_formatted_date())
    response = send_email(MAILERSEND_API_KEY, MAILERSEND_API_EMAIL, recipients, subject, body)

# Save HTML content to a file
    with open("new_items.html", "w") as f:
        f.write(body)

    # Open the HTML file in a web browser
    webbrowser.open("new_items.html")

