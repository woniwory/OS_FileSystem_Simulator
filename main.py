from Directory import Directory
from OperatingSystem import Filesystem
from File import File
from User import User
from datetime import datetime
import os
import shutil
from OperatingSystem import *

if __name__ == "__main__":
    operating_system = OperatingSystem()
    operating_system.main()
    shutil.rmtree('root')
    print("프로그램 종료")



     # Create the root Directory
    # filesystem = Filesystem()
    # filesystem.move_subdirectory(filesystem.root)  # cd
    # filesystem.print_file()
    #
    # print('=' * 50)
    # print()
    #
    # filesystem.add_subdirectory('home')
    # filesystem.print_file()
    #
    # filesystem.move_subdirectory(filesystem.getCurrent_directory().subdirectories['home'])
    # filesystem.add_subdirectory('abc')
    # filesystem.print_file()
    #
    # filesystem.move_parent_directory(filesystem.getCurrent_directory().parent)
    # filesystem.add_subdirectory('etc')
    #
    # filesystem.move_subdirectory(filesystem.getCurrent_directory().subdirectories['etc'])
