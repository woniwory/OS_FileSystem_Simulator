import os
from datetime import datetime

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.path = os.getcwd()
        self.created = datetime.now()
        self.modified = datetime.now()
        self.last_accessed = datetime.now()
        self.subdirectories = {}
        self.files = []
        self.parent = parent
        print(f'{self.name} created at {self.created}')


    def get_directory(self):
        return self.name

    def get_subdirectory(self):
        return self.subdirectories # print해주는 filesystem.py에 추가할 것

    def access_subdirectory(self):
        return self.subdirectories

    def get_file(self, name):
        return self.files.get(name)

    def access_file(self, name):
        return self.files.get(name)

    def __str__(self):
        subdirs = ', '.join(self.subdirectories.keys())
        files = ', '.join(self.files.keys())
        return (f"Directory(Name: {self.name}, Path: {self.path}, Subdirectories: [{subdirs}], Files: [{files}])")


