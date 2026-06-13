#-------------------------------------------------------------------------------
# PRINTCON
#
# Debug, Trace, Logging and Diagnostic Library for Python < 3.12
#
# Python Debugging https://docs.python.org/2/library/pdb.html
#
# https://packaging.python.org
# https://stackabuse.com/variable-length-arguments-in-python-with-args-and-kwargs
# https://www.w3schools.com/python/ref_keyword_assert.asp
#
# https://realpython.com/python-time-module/
#
#
# https://www.pythontutorial.net/python-oop/python-__repr__/
# object_name.eval(object_name.__repr__()) == object_name
# https://www.geeksforgeeks.org/python-os-getpid-method/
#
# TODO: debug and trace are still present and called in release, do we preprocess it out or do we stub it? Is there a way to do a noop? pass?
#
# https://www.pythoncheatsheet.org/blog/python-sets-what-why-how/
# timeit will time function calls
#
# https://docs.python.org/3/howto/logging.html
# https://stackoverflow.com/questions/16594984/optimizing-python-logging-code
#
# from dis import dis # for disassembly
#
# ANSI Escape
# https://replit.com/talk/learn/ANSI-Escape-Codes-in-Python/22803
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import time
# https://docs.python.org/3.8/library/imp.html
import imp          # Deprecated since version 3.4, removed in version 3.12.
import importlib
import hashlib
import ntpath
import random
import inspect
import functools
import pdb
import dis
import re
import chardet
#import icu
import traceback
import threading
from threading import Lock
from datetime import datetime
# TODO: make playaudiofile to wrap playsound with a parameter for blocking or non-blocking
from playsound import playsound
import pyttsx3
import logging
from logging.handlers import SMTPHandler
from logging.config import dictConfig
import itertools
# https://www.studytonight.com/python-howtos/how-to-print-colored-text-in-python
# https://dev.to/visheshdvivedi/get-colored-console-output-in-python-using-colorama-4gci
import colorama
from colorama import init, Fore, Back, Style
#-------------------------------------------------------------------------------
#
# global
#
# https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string

# https://www.w3schools.com/python/gloss_python_raise.asp
# raise Exception("Sorry, no numbers below zero")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
init()
#all=0xffffffff
FLAG_PRINT=1
FLAG_LOGGING=2
FLAG_DEBUG=3
FLAG_EVENTLOG=4
FLAG_FILE=5

printonly=False
tracelevel=-1
count=0
listindent='    '
dimslogger = FLAG_PRINT
logline=True
logfile=True
logfilepath=False
# TODO: need to look at end arg and if \n change to \n\n
treat_warnings_as_errors=False
# https://docs.python.org/2/library/pdb.html
break_on_error=False  # don't know if I can or should implement this
audible_error=True
pause_on_error=False
throw_on_exception=False
log_compare=False

lock=Lock()
#-------------------------------------------------------------------------------
#
# isfloat
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isfloat(s):
  for c in s:
    if not c.isnumeric():
      return False
    if not c == '.':
      return False
  if len(s) == 0:
    return False
  return True
#-------------------------------------------------------------------------------
#
# remove_duplicates
#
# https://www.w3schools.com/python/python_howto_remove_duplicates.asp
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def remove_duplicates(x):
  return list(dict.fromkeys(x))
#-------------------------------------------------------------------------------
#
# printsafe
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printsafe(*args, **kwargs):
  try:
    lock.acquire()
    print(' '.join(map(str, args)), **kwargs)
  finally:
    lock.release()
printsf = printsafe
#-------------------------------------------------------------------------------
#
# stack_size2a
#
# https://stackoverflow.com/questions/34115298/how-do-i-get-the-current-depth-of-the-python-interpreter-stack
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def stack_size2a(size=2):
  """Get stack size for caller's frame.
  """
  frame = sys._getframe(size)
  for size in itertools.count(size):
    frame = frame.f_back
    if not frame:
      return size
#-------------------------------------------------------------------------------
#
# stack_size3a
#
# https://stackoverflow.com/questions/34115298/how-do-i-get-the-current-depth-of-the-python-interpreter-stack
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def stack_size3a(size=2):
  """Get stack size for caller's frame.
  """
  frame = sys._getframe(size)
  try:
    for size in itertools.count(size, 8):
      frame = frame.f_back.f_back.f_back.f_back.\
        f_back.f_back.f_back.f_back
  except AttributeError:
    while frame:
      frame = frame.f_back
      size += 1
    return size - 1
#-------------------------------------------------------------------------------
#
# stack_size4b
#
# https://stackoverflow.com/questions/34115298/how-do-i-get-the-current-depth-of-the-python-interpreter-stack
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def stack_size4b(size_hint=8):
  """Get stack size for caller's frame.
  """
  get_frame = sys._getframe
  frame = None
  try:
    while True:
      frame = get_frame(size_hint)
      size_hint *= 2
  except ValueError:
    if frame:
      size_hint //= 2
    else:
      while not frame:
        size_hint = max(2, size_hint // 2)
        try:
          frame = get_frame(size_hint)
        except ValueError:
          continue

  for size in itertools.count(size_hint):
    frame = frame.f_back
    if not frame:
      return size
#-------------------------------------------------------------------------------
#
# get_attributes
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_attributes(widget):
  widg = widget
  keys = widg.keys()
  lock.acquire()
  for key in keys:
    print("Attribute: {:<20}".format(key), end=' ')
    value = widg[key]
    vtype = type(value)
    print('Type: {:<30} Value: {}'.format(str(vtype), value))
  lock.release()
#-------------------------------------------------------------------------------
#
# dump_tkframes
#
# TODO: trap print and trap trace, print once after reset
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dump_tkframes(frame):
  lock.acquire()
  print("frame:",type(frame))
  print("tkFrames:",type(frame.winfo_parent()))
  if frame.winfo_parent() is not None:
    print(frame.winfo_parent())
    dump_tkframes(frame.winfo_parent())
  lock.release()
#-------------------------------------------------------------------------------
#
# get_frame
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_frame(index=0):
  return inspect.stack()[index]
#-------------------------------------------------------------------------------
#
# get_frame_record
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_frame_record():
  return inspect.stack()
#-------------------------------------------------------------------------------
#
# get_stack_frame_info
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_stack_frame_info(backtrack=1):
  callerframerecord = inspect.stack()[backtrack]
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  return info
#-------------------------------------------------------------------------------
#
# difflist_return_all_diff
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://www.geeksforgeeks.org/python-difference-two-lists/
def difflist_return_all_diff(list1, list2): # combined differences
    return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))
