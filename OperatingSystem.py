import os
import sys
from datetime import datetime
from Directory import Directory


class Filesystem:
    def __init__(self):

        self.root = Directory('root', '')
        self.current_directory = self.root
        os.makedirs('root', exist_ok=True)

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
        # 새로운 디렉토리의 경로 생성

        new_directory = Directory(name, self.getCurrent_directory())
        os.makedirs(name, exist_ok=True)


        if new_directory.name in self.current_directory.subdirectories:
            del new_directory
            raise ValueError(f"Directory already exists.")

        else:
            print(f"/{new_directory.name} 생성")
            self.getCurrent_directory().subdirectories[new_directory.name]=new_directory
            print(self.getCurrent_directory().subdirectories)


            new_directory.modified = datetime.now()


    def print_file(self):
        sorted_keys = sorted(self.getCurrent_directory().subdirectories)
        print(os.listdir())
        print(sorted_keys)




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


            elif command == 'exit':
                break
            else:
                print("Invalid command")