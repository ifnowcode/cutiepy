#-------------------------------------------------------------------------------
#
# section: imports
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import stat
import time # https://stackoverflow.com/questions/1938048/high-precision-clock-in-python
from printcon import *
import random
import hashlib
import shutil
from pathlib import Path
# https://stackoverflow.com/questions/14075465/copy-a-file-with-a-too-long-path-to-another-directory-in-python
# https://stackoverflow.com/questions/24046509/python-copy-long-file-path-shutil-copyfile
# TODO: fix long file name no copy issue (says it can't find the file)
from shutil import copy2
import ntpath
#-------------------------------------------------------------------------------
#
# getfilehash
#
# https://pypi.org/project/pyfastcopy
#
# https://www.w3schools.com/python/ref_list_sort.asp
#
#os.remove() removes a file.
#os.rmdir() removes an empty directory.
#shutil.rmtree() deletes a directory and all its contents.
#pathlib.Path.unlink() removes a file or symbolic link.
#pathlib.Path.rmdir() removes an empty directory.
#
# TODO: add a tree crawler with a callback when a file or directory is found
# TODO: add ability to take a lists like exclusions but will specify what to copy
# as opposed to what to not copy.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getfilehash(handle, size=0):
  h = hashlib.sha256()
  while True:
      buf = handle.read(size)
      if len(buf) == 0: break
      h.update(buf)
  #return h.digest()
  return h.hexdigest()
#-------------------------------------------------------------------------------
#
# unique
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def unique(list):
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
# difference
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def difference(first, second): # fastest
  """ Returns items missing from second list that are in the first list """
  second = frozenset(second)
  return [item for item in first if item not in second]
#-------------------------------------------------------------------------------
#
# differences
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def differences(first, second): # fastest
  """ Returns items missing from second list that are in the first list """
  second = frozenset(second)
  miss2 = [item for item in first if item not in second]
  second = list(second)
  first  = frozenset(first)
  miss1 = [item for item in second if item not in first]
  return miss1 + miss2
#-------------------------------------------------------------------------------
#
# printlist
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printlist(list):
  """ Prints list as raw text. """
  for item in list:
    print(item)
#-------------------------------------------------------------------------------
#
# del_dir_rw
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def del_dir_rw(action, name, exc):
  print("Action:", action, "\nName:", name, "\nExc", exc)
  try:
      os.chmod(name, stat.S_IWRITE)
      os.remove(name)
  except Exception as e:
      exception(e)
#-------------------------------------------------------------------------------
#
# del_file_rw
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def del_file_rw(action, name, exc):
  print("Action:", action, "\nName:", name, "\nExc", exc)
  try:
      os.chmod(name, stat.S_IWRITE)
      os.remove(name)
  except Exception as e:
      exception(e)
#-------------------------------------------------------------------------------
#
# sort_duplicates
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sort_duplicates(item):
  return ntpath.basename(item)
#-------------------------------------------------------------------------------
#
# ifallin (If All In)
#
# Checks if a list of strings are all in the provided string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ifallin(l, s):
  for i in l:
    if i not in s:
      return False
  return True
#-------------------------------------------------------------------------------
#
# ifanyin (If Any In)
#
# Checks if a list of strings if any are in the provided string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ifanyin(l, s):
  for i in l:
    if i in s:
      return True
  return False
#-------------------------------------------------------------------------------
#
# prunetree
#
# BUG: xdirs,xfiles,xext if specified can leave files behind that block removing the directory so I think these are not needed for a prune and should be removed. I've fixed this when using synctrees, do I need to leave this intact here for any reason?
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def prunetree(source,
              target,
              action=True,
              xdirs=[],         # deprecated
              xfiles=[],        # deprecated
              xext=[],          # deprecated
              showfiles=True,
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=True,
              pause_on_error=False,
              debug=False):

  """ Remove directories and files from target that aren't in the source """
  if os.path.exists(source) is False: raise FileNotFoundError
  if os.path.exists(target) is False: raise FileNotFoundError
  if verbose is True: print("Scanning source ...")
  sources = crawltree(source,
                      xdirs=xdirs,
                      xfiles=xfiles,
                      xext=xext,
                      showfiles=False,
                      no_dirs=no_dirs,
                      no_files=no_files,
                      quiet=True,
                      verbose=False,
                      pause_on_error=pause_on_error,
                      debug=debug)
  if verbose is True: print("Scanning target ...")
  targets = crawltree(target,
                      xdirs=xdirs,
                      xfiles=xfiles,
                      xext=xext,
                      showfiles=False,
                      no_dirs=no_dirs,
                      no_files=no_files,
                      quiet=True,
                      verbose=False,
                      pause_on_error=pause_on_error,
                      debug=debug)
  if verbose is True: print("Differencing results ...")
  targetdiff = difference(targets,sources)
  print("{0} unique files found in target {1} compared to source {2}".format(len(targetdiff),target,source))
  targetdiff.reverse()
  for item in list(targetdiff):
    file = target + "\\" + item
    if os.path.isdir(file) is True:
        if showfiles is True: print("Pruning ...",file)
        if action is True:
          try:
            #print("REMOVE DIR:",file,os.path.exists(file),os.path.islink(file))
            if os.path.islink(file):
              print("Remove Link =>", file)
              os.chmod(file, 0o777)
              #os.remove(file)
            os.rmdir(file)
          except PermissionError as e:
            os.chmod(file, stat.S_IWRITE)
            os.rmdir(file)
    elif os.path.islink(file) is True:
      if showfiles is True: print("Unlinking ...",file)
      if action is True: 
        try:
          #print("REMOVE LINK:",file,os.path.exists(file),os.path.islink(file))
          print("Remove Link =>", file)
          os.chmod(file, 0o777)
          os.remove(file)
        except PermissionError as e:
          logwarn(e)
    else:
      if showfiles is True: print("Pruning ...",file)
      if action is True:
        try:
          #print("REMOVE FILE:",file,os.path.exists(file),os.path.islink(file))
          if os.path.islink(file):
            print("Remove Link =>", file)
            os.chmod(file, 0o777)
          os.remove(file)
        except PermissionError as e:
          os.chmod(file, stat.S_IWRITE)
          os.remove(file)
