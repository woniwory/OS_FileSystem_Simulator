import os
from datetime import datetime
from Directory import Directory
from File import File

class Filesystem:
    def __init__(self):
        self.root = Directory('root', '')
        self.current_directory = self.root
        os.makedirs('root', exist_ok=True)

    def create_file(self, name, content=""):
        file_path = os.path.join(os.getcwd(), name)
        if name in self.current_directory.files:
            raise ValueError(f"File {name} already exists.")
        new_file = File(name, 'abc13579', self.getCurrent_directory(), '1024', 'rwx')
        with open(file_path, 'w') as f:
            f.write(content)
        self.current_directory.files[name] = new_file
        print(f"File {name} created with content: {content}")


    def search_file_recursive(self, directory, name, path=""):
        if name in directory.files:
            print(f"File {name} found at: {path}/{directory.name}/{name}")
            return True
        for subdir_name, subdir in directory.subdirectories.items():
            if self.search_file_recursive(subdir, name, f"{path}/{directory.name}"):
                return True
        return False

    def search_file(self, name):
        if not self.search_file_recursive(self.root, name):
            print(f"File {name} not found in the filesystem.")

    def delete_file(self, name):
        if name in self.current_directory.files:
            file_path = os.path.join(os.getcwd(), name)
            os.remove(file_path)
            del self.current_directory.files[name]
            print(f"File {name} deleted.")
        else:
            print(f"File {name} not found in current directory.")

    def update_file(self, name, new_content):
        if name in self.current_directory.files:
            file_path = os.path.join(os.getcwd(), name)
            with open(file_path, 'w') as f:
                f.write(new_content)
            self.current_directory.files[name].modified = datetime.now()
            print(f"File {name} updated with new content: {new_content}")
        else:
            print(f"File {name} not found in current directory.")

    def move_subdirectory(self, directory):
        self.setCurrent_directory(directory)
        os.chdir(directory.name)
        print(os.getcwd())

    def move_parent_directory(self):
        if self.current_directory.parent:
            parent_directory = self.current_directory.parent
            self.current_directory = parent_directory
            os.chdir('..')
            print(f"Moved to {os.getcwd()} (parent directory)")
        else:
            print("No parent directory")

    def getCurrent_directory(self):
        return self.current_directory

    def setCurrent_directory(self, directory):
        print(f"current_directory = {directory.name}")
        self.current_directory = directory

    def add_subdirectory(self, name):
        new_directory = Directory(name, self.getCurrent_directory())
        os.makedirs(name, exist_ok=True)
        if new_directory.name in self.current_directory.subdirectories:
            del new_directory
            raise ValueError(f"Directory already exists.")
        else:
            print(f"/{new_directory.name} 생성")
            self.getCurrent_directory().subdirectories[new_directory.name] = new_directory
            print(self.getCurrent_directory().subdirectories)
            new_directory.modified = datetime.now()

    def print_file(self):
        sorted_keys = sorted(self.getCurrent_directory().subdirectories)
        print("디렉토리 :", sorted_keys)
        sorted_keys = sorted(self.getCurrent_directory().files)
        print("파일 :", sorted_keys)
        print(os.listdir())

class OperatingSystem:
    def __init__(self):
        self.filesystem = Filesystem()
        self.filesystem.move_subdirectory(self.filesystem.root)
        # self.filesystem.create_file("test_file", "hi")
        self.filesystem.search_file("test_file")

    def main(self):
        while True:
            command = input("Enter command: ").strip()
            if command.startswith('mkdir '):
                dir_name = command.split(' ', 1)[1]
                self.filesystem.add_subdirectory(dir_name)
            elif command == 'pwd':
                print(f"current_directory = {self.filesystem.getCurrent_directory().name}")
                print(os.getcwd())
            elif command == 'ls':
                self.filesystem.print_file()
            elif command.startswith('cd '):
                parts = command.split(' ', 1)
                if len(parts) == 1:  # No argument provided
                    self.filesystem.print_file()
                else:
                    dir_name = parts[1]
                    print(self.filesystem.getCurrent_directory)
                    print(os.getcwd())
                    print(self.filesystem.getCurrent_directory().subdirectories)
                    if dir_name not in self.filesystem.getCurrent_directory().subdirectories:
                        if self.filesystem.getCurrent_directory().parent and self.filesystem.getCurrent_directory().parent.name == dir_name:
                            self.filesystem.move_parent_directory()
                        else:
                            print(f"Directory {dir_name} not found")
                    else:
                        self.filesystem.move_subdirectory(
                            self.filesystem.getCurrent_directory().subdirectories[dir_name])
            elif command.startswith('create '):
                parts = command.split(' ', 2)
                if len(parts) < 2:
                    print("Usage: create <filename> [content]")
                else:
                    filename = parts[1]
                    content = parts[2] if len(parts) > 2 else ""
                    self.filesystem.create_file(filename, content)
            elif command.startswith('delete '):
                parts = command.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: delete <filename>")
                else:
                    filename = parts[1]
                    self.filesystem.delete_file(filename)
            elif command.startswith('update '):
                parts = command.split(' ', 2)
                if len(parts) < 3:
                    print("Usage: update <filename> <new_content>")
                else:
                    filename = parts[1]
                    new_content = parts[2]
                    self.filesystem.update_file(filename, new_content)
            elif command.startswith('search '):
                parts = command.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: search <filename>")
                else:
                    filename = parts[1]
                    self.filesystem.search_file(filename)
            elif command == 'exit':
                break
            else:
                print("Invalid command")

