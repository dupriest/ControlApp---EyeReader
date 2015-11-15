import easygui
import os
import sys
import datetime
import shutil
import Tkinter,tkFileDialog
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import pandas as pd
from pandas import DataFrame
from pandas import Series
import json
#import EyeReaderGraphs

class EyeReaderGraphs:
	def cPictureGraph(self, j_file):
	    data = []

	    with open(j_file) as f:
	        for line in f:
	            data.append(json.loads(line))
	    data = data[0]

	    pic = []
	    text = []
	    start = 0
	    page = 1
	    t = 0

	    while start < len(data) - 1:
	        x_coords = []
	        y_coords = []
	        x_fix = []
	        y_fix = []
	        for i in range(start,len(data)):
	            if t == page and data[i].get('type') == 'PageTurn':
	                start = i
	                break
	            if (data[i].get('type') == 'SampleGaze' or data[i].get('type') == 'SampleFixation') and t > page-1:
	                x_coords.append(data[i].get('x'))
	                y_coords.append(data[i].get('y'))
	                if(data[i].get('type') == 'SampleFixation' and data[i].get('event_type') == 2):
	                    x_fix.append(data[i].get('x'))
	                    y_fix.append(data[i].get('y'))
	            if data[i].get('type') == 'PageTurn':
	                t = t + 1
	            if data[i].get('type') == 'Picture':
	                pic = data[i]
	            if data[i].get('type') == 'Text':
	                text = data[i]
	            if i == len(data)-1:
	                start = i
	        
	        pict = plt.Rectangle((pic.get('pl'), pic.get('pt')), (pic.get('pr') - pic.get('pl')),(pic.get('pb') - pic.get('pt')), 
	                             facecolor="#097BCD", edgecolor="none", linewidth=3) # Makes a visible box
	        plt.gca().add_patch(pict)
	        textb = plt.Rectangle((text.get('tl'), text.get('tt')), text.get('tr') - text.get('tl'),text.get('tb') - text.get('tt'),
	                              facecolor="#090D9F", edgecolor="none", linewidth=3)
	        plt.gca().add_patch(textb)
	        plt.plot(x_coords, y_coords, 'o', color='#FF6600', markeredgewidth=0.0, alpha=0.6, markersize=10)
	        plt.plot(x_fix, y_fix, color='#FF3300')
	        plt.axis([0, 1920, 0, 1080])
	        plt.gca().invert_yaxis()
	        for i in range(0, len(x_fix)):
	            plt.plot(x_fix[i], y_fix[i], 'o', color='#FF3300', markersize=20, markeredgecolor='#FFFFFF') 
	            plt.annotate('%s' %(i+1), xy=(x_fix[i], y_fix[i]), xytext=(x_fix[i]-25, y_fix[i]+10), color='#ffffff')
	        plt.suptitle('Page ' + str(page), fontsize=20)
	        plt.xlabel('Width(pixels)', fontsize=15)
	        plt.ylabel('Height(pixels)', fontsize=15)
	        plt.savefig(j_file[0:-48] + "Picture Graphs/" + j_file[-36:-5] + '_' + str(page) + '.png')
	        plt.clf()
	        page = page + 1
	    print('Picture graph for ' + j_file + ' complete!')

	def cLineGraph(self, j_file):
	    data = []

	    with open(j_file) as f:
	        for line in f:
	            data.append(json.loads(line))
	    data = data[0]

	    in_other = 0
	    in_picture = 1
	    in_text = 2

	    values = []
	    time = []
	    x_coords = []
	    x_times = []

	    page_turns = []
	    pages = []

	    pic = []
	    text = []
	    p = 1
	    t0 = 0
	    first = 0

	    for i in range(0, len(data)):
	        if data[i].get('type') == 'Picture':
	            pic = data[i]
	            #print(pic, i)
	        if data[i].get('type') == 'Text':
	            text = data[i]
	            if first == 0:
	                page_turns.append(0)
	            else:
	                page_turns.append(data[i+1].get('timestamp') - t0)
	            pages.append(p)
	            p = p + 1
	            #print(text, i)
	        if data[i].get('type') == 'SampleGaze' or data[i].get('type') == 'SampleFixation':
	        #if data[i].get('type') == 'SampleFixation': # comment out line above and use this one for only fixation data
	            if first == 0:
	                t0 = data[i].get('timestamp')
	                first = 1
	            time.append(data[i].get('timestamp') - t0)
	            x = data[i].get('x')
	            y = data[i].get('y')
	            if x < pic.get('pr') and x > pic.get('pl') and y < pic.get('pb') and y > pic.get('pt'):
	                values.append(in_picture)
	            elif x < text.get('tr') and x > text.get('tl') and y < text.get('tb') and y > text.get('tt'):
	                values.append(in_text)
	                x_coords.append(x)
	                x_times.append(data[i].get('timestamp') - t0)
	            else:
	                values.append(in_other)
	    d = []
	    v = values[0]
	    vs = []
	    ts = []
	    vs.append(v)
	    ts.append(time[0])
	    for i in range(1, len(values)):
	        if values[i] == v:
	            vs.append(v)
	            ts.append(time[i])
	        else:
	            d.append([ts, vs])
	            vs = []
	            ts = []
	            v = values[i]
	            vs.append(v)
	            ts.append(time[i])
	    for i in range(0, len(x_times)):
	        x_coords[i] = ((1/1920.0)*(x_coords[i])) + 1.5

	    for plot in d:
	        if plot[1][0] == 0: # other
	            plt.plot(plot[0], plot[1], 'k', linewidth=10)
	        elif plot[1][0] == 1: # picture
	            plt.plot(plot[0], plot[1], 'b', linewidth=10)
	        elif plot[1][0] == 2:
	            plt.plot(plot[0], plot[1], 'g', linewidth=10)
	    plt.axis([0, time[-1], -0.5, 2.5])
	    plt.yticks([0, 1, 2], ['Other', 'Picture', 'Text'], size='small')
	    plt.xticks(page_turns, pages, size='small')
	    plt.xlabel('Page')
	    plt.ylabel('Eye Location on Page')
	    plt.savefig(j_file[0:-48] + "Line Graphs\\" + j_file[-36:-5] + '_linegraph.png')
	    print('Line graph for ' + j_file + ' complete!')

	def cCSV(self, j_file):
	    def json_to_df(j_file):
	        page = ''
	        pic = ''
	        text = ''
	        point = ''
	        point_list = []
	        with open(j_file) as data_file:    
	            data = json.load(data_file)
	            for i in range(0, len(data)):
	                if data[i]['type'] == 'PageTurn':
	                    page = data[i]
	                elif data[i]['type'] == 'Picture':
	                    pic = data[i]
	                elif data[i]['type'] == 'Text':
	                    text = data[i]
	                elif data[i]['type'] == 'SampleGaze':
	                    point = data[i]
	                    point.update(page)
	                    point.update(pic)
	                    point.update(text)
	                    point['type'] = u'SampleGaze'
	                    point_list.append(point)
	                elif data[i]['type'] == 'SampleFixation':
	                    point = data[i]
	                    point.update(page)
	                    point.update(pic)
	                    point.update(text)
	                    point['type'] = u'SampleFixation'
	                    point_list.append(point)
	            df = DataFrame(point_list)
	            start_time = df['timestamp'].min()
	            df['timestamp'] = df['timestamp'] - start_time
	            df = df.sort('timestamp')
	            return df

	    df = json_to_df(j_file)
	    loc = j_file[0:-48] + "CSVs\\" + j_file[-36:-5] + '.csv'
	    df.to_csv(loc)
	    print('CSV for ' + j_file + ' complete!')

