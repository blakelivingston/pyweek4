# RunMeToCreatePackage.py
# Version 0.2
# 2007/04/11
#
# This program was created by Clint (HanClinto) Herron for the April 2007 PyWeek competition.
#
# It packages up basic games created with the Skellington app as EXE files.
# It requires that py2exe be installed on your system.
# Simply run this script, and it will take care of the rest.
#
# This source program is released into the public domain

from distutils.core import setup
import py2exe
import sys
import glob

print "ATTENTION: THIS SCRIPT MUST BE RUN FROM WITHIN THE LIB DIRECTORY" # If someone would like to change this fact, I'm open to suggestions for the best way to do it.
print ""
print "INTRODUCTION:"
print "This program packages up basic games created with the Skellington framework."
print "It works on my machine for my game,"
print "but I can't guarantee that it will work on yours for yours."
print "Py2exe generally does a great job of automatically packaging dependencies,"
print "but I can't guarantee you won't need to tweak with all of this."
print "Still, I hope this give you a good push in the right direction.\n"

# First step is to create a temporary launcher file, similar to the run_game.py file, that has the name of the EXE that they wish to create. This is a workaround to a problem where EXEs created with py2exe cannot be renamed to anything other than that which they were originally created with (or else they won't run properly). I don't know of the proper py2exe option to fix this.

program_listing = "#This is an automatically generated file that can be deleted\nimport main\nmain.main()" # The basics needed to run a game packaged with the skellington
filename = 'Slacker.py' # The name of the temporary launcher script to create

filename = raw_input("What is the name of the executable that you wish to create (example: BubbleKong.exe or Slacker.exe) ? ")
package_name = filename.replace(".exe", "") # Remove .exe from the end of the file (if it was added at all)
filename = package_name + ".py" # Add .py to the end so that we can create this as a script file

print "\nCreating our launcher script file '" + filename + "'\n"

FILE = open(filename,"w")
FILE.write(program_listing)
FILE.close()

# Now that we have our script file, we add command line arguments to execute py2exe with the proper bundle options
sys.argv.append("py2exe")
sys.argv.append("--bundle")
sys.argv.append("2")
	
con_win_choice = 0
print "Do you want to build (1) an app with a visible console, or (2) a Windows app with no visible console?"

while (con_win_choice < 1 or con_win_choice > 2):
	con_win_choice = input("Please enter either 1 or 2: ")

if (con_win_choice == 1): # If they chose a console...
	setup(
		console=[filename],
		zipfile=None,
		dist_dir=package_name,
	    data_files=[ ("data",   glob.glob("../data/*.*")),
					 (".", glob.glob("../README.txt"))]
		)
else: # If they chose to create a Windows app...
	setup(
		windows=[
			{
				"script": filename,
				"icon_resources": [(1, "py.ico")]
			}
		],
		zipfile='resources.zip',
		dist_dir=package_name,
	    data_files=[ ("data",   glob.glob("../data/*.*")),
					 (".", glob.glob("../README.txt"))]
		)

print "\n\nThe game has now been built."
print "If there were any errors, they will be in the listing above."
print "Assuming you followed the basic Skellington model,"
print "your game and everything it needs will now be in the /lib/dist directory."
print "Rename the dist directory to be what you want, then zip it up, and publish it."
print "Enjoy!"