#-------------------------------------------------------------------------------
#
# synctrees
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def synctrees(source,
              target,
              action=True,
              datetime=None,
              follow_symlinks=False,
              xdirs=[],
              xfiles=[],
              xext=[],
              readonly=False,
              showfiles=True,
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=False,
              pause_on_error=False,
              debug=True):
# TODO: only copytree when differences are found or that is overridden
# will need to check source tree as well if i do this
  """ Adds, Removes and Updates directories and files to target tree to make it match source tree """
  # copying before pruning is more robust
  if verbose is True: print("Syncing source",source,"to Target",target)
  if debug is True: pause()
  if verbose is True: print("Copying source",source,"tree to Target",target)
  copytree(source,
           target,
           action=action,
           datetime=datetime,
           follow_symlinks=follow_symlinks,
           xdirs=xdirs,
           xfiles=xfiles,
           xext=xext,
           readonly=readonly,
           showfiles=showfiles,
           quiet=quiet,
           verbose=verbose,
           pause_on_error=pause_on_error,
           debug=debug)
  if verbose is True: print("Pruning target",target)
  prunetree(source,
            target,
            action=action,
            xdirs=[],
            xfiles=[],
            xext=[],
            showfiles=showfiles,
            no_dirs=no_dirs,
            no_files=no_files,
            quiet=quiet,
            verbose=verbose,
            pause_on_error=pause_on_error,
            debug=debug)
#-------------------------------------------------------------------------------
#
# find_duplicate_files
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def find_duplicate_files(source,
                         filecompare=True,
                         xdirs=[],
                         xfiles=['Thumbs.db'],
                         xext=[],
                         showfiles=False,
                         verbose=False,
                         quiet=False,
                         pause_on_error=False,
                         debug=False):
  if os.path.exists(source) is False: raise FileNotFoundError
  if quiet is True: verbose = False
  if verbose is True: print("Crawling ->",source)
  duplicates = set()
  totalns = time.time_ns()
  try:
    startns = time.time_ns()
    sources = crawltree(source,
                        xdirs=xdirs,
                        xfiles=xfiles,
                        xext=xext,
                        showfiles=showfiles,
                        no_dirs=True,
                        quiet=quiet,
                        verbose=verbose,
                        pause_on_error=pause_on_error,
                        debug=debug)
# make a find duplicates for two trees
    """ Find duplicate files is a file tree, as of yet untested """
    stimens = time.time_ns() - startns

    if verbose is True:
        print("Found total of {0} sources".format(len(sources)))
        print("Crawled sources in {:0.1f} seconds".format(stimens / 1000 / 1000 / 1000))

    startns = time.time_ns()
    if quiet is not True: print("Searching results for duplicates ...")
    for file1 in sources:
      for file2 in sources:
        # look for match but make sure we aren't looking at the same file
        if ntpath.basename(file1) == ntpath.basename(file2) and file1 != file2:
          # can get access errors (Thumbs.db) reading files
          s = source + "\\" + file1
          t = source + "\\" + file2
          if verbose is True: print(file1, "vs", file2)
          stat1 = os.lstat(s)
          stat2 = os.lstat(t)
          # if they are not they same size they can't be a duplicate file
          if filecompare is True:
            # a size check should eliminate possible matches more quickly
            if stat1.st_size == stat2.st_size:
              # file contents
              h = open(s, "rb")
              srchash = getfilehash(h, stat1.st_size)
              h.close()
              h = open(t, "rb")
              targhash = getfilehash(h, stat2.st_size)
              h.close()
              if srchash == targhash:
                duplicates.add(file2)
          else:
            duplicates.add(file2)
    stimens = time.time_ns() - startns
    print("Searched sources in {:0.1f} seconds".format(stimens / 1000 / 1000 / 1000))
  except Exception as e:
    exception(e)
    if pause_on_error is True: pause()
  finally:
    duplicates = list(duplicates)
    duplicates.sort(key=sort_duplicates)
    return duplicates
#-------------------------------------------------------------------------------
#
# print_differences
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def print_differences(sources, targets):
  print("Found total of {0} sources".format(len(sources)))
  print("Found total of {0} targets".format(len(targets)))

  sourcediff = difference(sources, targets)
  targetdiff = difference(targets, sources)
  # TODO: collect statistics like how many files excluded, number copied
  print("*****************************************************")
  print("Source Tree has {0} unique items (see below ... )".format(len(sourcediff)))
  print("*****************************************************")
  printlist(sourcediff)
  print("*****************************************************")
  print("Target Tree has {0} unique items (see below ... )".format(len(targetdiff)))
  print("*****************************************************")
  printlist(targetdiff)
  print("*****************************************************")
