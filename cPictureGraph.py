import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import json

data = []
j_file = "eyegazedata_2015-11-02-15-54-17.json"

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
	print(page, start, len(data)-1)
	for i in range(start,len(data)):
	    if t == page and data[i].get('type') == 'PageTurn':
	        #print(page)
	        #print(data[i].get('page'))
	        start = i
	        #print(start)
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
	                     facecolor="#3e1eff") # Makes a visible box
	plt.gca().add_patch(pict)
	textb = plt.Rectangle((text.get('tl'), text.get('tt')), text.get('tr') - text.get('tl'),text.get('tb') - text.get('tt'),
	                      facecolor="#008f25")
	plt.gca().add_patch(textb)
	plt.plot(x_coords, y_coords, 'o', color='#f6ff71', markeredgewidth=0.0)
	plt.plot(x_fix, y_fix, 'yo', markeredgewidth=0.0) 
	plt.plot(x_fix, y_fix, 'y')
	plt.axis([0, 1920, 0, 1080])
	plt.gca().invert_yaxis()
	for i in range(0, len(x_fix)):
		plt.annotate('%s' %(i+1), xy=(x_fix[i], y_fix[i]), xytext=(x_fix[i]+1, y_fix[i]+1))
	plt.savefig(j_file[0:-5] + '_' + str(page) + '.png')
	plt.clf()
	page = page + 1