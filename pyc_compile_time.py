import os
import py_compile as pc
from datetime import datetime

global_compile_time = 0
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(os.getcwd()):
    print(root, dirs, files)
    """path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)
    print(root, dirs, files)"""
    

    
    for filename in files:
    	if filename.endswith(".py"):
	    	t1 = datetime.now()
	    	pc.compile(os.path.join(root, filename))
	    	t2 = datetime.now()
	    	global_compile_time += ((t2 - t1).seconds + (t2 - t1).microseconds/1e6)

print(global_compile_time)
