from datetime import datetime


class File:
    def __init__(self, name, identifier, file_type, location, size, protection):
        self.name = str(name)
        self.identifier = identifier # 이름으로 할 것이 아니라 identifier
        self.file_type = file_type # .을 기준으로 오른쪽 글자를 저장
        self.location = location
        self.size = size
        self.protection = protection # 권한 수정 필요
        self.timestamps = {
            'created': datetime.now(),
            'modified': datetime.now(),
            'last_accessed': datetime.now()
        }

    def __str__(self):
        return (f"File(Name: {self.name}, Identifier: {self.identifier}, Type: {self.file_type}, "
                f"Location: {self.location}, Size: {self.size}, Protection: {self.protection}, "
                f"Timestamps: {self.timestamps})")



