"""
This module contains some very easy wrappers for commonly used functions.
Usage: 
import utility
After this one can call related functions in form - utility.function_call(...)
Requires Python 3.x
"""

import os
import errno
import subprocess
import fileinput
import hashlib
import re
                         

def make_sure_path_exists(path):
    """
    Checks directory existance, creates if nescessary. Raises an exception, if something went wrong.
    Input: folder name, nested one is possible - e.g. /hello/world. 
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def run_shell_command(command_line):
    """
    Runs shell command, e.g shell script.
    Rises an exception, in case exit code is non-zero.
    Input: Command line to execute
    Output: Combined stdout and stderror
    """
    return subprocess.check_output(command_line, stderr=subprocess.STDOUT,shell=True)

def run_multi_shell_command(command_line):
    """
    Runs multi shell command. Lines are extended with
    Rises an exception, in case exit code is non-zero.
    Input: Multiline command line to execute
    Output: Combined stdout and stderror
    """
    prefix = """set -e errexit
                set -o pipefail
             """
 
    return subprocess.check_output(prefix+command_line, stderr=subprocess.STDOUT,shell=True)


def silently_install_by_yum(package_name):
    """
    Installs package with yum assuming -yes- on all questions (yum install -y)
    Raises an exception on non-zero exit code
    Input: yum package name
    Output: Combined stdout and stderror
    """
    return run_shell_command("yum -y install "+package_name)

def silently_install_by_apt(package_name):
    """
    Installs package with yum assuming -yes- on all questions (apt-get y install)
    Raises an exception on non-zero exit code
    Input: apt package name
    Output: Combined stdout and stderror
    """
    return run_shell_command("apt-get -y install "+package_name)


def install_from_rpm(rpm_path,additional_options):
    """
    Installs package with rpm command using -ivh options and some extra options, if needed
    Raises an exception on non-zero exit code
    Input: rpm file path, additional optons
    Output: Combined stdout and stderror
    """
    return run_shell_command("rpm -ivh "+additional_options+" "+rpm_path)

def install_from_deb(deb_path,additional_options):
    """
    Installs package with dpkg command using -i options and some extra options, if needed
    Raises an exception on non-zero exit code
    Input: apt file path, additional optons
    Output: Combined stdout and stderror
    """
    return run_shell_command("dpkg -i "+additional_options+" "+deb_path)
    

def append_file_to_file(file_to_append,append_data):
     """
     Append text file to text file. Useful for extending some config files. For example, you extend /etc/config with tmp/config.addon
     Raises exception if something went wrong.
     Input: Original file, file to append.
     """
     f2append = open(file_to_append, 'a')
     f2read = open(append_data, 'r')
     data = f2read.read()
     data = "\n"+data
     f2read.close()
     f2append.write(data)
     f2append.close()


def replace_string_in_file(file_to_replace,initial_string,replacement_string):
    """
    Replaces pattern in file
    Raises exception if something went wrong.
    Input: Original file, initial pattern, string to replace
    """
    with fileinput.FileInput(file_to_replace, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(initial_string, replacement_string), end='')
    

def sha1OfFile(filepath):
    """
    Calculates sha1 checksum for file
    Raises exception if something went wrong.
    Input: filepath
    """
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            sha.update(block)
        return sha.hexdigest()

def run_piped(pipe_from,pipe_to):
    """
    Run processes in a pipe.
    Raises exception if something went wrong.
    Input: command from pipe, command to pipe
    Output: stdout,stderror tulip
    """
    run_from = subprocess.Popen([pipe_from],stdout=subprocess.PIPE)
    run_to = subprocess.Popen([pipe_to],stdin=run_from.stdout,stdout=subprocess.PIPE)
    return run_to.communicate()


