import os
import pandas as pd
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from openai import OpenAI

# Initialize OpenAI client with the environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Path to the Excel file
EXCEL_FILE_PATH = 'users.xlsx'

def create_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    # Create a table for storing chat history
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

create_db()

def store_chat_history(username, role, content):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO chat_history (username, role, content)
    VALUES (?, ?, ?)
    ''', (username, role, content))

    conn.commit()
    conn.close()

# Function to read users from Excel file
def read_users_from_excel():
    if not os.path.exists(EXCEL_FILE_PATH):
        return pd.DataFrame(columns=['username', 'password'])
    return pd.read_excel(EXCEL_FILE_PATH, sheet_name='users')

# Function to write users to Excel file
def write_users_to_excel(df):
    df.to_excel(EXCEL_FILE_PATH, sheet_name='users', index=False)

# Function to generate a response from OpenAI
def generate_summary(text_input, system_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        specialist = request.form['specialist']

        system_message = f"Please act as a {specialist}, respond to all the queries as if you are a {specialist}"
        response = generate_summary(user_input, system_message)
        if response:
            chat_history = session.get('chat_history', [])
            chat_history.append({'role': 'user', 'content': user_input})
            chat_history.append({'role': 'ai', 'content': response})
            session['chat_history'] = chat_history

            # Store chat history in the database
            store_chat_history(session['username'], 'user', user_input)
            store_chat_history(session['username'], 'ai', response)

        return redirect(url_for('home'))

    if 'chat_history' not in session:
        session['chat_history'] = []
        session['is_first_input'] = True
        session['specialist'] = None

    return render_template('index.html', chat_history=session.get('chat_history', []), is_first_input=session.get('is_first_input', True), specialist=session.get('specialist'))

def load_chat_history(username):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT role, content
    FROM chat_history
    WHERE username = ?
    ORDER BY timestamp
    ''', (username,))

    rows = cursor.fetchall()
    conn.close()

    return [{'role': row[0], 'content': row[1]} for row in rows]

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    chat_history = load_chat_history(username)
    return jsonify(chat_history)

@app.route('/clear_chat', methods=['GET'])
def clear_chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    session['chat_history'] = []
    session.modified = True
    return redirect(url_for('home'))

@app.route('/set_specialist/<role>', methods=['GET'])
def set_specialist(role):
    if 'username' not in session:
        return redirect(url_for('login'))

    session['specialist'] = role
    session.modified = True
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users_df = read_users_from_excel()

        if username in users_df['username'].values:
            user_password = users_df[users_df['username'] == username]['password'].values[0]
            if user_password == password:
                session['username'] = username
                session['chat_history'] = []
                return redirect(url_for('home'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('Username not found', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        users_df = read_users_from_excel()

        if username in users_df['username'].values:
            flash('Username already exists', 'danger')
        else:
            new_user = pd.DataFrame({'username': [username], 'password': [password]})
            updated_df = pd.concat([users_df, new_user], ignore_index=True)
            write_users_to_excel(updated_df)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('chat_history', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