EyeReaderGraphs = EyeReaderGraphs();
files = os.listdir(os.getcwd())
users = []
bookshelves = {}
master_loc = os.getcwd() + "\\ControlApp - EyeReader\\EyeReader v1.5 Cross-Browser\\Minimal EyeReader\\program files\\"
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
options.append('Create CSVs or Graphs')
options.append('Exit')
user_options.append('Return')

choice = easygui.buttonbox('What would you like to do?', 'ControlApp', options)
while choice != 'Exit':
	if choice == 'Create CSVs or Graphs':
		select = easygui.buttonbox('What kind of graph would you like to make?', 'ControlApp', ['CSV File', 'Line Graph', 'Picture Graph', 'Return'])
		if select != 'Return':
			root = Tkinter.Tk()
			root.withdraw()
			test = 0
			first = 0
			while test == 0:
				if first == 0:
					files = tkFileDialog.askopenfilenames(parent=root, title="Select json files from a user's data folder")
					first = 1
				else:
					files = tkFileDialog.askopenfilenames(parent=root, title="A file you selected was not a json file. Please select again.")
				test = 1
				for f in files:
					if f[-4::] != 'json':
						test = 0
						break;
			if type(files) == tuple:
				if select == 'CSV File':
					for f in files:
						EyeReaderGraphs.cCSV(f)
				if select == 'Line Graph':
					for f in files:
						EyeReaderGraphs.cLineGraph(f)
				if select == 'Picture Graph':
					for f in files:
						EyeReaderGraphs.cPictureGraph(f)
				easygui.msgbox('Files created!')
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
				shutil.copytree(os.getcwd() + "\\ControlApp - EyeReader\\" + "EyeReader v1.5 Cross-Browser\\Minimal EyeReader\\program files", os.getcwd() + "\\" + user1 + "\\Minimal EyeReader\\program files")
				f = open(bookshelves[user1][0], 'w')
				f.write(bookshelves[user1][2])
				f.close()
				bookshelves[user1][1] = master_copy[1]
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
			loc = os.getcwd() + "\\ControlApp - EyeReader\\" + "EyeReader v1.5 Cross-Browser" + "\\Minimal EyeReader\\program files\\Bookshelf.txt"
			f = open(loc, 'w')
			f.write(new_user[1])
			f.close()
			loc = os.getcwd() + "\\ControlApp - EyeReader\\" + "EyeReader v1.5 Cross-Browser" + "\\Minimal EyeReader\\program files\\Bookshelf_Date.txt"
			f = open(loc, 'w')
			current_date = str(datetime.datetime.now())
			for i in range(0, len(current_date)):
					if current_date[i] == '.':
						current_date = current_date[0:i]
						break
			f.write(current_date)
			f.close()
			shutil.copytree(os.getcwd() + "\\ControlApp - EyeReader\\" + "EyeReader v1.5 Cross-Browser", os.getcwd() + "\\" + new_user[0])
			bookshelves[new_user[0]] = [os.getcwd() + "\\" + new_user[0] + "\\Minimal EyeReader\\program files\\Bookshelf.txt", new_user[1], current_date]
			users.append(new_user[0])
			user_options.remove('Return')
			user_options.append(new_user[0])
			user_options.append('Return')
			easygui.msgbox('User ' + new_user[0] + ' created!' + '\n' + 'Bookshelf: ' + new_user[1] + '\n' + 'Date: ' + current_date)
	choice = easygui.buttonbox('What would you like to do?', 'ControlApp', options)
