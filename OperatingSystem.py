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
            print(f"\033[31mFile {name} already exists.\033[0m")
            return
        new_file = File(name, self.getCurrent_directory(), '1024')
        with open(file_path, 'w') as f:
            f.write(content)
        self.current_directory.files[name] = new_file
        creation_time = new_file.timestamps['created']
        print(f"\033[34mFile '{name}' created with content: {content} at {creation_time}\033[0m")

    def search_file_recursive(self, directory, name, path=""):
        if name in directory.files:
            print(f"\033[34mFile {name} found at: {path}/{directory.name}/{name}\033[0m")
            return True
        for subdir_name, subdir in directory.subdirectories.items():
            if self.search_file_recursive(subdir, name, f"{path}/{directory.name}"):
                return True
        return False

    def search_file(self, name):
        if not self.search_file_recursive(self.root, name):
            print(f"\033[31mFile {name} not found in the filesystem.\033[0m")

    def read_file(self, name):
        if name in self.current_directory.files:
            file_path = os.path.join(os.getcwd(), name)
            with open(file_path, 'r') as f:
                content = f.read()
            self.current_directory.files[name].accessed = datetime.now()
            print(f"\033[34mContent of file {name}:\033[0m")
            print(content)
        else:
            print(f"\033[31mFile {name} not found in current directory.\033[0m")

    def delete_file(self, name):
        if name in self.current_directory.files:
            file_path = os.path.join(os.getcwd(), name)
            os.remove(file_path)
            del self.current_directory.files[name]
            print(f"\033[34mFile '{name}' deleted.\033[0m")
        else:
            print(f"\033[31mFile {name} not found in current directory.\033[0m")

    def write_file(self, name, additional_content):
        if name in self.current_directory.files:
            file_path = os.path.join(os.getcwd(), name)
            with open(file_path, 'a') as f:
                f.write(additional_content)
            self.current_directory.files[name].modified = datetime.now()
            print(f"\033[34mAdditional content written to file {name}: {additional_content} at "
                  f"{self.current_directory.files[name].modified}\033[0m")
        else:
            print(f"\033[31mFile {name} not found in current directory.\033[0m ")

    def move_subdirectory(self, directory):
        self.setCurrent_directory(directory)
        os.chdir(directory.name)
        # print(f'\033[34m{os.getcwd()}\033[0m')

    def move_parent_directory(self):
        if self.current_directory.parent:
            parent_directory = self.current_directory.parent
            self.current_directory = parent_directory
            os.chdir('..')
            print(f"\033[34mMoved to parent directory: {os.getcwd()}\033[0m")
        else:
            print("\033[31mYou are in parent directory.\033[0m")

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
            print(f"\033[31mDirectory already exists.\033[0m")
        else:
            print(f"\033[34m/{new_directory.name} created\033[0m")
            self.getCurrent_directory().subdirectories[new_directory.name] = new_directory
            # print(self.getCurrent_directory().subdirectories)
            new_directory.modified = datetime.now()

    def remove_subdirectory(self, name):
        if name in self.current_directory.subdirectories:
            subdirectory = self.current_directory.subdirectories[name]
            os.rmdir(subdirectory.name)
            del self.current_directory.subdirectories[name]
            print(f"\033[34mDirectory '{name}' removed.\033[0m")
        else:
            print(f"\033[31mDirectory {name} not found in current directory.\033[0m")

    def print_file(self):
        sorted_keys = sorted(self.getCurrent_directory().subdirectories)
        print("\033[34mDirectories:\033[0m", sorted_keys)
        sorted_keys = sorted(self.getCurrent_directory().files)
        print("\033[34mFiles:\033[0m", sorted_keys)
        # print(os.listdir())

class OperatingSystem:
    def __init__(self):
        self.filesystem = Filesystem()
        self.filesystem.move_subdirectory(self.filesystem.root)


    def main(self):
        while True:
            command = input("Enter command: ").strip()
            if command.startswith('mkdir '):
                dir_name = command.split(' ', 1)[1]
                self.filesystem.add_subdirectory(dir_name)
            elif command.startswith('rmdir '):
                dir_name = command.split(' ', 1)[1]
                self.filesystem.remove_subdirectory(dir_name)
            elif command == 'pwd':
                print(f"current_directory = \033[34m{self.filesystem.getCurrent_directory().name}\033[0m")
                print(f"\033[34m{os.getcwd()}\033[0m")
            elif command == 'ls':
                self.filesystem.print_file()
            elif command.startswith('cd '):
                parts = command.split(' ', 1)
                dir_name = parts[1]
                if dir_name == '../':
                    self.filesystem.move_parent_directory()
                else:
                    if dir_name not in self.filesystem.getCurrent_directory().subdirectories:
                        print(f"\033[31mDirectory {dir_name} not found.\033[0m")
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
            elif command.startswith('rm '):
                parts = command.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: delete <filename>")
                else:
                    filename = parts[1]
                    self.filesystem.delete_file(filename)
            elif command.startswith('write '):
                parts = command.split(' ', 2)
                if len(parts) < 3:
                    print("Usage: write <filename> <additional_content>")
                else:
                    filename = parts[1]
                    additional_content = parts[2]
                    self.filesystem.write_file(filename, additional_content)
            elif command.startswith('search '):
                parts = command.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: search <filename>")
                else:
                    filename = parts[1]
                    self.filesystem.search_file(filename)
            elif command.startswith('cat '):
                parts = command.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: read <filename>")
                else:
                    filename = parts[1]
                    self.filesystem.read_file(filename)
            elif command == 'exit':
                break
            else:
                print("Invalid command")
