import easygui
import os
import sys
import datetime
import shutil

files = os.listdir(os.getcwd())
users = []
bookshelves = {}
master_loc = os.getcwd() + "\\ControlApp\\EyeReader v1.5 Cross-Browser\\Minimal EyeReader\\program files\\"
master_copy = [master_loc + "Bookshelf.txt", open(master_loc + "Bookshelf.txt", 'r').read(), open(master_loc + "Bookshelf_Date.txt", "r").read()]
options = []
user_options = []
options.append('Create User')
options.append('User-Bookshelf List')

for f in files:
	try:
		if 'Eye Reader Version.txt' in os.listdir(os.getcwd() + '\\' + f):
			users.append(f)
			user_options.append(f)
	except WindowsError:
		pass

for u in users:
	loc = os.getcwd() + "\\" + u + "\\Minimal EyeReader\\program files\\"
	b = [loc + "Bookshelf.txt", open(loc + "Bookshelf.txt", 'r').read(), open(loc + "Bookshelf_Date.txt", 'r').read()]
	bookshelves[u] = b
options.append('Manage Users')
options.append('Reinstall or Update User')
options.append('Exit')
user_options.append('Return')

choice = easygui.buttonbox('What would you like to do?', 'ControlApp', options)
while choice != 'Exit':
	if choice == 'Reinstall or Update User':
		user1 = easygui.buttonbox('Select a user to reinstall or update to the most recent version', 'ControlApp', user_options)
		if user1 != 'Return':
			final_call = easygui.ynbox('Are you sure that you want to reinstall/update ' + user1 + '?')
			while not final_call:
				user1 = easygui.buttonbox('Select a user to reinstall or update to the most recent version', 'ControlApp', user_options)
				if user1 == 'Return':
					break
				final_call = easygui.ynbox('Are you sure that you want to reinstall/update ' + user1 + '?')
			if user1 != 'Return':
				shutil.rmtree(os.getcwd() + "\\" + user1 + "\\Minimal EyeReader\\program files")
				shutil.copytree(os.getcwd() + "\\" + "EyeReader v1.5 Cross-Browser\\Minimal EyeReader\\program files", os.getcwd() + "\\" + user1 + "\\Minimal EyeReader\\program files")
				f = open(bookshelves[user1][0], 'w')
				f.write(bookshelves[user1][2])
				f.close()
				bookshelves[user1][1] = bookshelves['EyeReader v1.5 Cross-Browser'][1]
				#bookshelves[user1][2] = bookshelves['EyeReader v1.5 Cross-Browser'][2]
				easygui.msgbox('Reinstall/Update Complete!')
	elif choice == 'User-Bookshelf List':
		msg = 'User-Bookshelf List\n\n'
		for u in users:
			msg = msg + u + ':    ' + bookshelves[u][1] + "    " + bookshelves[u][2] + '\n'
		easygui.msgbox(msg)
	elif choice == 'Manage Users':
		user = easygui.buttonbox('Choose a user', 'ControlApp', user_options)
		if user != 'Return':
			loc = os.getcwd() + "\\" + user + "\\Minimal EyeReader\\program files\\Bookshelf.txt"
			f = open(loc, 'r')
			current_bookshelf = f.read()
			f.close()
			f = open(loc, 'w')
			msg = "Bookshelf is currently: " + current_bookshelf + "\n Would you like to switch it to Bookshelf "
			if current_bookshelf == 'A':
				msg = msg + 'B?'
			else:
				msg = msg + 'A?'
			title = 'Change Bookshelf'
			if easygui.ynbox(msg, title):
				if current_bookshelf == 'A':
					f.write('B')
					f.close()
					bookshelves[user][1] = 'B'
				if current_bookshelf == 'B':
					f.write('A')
					f.close()
					bookshelves[user][1] = 'A'
				d = open(os.getcwd() + "\\" + user + "\\Minimal EyeReader\\program files\\Bookshelf_Date.txt", 'w')
				current_date = str(datetime.datetime.now())

				for i in range(0, len(current_date)):
					if current_date[i] == '.':
						current_date = current_date[0:i]
						break
				d.write(current_date)
				d.close()
				bookshelves[user][2] = current_date

			else:
				f.write(current_bookshelf)
				f.close()
		else:
			pass
	elif choice == 'Create User':
		msg = 'Enter a name and bookshelf for the new user:'
		title = 'Create New User'
		fieldNames = ['User name:', 'Bookshelf:']
		new_user = easygui.multenterbox(msg, title, fieldNames)
		if new_user is not None:
			while new_user[0] == '' or (new_user[1] != 'A' and new_user[1] != 'B'):
				if new_user[0] == '' and (new_user[1] == 'A' or new_user[1] == 'B'):
					new_user = easygui.multenterbox('Please enter value for both fields', title, fieldNames, ['', new_user[1]])
				elif new_user[0] != '' and (new_user[1] != 'A' or new_user[1] != 'B'):
					new_user = easygui.multenterbox('Please enter value for both fields', title, fieldNames, [new_user[0]])
				else:
					new_user = easygui.multenterbox('Please enter value for both fields', title, fieldNames)
			loc = os.getcwd() + "\\" + "EyeReader v1.5 Cross-Browser" + "\\Minimal EyeReader\\program files\\Bookshelf.txt"
			f = open(loc, 'w')
			f.write(new_user[1])
			f.close()
			loc = os.getcwd() + "\\" + "EyeReader v1.5 Cross-Browser" + "\\Minimal EyeReader\\program files\\Bookshelf_Date.txt"
			f = open(loc, 'w')
			current_date = str(datetime.datetime.now())
			for i in range(0, len(current_date)):
					if current_date[i] == '.':
						current_date = current_date[0:i]
						break
			f.write(current_date)
			f.close()
			shutil.copytree(os.getcwd() + "\\" + "EyeReader v1.5 Cross-Browser", os.getcwd() + "\\" + new_user[0])
			bookshelves[new_user[0]] = [os.getcwd() + "\\" + new_user[0] + "\\Minimal EyeReader\\program files\\Bookshelf.txt", new_user[1], current_date]
			users.append(new_user[0])
			user_options.remove('Return')
			user_options.append(new_user[0])
			user_options.append('Return')
			easygui.msgbox('User ' + new_user[0] + ' created!' + '\n' + 'Bookshelf: ' + new_user[1] + '\n' + 'Date: ' + current_date)
	choice = easygui.buttonbox('What would you like to do?', 'ControlApp', options)
