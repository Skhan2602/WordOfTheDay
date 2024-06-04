# Word of The Day

"Word of The Day" is a Python project that sends an email every day with a new word, its definition, and example usage. The project uses two APIs to fetch word definitions and examples. If the first API fails to find a word, the second API is used as a fallback. The project keeps track of words that have already been sent to ensure that a new word is sent each day.

## Features
- Fetches a new word, its definition, and example usage from two different APIs.
- Sends an email with the word, definition, and example usage to a list of recipients.
- Keeps track of words that have already been sent to avoid repetition.
- Automatically retries with a different word if the current word is not found in both APIs.

## Project Structure
- `main.py`: The main script that loads the words, checks if they have been sent, fetches definitions and examples from APIs, and sends the email.
- `words_alpha.txt`: A text file containing a list of words from which the script randomly selects a word each day.
- `sent_words.txt`: A text file that keeps track of the words that have already been sent.

## Files

### `main.py`
This is the main script of the project. It performs the following tasks:
- Loads the list of words from `words_alpha.txt`.
- Randomly selects a word that has not been sent yet.
- Fetches the word's definition and example usage from two APIs.
- Sends an email with the word, definition, and example usage to a list of recipients.
- Updates `sent_words.txt` to mark the word as sent.

### `words_alpha.txt`
This file contains a list of words, one per line. The script randomly selects a word from this list each day.

### `sent_words.txt`
This file keeps track of the words that have already been sent. Each time a word is sent, it is added to this file to ensure it is not sent again in the future.

## Requirements
- Python 3.x
- `requests` library
- `smtplib` library
- `email` library

You can install the required libraries using pip:
```bash
pip install requests
```

## Setup and Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WordOfTheDay.git
   ```
2. Navigate to the project directory:
   ```bash
   cd WordOfTheDay
   ```
3. Make sure `words_alpha.txt` contains the words you want to use.
4. Update the email credentials and recipient list in the `send_email` function in `main.py`.
5. Run the script:
   ```bash
   python main.py
   ```

## Note
- Make sure to replace the placeholders in the script (`"X-RapidAPI-Key"`, `"sender_email"`, and `"sender_password"`) with your actual API key and email credentials.
- Ensure that you have appropriate permissions to access the SMTP server and send emails.
- To ensure the email is sent every day, you can use a task scheduler.



Happy learning with the Word of The Day!
