import sqlite3
import requests
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize SQLite database and table
def initialize_database():
    conn = sqlite3.connect('sent_words.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SentWords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# Load words from a specified file
def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Check if a word has already been sent
def is_word_sent(word):
    conn = sqlite3.connect('sent_words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM SentWords WHERE word = ?", (word,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Add a word to the sent words table
def add_sent_word(word):
    conn = sqlite3.connect('sent_words.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SentWords (word) VALUES (?)", (word,))
    conn.commit()
    conn.close()

# Check word definition and example from the first API
def check_word_in_first_api(word, headers):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            definition = data['results'][0].get('definition', 'No definition available')
            example = data['results'][0].get('examples', [None])[0]
            return definition, example
    return None, None

# Check word definition and example from the second API
def check_word_in_second_api(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        first_meaning = data[0]['meanings'][0]
        definition = first_meaning['definitions'][0].get('definition')
        example = first_meaning['definitions'][0].get('example')
        return definition, example
    return None, None

# Send an email with the provided subject, body, and recipient details
def send_email(subject, body, recipient_emails, sender_email, sender_password):
    server = smtplib.SMTP('smtp.mail.example.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    for recipient_email in recipient_emails:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

    server.quit()
    print("Email sent successfully to all recipients.")

# Initialize database
initialize_database()

# Load the list of words and the file of already sent words
words_list = load_words(r'C:\path\to\words_alpha.txt')

headers = {
    "X-RapidAPI-Key": "your-rapidapi-key",
    "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
}

word_found = False
attempts = 0
max_attempts = len(words_list)

# Try to find a valid word to send
while not word_found and attempts < max_attempts:
    random_word = random.choice(words_list)
    
    # Check if the word has not been sent before
    if not is_word_sent(random_word):
        
        # Check word details from the first API
        first_api_definition, first_api_example = check_word_in_first_api(random_word, headers)

        if first_api_definition and first_api_example:
            word_found = True
            definition = first_api_definition
            example = first_api_example
        else:
            # Check word details from the second API if the first API fails
            second_api_definition, second_api_example = check_word_in_second_api(random_word)
            if second_api_definition and second_api_example:
                word_found = True
                definition = second_api_definition
                example = second_api_example

        # If a valid word is found, prepare and send the email
        if word_found:
            email_body = f"Word of the Day: {random_word}\n\nDefinition: {definition}\n\nExample: {example}"
            recipient_list = ["recipient1@example.com", "recipient2@example.com"]
            send_email("Word of the Day", email_body, recipient_list, "your-email@example.com", "your-email-password")
            add_sent_word(random_word)
            print("Email sent successfully.")
        
    attempts += 1

# Print a message if no valid word was found
if not word_found:
    print("Failed to find a valid word with details after multiple attempts.")
