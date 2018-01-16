from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
app = Flask(__name__)

# db connection is open
db = sqlite3.connect('address_book.db') 
 
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/contacts')
def contacts():
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM contacts ORDER BY BIRTHDAY''')
    # fetchall returns an array of arrays
    all_rows = cursor.fetchall()
    return render_template ('contacts.html', all_rows=all_rows)
    
@app.route('/contacts/edit_contact/<contact_id>')
def edit_contact(contact_id):
    cursor = db.cursor()
    # retrives the info of the contact in the edit_contact form
    cursor.execute("SELECT * FROM contacts WHERE ID = " + contact_id)
    # fetchone returns an array representing the fields of the first row
    row = cursor.fetchone()
    return render_template ('edit_contact.html', row=row)

@app.route('/contacts/update_contact/<contact_id>', methods = ['POST'])
def update_contact(contact_id):
    first_name = request.form['FIRST_NAME']
    middle_name = request.form['MIDDLE_NAME']
    last_name = request.form['LAST_NAME']
    birthday = request.form['BIRTHDAY']
    cursor = db.cursor()
    sql = ("UPDATE contacts SET FIRST_NAME='" + first_name + "'" +
        ", MIDDLE_NAME ='" + middle_name + "'" +
        ", LAST_NAME ='" + last_name + "'"+
        ", BIRTHDAY ='" + birthday + "'" +
        " WHERE ID = '" + contact_id + "'")
    #print sql
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('contacts'))
    
@app.route('/contacts/add_contact')
def add_contact():
    return render_template ('add_contact.html')
    
@app.route('/contacts/insert_contact', methods = ['POST'])
def insert_contact():
    first_name = request.form['FIRST_NAME']
    middle_name = request.form['MIDDLE_NAME']
    last_name = request.form['LAST_NAME']
    birthday = request.form['BIRTHDAY']
    cursor = db.cursor()
    sql = ("INSERT INTO contacts(FIRST_NAME, MIDDLE_NAME, LAST_NAME, BIRTHDAY) " +
        "VALUES ('" + first_name + "', " +
        "'" + middle_name + "', " +
        "'" + last_name + "', "+
        "'" + birthday + "')" )
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('contacts'))
    
@app.route('/contacts/delete_contact/<id_contact>')
def delete_contact(id_contact):
    cursor = db.cursor()
    sql = ("DELETE FROM contacts WHERE ID =" + id_contact)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('contacts'))
    
@app.route('/birthdays')
def birthdays():
    current_date = datetime.date.today()
    cursor = db.cursor()
    sql = ("SELECT * FROM contacts WHERE strftime('%m %d', BIRTHDAY) = strftime('%m %d', 'now')")
    cursor.execute(sql)
    birthdays_today = cursor.fetchall()
    cursor2 = db.cursor()
    sql2 = ("SELECT * FROM contacts WHERE strftime('%m %d', BIRTHDAY) > strftime('%m %d', 'now') AND strftime('%m %d', BIRTHDAY) <= strftime('%m %d', 'now', '+7 days')")
    cursor2.execute(sql2)
    birthdays_next_week = cursor2.fetchall()
    return render_template ('birthdays.html', current_date = current_date, birthdays_today = birthdays_today, birthdays_next_week = birthdays_next_week)
    
@app.route('/namedays')
def namedays():
    current_date = datetime.date.today()
    current_month = current_date.month
    current_day = current_date.day
    next_month = current_date + datetime.timedelta(days=30)
    cursor = db.cursor()
    sql = ("SELECT HOLIDAY_NAME FROM saints WHERE DAY =" + str(current_day) + " AND MONTH = " + str(current_month))
    cursor.execute(sql)
    today_saint = cursor.fetchall()
    cursor2 = db.cursor()
    sql2 = ("SELECT contacts.ID, contacts.FIRST_NAME, contacts.MIDDLE_NAME, contacts.LAST_NAME FROM saints" +
    " INNER JOIN nameday ON saints.ID = nameday.SAINT_ID" +
    " INNER JOIN contacts ON (nameday.NAME = contacts.FIRST_NAME OR nameday.NAME = contacts.MIDDLE_NAME)" +
    "WHERE saints.DAY =" + str(current_day) + " AND saints.MONTH = " + str(current_month))
    cursor2.execute(sql2)
    namedays_today = cursor2.fetchall()
    cursor3 = db.cursor()
    saint_date_fragment = "date(" + str(current_date.year) + " || '-' || substr('0'||saints.month,-2) || '-' || substr('0'||saints.day,-2))" 
    sql3 = ("SELECT contacts.ID, contacts.FIRST_NAME, contacts.MIDDLE_NAME, contacts.LAST_NAME FROM saints" +
    " INNER JOIN nameday ON saints.ID = nameday.SAINT_ID" +
    " INNER JOIN contacts ON (nameday.NAME = contacts.FIRST_NAME OR nameday.NAME = contacts.MIDDLE_NAME)" +
    " WHERE " + saint_date_fragment + " > date('now') " +
    " AND " + saint_date_fragment + " <= date('now', '+30 days')")
    cursor3.execute(sql3)
    namedays_next_month = cursor3.fetchall()
    cursor4 = db.cursor()
    sql4 = ("SELECT saints.HOLIDAY_NAME FROM saints WHERE " + saint_date_fragment + " > date('now') " +
    " AND " + saint_date_fragment + " <= date('now', '+30 days')")
    cursor4.execute(sql4)
    rows4 = cursor4.fetchall()
    saints_next_month = [row[0] for row in rows4]
    return render_template ('namedays.html', current_date = current_date, 
                                             today_saint = today_saint, 
                                             namedays_today = namedays_today,
                                             namedays_next_month = namedays_next_month, 
                                             saints_next_month = saints_next_month)
    
if __name__ == '__main__':
    app.run(debug = True)