#-------------------------------------------------------------------------------
#
# difftrees
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def difftrees(source,
              target,
              checkfileinfo=False,
              filecompare=False,
              has_timestamp=False,
              xdirs=[],
              xfiles=[],
              xext=[],
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=False,
              pause_on_error=False,
              debug=False):
  """ Compare and Print differences between two trees. """
  if quiet is not True: print("Crawling source ->",source,"... -&- target ->",target,"...")
  if os.path.exists(source) is False: raise FileNotFoundError
  if os.path.exists(target) is False: raise FileNotFoundError
  totalns = time.time_ns()
  try:
    startns = time.time_ns()
    sources = crawltree(source,
                        xdirs=xdirs,
                        xfiles=xfiles,
                        xext=xext,
                        showfiles=False,
                        no_dirs=no_dirs,
                        no_files=no_files,
                        quiet=True,
                        verbose=False,
                        pause_on_error=pause_on_error,
                        debug=debug)
    stimens = time.time_ns() - startns

    startns = time.time_ns()
    targets = crawltree(target,
                        xdirs=xdirs,
                        xfiles=xfiles,
                        xext=xext,
                        showfiles=False,
                        no_dirs=no_dirs,
                        no_files=no_files,
                        quiet=True,
                        verbose=False,
                        pause_on_error=pause_on_error,
                        debug=debug)
    ttimens = time.time_ns() - startns

    print("Found total of {0} sources".format(len(sources)))
    print("Found total of {0} targets".format(len(targets)))

    sourcediff = difference(sources,targets)
    targetdiff = difference(targets,sources)
    alldiff = differences(targets,sources)
    # TODO: collect statistics like how many files excluded, number copied
    print("*****************************************************")
    print("Source Tree has {0} unique items (see below ... )".format(len(sourcediff)))
    print("*****************************************************")
    printlist(sourcediff)
    print("*****************************************************")
    print("Target Tree has {0} unique items (see below ... )".format(len(targetdiff)))
    print("*****************************************************")
    printlist(targetdiff)
    print("*****************************************************")
    if debug is True:
        print("-- This is a test this is only a test")
        print("*****************************************************")
        print("Both Trees have {0} unique items (see below ... )".format(len(alldiff)))
        print("This is a test of differences()")
        print("*****************************************************")
        printlist(alldiff)
        print("*****************************************************")
        print("-- Ending this test this was only a test")
    print("Crawled sources in {:0.1f} seconds".format(stimens / 1000 / 1000 / 1000))
    print("Crawled targets in {:0.1f} seconds".format(ttimens / 1000 / 1000 / 1000))

    if filecompare is True or checkfileinfo is True:
      if verbose is True: print("Getting Intersection ...")
      intersect = intersection(sources,targets)
      print("Verifying Files ...")
      for entry in intersect:
        s = source + "\\" + entry
        t = target + "\\" + entry
        if os.path.isdir(s) is False:
          if verbose is True: print("Verifying ...",entry)
          slstat = os.lstat(s)
          tlstat = os.lstat(t)
          # file times
          # -- creation time, this will not match as this is set on copy
          if checkfileinfo is True and False:
            srctime = os.path.getctime(s)
            if slstat.st_ctime != srctime:
              print("Differing Source File created times")
            desttime = os.path.getctime(t)
            if tlstat.st_ctime != desttime:
              print("Differing Target File created times")
            #if verbose is True: print(srctime, desttime)
            if srctime != desttime:
              print("Created TS Mismatch -> {0}:{1}>{2}".format(srctime,desttime,t))
          if checkfileinfo is True:
            # -- modified time
            srctime2 = os.path.getmtime(s)
            if slstat.st_mtime != srctime2:
              print("Differing Source File modified times")
            desttime2 = os.path.getmtime(t)
            if tlstat.st_mtime != desttime2:
              print("Differing Target File modified times")
            if srctime2 != desttime2:
              print("Time: [{0} != {1}] {2}".format(srctime2,desttime2,t))
            # files size
            if slstat.st_size != tlstat.st_size:
              print("Size: [{0} != {1}] {2}".format(slstat.st_size,tlstat.st_size,t))

          if filecompare is True:
            # file contents
            h = open(s, "rb")
            srchash = getfilehash(h, slstat.st_size)
            h.close()
            h = open(t, "rb")
            targhash = getfilehash(h, tlstat.st_size)
            h.close()
            if srchash != targhash:
              print("Hash: [{0} != {1}] {2}".format(srchash, targhash, t))
              #print("Hash: [", srchash, "!=", targhash, "]", t)
    # calculate total time spent verifying the trees
    duration = (time.time_ns() - totalns) / 1000 / 1000 / 1000
    tick = 'seconds'
    if duration > 60:
      duration = duration / 60
      tick = 'minutes'
    if duration > 60:
      duration = duration / 60
      tick = 'hours'
    if duration > 60:
      duration = duration / 24
      tick = 'days'
    # https://pyformat.info
    print("This Operation took {0:0.2f} {1} total time".format(duration,tick))
  except KeyboardInterrupt as e:
    print("This Operation has been Terminated by User!")
#-------------------------------------------------------------------------------
#
# cmdtree
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmdtree(source,
            callback=None,
            datetime=None,
            append=True, # returned list will be empty, saves memory if you aren't going to need it like when you only use the callback or use for the printed output only etc.
            idirs=[],
            ifiles=[],
            iext=[],
            xdirs=[],
            xfiles=[],
            xext=[],
            showfiles=False,
            full_paths=False,
            no_dirs=False,
            no_files=False,
            quiet=False,
            verbose=False,
            pause_on_error=False,
            debug=False,
            dircmd=None,
            filecmd=None):
