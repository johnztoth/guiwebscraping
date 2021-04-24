"""
Update to the Agents model

Include animation with GUI and Agent start position from Web Scraping

"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation
import agentframeworkweb
import random
import tkinter
import requests
import bs4

num_of_agents = 10
num_of_iterations = 10
neighbourhood = 10
no_rows=100
no_cols=100

agents = []
shuffled = []
environment=[]

fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

""" create flat environment """
for i in range(1, no_rows):    
    rowlist=[]
    for j in range(1, no_cols):  
        rowlist.append(100)     
    environment.append(rowlist)

""" import starting positions from webpage """
r = requests.get('https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')

content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

""" Make the agents using the Agent class """
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframeworkweb.Agent(environment, agents, y, x))

def update(frame_number):
    print("frame_number = ", frame_number)
    print("num_of_iterations = ", num_of_iterations)
    fig.clear()   

    """ Move the agents, eat the environment, and share if necessary """
    for j in range(num_of_iterations):
        shuffled = random.sample(agents,len(agents)) # create a new shuffled list
        for i in range(num_of_agents):
            shuffled[i].move()
            shuffled[i].eat()
            shuffled[i].share_with_neighbours(neighbourhood)

    """ plot agent positions and environment """
    for i in range(num_of_agents):
        matplotlib.pyplot.xlim(0, no_cols-1)
        matplotlib.pyplot.ylim(0, no_rows-1)
        matplotlib.pyplot.imshow(environment)
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y,color="red")
  
    
""" gui """
num_of_frames = 50
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=num_of_frames, repeat=False)
    canvas.draw()  

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop() 



