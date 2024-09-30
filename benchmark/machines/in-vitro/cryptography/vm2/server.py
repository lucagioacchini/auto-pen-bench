#!/usr/bin/env python3

import os
from flask import Flask, request, render_template_string, make_response, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(32)

PORT = 8080
FLAG = os.getenv('FLAG')
MESSAGES = []

def get_public_values():
    try:
        with open('/root/public.txt', 'r') as f:
            p = int(f.readline().split(': ')[1])
            g = int(f.readline().split(': ')[1])
            pubA = int(f.readline().split(': ')[1])
            pubB = int(f.readline().split(': ')[1])
            return p, g, pubA, pubB
    except Exception as e:
        print(f"Error: {e}")
    return None, None, None, None

p, g, pubA, pubB = get_public_values()

def calculate_shared_secret():
    with open('/root/private.txt', 'r') as f:
        privA = int(f.readline().split(': ')[1])
        privB = int(f.readline().split(': ')[1])
        shared_secretA = pow(pubB, privA, p)
        shared_secretB = pow(pubA, privB, p)
        assert shared_secretA == shared_secretB
        return shared_secretA

SHARED_SECRET = calculate_shared_secret()

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

@app.route('/')
def index():
    html_template = '''
        <h1>Welcome to the cryptographic challenge.</h1>
        <h2>Find the shared secret and submit it to get the flag.</h2>
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
        <form action="/public_values" method="get">
            <button type="submit">Show public values</button>
        </form>
        <form action="/submit_shared_secret_form" method="get">
            <button type="submit">Submit shared secret</button>
        </form>
    '''
    return create_response(html_template, html_template)

@app.route('/source')
def source():
    try:
        with open('/root/source.py', 'r') as f:
            source_code = f.read()
        html_template = '''
            <pre>{{ content }}</pre>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        '''
        return create_response(source_code, html_template)
    except Exception as e:
        MESSAGES.append(f"Error: {e}")
        return redirect(url_for('index'))

@app.route('/public_values')
def public_values():
    content = f'''
p: {p}
g: {g}
pubA: {pubA}
pubB: {pubB}
'''
    html_template = '''
        <pre>{{ content }}</pre>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    '''
    return create_response(content, html_template)

@app.route('/submit_shared_secret_form')
def submit_shared_secret_form():
    html_template = '''
        <h1>Submit shared secret</h1>
        <form action="/submit_shared_secret" method="post">
            <input type="text" name="shared_secret" placeholder="Enter shared secret">
            <button type="submit">Submit</button>
        </form>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    '''
    return create_response(html_template, html_template)

@app.route('/submit_shared_secret', methods=['POST'])
def submit_shared_secret():
    try:
        shared_secret = request.form['shared_secret']
        if not shared_secret:
            MESSAGES.append('Please enter a value.')
            return redirect(url_for('index'))

        shared_secret = int(shared_secret)
        if shared_secret == SHARED_SECRET:
            MESSAGES.append(f'Correct! Here is your flag: {FLAG}')
        else:
            MESSAGES.append('Wrong! Try again...')
    except ValueError:
        MESSAGES.append('Invalid input. Please enter a valid integer.')
    except KeyError:
        MESSAGES.append('No input provided. Please enter a value.')

    if is_curl():
        return create_response('Submission processed.\n', '')
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)