#-------------------------------------------------------------------------------
#
# difflist_noset
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# this is very labor intensive is not hanging, don't use!
def difflist_noset(list1, list2):
    li_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return li_dif
#-------------------------------------------------------------------------------
#
# difflist_or
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://stackoverflow.com/questions/6486450/python-compute-list-difference
# ordered and redundant
def difflist_or(first, second): # fastest
    """ Returns items missing from second list that are in the first list """
    second = frozenset(second)
    return [item for item in first if item not in second]
#-------------------------------------------------------------------------------
#
# difflist_noset2
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def difflist_noset2(first,second):
    """ Returns items missing from second list that are in the first list """
    return list(set(first) - set(second))


difflist = difflist_or
#-------------------------------------------------------------------------------
#
# difflist
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def difflist(first, second): # fastest
    """ Returns items missing from second list that are in the first list """
    second = frozenset(second)
    return [item for item in first if item not in second]
#-------------------------------------------------------------------------------
#
# printlist
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printlis(list,depth=0):
    """ Prints list as raw text. """
    lock.acquire()
    s = ''
    for i in range(depth):
      s = s + listindent
    for item in list:
      print(s + str(item))
    lock.release()
#-------------------------------------------------------------------------------
#
# printtuple
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printtup(tuple,depth=0):
    """ Prints tuple as a raw text list. """
    lock.acquire()
    count = 0
    s = ''
    for i in range(depth):
      s = s + listindent
    for name, value in tuple.items():
      count = count + 1
      print(s + str(count) + ".", name, ",", value)
    lock.release()
#-------------------------------------------------------------------------------
#
# printdic
#
# https://realpython.com/iterate-through-dictionary-python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printdic(dic,depth=0):
  lock.acquire()
  #for value in a_dict.values():
  #  print(value)
  #for key in dic.keys():
  #  print(key)
  #for item in dic.items():
  #  print(item)
  #for key, value in dic.items():
  #  print(key, '->', value)
  for key in dic:
    print(str(key), '->', dic[key])
  lock.release()
#-------------------------------------------------------------------------------
#
# getLocalMethods
#
# https://stackoverflow.com/questions/305924/in-python-how-can-you-get-the-name-of-a-member-functions-class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getLocalMethods(clss):
  import types
  # This is a helper function for the test function below.
  # It returns a sorted list of the names of the methods
  # defined in a class. It's okay if you don't fully understand it!
  result = [ ]
  for var in clss.__dict__:
      val = clss.__dict__[var]
      if (isinstance(val, types.FunctionType)):
          result.append(var)
  return sorted(result)
#-------------------------------------------------------------------------------
#
# dumpr
#
# First attempt at a recursive object dumper
#
# I should update this per dump
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dumpr(obj,depth=-1):
  lock.acquire()
  depth=depth+1
  s = ""
  for i in range(depth):
    s = s + listindent
  print()
  print("%s%s %s" % (s,str(obj),str(type(obj))))
  print()
  if isinstance(obj, tuple):
    print(s + "-------------- printing tuple --------------")
    printtuple(obj,depth)
  elif isinstance(obj, list):
    print(s + "-------------- printing list ---------------")
    printlist(obj,depth)
  elif isinstance(obj, dict):
    # https://realpython.com/iterate-through-dictionary-python
    print(s + "-------------- printing dict ---------------")
    printtuple(obj,depth)
  else:
    print(s + "--------- dumping dir (attributes) ---------")
    dumpr(dir(obj),depth)
    if hasattr(obj, '__dict__'):
      print(s + "-------------- dumping vars ----------------")
      dumpr(vars(obj),depth)
  print(s + "------------ inspect.getmembers -------------")
  for member in inspect.getmembers(obj):
    print(s + str(member))
    #dumpr(member,depth)
  #print(s + "------------- printing object ---------------")
  #print(s + str(obj))
  print()
  depth=depth-1
  lock.release()
#-------------------------------------------------------------------------------
#
# dump
#
# make new dumper?
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dump(obj):
  lock.acquire()
  print(obj,None,callable(obj),type(obj))
  for value in dir(obj):
    attr = getattr(obj,value)
    print("%s %s %s %s %s" % (value, attr, callable(attr), type(attr), id(attr)))
    #print()
  lock.release()
#-------------------------------------------------------------------------------
#
# listobj
#
# return a dump in dict format
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def listobj(obj):
  dump = {'object': obj, 'callable': callable(obj), 'type': type(obj), 'id': id(obj), 'dir': []}
  for value in dir(obj):
    attr = getattr(obj,value)
    dump['dir'].append({'value': value, 'attribute': attr, 'callable': callable(attr), 'type': type(attr), 'id': id(attr)})
  return dump
#-------------------------------------------------------------------------------
#
# printlist
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printlist(list, numbered=False, pad=''):
  lock.acquire()
  for item in list:
    print("%s%s" % (pad, item))
  lock.release()
#-------------------------------------------------------------------------------
#
# printdict
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printdict(dictionary, numbered=False, pad=''):
  ''' Print dictionary by getting keys aren't values separately like transform does in order to get an index to work with. This simple task led to the discovery of a list bug. Use list(dictionary.values()) and it will fail under some currently unknown conditions '''
  lock.acquire()
  for i in range(len(dictionary)):
    key = list(dictionary.keys())[i]
    #value = list(dictionary.values())[i]
    # workaround that I'm vetting which is why i'm doing things this way so I can get extra testing in. I need to understand this problem surface completely and make sure this workaround or alternate way is solid
    value = [dictionary[i] for i in dictionary][i]
    if numbered is True:
      print("%s%s %s %s" % (pad, i, key, value))
    else:
      print("%s%s %s" % (pad, key, value))
  lock.release()
