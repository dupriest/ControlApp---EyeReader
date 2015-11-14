import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import json

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