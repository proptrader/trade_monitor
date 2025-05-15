from flask import Flask, render_template, render_template_string, request
import os
import requests

app = Flask(__name__)

# Backend API configuration
app.config['BACKEND_URL'] = 'http://localhost:5000'

def is_htmx_request():
    """Check if the request is coming from HTMX."""
    return request.headers.get('HX-Request') == 'true'

@app.route('/')
def index():
    # Render the main layout with nav and empty content area
    return render_template('base.html', title='Home')

@app.route('/dashboard')
def dashboard():
    # Return either full page or partial based on request type
    template = 'dashboard_summary.html'
    context = {
        'title': 'Dashboard',
        'backend_url': app.config['BACKEND_URL']
    }
    
    if is_htmx_request():
        return render_template(f'partials/{template}', **context)
    return render_template(template, **context)

@app.route('/trades')
def trades():
    # Return either full page or partial based on request type
    template = 'dashboard.html'
    context = {
        'title': 'Trades',
        'backend_url': app.config['BACKEND_URL']
    }
    
    if is_htmx_request():
        return render_template(f'partials/{template}', **context)
    return render_template(template, **context)

@app.route('/accounts')
def accounts():
    try:
        # Fetch accounts from backend API
        response = requests.get(f"{app.config['BACKEND_URL']}/api/accounts")
        accounts = response.json()
        context = {
            'title': 'Accounts',
            'accounts': accounts,
            'backend_url': app.config['BACKEND_URL']
        }
    except Exception as e:
        context = {
            'title': 'Accounts',
            'accounts': [],
            'error': str(e),
            'backend_url': app.config['BACKEND_URL']
        }
    
    template = 'accounts.html'
    if is_htmx_request():
        return render_template(f'partials/{template}', **context)
    return render_template(template, **context)

@app.route('/logs')
def logs():
    # Return either full page or partial based on request type
    template = 'logs.html'
    context = {
        'title': 'Logs',
        'backend_url': app.config['BACKEND_URL']
    }
    
    if is_htmx_request():
        return render_template(f'partials/{template}', **context)
    return render_template(template, **context)

if __name__ == '__main__':
    app.run(debug=True, port=3000) 