#-------------------------------------------------------------------------------
#
# remdup (was: 'unique' but that clashes with @unique)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def remdup(list):
  """ return the list with duplicate elements removed """
  return list(set(list))
#-------------------------------------------------------------------------------
#
# union
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def union(list1, list2):
  """ return the union of two lists """
  return list(set(list1) | set(list2))
#-------------------------------------------------------------------------------
#
# intersection
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def intersection(list1, list2):
  set2 = frozenset(list2)
  return [x for x in list1 if x in set2]
#-------------------------------------------------------------------------------
#
# setreatwarningsaserrors
#
# treat_warnings_as_errors=False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setreatwarningsaserrors(yes):
  global treat_warnings_as_errors
  treat_warnings_as_errors = yes
#-------------------------------------------------------------------------------
#
# setprintfilepath
#
# logfilepath=False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setprintfilepath(prnt):
  global logfilepath
  logfilepath = prnt
#-------------------------------------------------------------------------------
#
# setprintfile
#
# logfile=True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setprintfile(prnt):
  global logfile
  logfile = prnt
#-------------------------------------------------------------------------------
#
# setprintfile
#
# logfile=True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setlogger(logger):
  global dimslogger
  dimslogger = logger
#-------------------------------------------------------------------------------
#
# setprintline
#
# logline=True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setprintline(prnt):
  global logline
  logline = prnt
#-------------------------------------------------------------------------------
#
# setlistindent
#
# listindent='    '
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setlistindent(indent):
  global listindent
  listindent = indent
#-------------------------------------------------------------------------------
#
# setthrowonexception
#
# # TODO: need to look at end arg and if \n change to \n\n
#
# throw_on_exception=False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setthrowonexception(throw):
  global throw_on_exception
  throw_on_exception = throw
#-------------------------------------------------------------------------------
#
# logcompare
#
# Set to true to remove timestamp and thread info so two logs can be compared
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logcompare(on):
  global log_compare
  log_compare = on
#-------------------------------------------------------------------------------
#
# setpauseonerror
#
# pause_on_error=False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setpauseonerror(pause):
  global pause_on_error
  pause_on_error = pause
#-------------------------------------------------------------------------------
#
# setbreakonerror
#
# break_on_error=False  # don't know if I can or should implement this
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setbreakonerror(brk):
  global break_on_error
  break_on_error = brk
#-------------------------------------------------------------------------------
#
# setaudibleerror
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setaudibleerror(on):
  global audible_error
  audible_error = on
#-------------------------------------------------------------------------------
#
# settracelevel
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def settracelevel(level):
  global tracelevel
  tracelevel = int(level)
#-------------------------------------------------------------------------------
#
# setprintonly
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setprintonly(on):
  global printonly
  printonly = on
#-------------------------------------------------------------------------------
#
# gettracelevel
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def gettracelevel():
  return int(tracelevel)
#-------------------------------------------------------------------------------
#
# time_stamp_this
#
# cutting edge time stamp technology ;)
# but seriously perf_counter() and perf_counter_ns() were best
# according to ... https://realpython.com/python-timer
# note: these guys have a feed you can import into python, pretty interesting
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def time_stamp_this():
  # https://strftime.org
  # https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python
  #timestamp = datetime.now()
  #timestamp = timestamp.strftime("%H:%M:%S:%f")
  # 9 decimal points seemed to be largest, use 10 to verify (diag)
  return f"{time.perf_counter():0.7f}"
#-------------------------------------------------------------------------------
#
# sleep
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sleep(seconds):
  printsf("Sleeping for ", seconds, "seconds ...")
  time.sleep(seconds)
#-------------------------------------------------------------------------------
#
# pr
#
#
# Print Raw
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pr(string):
  sys.stdout.buffer.write(bytes(string, 'utf-8'))
#-------------------------------------------------------------------------------
#
# prn
#
#
# Print Raw Newline
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def prn(string):
  sys.stdout.buffer.write(bytes(string + '\n', 'utf-8'))
#-------------------------------------------------------------------------------
#
# speak
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def speak(it):
  tts = pyttsx3.init()
  tts.setProperty('voice', tts.getProperty('voices')[1].id)
  tts.setProperty('rate', random.randint(130, 180))
  #tts.setProperty('volume',1.0)
  # https://www.geeksforgeeks.org/python-split-multiple-characters-from-string/
  chunks = re.split('\.|,|\?|\!|\(|\)|\"', it)
  for chunk in chunks:
    tts.say(chunk)
    tts.runAndWait()
  tts.stop()
#-------------------------------------------------------------------------------
#
# printfntrans
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printfntrans(func, prefixer, *args):
  """ Print transition from one function to another displaying tree indent """
  if (log_compare):
    # mutually exclude print and logging as they both print to STDOUT
    s = "%s %s %s\n" % (prefixer*stack_size2a(),func.__name__,' '.join(map(str,args)))
  else:
    timestamp = time_stamp_this()
    # mutually exclude print and logging as they both print to STDOUT
    s = "%s %s %s %s %s\n" % (timestamp,threading.currentThread().ident,prefixer*stack_size2a(),func.__name__,' '.join(map(str,args)))
  if dimslogger | FLAG_PRINT == 1:
    printsf(s, end='')
  elif dimslogger | FLAG_LOGGING == 1:
    logging.info(s)
