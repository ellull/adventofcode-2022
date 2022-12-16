#!/usr/bin/env python3
from __future__ import annotations
import fileinput
import re
from typing import Callable, List

TOTAL_DISK_SPACE = 70000000
UPDATE_SIZE = 30000000

class File(object):
    def __init__(self, name: str, size: int, directory: Directory) -> None:
        self.name = name
        self.size = size
        self.directory = directory

class Directory(object):
    def __init__(self, name: str, parent: Directory = None) -> None:
        self.name = name
        self.parent = parent
        self._directories = {}
        self._files = []

    def cd(self, directory_name: str) -> Directory:
        return self._directories[directory_name]

    def mkdir(self, directory_name: str) -> Directory:
        child = Directory(directory_name, self)
        self._directories[directory_name] = child
        return child

    def create_file(self, file_name: str, file_size: int) -> Directory:
        self._files.append(File(file_name, file_size, self))
        return self

    def find_directories(self, predicate: Callable[[Directory], bool]) -> List[Directory]:
        directories = []
        if predicate(self):
            directories.append(self)
        for directory in self._directories.values():
            directories.extend(directory.find_directories(predicate))
        return directories

    @property
    def size(self) -> int:
        return sum(directory.size for directory in self._directories.values()) \
            + sum(file.size for file in self._files)

class Parser(object):
    __cd_regex = re.compile('^\$ cd (?P<directory>\w+)')
    __file_regex = re.compile('^(?P<file_size>\d+) (?P<file_name>.+)')

    def __init__(self, root: Directory) -> None:
        self._root = root
        self._current = root
    
    def parse(self, input: str) -> None:
        # parse commands
        if input == '$ ls':
            return

        if input == '$ cd /':
            self._current = self._root
            return

        if input == '$ cd ..':
            self._current = self._current.parent
            return

        cd_match = self.__cd_regex.match(input)
        if cd_match:
            self._current = self._current.cd(cd_match['directory'])
            return

        # parse ls output
        if input.startswith('dir '):
            self._current.mkdir(input[4:])
            return

        file_match = self.__file_regex.match(input)
        if file_match:
            self._current.create_file(file_match['file_name'], int(file_match['file_size']))
            return


if __name__ == '__main__':

    # part 1
    test_root = Directory('/')
    test_parser = Parser(test_root)
    test_parser.parse('$ cd /')
    test_parser.parse('$ ls')
    test_parser.parse('dir a')
    test_parser.parse('14848514 b.txt')
    test_parser.parse('8504156 c.dat')
    test_parser.parse('dir d')
    test_parser.parse('$ cd a')
    test_parser.parse('$ ls')
    test_parser.parse('dir e')
    test_parser.parse('29116 f')
    test_parser.parse('2557 g')
    test_parser.parse('62596 h.lst')
    test_parser.parse('$ cd e')
    test_parser.parse('$ ls')
    test_parser.parse('584 i')
    test_parser.parse('$ cd ..')
    test_parser.parse('$ cd ..')
    test_parser.parse('$ cd d')
    test_parser.parse('$ ls')
    test_parser.parse('4060174 j')
    test_parser.parse('8033020 d.log')
    test_parser.parse('5626152 d.ext')
    test_parser.parse('7214296 k')
    assert sum(directory.size for directory in test_root.find_directories(lambda d: d.size <= 100000)) == 95437

    root = Directory('/')
    parser = Parser(root)
    for line in fileinput.input():
        parser.parse(line.strip())
    sum_sizes = sum(directory.size for directory in root.find_directories(lambda d: d.size <= 100000))
    print(f"Sum total sizes directories at most 100000: {sum_sizes}")
    
    # part 2
    test_minimum_size = UPDATE_SIZE - (TOTAL_DISK_SPACE - test_root.size)
    test_directory_to_delete = min(test_root.find_directories(lambda d: d.size >= test_minimum_size), key=lambda d: d.size)
    assert test_directory_to_delete.name == 'd'
    assert test_directory_to_delete.size == 24933642

    minimum_size = UPDATE_SIZE - (TOTAL_DISK_SPACE - root.size)
    directory_to_delete = min(root.find_directories(lambda d: d.size >= minimum_size), key=lambda d: d.size)
    print(f"Directory to delete size: {directory_to_delete.size}")
