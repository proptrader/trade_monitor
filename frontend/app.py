from flask import Flask, render_template, render_template_string
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main layout with nav and empty content area
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    # TODO: Implement summary/overview partial
    return render_template('dashboard_summary.html')

@app.route('/trades')
def trades():
    # Return the live/all trades tabbed interface
    return render_template('dashboard.html')

@app.route('/accounts')
def accounts():
    try:
        # Fetch accounts from backend API
        response = requests.get('http://localhost:5000/api/accounts')
        accounts = response.json()
        return render_template('accounts.html', accounts=accounts)
    except Exception as e:
        return render_template('accounts.html', accounts=[], error=str(e))

@app.route('/logs')
def logs():
    return render_template('logs.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000) 