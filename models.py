import datetime

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
