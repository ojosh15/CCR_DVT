from CAT import db 

class Component(db.Document):
    model = db.StringField(max_length=50)
    comp_type = db.StringField(max_length=50)
    manufacturer = db.StringField(max_length=50)
    active = db.BooleanField(default=False,null=False)
    source = db.StringField(max_length=50)