# http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
# Numbers Strings Lists Tuples Dictionaries_Maps
# TODO: wild card support in inclusion and exclusion lists
  """ Crawl Files from Source an return them in a list. No wildcard support for inclusion and exclusion lists yet. Callback takes one parameter and that is a file path as string """
  if os.path.exists(source) is False: raise FileNotFoundError
  sources = []
  interrupted = False
  try:
    [i.lower() for i in idirs]
    [i.lower() for i in ifiles]
    [i.lower() for i in iext]
    [x.lower() for x in xdirs]
    [x.lower() for x in xfiles]
    [x.lower() for x in xext]
    for dirpath, dirs, files in os.walk(source):
      if len(idirs): # if any directories perform a reverse exclusion
        for d in list(dirs):
          if d.lower() not in idirs: # remove all dirs not in inclusion list
            if verbose is True: print("Excluding -> " + dirpath + "\\" + d)
            dirs.remove(d)
      for d in list(dirs):
        if d.lower() in xdirs:
          if verbose is True: print("Excluding -> " + dirpath + "\\" + d)
          dirs.remove(d)
      relpath = os.path.relpath(dirpath, source)
      if relpath != "." and relpath != "..":
        if verbose is True and showfiles is True: # everything searched
          if full_paths is True:
            print(source + '\\' + relpath)
          else:
            print(relpath)
        if append is True and no_dirs is not True:
          sources.append(relpath)
          #if dircmd: 
        if callback is not None: callback(sources + "\\" + relpath)
      for filename in list(files):
        exsplit = filename.split('.')
        ext = None
        if len(exsplit) > 1:
          ext = exsplit[-1]
        if len(ifiles): # if any files perform a reverse exclusion
          if filename.lower() not in ifiles:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        if len(iext): # if any extensions perform a reverse exclusion
          if ext is not None and len(ext):
            if ext.lower() not in iext:
              #if verbose is True: print("Excluding ("+ext.lower()+")-> " + dirpath + "\\" + filename)
              continue
          else:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        if filename.lower() in xfiles: # exlcude any files specified
          if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
          continue
        if ext is not None and len(ext):
          if ext.lower() in xext: # exlcude any extensions specified
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        try:
          # TODO: looks like file and extension inclusions would be better here, that way only the files are included instead of trying to do a reverse exclusion which has so far let files with no extensions through
          if relpath != "." and relpath != "..": #
            # os.path.join(dir, path) # TODO: try it and see if it works
            srcfile = relpath + "\\" + filename
          else:
            srcfile = filename
          if showfiles is True: # files found
            if full_paths is True:
              print(source + '\\' + srcfile)
            else:
              print(srcfile)
          if append is True and no_files is not True:
            sources.append(srcfile)
          if callback is not None: callback(sources + "\\" + srcfile)
        except KeyboardInterrupt as e:
          raise # pops up out to the next exception handler
        except Exception as e:
          exception(e)
          if pause_on_error is True: pause()
  except KeyboardInterrupt as e:
    interrupted = True
  except Exception as e:
    exception(e)
    if pause_on_error is True: pause()
  finally:
    if interrupted is True: raise KeyboardInterrupt
  return sources
#-------------------------------------------------------------------------------
#
# listdir2
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def listdir2(source,
              callback=None,
              datetime=None,
              append=True, # false and returned list is always empty (faster if not used?)
              idirs=[],
              ifiles=[],
              iext=[],
              xdirs=[],
              xfiles=[],
              xext=[],
              full_paths=False,
              no_dirs=False,
              no_files=False,
              search=None,
              topdown=True,
              followlinks=False,
              onerror=None):
  if os.path.exists(source) is False: raise FileNotFoundError
  sources = []
  interrupted = False # code review this
  # lowercase all user entries for easier processing
  [i.lower() for i in idirs]
  [i.lower() for i in ifiles]
  [i.lower() for i in iext]
  [x.lower() for x in xdirs]
  [x.lower() for x in xfiles]
  [x.lower() for x in xext]
  # just check this dir
