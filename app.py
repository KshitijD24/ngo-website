from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

def get_db():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        # Render / Production
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    else:
        # Local development
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/certifications')
def certifications():
    return render_template('certifications.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['message']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO contacts (name, email, phone, message) VALUES (%s, %s, %s, %s)",(name, email, phone, msg))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/contact')

    return render_template('contact.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='admin123':
            session['admin']=True
            return redirect('/dashboard')
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    SELECT id, name, email, phone, message
    FROM contacts
    ORDER BY id DESC""")
    contacts = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('admin_dashboard.html', contacts=contacts)

@app.route('/logout')
def logout():
    session.pop('admin',None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
