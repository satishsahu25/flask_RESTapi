from datetime import datetime,time,date
from sqlalchemy import DateTime
from geoalchemy2 import Geometry
from app import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    @property
    def time_ago(self):
        now = datetime.utcnow()
        d_datetime = datetime.combine(self.created_at,time(0,0))
        delta = now - d_datetime
        if delta.days == 0:
            if delta.seconds < 10:
                return "just now"
            elif delta.seconds < 60:
                return f"{delta.seconds} seconds ago"
            elif delta.seconds < 120:
                return "1 minute ago"
            elif delta.seconds < 3600:
                return f"{delta.seconds // 60} minutes ago"
            elif delta.seconds < 7200:
                return "1 hour ago"
            else:
                return f"{delta.seconds // 3600} hours ago"
        elif delta.days == 1:
            return "yesterday"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        elif delta.days < 31:
            return f"{delta.days // 7} weeks ago"
        elif delta.days < 365:
            return f"{delta.days // 30} months ago"
        else:
            return f"{delta.days // 365} years ago"

    def __init__(self,message,location):
        self.message = message
        self.location = location

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'location': str(self.location),
            'time': self.time_ago
        }
