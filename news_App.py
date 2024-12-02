from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'Dangelo26'

# API Key
NEWS_API_KEY = 'ee1114d3267443c4b749d4655f22658d'

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # For simplicity, using hardcoded credentials
        if username == 'user' and password == 'password':
            session['user_id'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    categories = ["Technology", "Sports", "Entertainment", "Politics"]
    return render_template('dashboard.html', title="Dashboard", categories=categories)

@app.route('/category/<category>')
def category_feed(category):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    url = f'https://newsapi.org/v2/top-headlines?category={category.lower()}&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    articles = response.get('articles', [])
    
    if not articles:
        flash('No articles available in this category.', 'info')

    return render_template('category_feed.html', category=category.capitalize(), articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
