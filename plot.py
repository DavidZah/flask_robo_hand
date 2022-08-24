import random
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from scipy.signal import savgol_filter

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)

i_good = 0
i_bad = 0
i_medium = 0

state = 0
data_good = None
data_bad = None
data_medium = None



def animate(i):



    xs_good = []
    ys_good = []

    for i in range(1500):
        xs.append(float(i))
        ys.append(float(random.randint(1,10)))
        i += 1

    if state == 1:

        ax1.clear()
        ax1.plot(xs, ys,color='green')
    if state == 2:
        ax2.clear()
        ax2.plot(xs, ys,color='red')
    if state == 3:
        ax3.clear()
        ax3.plot(xs, ys, color='yellow')

def load_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        print(data)

if __name__ == "__main__":

    data_good = load_json("json_data.json")
    data_bad = load_json("json_data_bad.json")
    data_medium = load_json("json_data_medium.json")

    data_good = savgol_filter(data_good["AcY"], 101, 2)
    data_bad = savgol_filter(data_bad["AcY"], 101, 2)
    data_medium = savgol_filter(data_medium["AcY"], 101, 2)

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()