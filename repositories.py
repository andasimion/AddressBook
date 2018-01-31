#import sqlite3
import datetime
from models import contact_from_row, saint_from_row

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
        self.db.commit()
        
    def update_contact(self, contact_id, new_contact_data):
        cursor = self.db.cursor()
        sql = ("UPDATE contacts SET FIRST_NAME='" + new_contact_data.first_name + "'" +
            ", MIDDLE_NAME ='" + new_contact_data.middle_name + "'" +
            ", LAST_NAME ='" + new_contact_data.last_name + "'"+
            ", BIRTHDAY ='" + new_contact_data.birthday + "'" +
            " WHERE ID = '" + contact_id + "'")
        #print sql
        cursor.execute(sql)
        self.db.commit()
    
    def delete_contact(self, contact_id):
        cursor = self.db.cursor()
        sql = ("DELETE FROM contacts WHERE ID =" + contact_id)
        cursor.execute(sql)
        self.db.commit()

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

        

