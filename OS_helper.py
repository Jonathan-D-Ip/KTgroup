import os
import sys
import time

def getTimeStamp():
	return str(time.strftime("%Y:%m:%d-%H:%M:%S"))

def getFileTimeStamp():
	return str(time.strftime("%Y%m%d-%H%M%S"))

def listFilesOfGivenExt(path, ext=None) :
	l = []
	for f in os.listdir(path) :
		if ext==None :
			l.append(f)
		elif f.endswith(ext) :
			l.append(f)
	return l

def listOnlyDir(path):
	oup_dir=[]
	for d in os.listdir(path) :
		if os.path.isdir(os.path.join(path,d)) :
			oup_dir.append(d)
	return oup_dir

def checkDir(path, dir_list):
	# Takes a list of dir name and return list of bool indicating the existance of dir in PATH
	checkList = []
	ext_dir_List = listOnlyDir(path)
	if path[-1] == '/' :
		path = path[:-1]
	for i in range(len(dir_list)) :
		checkList.append(dir_list[i] in ext_dir_List)
	return checkList

def getCurrentDir():
	return os.path.realpath(".")

def exitDir():
	print " [ ", getTimeStamp(), " ] ", " <<< Exiting :: ", getCurrentDir(), " ..."
	os.chdir(os.path.realpath(".."))

def chDir(dir) :
	if dir == ".." :
		exitDir()
		return
	print " [ ", getTimeStamp(), " ] ", " >>> Entering :: ", os.path.join(getCurrentDir(),dir), " ..."
	os.chdir(os.path.join(os.path.realpath("."),dir))

def printCwd():
	print " [ ", getTimeStamp(), " ] Current directory :: ", getCurrentDir(), " ..."

def checkDirExistinCWD(dir):
	return os.path.isdir(os.path.join(getCurrentDir(),dir))

def createDirAtCWD(dir):
	if checkDir(getCurrentDir(), [dir])[0] :
		print " [ ", getTimeStamp(), " ] The directory exists ..."
	else :
		os.makedirs(os.path.join(getCurrentDir(), dir))
		print " [ ", getTimeStamp(), " ] Creating ", dir," ..."

def getFileName(fn) :
	return ".".join(fn.split('.')[:-1])

timer={}

def startTimer(tag) :
	if not tag :
		tag = getTimeStamp()
	timer[tag] = time.time()
	print " [ ", getTimeStamp(), " ] ", " Start timer :: ", timer[tag]
	return tag

def endTimer(tag) :
	t = time.time()
	print " [ ", getTimeStamp(), " ] ", " Stop timer :: ", t
	print " [ ", getTimeStamp(), " ] ", " Time used in seconds :: ", t - timer[tag]
	del timer[tag]
	return

if __name__!="__main__" :
	print "Importing OS_helper"
