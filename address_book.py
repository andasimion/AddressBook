from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
app = Flask(__name__)

# db connection is open
db = sqlite3.connect('address_book.db') 

class Contact:
    def __init__(self, id, first_name, middle_name, last_name, birthday):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birthday = birthday
        
    def full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name
        

#returns an object
def contact_from_form(form):
    return Contact(id = 0,
                   first_name = form['FIRST_NAME'],
                   middle_name = form['MIDDLE_NAME'],
                   last_name = form['LAST_NAME'],
                   birthday = form['BIRTHDAY'])

#row from db contacts table
#returns an object
def contact_from_row(row):
    return Contact(id = row[0],
                    first_name = row[1],
                    middle_name = row[2],
                    last_name = row[3],
                    birthday = row[4])

class Saint:
    def __init__(self, id, holiday_name, day, month):
        self.id = id  
        self.holiday_name = holiday_name
        self.day = day
        self.month = month

def saint_from_row(row):
    return Saint(id = row[0],
                    holiday_name = row[1],
                    day = row[2],
                    month = row[3])

class Nameday:
    def __init__(self, id, name, saint_id):
        self.id = id
        self.name = name
        self.saint_id = saint_id
        
class ContactsRepository:
    def __init__(self, db):
        self.db = db 
    
    def birthdays_today(self):
        cursor = self.db.cursor()
        sql = ("SELECT * FROM contacts WHERE strftime('%m %d', BIRTHDAY) = strftime('%m %d', 'now')")
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [contact_from_row(row) for row in rows]
    
    def birthdays_next_week(self):
        cursor = self.db.cursor()
        sql = ("SELECT * FROM contacts WHERE strftime('%m %d', BIRTHDAY) > strftime('%m %d', 'now') AND strftime('%m %d', BIRTHDAY)    <=strftime('%m %d', 'now', '+7 days')")
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [contact_from_row(row) for row in rows]
        
    def namedays_today(self, current_date):
        current_day = current_date.day
        current_month = current_date.month
        cursor = self.db.cursor()
        sql = ("SELECT contacts.ID, contacts.FIRST_NAME, contacts.MIDDLE_NAME, contacts.LAST_NAME FROM saints" +
        " INNER JOIN nameday ON saints.ID = nameday.SAINT_ID" +
        " INNER JOIN contacts ON (nameday.NAME = contacts.FIRST_NAME OR nameday.NAME = contacts.MIDDLE_NAME)" +
        "WHERE saints.DAY =" + str(current_day) + " AND saints.MONTH = " + str(current_month))
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [contact_from_row(row) for row in rows]
        
    def saints_today(self, current_date):
        current_day = current_date.day
        current_month = current_date.month
        cursor = self.db.cursor()
        sql = ("SELECT HOLIDAY_NAME FROM saints WHERE DAY =" + str(current_day) + " AND MONTH = " + str(current_month))
        cursor.execute(sql)
        return cursor.fetchall()
          
    def namedays_next_month(self):
        current_date = datetime.date.today()
        cursor = self.db.cursor()
        saint_date_fragment = "date(" + str(current_date.year) + " || '-' || substr('0'||saints.month,-2) || '-' || substr('0'||saints.day,-2))" 
        sql = ("SELECT contacts.ID, contacts.FIRST_NAME, contacts.MIDDLE_NAME, contacts.LAST_NAME, contacts.BIRTHDAY FROM saints" +
        " INNER JOIN nameday ON saints.ID = nameday.SAINT_ID" +
        " INNER JOIN contacts ON (nameday.NAME = contacts.FIRST_NAME OR nameday.NAME = contacts.MIDDLE_NAME)" +
        " WHERE " + saint_date_fragment + " > date('now') " +
        " AND " + saint_date_fragment + " <= date('now', '+300 days')")
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [contact_from_row(row) for row in rows]
        
    def saints_next_month(self):
        current_date = datetime.date.today()
        cursor = self.db.cursor()
        saint_date_fragment = "date(" + str(current_date.year) + " || '-' || substr('0'||saints.month,-2) || '-' || substr('0'||saints.day,-2))" 
        sql = ("SELECT * FROM saints WHERE " + saint_date_fragment + " > date('now') " +
        " AND " + saint_date_fragment + " <= date('now', '+300 days')")
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [saint_from_row(row) for row in rows]
    
    def insert_contact(self, contact):
        cursor = self.db.cursor()
        sql = ("INSERT INTO contacts(FIRST_NAME, MIDDLE_NAME, LAST_NAME, BIRTHDAY) " +
            "VALUES ('" + contact.first_name + "', " +
            "'" + contact.middle_name + "', " +
            "'" + contact.last_name + "', "+
            "'" + contact.birthday + "')" )
        cursor.execute(sql)
        db.commit()
        
    def update_contact(self, contact_id, new_contact_data):
        cursor = self.db.cursor()
        sql = ("UPDATE contacts SET FIRST_NAME='" + new_contact_data.first_name + "'" +
            ", MIDDLE_NAME ='" + new_contact_data.middle_name + "'" +
            ", LAST_NAME ='" + new_contact_data.last_name + "'"+
            ", BIRTHDAY ='" + new_contact_data.birthday + "'" +
            " WHERE ID = '" + contact_id + "'")
        #print sql
        cursor.execute(sql)
        db.commit()
    
    def delete_contact(self, contact_id):
        cursor = self.db.cursor()
        sql = ("DELETE FROM contacts WHERE ID =" + contact_id)
        cursor.execute(sql)
        db.commit()

    def get_contacts(self):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM contacts ORDER BY BIRTHDAY''')
        # fetchall returns an array of arrays
        rows = cursor.fetchall()
        return [contact_from_row(row) for row in rows]
        
    def get_contact(self, contact_id):
        cursor = self.db.cursor()
        # retrives the info of the contact in the edit_contact form
        cursor.execute("SELECT * FROM contacts WHERE ID = " + contact_id)
        # fetchone returns an array representing the fields of the first row
        return contact_from_row(cursor.fetchone())

        
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/contacts')
def contacts():
    repo = ContactsRepository(db)    
    all_rows = repo.get_contacts()
    return render_template ('contacts.html', all_rows=all_rows)
    
@app.route('/contacts/edit_contact/<contact_id>')
def edit_contact(contact_id):
    repo = ContactsRepository(db)    
    row = repo.get_contact(contact_id)
    return render_template ('edit_contact.html', row=row)

@app.route('/contacts/update_contact/<contact_id>', methods = ['POST'])
def update_contact(contact_id):
    new_contact_data = contact_from_form(request.form)
    repo = ContactsRepository(db)
    repo.update_contact(contact_id, new_contact_data)    
    return redirect(url_for('contacts'))
    
@app.route('/contacts/add_contact')
def add_contact():
    return render_template ('add_contact.html')


@app.route('/contacts/insert_contact', methods = ['POST'])
def insert_contact():
    contact = contact_from_form(request.form)
    repo = ContactsRepository(db)
    repo.insert_contact(contact)    
    return redirect(url_for('contacts'))
    
@app.route('/contacts/delete_contact/<contact_id>')
def delete_contact(contact_id):
    repo = ContactsRepository(db)
    repo.delete_contact(contact_id)
    return redirect(url_for('contacts'))
    
@app.route('/birthdays')
def birthdays():
    current_date = datetime.date.today()
    repo = ContactsRepository(db)
    birthdays_today = repo.birthdays_today()
    birthdays_next_week = repo.birthdays_next_week()
    return render_template ('birthdays.html', current_date = current_date, birthdays_today = birthdays_today, birthdays_next_week = birthdays_next_week)
    
@app.route('/namedays')
def namedays():
    current_date = datetime.date.today()
    repo = ContactsRepository(db)
    saints_today = repo.saints_today(current_date)
    namedays_today = repo.namedays_today(current_date)
    namedays_next_month = repo.namedays_next_month()
    saints_next_month = repo.saints_next_month()
    return render_template ('namedays.html', current_date = current_date, 
                                             today_saint = saints_today, 
                                             namedays_today = namedays_today,
                                             namedays_next_month = namedays_next_month, 
                                             saints_next_month = saints_next_month)
    
if __name__ == '__main__':
    app.run(debug = True)

