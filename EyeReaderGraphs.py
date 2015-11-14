import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import json

def cPictureGraph(j_file):
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
        #print(page, start, len(data)-1)
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

def cLineGraph(j_file):
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
     
    # THESE TWO LINES IMPLEMENT THE READING POINT PLOT FUNCTIONALITY        
    #plt.plot(x_times, x_coords, 'go')
    #plt.plot(x_times, x_coords, 'g')

    plt.axis([0, time[-1], -0.5, 2.5])
    plt.yticks([0, 1, 2], ['Other', 'Picture', 'Text'], size='small')
    plt.xticks(page_turns, pages, size='small')
    plt.xlabel('Page')
    plt.ylabel('Eye Location on Page')
    plt.savefig('linegraph' + j_file[11:-5] + '.png')