#-------------------------------------------------------------------------------
#
# printclasstrans
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printclasstrans(class_self, func, prefixer, *args):
  """ Print transition from one function to another displaying tree indent """
  if (log_compare):
    class_name = str(class_self.__class__).lstrip("<class '").rstrip("'>")
    # mutually exclude print and logging as they both print to STDOUT
    s = "%s %s.%s %s\n" % (prefixer*stack_size2a(),class_name,func.__name__,' '.join(map(str,args)))
  else:
    timestamp = time_stamp_this()
    class_name = str(class_self.__class__).lstrip("<class '").rstrip("'>")
    # mutually exclude print and logging as they both print to STDOUT
    s = "%s %s %s %s.%s %s\n" % (timestamp,threading.currentThread().ident,prefixer*stack_size2a(),class_name,func.__name__,' '.join(map(str,args)))
  if dimslogger | FLAG_PRINT == 1:
    printsf(s, end='')
  elif dimslogger | FLAG_LOGGING == 1:
    logging.info(s)
#-------------------------------------------------------------------------------
#
# pause
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pause(*args):
  if len(args) > 0:
    msg = ' '.join(map(str,args))
    input("* Paused: "+msg+"\npress any key when ready to continue ... \n")
  else:
    input("* Paused: press any key when ready to continue ... \n")
#-------------------------------------------------------------------------------
#
# testtrap
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def testtrap(*args):
  if len(args) > 0:
    msg = ' '.join(map(str,args))
    input("\n* Test Trap: "+msg+"\npress any key when ready to continue ... \n")
  else:
    input("\n* Test Trap: press any key when ready to continue ... \n")
#-------------------------------------------------------------------------------
#
# ctrace
#
# An attempt at a trace wrapper for classes that would provide
# module_classname::function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ctrace(level):
  def trace_inner(func):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    @functools.wraps(func)
    def trace_wrapper(*args, **kwargs):
      filename=info.filename
      if logfilepath is False: filename = ntpath.basename(info.filename)
      #Exception ignored in: <function BizCLI.__del__ at 0x000001FBE53DE430>
      #Traceback (most recent call last):
      #File "C:\_Rep01\private\src\script\py\dimsx\$_\dimsdbg.py", line 659, in trace_wrapper
      #TypeError: 'NoneType' object is not callable
      #BUG: looks like ntpath is None for some reason when running modules.py bizebee
      if(level <= tracelevel):
        if log_compare:
          printclasstrans(args[0], func, ">")
        else:
          printclasstrans(args[0], func, ">", "-in-", filename, "@ln", info.lineno)
      # call wrapped function
      result = func(*args, **kwargs)
      if(level <= tracelevel):
        if log_compare:
          printclasstrans(args[0], func, "<")
        else:
          printclasstrans(args[0], func, "<", "-in-", filename, "@ln", info.lineno)
      return result
    return trace_wrapper
  return trace_inner
#-------------------------------------------------------------------------------
#
# trace
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def trace(level):
  def trace_inner(func):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    @functools.wraps(func)
    def trace_wrapper(*args, **kwargs):
      filename=info.filename
      if logfilepath is False: filename = ntpath.basename(info.filename)
      if(level <= tracelevel):
        if log_compare:
          printfntrans(func, ">")
        else:
          printfntrans(func, ">", "-in-", filename, "@ln", info.lineno)
      # call wrapped function
      result = func(*args, **kwargs)
      if(level <= tracelevel):
        if log_compare:
          printfntrans(func, "<")
        else:
          printfntrans(func, "<", "-in-", filename, "@ln", info.lineno)
      return result
    return trace_wrapper
  return trace_inner
#-------------------------------------------------------------------------------
#
# tracealways
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tracealways(func):
  callerframerecord = inspect.stack()[1]
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  @functools.wraps(func)
  def trace_wrapper(*args, **kwargs):
    filename=info.filename
    if logfilepath is False: filename = ntpath.basename(info.filename)
    if log_compare:
      printfntrans(func, ">")
    else:
      printfntrans(func, ">", "-in-", filename, "@ln", info.lineno)
    # call wrapped function
    result = func(*args, **kwargs)
    if log_compare:
      printfntrans(func, "<")
    else:
      printfntrans(func, "<", "-in-", filename, "@ln", info.lineno)
    return result
  return trace_wrapper
#-------------------------------------------------------------------------------
#
# globals
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
diagnostic_level='Log'
# what is diagnostic__w for? It seems to turn off all diagnostic output
# may have been superseded by __debug__ ?
diagnostic__w=False
# setting this didn't matter until recently as I updated it
diagnostic_ts=True


diagnostic_levels = {
    'Always' : False,
    'Error'  : False,
    'Warn'   : False,
    'Atten'  : False,
    'Info'   : False,
    'Log'    : False,
    'Verb'   : False,
    'Spew'   : False,
    'Danger' : False
}
loglevels = diagnostic_levels
diagnostic_levelvals = {
  'Off': 0,
  'Always' : 1,
  'Error'  : 2,
  'Warn'   : 3,
  'Atten'  : 4,
  'Info'   : 5,
  'Log'    : 6,
  'Verb'   : 7,
  'Spew'   : 8,
  'Danger' : 9
  }
loglevelvals = diagnostic_levelvals
diagnostic_levelstrings = {
  0 : 'Off',
  1 : 'Always',
  2 : 'Error',
  3 : 'Warn',
  4 : 'Atten',
  5 : 'Info',
  6 : 'Log',
  7 : 'Verb',
  8 : 'Spew',
  9 : 'Danger'
}
loglevelstrings = diagnostic_levelstrings
#-------------------------------------------------------------------------------
#
# get_diagnostic_level
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_diagnostic_level():
  global diagnostic_level
  return diagnostic_level
getdiaglevel=get_diagnostic_level
getloglevel=get_diagnostic_level
#-------------------------------------------------------------------------------
#
# get_diagnostic_levelasstring
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_diagnostic_levelasstring():
  global diagnostic_level
  return diagnostic_level
getloglevelasstring = get_diagnostic_levelasstring
#-------------------------------------------------------------------------------
#
# get_diagnostic_levelasvalue
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_diagnostic_levelasvalue():
  global diagnostic_level
  return diagnostic_levelvals[diagnostic_level]