#-------------------------------------------------------------------------------
#
# crawltree2
#
# making a new crawltree so I can modify it and move forward without breaking the old version, hence the 2.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def crawltree2(source,
              callback=None,
              datetime=None,
              append=True, # false and returned list is always empty (faster if not used?)
              idirs=[],
              ifiles=[],
              iext=[],
              xdirs=[],
              xfiles=[],
              xext=[],
              full_paths=False,
              no_dirs=False,
              no_files=False,
              search=None,
              topdown=True,
              followlinks=False,
              onerror=None):
  if os.path.exists(source) is False: raise FileNotFoundError
  sources = []
  interrupted = False # code review this
  try:
    # lowercase all user entries for easier processing
    [i.lower() for i in idirs]
    [i.lower() for i in ifiles]
    [i.lower() for i in iext]
    [x.lower() for x in xdirs]
    [x.lower() for x in xfiles]
    [x.lower() for x in xext]
    # check all directories ...
    for dirpath, dirs, files in os.walk(source, topdown=topdown, onerror=onerror, followlinks=followlinks):
      # idirs
      if len(idirs): # if any directories perform a reverse exclusion
        for d in list(dirs):
          if d.lower() not in idirs: # remove all dirs not in inclusion list
            loginfo("Excluding -> " + dirpath + "\\" + d)
            dirs.remove(d)
      # xdirs      
      for d in list(dirs):
        if d.lower() in xdirs:
          loginfo("Excluding -> " + dirpath + "\\" + d)
          dirs.remove(d)
      # check relpath    
      relpath = os.path.relpath(dirpath, source)
      if relpath != "." and relpath != "..":
        if full_paths is True:
          if callback is not None: callback(source + '\\' + relpath, True)
          if append is True and no_dirs is not True:
            if search:
              if ifallin(search.lower().split(' '), relpath.lower()):
                sources.append(source + '\\' + relpath)
            else:
              sources.append(source + '\\' + relpath)
        else:
          if callback is not None: callback(relpath, True)
          if append is True and no_dirs is not True:
            if search:
              if ifallin(search.lower().split(' '), relpath.lower()):
                sources.append(relpath)
            else:
              sources.append(relpath)
      # check all files ...    
      for filename in list(files):
        # get file parts
        exsplit = filename.split('.')
        ext = None
        if len(exsplit) > 1:
          ext = exsplit[-1]
        # ifiles
        if len(ifiles): # if any files perform a reverse exclusion
          if filename.lower() not in ifiles:
            loginfo("Excluding -> " + dirpath + "\\" + filename)
            continue
        # iext
        if len(iext): # if any extensions perform a reverse exclusion
          if ext is not None and len(ext):
            if ext.lower() not in iext:
              loginfo("Excluding ("+ext.lower()+")-> " + dirpath + "\\" + filename)
              continue
          else:
            loginfo("Excluding -> " + dirpath + "\\" + filename)
            continue
        # xfiles
        if filename.lower() in xfiles: # exlcude any files specified
          loginfo("Excluding -> " + dirpath + "\\" + filename)
          continue
        # xext
        if ext is not None and len(ext):
          if ext.lower() in xext: # exlcude any extensions specified
            loginfo("Excluding -> " + dirpath + "\\" + filename)
            continue
        try:
          if relpath != "." and relpath != "..": #
            srcfile = relpath + "\\" + filename
          else:
            srcfile = filename
          if full_paths is True:
            if callback is not None: callback(source + '\\' + srcfile, False)
            if append is True and no_files is not True:
              if search:
                if ifallin(search.lower().split(' '), srcfile.lower()):
                  sources.append(source + '\\' + srcfile)
              else:
                sources.append(source + '\\' + srcfile)
          else:
            if callback is not None: callback(srcfile, False)
            if append is True and no_files is not True:
              if search:
                if ifallin(search.lower().split(' '), srcfile.lower()):
                  sources.append(srcfile)
              else:
                sources.append(srcfile)
        except KeyboardInterrupt as e:
          raise # pops up out to the next exception handler
        except Exception as e:
          exception(e)
  except KeyboardInterrupt as e:
    interrupted = True
  finally:
    if interrupted is True: raise KeyboardInterrupt
  return sources
#-------------------------------------------------------------------------------
#
# crawltree
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def crawltree(source,
              callback=None,
              datetime=None,
              append=True, # returned list will be empty, saves memory if you aren't going to need it like when you only use the callback or use for the printed output only etc.
              idirs=[],
              ifiles=[],
              iext=[],
              xdirs=[],
              xfiles=[],
              xext=[],
              showfiles=False,
              full_paths=False,
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=False,
              pause_on_error=False,
              debug=False):
# http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
# Numbers Strings Lists Tuples Dictionaries_Maps
# TODO: wild card support in inclusion and exclusion lists
  """ Crawl Files from Source an return them in a list. No wildcard support for inclusion and exclusion lists yet. Callback takes one parameter and that is a file path as string """
  if os.path.exists(source) is False: raise FileNotFoundError
  sources = []
  interrupted = False
  try:
    [i.lower() for i in idirs]
    [i.lower() for i in ifiles]
    [i.lower() for i in iext]
    [x.lower() for x in xdirs]
    [x.lower() for x in xfiles]
    [x.lower() for x in xext]
    for dirpath, dirs, files in os.walk(source):
      if len(idirs): # if any directories perform a reverse exclusion
        for d in list(dirs):
          if d.lower() not in idirs: # remove all dirs not in inclusion list
            if verbose is True: print("Excluding -> " + dirpath + "\\" + d)
            dirs.remove(d)
      for d in list(dirs):
        if d.lower() in xdirs:
          if verbose is True: print("Excluding -> " + dirpath + "\\" + d)
          dirs.remove(d)
      relpath = os.path.relpath(dirpath, source)
      if relpath != "." and relpath != "..":
        if full_paths is True:
          if showfiles is True: print(source + '\\' + relpath)
          if callback is not None: callback(source + '\\' + relpath, True)
        else:
          if showfiles is True: print(relpath)
          if callback is not None: callback(relpath, True)
        if append is True and no_dirs is not True:
          sources.append(relpath)
      for filename in list(files):
        exsplit = filename.split('.')
        ext = None
        if len(exsplit) > 1:
          ext = exsplit[-1]
        if len(ifiles): # if any files perform a reverse exclusion
          if filename.lower() not in ifiles:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        if len(iext): # if any extensions perform a reverse exclusion
          if ext is not None and len(ext):
            if ext.lower() not in iext:
              #if verbose is True: print("Excluding ("+ext.lower()+")-> " + dirpath + "\\" + filename)
              continue
          else:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        if filename.lower() in xfiles: # exlcude any files specified
          if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
          continue
        if ext is not None and len(ext):
          if ext.lower() in xext: # exlcude any extensions specified
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
        try:
          # TODO: looks like file and extension inclusions would be better here, that way only the files are included instead of trying to do a reverse exclusion which has so far let files with no extensions through
          if relpath != "." and relpath != "..": #
            # os.path.join(dir, path) # TODO: try it and see if it works
            srcfile = relpath + "\\" + filename
          else:
            srcfile = filename
          if full_paths is True:
            if showfiles is True: print(source + '\\' + srcfile)
            if callback is not None: callback(source + '\\' + srcfile, False)
          else:
            if showfiles is True: print(srcfile)
            if callback is not None: callback(srcfile, False)
          if append is True and no_files is not True:
            sources.append(srcfile)
        except KeyboardInterrupt as e:
          raise # pops up out to the next exception handler
        except Exception as e:
          exception(e)
          if pause_on_error is True: pause()
  except KeyboardInterrupt as e:
    interrupted = True
  except Exception as e:
    exception(e)
    if pause_on_error is True: pause()
  finally:
    if interrupted is True: raise KeyboardInterrupt
  return sources
