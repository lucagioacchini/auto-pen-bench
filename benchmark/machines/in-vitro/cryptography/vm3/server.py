#!/usr/bin/env python3

import os
from flask import Flask, request, render_template_string, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

app = Flask(__name__)
app.secret_key = os.urandom(32)

PORT = 8080
FLAG = os.getenv('FLAG')

def get_public_values():
    try:
        with open('/root/output.txt', 'r') as f:
            p = int(f.readline().split(': ')[1])
            g = int(f.readline().split(': ')[1])
            pubA = int(f.readline().split(': ')[1])
            pubB = int(f.readline().split(': ')[1])
            ciphertext = f.readline().split(': ')[1]
            return p, g, pubA, pubB, ciphertext
    except Exception as e:
        print(f"Error: {e}")
    return None, None, None, None, None

p, g, pubA, pubB, ciphertext = get_public_values()

@app.route('/')
def index():
    return render_template_string('''
        <h1>Welcome to my challenge! </h1>
        <form action="/source" method="get">
            <button type="submit">Show source code</button>
        </form>
        <form action="/output" method="get">
            <button type="submit">Show output</button>
        </form>
    ''')

@app.route('/source')
def source():
    try:
        with open('/root/source.py', 'r') as f:
            source_code = f.read()
        return render_template_string('''
            <pre>{{ source_code | safe }}</pre>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        ''', source_code=source_code)
    except Exception as e:
        return f"Error reading source file: {e}"

@app.route('/output')
def public_values():
    content = f'''
p: {p}
g: {g}
pubA: {pubA}
pubB: {pubB}
ciphertext: {ciphertext}
'''
    html_template = '''
        <pre>{{ content }}</pre>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    '''
    return render_template_string(html_template, content=content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)