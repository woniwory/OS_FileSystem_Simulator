import uuid
from datetime import datetime

class File:
    def __init__(self, name, location, size):
        self.name = str(name)
        self.location = location
        self.size = size
        self.identifier = str(uuid.uuid4())
        self.timestamps = {
            'created': datetime.now(),
            'modified': datetime.now(),
            'last_accessed': datetime.now()
        }

    def __str__(self):
        return (f"File(Name: {self.name}, Location: {self.location}, "
                f"Size: {self.size}, Timestamps: {self.timestamps})")