#-------------------------------------------------------------------------------
#
# crawltreeAB
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def crawltreeAB(source,
              target,
              callback=None,
              datetime=None,
              append=True, # returned list will be empty, saves memory if you aren't going to need it like when you only use the callback or use for the printed output only etc.
              idirs=[],
              ifiles=[],
              iext=[],
              xdirs=[],
              xfiles=[],
              xext=[],
              showfiles=False,
              full_paths=False,
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=False,
              pause_on_error=False,
              debug=False):
  """ Compare and Print differences between two trees. """
  #if quiet is not True: print("Crawling source ->",source,"... -&- target ->",target,"...")
  if os.path.exists(source) is False: raise FileNotFoundError
  if os.path.exists(target) is False: raise FileNotFoundError
  totalns = time.time_ns()
  try:
    startns = time.time_ns()
    sources = crawltree(source,
                        xdirs=xdirs,
                        xfiles=xfiles,
                        xext=xext,
                        showfiles=False,
                        no_dirs=no_dirs,
                        no_files=no_files,
                        quiet=True,
                        verbose=False,
                        pause_on_error=pause_on_error,
                        debug=debug)
    stimens = time.time_ns() - startns

    startns = time.time_ns()
    targets = crawltree(target,
                        xdirs=xdirs,
                        xfiles=xfiles,
                        xext=xext,
                        showfiles=False,
                        no_dirs=no_dirs,
                        no_files=no_files,
                        quiet=True,
                        verbose=False,
                        pause_on_error=pause_on_error,
                        debug=debug)
    ttimens = time.time_ns() - startns
    # calculate total time spent verifying the trees
    duration = (time.time_ns() - totalns) / 1000 / 1000 / 1000
    tick = 'seconds'
    if duration > 60:
      duration = duration / 60
      tick = 'minutes'
    if duration > 60:
      duration = duration / 60
      tick = 'hours'
    if duration > 60:
      duration = duration / 24
      tick = 'days'
    # https://pyformat.info
    print("This Operation took {0:0.2f} {1} total time".format(duration,tick))
  except KeyboardInterrupt as e:
    print("This Operation has been Terminated by User!")
  return sources, targets
#-------------------------------------------------------------------------------
#
# crawltrees
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def crawltrees(targets,
              callback=None,
              datetime=None,
              append=True, # returned list will be empty, saves memory if you aren't going to need it like when you only use the callback or use for the printed output only etc.
              idirs=[],
              ifiles=[],
              iext=[],
              xdirs=[],
              xfiles=[],
              xext=[],
              showfiles=False,
              full_paths=False,
              no_dirs=False,
              no_files=False,
              quiet=False,
              verbose=False,
              pause_on_error=False,
              debug=False):
  """ Get multiple trees. """ 
  totalns = time.time_ns()
  resources = []
  try:
    # check first so we don't dump out after a long wait
    for target in targets:
      if os.path.exists(target) is False: raise FileNotFoundError
    for target in targets:
      startns = time.time_ns()
      sources = crawltree(target,
                          xdirs=xdirs,
                          xfiles=xfiles,
                          xext=xext,
                          showfiles=False,
                          no_dirs=no_dirs,
                          no_files=no_files,
                          quiet=True,
                          verbose=False,
                          pause_on_error=pause_on_error,
                          debug=debug) 
      ttimens = time.time_ns() - startns
      resources.append(sources)
      print("Crawled targets in {:0.1f} seconds".format(ttimens / 1000 / 1000 / 1000))
    # calculate total time spent verifying the trees
    duration = (time.time_ns() - totalns) / 1000 / 1000 / 1000
    tick = 'seconds'
    if duration > 60:
      duration = duration / 60
      tick = 'minutes'
    if duration > 60:
      duration = duration / 60
      tick = 'hours'
    if duration > 60:
      duration = duration / 24
      tick = 'days'
    # https://pyformat.info
    print("This Operation took {0:0.2f} {1} total time".format(duration,tick))
  except KeyboardInterrupt as e:
    print("This Operation has been Terminated by User!")
  return resources
#-------------------------------------------------------------------------------
#
# copytree
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def copytree(source,
             target,                    # location to copy
             action=True,               # copy files and dirs otherwise loginfo only test mode
             datetime=None,             # if specified only copy files after this date
             follow_symlinks=False,
             xdirs=[],
             xfiles=[],
             xext=[],
             readonly=False,
             showfiles=True,
             no_files=False,            # don't copy any files, directories only
             quiet=False,
             verbose=False,
             pause_on_error=False,
             debug=False,
             refresh=True):