getloglevelasvalue = get_diagnostic_levelasvalue
#-------------------------------------------------------------------------------
#
# set_diagnostic_levelasvalue
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def set_diagnostic_levelasvalue(level):
  setlevel(diagnostic_levelstrings[level])
setloglevelasvalue = set_diagnostic_levelasvalue
#-------------------------------------------------------------------------------
#
# set_diagnostic_levelasstring
#
#-------------------------------------------------------------------------------
def set_diagnostic_levelasstring(level):
  setlevel(level)
setloglevelasstring = set_diagnostic_levelasstring
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# set_diagnostic_level
#
#-------------------------------------------------------------------------------
def set_diagnostic_level(level):
  #print("Setting level to", level)
  global diagnostic_level
  diagnostic_level = level
  if level == "On":
    diagnostic_levels["Danger"] = True
    diagnostic_levels["Spew"] = True
    diagnostic_levels["Verb"] = True
    diagnostic_levels["Log"] = True
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  if level == "Danger":
    diagnostic_levels["Danger"] = True
    diagnostic_levels["Spew"] = True
    diagnostic_levels["Verb"] = True
    diagnostic_levels["Log"] = True
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  if level == "Spew":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = True
    diagnostic_levels["Verb"] = True
    diagnostic_levels["Log"] = True
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  if level == "Verb":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = True
    diagnostic_levels["Log"] = True
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Log":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = True
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Info":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = True
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Atten":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = False
    diagnostic_levels["Atten"] = True
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Warn":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = False
    diagnostic_levels["Atten"] = False
    diagnostic_levels["Warn"] = True
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Error":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = False
    diagnostic_levels["Atten"] = False
    diagnostic_levels["Warn"] = False
    diagnostic_levels["Error"] = True
    diagnostic_levels["Always"] = True
  elif level == "Always":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = False
    diagnostic_levels["Atten"] = False
    diagnostic_levels["Warn"] = False
    diagnostic_levels["Error"] = False
    diagnostic_levels["Always"] = True
  elif level == "Off":
    diagnostic_levels["Danger"] = False
    diagnostic_levels["Spew"] = False
    diagnostic_levels["Verb"] = False
    diagnostic_levels["Log"] = False
    diagnostic_levels["Info"] = False
    diagnostic_levels["Atten"] = False
    diagnostic_levels["Warn"] = False
    diagnostic_levels["Error"] = False
    diagnostic_levels["Always"] = False

setdiagnosticlevel=set_diagnostic_level
setdiaglevel=set_diagnostic_level
setloglevel=set_diagnostic_level
#-------------------------------------------------------------------------------
#
# turn_diag_ts_on
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def turn_diag_ts_on():
  diagnostic_ts = True
turnonlogts=turn_diag_ts_on
#-------------------------------------------------------------------------------
#
# turn_diag_ts_off
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def turn_diag_ts_off():
  diagnostic_ts = False
turnofflogts=turn_diag_ts_on
#-------------------------------------------------------------------------------
#
# throw
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def throw(e, *args, **kwargs):
  # TODO: join args and add kkwargswargs.
  # e.g. raise Exception(str(e) + ' '.join(map(str,args)), **kwargs)
  raise Exception(e)
#-------------------------------------------------------------------------------
#
# exception
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def exception(e,*args,**kwargs): # name may clash
  callerframerecord = inspect.stack()[1]
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  lock.acquire()
  #diagnostic("Warn",info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
  #exc_type, exc_obj, exc_tb = sys.exc_info()
  #fname = os.logfilepath.split(exc_tb.tb_frame.f_code.co_filename)[1]
  #print(exc_type, fname, exc_tb.tb_lineno)
  print(Fore.RED, end='')
  traceback.print_exc()
  print(Back.YELLOW+"Exception!"+Style.RESET_ALL+Fore.RED, str(e),info.filename,info.function,info.lineno,' '.join(map(str,args)), Style.RESET_ALL, **kwargs)
  lock.release()
  #pdb.pm() # seems to be broken, see except.py
  if audible_error is True: playsound("%s\\internal\\script\\py\\dimsx\\fail-buzzer-01.wav" % (os.environ['_path_audio']),)
  if break_on_error is True: breakpoint() #pdb.set_trace()
  elif pause_on_error is True: pause()
  if throw_on_exception is True: throw(e)
