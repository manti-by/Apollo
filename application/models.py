from app import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    term_01 = db.Column(db.Float, default = 0.0)
    term_02 = db.Column(db.Float, default = 0.0)
    term_03 = db.Column(db.Float, default = 0.0)
    term_04 = db.Column(db.Float, default = 0.0)
    term_05 = db.Column(db.Float, default = 0.0)
    
    water_sensor = db.Column(db.SmallInteger, default = 0)
    
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Record #%d>' % (self.id)