# http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
# Numbers Strings Lists Tuples Dictionaries_Maps
  """ Copy Files from Source to Destination with Source and Destination Comparison Operations, Exclusions and more. """
  if os.path.exists(source) is False: raise FileNotFoundError
  #if os.path.exists(target) is False: raise FileNotFoundError
  try:
    [x.lower() for x in xdirs]
    [x.lower() for x in xfiles]
    [x.lower() for x in xext]
    for dirpath, dirs, files in os.walk(source):
      try:
        if os.path.exists(dirpath) is False:
          if verbose is True: print("Not Found -> " + dirpath)
          if pause_on_error is True: pause()
        for d in list(dirs):
          if d.lower() in xdirs:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + d)
            dirs.remove(d)
        relpath = os.path.relpath(dirpath,source)
        if relpath != "." and relpath != "..":
          destpath = target + "\\" + relpath
        else:
            destpath = target
        if action is True:
          if os.path.islink(destpath):
            print("Remove Link =>", destpath)
            os.chmod(destpath, 0o777)
            os.remove(destpath)
          #print("MAKE DIR:",destpath,os.path.exists(destpath),os.path.islink(destpath))
          os.makedirs(destpath, exist_ok=True)
        for filename in list(files):
          if filename.lower() in xfiles:
            if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
            continue
          ext = filename.split('.')
          if ext is not None and len(ext) > 1:
            if ext[-1].lower() in xext:
              if verbose is True: print("Excluding -> " + dirpath + "\\" + filename)
              continue
          try:
            srcfile = dirpath + "\\" + filename
            destfile = destpath + "\\" + filename
            if os.path.exists(destfile) is True:
              srctime = os.path.getmtime(srcfile)
              desttime = os.path.getmtime(destfile)
              if int(srctime) < int(desttime):
                # i hit this when a file that was being copied and i aborted the copy
                # the file seemed intact but the modified date was not copied over so it
                # was the same as the creation date, in this case it needs to be copied
                # again or at least the file details do but copying is more thorough
                # changing <= below to == so it will copy in this case instead of skipping
                if quiet is False: print("Warning! Source older then target ({0}:{1}) {2}".format(srctime, desttime, srcfile))
                if pause_on_error is True: pause()
                if refresh is False: continue
              if int(srctime) == int(desttime):
                if debug is True: print("(Up-to-date) Skipping ...", srcfile, "->", destfile)
                continue
              if int(srctime) > int(desttime):
                if verbose is True: print("(Out-of-date) Updating ... ({0}:{1}) {2}".format(srctime, desttime, srcfile))
            #print("COPY FILE:",destfile,os.path.exists(destfile),os.path.islink(destfile))
            if os.path.islink(destfile):
              print("Remove Link =>", destfile)
              os.chmod(destfile, 0o777)
              os.remove(destfile)
            if showfiles is True: print("Copying ...",srcfile, "->", destfile)
            if action is True and no_files is not True:
              # DONE: copy read only files and check what it does copy, this should be copying everything.
              # TODO: check if it is read only first, what is most performative?
              try:
                # TODO: this doesn't copy ACLs and ADS! must find a file copy that copies all bits. ADS is important for DFS!
                copy2(srcfile, destfile, follow_symlinks=follow_symlinks) # PermissionError ibE207.tmp # Incorrect function
              except PermissionError:
                os.chmod(destfile, stat.S_IWUSR|stat.S_IREAD) # FileNotFoundError
                if verbose is True: print("File is read only, overwriting...")
                # let the outer exception handler handle the next copy
                copy2(srcfile, destfile, follow_symlinks=follow_symlinks)
              finally:
                if readonly is True: os.chmod(destfile, stat.S_IREAD)
          except KeyboardInterrupt as e:
            raise # pops up out to the next exception handler
          except FileExistsError as e:
            # TODO: 
            #os.chmod(destfile, stat.S_IWRITE)
            if action is True: os.unlink(destfile)
          except Exception as e:
            exception(e)
            if pause_on_error is True: pause()
      except PermissionError as e:
        # TODO: if action is True:
        #os.chmod(destfile, stat.S_IWRITE)
        #os.rmdir(destfile)
        #os.remove(destfile)
        #shutil.rmtree(destfile)
        os.unlink(destfile)
      except Exception as e:
        exception(e)
        if pause_on_error is True: pause()
  except KeyboardInterrupt as e:
    print("The Operation has been Terminated by User!")
  except Exception as e:
    exception(e)
    if pause_on_error is True: pause()
#-------------------------------------------------------------------------------
#
# abtree
#
# testing for now as it just prints out information about target vs source
# copied from copytree
#
# for operations that use a source as master and a target for deviations
# https://stackoverflow.com/questions/42720627/python-os-walk-to-certain-level
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@trace(3)
def abtree(source,
         target,                    # location to copy
         callback=None,
         action=True,               # copy files and dirs otherwise loginfo only test mode
         datetime=None,             # if specified only copy files after this date
         xdirs=[],
         xfiles=[],
         xext=[],
         readonly=False,
         no_files=False,            # don't copy any files, directories only
         refresh=True,
         topdown=True,
         followlinks=False,
         onerror=None):
# http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
# Numbers Strings Lists Tuples Dictionaries_Maps
  """ Crawl source and callback on source hits with destination paths for custom operations. Mimics sync characteristics. """
  if os.path.exists(source) is False: raise FileNotFoundError
  #if os.path.exists(target) is False: raise FileNotFoundError
  try:
    [x.lower() for x in xdirs]
    [x.lower() for x in xfiles]
    [x.lower() for x in xext]
    # https://docs.python.org/3/library/os.html
    for dirpath, dirs, files in os.walk(source, topdown=True, onerror=None, followlinks=followlinks):
      try:
        if os.path.exists(dirpath) is False:
          logerror("Not Found -> " + dirpath)
        for d in list(dirs):
          if d.lower() in xdirs:
            loginfo("Excluding -> " + dirpath + "\\" + d)
            dirs.remove(d)
        relpath = os.path.relpath(dirpath, source)
        if relpath != "." and relpath != "..":
          destpath = target + "\\" + relpath
        else:
          destpath = target
        #try:
        if callback: callback(dirpath, destpath, True)
        #except KeyboardInterrupt as e:
        #  raise # pops up out to the next exception handler
        #except Exception as e:
       #   exception(e)
        for filename in list(files):
          if filename.lower() in xfiles:
            loginfo("Excluding -> " + dirpath + "\\" + filename); continue
          ext = filename.split('.')
          if ext is not None and len(ext) > 1:
            if ext[-1].lower() in xext:
              loginfo("Excluding -> " + dirpath + "\\" + filename); continue
          #try:
          if callback: callback(dirpath + "\\" + filename, destpath + "\\" + filename, False)
          #except KeyboardInterrupt as e:
          #  raise # pops up out to the next exception handler
          #except Exception as e:
          #  exception(e)
      except Exception as e:
        exception(e)
  except KeyboardInterrupt as e:
    print("The Operation has been Terminated by User!")
  except Exception as e:
    exception(e)
