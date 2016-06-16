import os
import re


class GetDependancies:
    def __init__(self):
        self.top_level_path = os.getcwd()
        folder_list = self.get_folder_list()
        self.module_list = self.get_module_list(folder_list)

        self.python_default_packages=\
            [
                'site', 'and', 'or', 'not', 'int', 'float', 'long', 'complex', 'str', 'unicode', 'list', 'tuple', 'bytearray',
                'buffer', 'xrange', 'set', 'frozenset', 'dict', 'string', 're', 'struct', 'difflib', 'StringIO', 'cStringIO',
                'StringIO', 'textwrap', 'codecs', 'unicodedata', 'stringprep', 'fpformat', 'datetime', 'calendar', 'collections',
                'heapq', 'bisect', 'array', 'sets', 'sched', 'mutex', 'queue', 'weakref', 'UserDict', 'UserList', 'UserString',
                'types', 'new', 'copy', 'pprint', 'repr', 'repr()', 'numbers', 'math', 'cmath', 'decimal', 'fractions', 'random',
                'itertools', 'functools', 'operator', 'os.path', 'fileinput', 'stat', 'stat()', 'statvfs', 'os.statvfs()', 'filecmp',
                'tempfile', 'glob', 'fnmatch', 'linecache', 'shutil', 'dircache', 'macpath', 'pickle', 'cPickle', 'pickle', 'copy_reg',
                'pickle', 'shelve', 'marshal', 'anydbm', 'whichdb', 'dbm', 'gdbm', 'dbhash', 'bsddb', 'dumbdbm', 'sqlite3', 'zlib',
                'gzip', 'bz2', 'zipfile', 'tarfile', 'csv', 'ConfigParser', 'robotparser', 'netrc', 'xdrlib', 'plistlib', '.plist',
                'hashlib', 'hmac', 'md5', 'sha', 'os', 'io', 'time', 'argparse', 'optparse', 'getopt', 'logging', 'logging.config',
                'logging.handlers', 'getpass', 'curses', 'curses.textpad', 'curses.wrapper', 'curses.ascii', 'curses.panel', 'platform',
                'errno', 'ctypes', 'select', 'threading', 'thread', 'dummy_threading', 'threading', 'dummy_thread', 'thread', 'multiprocessing',
                'mmap', 'readline', 'rlcompleter', 'subprocess', 'socket', 'ssl', 'signal', 'popen2', 'asyncore', 'asynchat', 'email',
                'json', 'mailcap', 'mailbox', 'mhlib', 'mimetools', 'mimetypes', 'MimeWriter', 'mimify', 'multifile', 'rfc822',
                'base64', 'binhex', 'binascii', 'quopri', 'uu', 'HTMLParser', 'sgmllib', 'htmllib', 'htmlentitydefs', 'xml.parsers.expat',
                'xml.dom', 'xml.dom.minidom', 'xml.dom.pulldom', 'xml.sax', 'xml.sax.handler', 'xml.sax.saxutils', 'xml.sax.xmlreader',
                'xml.etree.ElementTree', 'webbrowser', 'cgi', 'cgitb', 'wsgiref', 'urllib', 'urllib2', 'httplib', 'ftplib', 'poplib',
                'imaplib', 'nntplib', 'smtplib', 'smtpd', 'telnetlib', 'uuid', 'urlparse', 'SocketServer', 'BaseHTTPServer', 'SimpleHTTPServer',
                'CGIHTTPServer', 'cookielib', 'Cookie', 'xmlrpclib', 'SimpleXMLRPCServer', 'DocXMLRPCServer', 'audioop', 'imageop',
                'aifc', 'sunau', 'wave', 'chunk', 'colorsys', 'imghdr', 'sndhdr', 'ossaudiodev', 'gettext', 'locale', 'cmd', 'shlex',
                'Tkinter', 'ttk', 'Tix', 'ScrolledText', 'turtle', 'pydoc', 'doctest', 'unittest', 'test', 'test.test_support', 'bdb',
                'pdb', 'hotshot', 'timeit', 'trace', 'sys', 'sysconfig', '__builtin__', 'future_builtins', '__main__', 'warnings',
                'contextlib', 'with', 'abc', 'atexit', 'traceback', '__future__', 'gc', 'inspect', 'site', 'user', 'fpectl', 'distutils',
                'code', 'codeop', 'rexec', 'Bastion', 'imp', 'import', 'importlib', '__import__()', 'imputil', 'zipimport', 'pkgutil',
                'modulefinder', 'runpy', 'parser', 'symtable', 'symbol', 'token', 'keyword', 'tokenize', 'tabnanny', 'pyclbr', 'py_compile',
                'compileall', 'dis', 'pickletools', 'formatter', 'msilib', 'msvcrt', '_winreg', 'winsound', 'posix', 'pwd', 'spwd',
                'grp', 'crypt', 'dl', 'termios', 'tty', 'pty', 'fcntl', 'fcntl()', 'ioctl()', 'pipes', 'posixfile', 'resource',
                'nis', 'syslog', 'commands', 'ic', 'MacOS', 'macostools', 'findertools', 'EasyDialogs', 'FrameWork', 'autoGIL','__init__',
                'ColorPicker', 'gensuitemodule', 'aetools', 'aepack', 'aetypes', 'MiniAEFrame', 'al', 'AL', 'al', 'cd', 'fl', 'FL',
                'fl', 'flp', 'fm', 'gl', 'DEVICE', 'gl', 'GL', 'gl', 'imgfile', 'jpeg', 'sunaudiodev', 'SUNAUDIODEV', 'sunaudiodev']

    def get_python_files_from_dir(self, directory):
        """
        Given a path, return all python files included in the path
        :param directory:
        :return:
        """
        containers = os.listdir(directory)
        python_files = []
        for containor in containers:
            if ".py" in containor and "get_dependancies" not in containor:
                python_files.append(containor)
        return python_files

    def get_imports_from_file(self, python_file_path):
        f = open(python_file_path)
        imports = []
        for line in f:
            if 'import' in line:
                try:
                    imports.append(re.search('((?<=from )|(?<=import ))(.*?)(\w+)', line).group(0))
                except AttributeError:
                    pass
        return imports

    def check_if_import_not_default(self, package_name):
        package_name = package_name.replace('import', '').replace('from', '').replace(' ', '').strip()
        for default_package in self.python_default_packages:
            if default_package == package_name:
                return False
        return True

    def get_packages_non_default_imports(self, package_list):
        """
        Gets a list of non default packages
        :param package_list:
        :return:
        """
        package_list_no_default = []
        for package in package_list:
            if self.check_if_import_not_default(package):
                package_list_no_default.append(package)
        return package_list_no_default

    def check_if_import_not_module(self, package_name, modules):
        package_name = package_name.replace('import', '').replace('from', '').replace(' ', '').strip()
        for module in modules:
            if module in package_name:
                return False
        return True

    def get_packages_non_module_imports(self, package_list, modules):
        package_list_no_modules = []
        for package in package_list:
            if self.check_if_import_not_module(package, modules):
                package_list_no_modules.append(package)
        return package_list_no_modules

    def check_folder_if_module(self, folder_path):
        folder_files = os.listdir(folder_path)
        if "__init__.py" not in folder_files:
            return False
        else:
            return True

    def get_folder_list(self):
        containers = os.listdir(self.top_level_path)
        folder_list = []
        for container in containers:
            if '.' not in container:
                folder_list.append(container)

        return folder_list

    def get_module_list(self, folder_list):
        module_list = []
        for folder in folder_list:
            folder_path = os.path.join(self.top_level_path, folder)
            if self.check_folder_if_module(folder_path):
                module_list.append(folder)
        return module_list

    def get_non_module_non_default_imports_from_file(self, file_path, module_files):
        imports_list = self.get_imports_from_file(file_path)
        imports_list = list(set(imports_list))
        imports_list = self.get_packages_non_default_imports(imports_list)
        module_list_and_file = self.module_list
        module_list_and_file.extend(module_files)
        imports_list = self.get_packages_non_module_imports(imports_list, module_list_and_file)
        return imports_list

    def get_non_module_non_default_imports_from_path(self, folder_path):
        imports_list = []
        module_files = self.get_module_files(folder_path)

        python_files = self.get_python_files_from_dir(folder_path)
        for python_file in python_files:
            python_path = os.path.join(folder_path, python_file)
            imports_list.extend(self.get_non_module_non_default_imports_from_file(python_path, module_files))
        return imports_list

    def get_module_files(self, module_path):
        module_files = []
        containers = os.listdir(module_path)
        for container in containers:
            if '.py' == container[-3:]:
                module_files.append(container[:-3])
        return module_files

    def write_output_to_file(self, dependency_list):
        f = open('dependency_list.txt', 'w+')
        for dependency in dependency_list:
            f.write(dependency+'\n')
        return True

    def run(self):
        dependency_list = []
        folder_list = self.get_folder_list()
        modules = self.get_module_list(folder_list)
        for module in modules:
            module_path = os.path.join(self.top_level_path, module)
            import_list = self.get_non_module_non_default_imports_from_path(module_path)
            dependency_list.extend(import_list)
        import_list = self.get_non_module_non_default_imports_from_path(self.top_level_path)
        dependency_list.extend(import_list)
        dependency_list = list(set(dependency_list))
        self.write_output_to_file(dependency_list)
        print "Check completed! Check dependency_list.txt for errors!"


checker = GetDependancies()
checker.run()




