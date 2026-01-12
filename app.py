from flask import Flask, render_template, request, redirect, session, flash
from googlesheets import save_to_google_sheet, get_all_contacts
import pandas as pd
from flask import send_file
import tempfile
import os
from flask import Response
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")


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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        save_to_google_sheet(
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['message']
        )
        return redirect('/contact')

    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin_user = os.getenv("ADMIN_USERNAME")
        admin_pass = os.getenv("ADMIN_PASSWORD")

        if username == admin_user and password == admin_pass:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            flash("Invalid username or password", "danger")

    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    contacts = get_all_contacts()
    return render_template('admin_dashboard.html', contacts=contacts)

@app.route('/download-contacts')
def download_contacts():
    if not session.get('admin'):
        return redirect('/admin')

    contacts = get_all_contacts()
    df = pd.DataFrame(contacts)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(temp.name, index=False)

    return send_file(
        temp.name,
        as_attachment=True,
        download_name="ngo_contacts.xlsx"
    )

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/sitemap.xml')
def sitemap():
    pages = [
        "",
        "about",
        "programs",
        "gallery",
        "certifications",
        "donate",
        "contact"
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append(f"""
        <url>
            <loc>https://www.ngoaadharfoundation.org.in/{page}</loc>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        """)

    xml.append('</urlset>')
    return Response("".join(xml), mimetype='application/xml')

if __name__ == "__main__":
    app.run(debug=False)