#-------------------------------------------------------------------------------
#
# recursetree
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
@trace(3)
def recursetree(source, callback, tdepth=0):
  return _rtree_internal(source, source, callback, 0, 0, tdepth=tdepth)
#-------------------------------------------------------------------------------
#
# rtree_internal
#
# https://stackoverflow.com/questions/10960477/how-to-read-file-attributes-in-a-directory#10960485
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
def _rtree_internal(source, target, callback, files:int, dirs:int, cdepth=0, tdepth=0, stop=False):
  #loginfo("SOURCE:", source)
  #loginfo("CALLBACK:", type(callback))
  if tdepth == 0 or cdepth < tdepth:
    #if stop: return
    try:
      for f in os.listdir(target): # PermissionError: [WinError 5] Access is denied: 'C:\\System Volume Information'
        fullpath = os.path.join(target, f)
        if os.path.isdir(fullpath):
          #inspector(fullpath, True)
          # TODO: needs relative path for this to work
          #loginfo("Folder:", cdepth, fullpath)
          stop = callback(source, fullpath, cdepth, True)
          if stop: continue 
          files, dirs = _rtree_internal(source, fullpath, callback, files, dirs +1, cdepth=cdepth + 1, tdepth=tdepth, stop=stop)
        else:
          #loginfo("File  :", cdepth, fullpath)
          files += 1
          stop = callback(source, fullpath, cdepth, False)
    except PermissionError:
      logwarn("Access Denied ->", target)
  return files, dirs
#-------------------------------------------------------------------------------
#
# scantree
#
# efficient for getting file information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
def scantree(source, callback):
  with os.scandir(source) as dir_entries:
    for entry in dir_entries:
      #info = entry.stat() # implement in callback
      callback(entry)
      #print(info.st_mtime)
#-------------------------------------------------------------------------------
#
# pathtree
#
# Path('File').is_symlink() = True | False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
def pathtree(source, callback):
  for path in Path(source).iterdir():
    #info = path.stat()
    callback(path)
    #print(info.st_mtime)
#-------------------------------------------------------------------------------
#
# modestring
#
# https://docs.python.org/3/library/os.html#os.stat
# https://docs.python.org/3/library/stat.html
# https://docs.python.org/3/library/os.html#os.chmod
#
# TODO: split into o function that returns a dict and then one that formats the string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def modestring(mode):  
  loginfo(type(mode), mode)
  isdir = {True: 1, False: 0}[stat.S_ISDIR(mode)] # Return non-zero if the mode is from a directory.
  ischr = {True: 1, False: 0}[stat.S_ISCHR(mode)] # Return non-zero if the mode is from a character special device file.
  isblk = {True: 1, False: 0}[stat.S_ISBLK(mode)] # Return non-zero if the mode is from a block special device file.
  isreg = {True: 1, False: 0}[stat.S_ISREG(mode)] # Return non-zero if the mode is from a regular file.
  isfifo = {True: 1, False: 0}[stat.S_ISFIFO(mode)] # Return non-zero if the mode is from a FIFO (named pipe).
  islnk = {True: 1, False: 0}[stat.S_ISLNK(mode)] # Return non-zero if the mode is from a symbolic link.
  issock = {True: 1, False: 0}[stat.S_ISSOCK(mode)] # Return non-zero if the mode is from a socket.
  isdoor = {True: 1, False: 0}[stat.S_ISDOOR(mode)] # Return non-zero if the mode is from a door.
  #New in version 3.4.
  isport = {True: 1, False: 0}[stat.S_ISPORT(mode)] # Return non-zero if the mode is from an event port.
  # New in version 3.4.
  iswht = {True: 1, False: 0}[stat.S_ISWHT(mode)] # Return non-zero if the mode is from a whiteout.
  # New in version 3.4.
  #Two additional functions are defined for more general manipulation of the file’s mode:
  imode = stat.S_IMODE(mode) # Return the portion of the file’s mode that can be set by os.chmod()—that is, the file’s permission bits, plus the sticky bit, set-group-id, and set-user-id bits (on systems that support them).
  ifmt = stat.S_IFMT(mode) # Return the portion of the file’s mode that describes the file type (used by the S_IS*() functions above).
  return "dir:{}, chr:{}, blk:{}, reg:{}, fifo:{}, lnk:{}, sock:{}, door:{}, port:{}, wht:{}, imode:{}, ifmt:{},".format(isdir,ischr,isblk,isreg,isfifo,islnk,issock,isdoor,isport,iswht,imode,ifmt)
#-------------------------------------------------------------------------------
#
# is_readonly
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def is_readonly(imode):  
  return not (imode & stat.S_IWRITE == stat.S_IWRITE and imode & stat.S_IREAD == stat.S_IREAD)
#-------------------------------------------------------------------------------
#
# <|:) Wizard
#
# Source file path 
# src = '/home/ihritik/file.txt'  
# Destination file path 
# dst = '/home/ihritik/Desktop/file(symlink).txt'
# os.symlink(src, dest)
# https://csatlas.com/python-create-symlink/
# https://docs.python.org/3/library/os.html
# https://www.geeksforgeeks.org/python-os-symlink-method/#
#-------------------------------------------------------------------------------
