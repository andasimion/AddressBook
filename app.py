from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from repositories import ContactsRepository
from models import contact_from_form
app = Flask(__name__)

def open_db():
    return sqlite3.connect('address_book.db')
    
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/contacts')
def contacts():
    db = open_db()
    repo = ContactsRepository(db)    
    all_rows = repo.get_contacts()
    db.close()
    return render_template ('contacts.html', all_rows=all_rows)
    
@app.route('/contacts/edit_contact/<contact_id>')
def edit_contact(contact_id):
    db = open_db()
    repo = ContactsRepository(db)    
    row = repo.get_contact(contact_id)
    db.close()
    return render_template ('edit_contact.html', row=row)

@app.route('/contacts/update_contact/<contact_id>', methods = ['POST'])
def update_contact(contact_id):
    new_contact_data = contact_from_form(request.form)
    db = open_db()
    repo = ContactsRepository(db)
    repo.update_contact(contact_id, new_contact_data)  
    db.close()  
    return redirect(url_for('contacts'))
    
@app.route('/contacts/add_contact')
def add_contact():
    return render_template ('add_contact.html')


@app.route('/contacts/insert_contact', methods = ['POST'])
def insert_contact():
    contact = contact_from_form(request.form)
    db = open_db()
    repo = ContactsRepository(db)
    repo.insert_contact(contact)   
    db.close() 
    return redirect(url_for('contacts'))
    
@app.route('/contacts/delete_contact/<contact_id>')
def delete_contact(contact_id):
    db = open_db()
    repo = ContactsRepository(db)
    repo.delete_contact(contact_id)
    db.close()
    return redirect(url_for('contacts'))
    
@app.route('/birthdays')
def birthdays():
    current_date = datetime.date.today()
    db = open_db()
    repo = ContactsRepository(db)
    birthdays_today = repo.birthdays_today()
    birthdays_next_week = repo.birthdays_next_week()
    db.close()
    return render_template ('birthdays.html', current_date = current_date,
                                              birthdays_today = birthdays_today,
                                              birthdays_next_week = birthdays_next_week)
    
@app.route('/namedays')
def namedays():
    current_date = datetime.date.today()
    db = open_db()
    repo = ContactsRepository(db)
    saints_today = repo.saints_today(current_date)
    namedays_today = repo.namedays_today(current_date)
    namedays_next_month = repo.namedays_next_month()
    saints_next_month = repo.saints_next_month()
    db.close()
    return render_template ('namedays.html', current_date = current_date, 
                                             today_saint = saints_today, 
                                             namedays_today = namedays_today,
                                             namedays_next_month = namedays_next_month, 
                                             saints_next_month = saints_next_month)
    
if __name__ == '__main__':
    app.run(debug = True)

