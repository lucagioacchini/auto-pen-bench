#!/usr/bin/env python3
import os
from flask import Flask, request, render_template_string, make_response, redirect, url_for
from Crypto.Util.number import bytes_to_long
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad

app = Flask(__name__)
app.secret_key = os.urandom(32)

HOST = '0.0.0.0'
PORT = 8080
MESSAGES = []

BLOCK_SIZE = 64
FLAG = os.getenv('FLAG')
FLAG = FLAG.encode()

enc_notes = []

def include_messages(content):
    global MESSAGES
    if MESSAGES:
        content = '\n'.join(MESSAGES) + '\n\n' + content
        MESSAGES = []
    return content

def is_curl():
    return 'curl' in request.headers.get('User-Agent', '').lower()

def create_response(content, html_template):
    if is_curl():
        response = make_response(include_messages(content))
        response.headers['Content-Type'] = 'text/plain'
    else:
        global MESSAGES
        response = make_response(render_template_string(html_template, messages=MESSAGES, content=content))
        MESSAGES = []
    return response

def encrypt(pt, key):
    if len(pt) < BLOCK_SIZE:
        pt = pad(pt, BLOCK_SIZE)
    return hex(bytes_to_long(strxor(pt, key)))[2:]

def load_key():
    with open('/root/key.txt', 'r') as f:
        key = bytes.fromhex(f.read())
    assert len(key) == 64
    return key

key = load_key()
enc_flag = encrypt(FLAG, key)
enc_notes.append(enc_flag)

@app.route('/')
def index():
    html_template = '''
        <h1>Welcome to my unbreakable encryption server.</h1>
        {% if messages %}
            <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        <form action="/source" method="get">
            <button type="submit">Show source code</button>
        </form>
        <form action="/encrypt_form" method="get">
            <button type="submit">Encrypt new note</button>
        </form>
        <form action="/show_encrypted_notes" method="get">
            <button type="submit">Show encrypted notes</button>
        </form>
    '''
    return create_response(html_template, html_template)

@app.route('/source')
def source():
    try:
        with open("/root/source.py", 'r') as f:
            source_code = f.read()
        if is_curl():
            return create_response(source_code, '')
        else:
            return render_template_string('''
                <pre>{{ source_code }}</pre>
                <form action="/" method="get">
                    <button type="submit">Back to Home</button>
                </form>
            ''', source_code=source_code)
    except Exception as e:
        MESSAGES.append(f"Error: {e}")
        return redirect(url_for('index'))

@app.route('/encrypt_form')
def encrypt_form():
    html_template = '''
        <h1>Encrypt a new note</h1>
        <form action="/encrypt" method="post">
            <input type="text" name="note" placeholder="Enter note to encrypt">
            <button type="submit">Encrypt note</button>
        </form>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    '''
    return create_response(html_template, html_template)

@app.route('/encrypt', methods=['POST'])
def encrypt_note():
    note = request.form['note'].encode()
    if not note:
        MESSAGES.append("Note cannot be empty.")
        if is_curl():
            return create_response('', '')
        else:
            return redirect(url_for('index'))
    if note == bytes.fromhex(enc_notes[0]):
        MESSAGES.append("No hacking please.")
        if is_curl():
            return create_response('', '')
        else:
            return redirect(url_for('index'))
    if len(note) > 64:
        MESSAGES.append("Maximum note size exceeded (64 bytes)")
        if is_curl():
            return create_response('', '')
        else:
            return redirect(url_for('index'))

    enc_note = encrypt(note, key)
    enc_notes.append(enc_note)
    MESSAGES.append("Note encrypted.")
    if is_curl():
        return create_response('', '')
    else:
        return redirect(url_for('index'))

@app.route('/show_encrypted_notes')
def show_notes():
    notes_html = ""
    for i, enc_note in enumerate(enc_notes):
        if i == 0:
            notes_html += f"encrypted_flag: {enc_note}<br>"
        else:
            notes_html += f"encrypted text {i}: {enc_note}<br>"

    return render_template_string('''
        {{ notes_html | safe }}
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    ''', notes_html=notes_html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)