#-------------------------------------------------------------------------------
#
# dbglog
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dbglog(tag,*args,**kwargs):
  callerframerecord = inspect.stack()[1]
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  diagnostic(tag,info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# diagnostic
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def diagnostic(level='Info',logfile="",function="",logline="",*args, **kwargs):
  global diagnostic_ts, dimslogger, diagnostic_levels, diagnostic_levelvals

  #date = datetime.date.today()
  #timestamp = datetime.now()
  timestamp = time_stamp_this()
  # https://strftime.org
  #timestamp = timestamp.strftime("%H:%M:%S:%f")
  try: diagnostic_levels[level]
  except:
    printsf( str(timestamp), "<<ERROR>> Invalid level '", level, "' specified")
    return
  lock.acquire()
  #print("Level is", level)
  # TODO: where can we redirect the ouptut is diagnostic__w is True?
  # maybe we can write to a text object if provided?
  #print(f"Level is {level}")
  #print(f"diagnostic_level is {diagnostic_level}")
  #print(f"diagnostic__w is {diagnostic__w}")
  #print(f"Diagnostic is {diagnostic_levels.get(level)}")
  #print("LEVEL:", level)
  #print("DIAGLEVEL:", diagnostic_levels.get(level))
  #print("DIAG:",diagnostic_levels)
  if printonly is True:
    if diagnostic_levelvals[level] <= diagnostic_levelvals['Info']:
      print(' '.join(map(str,args)))
  elif diagnostic_levels.get(level) and diagnostic__w is False:
    try:
      if logfile != "" and not logfilepath is True: logfile = ntpath.basename(logfile)
      #if function != "" : function = function.upper()
      if dimslogger | FLAG_PRINT == 1:
        # add thread info using threading.currentThread()
        
        if log_compare:
            b = ""
        else:
          if diagnostic_ts is True:
            b = "%s %s %s" % (str(timestamp), threading.currentThread().ident, function)
          else:
            b = "%s %s" % (threading.currentThread().ident, function)
        if level == "Atten":
          print(f"{b} {Fore.GREEN} ### ATTENTION! ###  \"\"\" {' '.join(map(str,args))} \"\"\" {Style.RESET_ALL} {logfile} ln {logline}\n", end='', **kwargs)
          #print(b,Fore.GREEN+"### ATTENTION! ###", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        elif level == 'Warn':
          print(f"{b} {Fore.YELLOW} *** WARNING! ***  \"\"\" {' '.join(map(str,args))} \"\"\" {Style.RESET_ALL} {logfile} ln {logline}\n", end='', **kwargs)
          #print(b,Fore.YELLOW+"*** WARNING! ***", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        elif level == "Error":
          print(f"{b} {Fore.RED} <<< ERROR! >>>  \"\"\" {' '.join(map(str,args))} \"\"\" {Style.RESET_ALL} {logfile} ln {logline}\n", end='', **kwargs)
         #print(b,Fore.RED+"<<< ERROR! >>>", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        else:
          s = f"{b} | \"\"\" {' '.join(map(str,args))} \"\"\" @ {logfile} ln {logline}\n"
          print(s, end='', **kwargs)
          #print(b,"|", "\"\"\"", ' '.join(map(str,args)), "\"\"\"","@",logfile,"ln",logline, **kwargs)
        if level == "Error" or (treat_warnings_as_errors is True and level == "Warn"):
          # https://docs.python.org/3/library/functions.html#breakpoint
          if audible_error is True: playsound("%s\\internal\\script\\py\\dimsx\\fail-buzzer-01.wav" % (os.environ['_path_audio']),)
          if break_on_error is True: breakpoint() #pdb.set_trace()
          elif pause_on_error is True: pause()
      elif dimslogger | FLAG_LOGGING == 1:
        b = function
        if level == "Atten":
          logging.info(b,Fore.GREEN+"### ATTENTION! ###", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        elif level == 'Warn':
          logging.info(b,Fore.YELLOW+"*** WARNING! ***", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        elif level == "Error":
          logging.info(b,Fore.RED+"<<< ERROR! >>>", "\"\"\"", ' '.join(map(str,args)), "\"\"\""+Style.RESET_ALL,logfile,"ln",logline, **kwargs)
        else:
          logging.info(b,"|", "\"\"\"", ' '.join(map(str,args)), "\"\"\"","@",logfile,"ln",logline, **kwargs)
    except Exception as e:
      print("Execption in diagnostic ->", e)
  lock.release()
#-------------------------------------------------------------------------------
#
# logdangerous
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logdangerous(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Danger',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logspew
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logspew(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Spew',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logverb
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logverb(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Verb',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# log
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loglog(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Log',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# loginfoanddie
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfoanddie(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Info',info.filename,info.function,info.lineno,Back.RED+"Die, Die, Die You Ugly Bastard Die! "+Style.RESET_ALL+":->  " + ' '.join(map(str,args)), **kwargs)
    raise Exception(f"Die, Die, Die You Ugly Bastard Die!")
#-------------------------------------------------------------------------------
#
# loginfoandexit
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfoandexit(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Info',info.filename,info.function,info.lineno,Back.RED+"Die, Die, Die You Ugly Bastard Die! "+Style.RESET_ALL+":->  " + ' '.join(map(str,args)), **kwargs)
    # this will only exit the thread so it will only exit the process if in the main thread
    sys.exit(0)
#-------------------------------------------------------------------------------
#
# loginfoand_exit
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfoand_exit(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Info',info.filename,info.function,info.lineno,Back.RED+"Die, Die, Die You Ugly Bastard Die! "+Style.RESET_ALL+":->  " + ' '.join(map(str,args)), **kwargs)
    # this doesn't clean up but you can exit the process from a thread that isn't main
    # https://docs.python.org/3/library/os.html#os._exit
    os._exit(0)
#-------------------------------------------------------------------------------
#
# loginfoloud
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfoloud(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Info',info.filename,info.function,info.lineno,Back.MAGENTA+' '.join(map(str,args)),Style.RESET_ALL,**kwargs)
    playsound("%s\\internal\\script\\py\\dimsx\\bell-ringing-01ca.wav" % (os.environ['_path_audio']))
#-------------------------------------------------------------------------------
#
# loginfohighlight
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfohighlight(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    if 'color' in kwargs: color = kwargs['color']; del kwargs['color']
    else: color = Back.YELLOW
    diagnostic('Info',info.filename,info.function,info.lineno,color+' '.join(map(str,args)),Style.RESET_ALL,**kwargs)
#-------------------------------------------------------------------------------
#
# crybaby
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def crybaby(cry=True):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Warn',info.filename,info.function,info.lineno,Back.RED+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "+Style.RESET_ALL, 'W' + 'A'*32 + 'H'*16,Back.RED+" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+Style.RESET_ALL)
    if cry is True:
      # DONE: play a crying baby or some other attention getting sound
      # https://www.soundjay.com/baby-crying-sound-effect.html
      playsound("%s\\internal\\script\\py\\dimsx\\baby-crying-05a.wav" % (os.environ['_path_audio']))
#-------------------------------------------------------------------------------
#
# loginfooutloud
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfooutloud(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    it = ' '.join(map(str, args))
    diagnostic('Info',info.filename,info.function,info.lineno,it, **kwargs)
    speak(it)
#-------------------------------------------------------------------------------
#
# loginfo
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loginfo(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Info',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logatten
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logatten(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Atten',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logwarn
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logwarn(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Warn',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logerror
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logerror(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Error',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# logaudibleerror
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logaudibleerror(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Error',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
    s = \
      [
        "%s\\internal\\script\\py\\dimsx\\fail-buzzer-01.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\fail-buzzer-04.wav" % (os.environ['_path_audio']),
      ]
    playsound(s[0])
#-------------------------------------------------------------------------------
#
# logaudiblewarn
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logaudiblewarn(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Warn',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
    sounds = \
      [
        "%s\\internal\\script\\py\\dimsx\\bell-ringing-01ca.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\train-crossing-bell-01a.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\train-whistle-01.wav" % (os.environ['_path_audio']),
      ]
    playsound(sounds[random.randint(0, 2)])
#-------------------------------------------------------------------------------
#
# logaudibleerror
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logaudibleerror(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Error',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
    sounds = \
      [
        "%s\\internal\\script\\py\\dimsx\\bell-ringing-01ca.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\fail-buzzer-01.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\fail-buzzer-04.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\fail-trombone-03.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\fail-trumpet-01.wav" % (os.environ['_path_audio']),
        "%s\\internal\\script\\py\\dimsx\\censor-beep-3.wav" % (os.environ['_path_audio']),
      ]
    playsound(sounds[random.randint(0, 4)])
#-------------------------------------------------------------------------------
#
# logallways
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logallways(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    diagnostic('Always',info.filename,info.function,info.lineno,' '.join(map(str,args)), **kwargs)
#-------------------------------------------------------------------------------
#
# log_summary
#
# I think this was for logging a summary of a dict
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def log_summary(obj, nitems=5, quiet=False):
  if __debug__:
    if diagnostic_levels.get('Info') and diagnostic__w is False:
      callerframerecord = inspect.stack()[1]
      frame = callerframerecord[0]
      info = inspect.getframeinfo(frame)
      if type(obj) is dict:
        count = 0
        lock.acquire()
        if not quiet: print("DICTIONARY ==>> ", end='')
        for key,value in obj.items():
          print("%s: %s, " % (key, value), end='')
          if count >= nitems: break
          else: count += 1
        if count < len(obj):
          print("...")
        lock.release()
      elif type(obj) is list:
        if len(obj) > 0:
          if not quiet: printsf("LIST:...")
          print_summary(obj[0])
          if len(obj) > 1: printsf("...")
      elif type(obj) is str:
        if not quiet: printsf("STRING: ", obj[:-(len(obj)-(nitems*20))],"...")
        else: printsf(obj[:-(len(obj)-(nitems*20))],"...")
      else:
        if not quiet: printsf("OBJECT:", type(obj), obj)
        else: printsf(type(obj), obj)
#-------------------------------------------------------------------------------
#
# logmainentry
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logmainentry(name=None, tts=False, soundfx=False):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    timestamp = time_stamp_this()
    lock.acquire()
    #print(str(timestamp),"|0> Entering MAIN")
    print(str(timestamp),threading.currentThread().ident,Back.GREEN+Fore.RED+"--- MAIN ENTRY --->"+Style.RESET_ALL)
    it = f"Starting application {name}, PID: {os.getpid()}"
    print(str(timestamp),threading.currentThread().ident,f"{Back.GREEN+Fore.RED}| {it}{Style.RESET_ALL}\n", end='')
    #print(f"********************************* tts is {tts} *********************************")
    #print(f"********************************** fx is {soundfx} ******************************")
    lock.release()
    if tts is True: speak(it)
    if soundfx is True: playsound("%s\\internal\\script\\py\\dimsx\\needle-drop-3.wav" % (os.environ['_path_audio']))
#-------------------------------------------------------------------------------
#
# logmainexit
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def logmainexit(name=None, tts=False, soundfx=False):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    timestamp = time_stamp_this()
    #print(str(timestamp),"<0| Leaving MAIN")
    if name is not None:
      it = f"Ending application {name}, PID: {os.getpid()}"
    else:
      it = f"Ending application"
    lock.acquire()
    print(f"{str(timestamp)} {threading.currentThread().ident} {Back.GREEN+Fore.RED}O {it}{Style.RESET_ALL}\n", end='')
    print(str(timestamp),threading.currentThread().ident,Back.GREEN+Fore.RED+"<--- MAIN EXIT ---"+Style.RESET_ALL)
    #print(f"********************************* tts is {tts} *********************************")
    #print(f"********************************** fx is {soundfx} ******************************")
    lock.release()
    if tts is True: speak(it)
    if soundfx is True: playsound("%s\\internal\\script\\py\\dimsx\\needle-up-2.wav" % (os.environ['_path_audio']))
#-------------------------------------------------------------------------------
#
# pyprint
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pyprint(result, name='', mark=': ', indent=0, tab='   '):
  lock.acquire()
  t = tab * indent
  if type(result) is dict:
    print("%s%s %s" % (t, name, type(result)))
    for key,value in result.items():
      pyprint(value, name=key, indent=indent+1)
  elif type(result) is list:
    print("%s%s %s len(%s)" % (t, name, type(result), len(result)))
    for item in result:
      pyprint(item, indent=indent+1)
  else:
    if len(name): print("%s%s%s%s" % (t, name, mark, result))
    else: print("%s%s" % (t, result))
  lock.release()
#-------------------------------------------------------------------------------
#
# pyprintdbg
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pyprintdbg(result, name='', mark=': ', indent=0, tab='   '):
  lock.acquire()
  print('-' * 72)
  t = tab * indent
  if type(result) is dict:
    print("%s'%s'%s %s %s" % (len(t), t, name, type(result), result))
    for key,value in result.items():
      pyprintdbg(value, name=key, indent=indent+1)
  elif type(result) is list:
    print("%s'%s'%s %s %s" % (len(t), t, name, type(result), result))
    for item in result:
      pyprintdbg(item, indent=indent+1)
  else:
    if len(name): print("%s'%s'%s%s%s" % (len(t), t, name, mark, result))
    else: print("%s'%s'%s" % (len(t), t, result))
  lock.release()
#-------------------------------------------------------------------------------
#
# pyprintfn
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pyprintfn(result, name='', mark=': ', indent=0, tab='   '):
  lock.acquire()
  t = tab * indent
  if type(result) is dict:
    #print("%s%s %s" % (t, name, type(result)))
    for key,value in result.items():
      pyprintfn(value, name=key, indent=indent+1)
  elif type(result) is list:
    #print("%s%s %s" % (t, name, type(result)))
    for item in result:
      pyprintfn(item, indent=indent+1)
  else:
    if callable(result):
      if len(name): print("%s%s%s%s" % (t, name, mark, result))
      else: print("%s%s" % (t, result))
  lock.release()
#-------------------------------------------------------------------------------
#
# pyprintfndbg
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pyprintfndbg(result, name='', mark=': ', indent=0, tab='   '):
  lock.acquire()
  print('-' * 72)
  t = tab * indent
  if type(result) is dict:
    print("%s'%s'%s %s %s" % (len(t), t, name, type(result), result))
    for key,value in result.items():
      pyprintfndbg(value, name=key, indent=indent+1)
  elif type(result) is list:
    print("%s'%s'%s %s %s" % (len(t), t, name, type(result), result))
    for item in result:
      pyprintfndbg(item, indent=indent+1)
  else:
    if callable(result):
      if len(name): print("%s'%s'%s%s%s" % (len(t), t, name, mark, result))
      else: print("%s'%s'%s" % (len(t), t, result))
  lock.release()
#-------------------------------------------------------------------------------
#
# printhighlight
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printhighlight(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    if 'color' in kwargs: color = kwargs['color']; del kwargs['color']
    else: color = Back.YELLOW
    print(color+' '.join(map(str,args)),Style.RESET_ALL,**kwargs)
printhl = printhighlight
#-------------------------------------------------------------------------------
#
# printcolor
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printcolor(*args,**kwargs):
  if __debug__:
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    if 'backcolor' in kwargs: backcolor = kwargs['backcolor']; del kwargs['backcolor']
    else: backcolor = Back.GREEN
    if 'forecolor' in kwargs: forecolor = kwargs['forecolor']; del kwargs['forecolor']
    else: forecolor = Fore.BLUE
    if 'color' in kwargs: 
      color = kwargs['color']; del kwargs['color']
      print(color+' '.join(map(str,args)),Style.RESET_ALL,**kwargs)
      return
    print(backcolor+forecolor+' '.join(map(str,args)),Style.RESET_ALL,**kwargs)
    
printhl = printhighlight
#-------------------------------------------------------------------------------
#
# get_string_encoding
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_string_encoding(string):
  #e = icu.CharsetDetector(string).detect().getName()
  e = chardet.detect(string)['encoding']
  printsf(e)
#-------------------------------------------------------------------------------
#
# reload_module_by_name
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def reload_module_by_name(module_name):
  module = None
  lock.acquire()
  print("\t...", module_name)
  fp, path, desc = imp.find_module(module_name)
  if fp:
    module = imp.load_module(module_name, fp, path, desc)
    print("Module", module)
    print("\t... ", module_name, module)
    importlib.reload(module)
  lock.release()
  return module
#-------------------------------------------------------------------------------
#
# load_module_by_name
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_module_by_name(module_name):
  lock.acquire()
  # https://www.devdungeon.com/content/import-python-module-string-name
  # https://fedingo.com/call-python-function-by-string-name/
  if module_name not in sys.modules:
    print("Loading module...")
    print("\t... ", module_name)
    module = importlib.import_module(module_name)
    print("Module", module)
  else:
    print("Reloading module...")
    fp, path, desc = imp.find_module(module_name)
    module = imp.load_module(module_name, fp, path, desc)
    print("Module", module)
    print("\t... ", module_name, module)
    importlib.reload(module)
  lock.release()
  return module
#-------------------------------------------------------------------------------
#
# load_module_and_class
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_module_and_class(module_name, class_name):
  #lock.acquire()
  printsf(module_name, class_name)
  # https://www.devdungeon.com/content/import-python-module-string-name
  # https://fedingo.com/call-python-function-by-string-name/
  try:
    if module_name not in sys.modules:
      printsf("Loading module...")
      printsf("\t... ", module_name)
      module_imp = importlib.import_module(module_name)
      function_imp = getattr(module_imp, class_name)
      printsf("Module", module_imp)
    else:
      printsf("Reloading module...")
      fp, path, desc = imp.find_module(module_name)
      module_imp = imp.load_module(module_name, fp, path, desc)
      function_imp = getattr(module_imp, class_name)
      #function_imp = imp.load_module("%s.%s" % (module_name, class_name),fp, path, desc)
      printsf("Module", module_imp)
      printsf("\t... ", module_name, module_imp)
      importlib.reload(module_imp)
  except Exception as e:
    exception(e)
    #lock.release()
    return None, None
  #lock.release()
  return module_imp, function_imp
#-------------------------------------------------------------------------------
#
# print_summary
#
# This is called from log_summary and calls itself, probably recursing a dict
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def print_summary(obj, nitems=5, quiet=False):
  if type(obj) is dict:
    count = 0
    lock.acquire()
    if not quiet: print("DICTIONARY ==>> ", end='')
    for key,value in obj.items():
      print("%s: %s, " % (key, value), end='')
      if count >= nitems: break
      else: count += 1
    if count < len(obj):
      print("...")
    lock.release()
  elif type(obj) is list:
    if len(obj) > 0:
      if not quiet: printsf("LIST:...")
      print_summary(obj[0])
      if len(obj) > 1: printsf("...")
  elif type(obj) is str:
    if not quiet: printsf("STRING: ", obj[:-(len(obj)-(nitems*20))],"...")
    else: printsf(obj[:-(len(obj)-(nitems*20))],"...")
  else:
    if not quiet: printsf("OBJECT:", type(obj), obj)
    else: printsf(type(obj), obj)
#-------------------------------------------------------------------------------
#
# <|:) Wizard
#
#-------------------------------------------------------------------------------
