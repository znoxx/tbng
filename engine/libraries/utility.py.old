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
import threading
import re

class Validator(object):

    def __init__(self, input_string):
          self.data=input_string

    def all(self, list_of_regexp,reflags=re.MULTILINE|re.UNICODE):
        result=True
        error_message=""
        if not isinstance(list_of_regexp,list):
            raise Exception("Input data of .all is not a list")
        for val in list_of_regexp:
            res=re.search(val,self.data,reflags)
            if res is not None:
               result=(result and True)
            else:
               result=(result and False)
               error_message= error_message+"NOT FOUND: "+val
        if result == False:
           raise Exception("No match found .all() -- "+ error_message)

    def any(self, list_of_regexp,reflags=re.MULTILINE|re.UNICODE):
        result=False
        error_message=""
        if not isinstance(list_of_regexp,list):
            raise Exception("Input data of .all is not a list")
        for val in list_of_regexp:
            error_message=error_message + " " + val
            res=re.search(val,self.data,reflags)
            if res is not None:
               result=(result or True)
            else:
               result=(result or False)
        if result == False:
           raise Exception("No match found .any(), tested with: "+error_message)

class ExecResult(object):

    def __init__(self, run_result):
        self.out=run_result.stdout
        self.ret=run_result.returncode
        self.args=run_result.args
        print("OUTPUT_COMBINED: "+self.out)
        print("ARGUMENTS: "+ self.args)
        print("RETURN CODE: " +str(self.ret))
      
    def expect_error(self):
        if self.ret == 0:
                raise Exception("Process finished with zero exit code!")
        return Validator(self.out)

    def expect_ok(self, Substring=None):
        if self.ret != 0:
                raise Exception("Process finished with nonzero exit code!")
        return Validator(self.out)
    
    def get_output(self):
        return self.out

    def get_retcode(self):
        return self.ret
    
    def get_args(self):
        return self.args


class BGExecutor(object):

    def __init__(self, command_line):
        self.out=""
        self.args=command_line
        self.subproc=None
        self.exec_thread=None

    def __del__(self):
        if self.subproc is not None:
            print("In destructor of BGExecutor - waiting for process to finish...")
            self.subproc.wait()
        if self.exec_thread is not None:
            print("In destructor of BGExecutor - waiting for thread to finish...")
            self.exec_thread.join()
    
    def plain_output(self):
        return self.out

    def output(self):
        return Validator(self.out)

    def wait(self):
        if self.subproc is not None:
            self.subproc.wait()
        if self.exec_thread is not None:
            self.exec_thread.join()

    def kill(self):
        if self.subproc is not None:
            print ("Killing process...")
            self.subproc.kill()
        if self.exec_thread is not None:
            self.exec_thread.join()
        else:
            raise Exception("No internal thread found, that's odd!")  

    def is_alive(self):
       if self.exec_thread is not None:
           if self.subproc.poll() is not None:
              return False
           else:
              return True
       
       else:
           raise Exception("Process is not even started!!") 

    def retcode(self):
         if self.exec_thread is not None:
             return self.subproc.poll()
         else:
             raise Exception("Process was not started")            

    def execute_bg(self):
        if self.exec_thread is None: 
            self.exec_thread=threading.Thread(target=self.__execute_thread,daemon=True)
            self.exec_thread.start()
        else:
             raise Exception("This instance is already in use, please create a new one")
        
    def __execute_thread(self):
        self.subproc=subprocess.Popen(self.args,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
        print("Execution of "+self.args + " started")
        while self.subproc.poll() is None:  
            nextline = self.subproc.stdout.readline()
            if nextline !='':
                self.out=self.out+nextline
                 
             
             

def execute(command_line):
    """
    Function executes given command line, returns ExecResult instance. 
    """
    print("Running command: "+command_line)
    return ExecResult(subprocess.run(command_line, shell=True, check=False, universal_newlines=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT))


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
    Rises an exception, in case exit code is non-zero 
    Input: Command line to execute
    """
    subprocess.run(command_line, shell=True, check=True)


def silently_install_by_yum(package_name):
    """
    Installs package with yum assuming -yes- on all questions (yum install -y)
    Raises an exception on non-zero exit code
    Input: yum package name
    """
    run_shell_command("yum -y install "+package_name)

def silently_install_by_apt(package_name):
    """
    Installs package with yum assuming -yes- on all questions (apt-get y install)
    Raises an exception on non-zero exit code
    Input: apt package name
    """
    run_shell_command("apt-get -y install "+package_name)


def install_from_rpm(rpm_path,additional_options):
    """
    Installs package with rpm command using -ivh options and some extra options, if needed
    Raises an exception on non-zero exit code
    Input: rpm file path, additional optons
    """
    run_shell_command("rpm -ivh "+additional_options+" "+rpm_path)

def install_from_deb(deb_path,additional_options):
    """
    Installs package with dpkg command using -i options and some extra options, if needed
    Raises an exception on non-zero exit code
    Input: apt file path, additional optons
    """
    run_shell_command("dpkg -i "+additional_options+" "+deb_path)
    

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


