class User:
    def __init__(self, name, group):
        self.name = name
        self.group = group

    def __str__(self):
        return f"User(Name: {self.name}, Group: {self.group})"

