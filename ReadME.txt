To Create Executable: (if there is no other additional file needed in the exe)
	pyinstaller --onefile --windowed --icon=app.ico Messenger.py 


For this program, we have a ico file to add

Create the spec file:
	pyi -makespec --onefile Messenger.py

Add line to spec:
	a.datas += [('app.ico', 'E:\\Grizder\\OneDrive\\Desktop\\Code Tmp\\Instant Messenger\\app.ico', 'DATA')]

Now create exe:
	pyinstaller --onefile --windowed --icon=app.ico Messenger.spec



