import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

def calculate_speeds(trajectory, dis_conversion):
    speeds = []
    for i in range(1, len(trajectory)):
        (x1, y1), t1 = trajectory[i - 1]
        (x2, y2), t2 = trajectory[i]
        if (x1, y1) != (0, 0) and (x2, y2) != (0, 0):
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) * dis_conversion
            speed = distance / (t2 - t1)
            speeds.append(speed)
    return speeds

def calculate_accelerations(trajectory, dis_conversion):
    accelerations = []
    for i in range(2, len(trajectory)):
        (x1, y1), t1 = trajectory[i - 2]
        (x2, y2), t2 = trajectory[i - 1]
        (x3, y3), t3 = trajectory[i]
        if (x1, y1) != (0, 0) and (x2, y2) != (0, 0) and (x3, y3) != (0, 0):
            distance1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) * dis_conversion
            distance2 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2) * dis_conversion
            speed1 = distance1 / (t2 - t1)
            speed2 = distance2 / (t3 - t2)
            acceleration = (speed2 - speed1) / (t3 - t1)
            accelerations.append(acceleration)
    return accelerations

def plot_trajectory(ax, trajectory, dis_conversion):
    x = [point[0][0] * dis_conversion for point in trajectory if int(point[0][0]) != 0 and int(point[0][1]) != 0]
    y = [point[0][1] * dis_conversion for point in trajectory if int(point[0][0]) != 0 and int(point[0][1]) != 0]
    ax.plot(y, x, label='Trajectoire')
    ax.set_xlabel('Position en Y')
    ax.set_ylabel('Position en X')
    ax.set_title('Trajectoire du mouvement')
    ax.set_xlim(0, 35)  
    ax.set_ylim(0, 30)

def plot_fig(trajectory, dis_conversion):
    fig, ax = plt.subplots()
    plot_trajectory(ax, trajectory, dis_conversion)
    plt.show()


trajectory = [((0.0, 0.0), 0.0), ((0.0, 0.0), 0.03333333333333333), ((0.0, 0.0), 0.06666666666666667), ((0.0, 0.0), 0.1), ((0.0, 0.0), 0.13333333333333333), ((0.0, 0.0), 0.16666666666666666), ((0.0, 0.0), 0.2), ((0.0, 0.0), 0.23333333333333334), ((0.0, 0.0), 0.26666666666666666), ((0.0, 0.0), 0.3), ((0.0, 0.0), 0.3333333333333333), ((0.0, 0.0), 0.36666666666666664), ((0.0, 0.0), 0.4), ((0.0, 0.0), 0.43333333333333335), ((0.0, 0.0), 0.4666666666666667), ((0.0, 0.0), 0.5), ((0.0, 0.0), 0.5333333333333333), ((0.0, 0.0), 0.5666666666666667), ((0.0, 0.0), 0.6), ((0.0, 0.0), 0.6333333333333333), ((0.0, 0.0), 0.6666666666666666), ((0.0, 0.0), 0.7), ((0.0, 0.0), 0.7333333333333333), ((0.0, 0.0), 0.7666666666666667), ((0.0, 0.0), 0.8), ((0.0, 0.0), 0.8333333333333334), ((0.0, 0.0), 0.8666666666666667), ((0.0, 0.0), 0.9), ((0.0, 0.0), 0.9333333333333333), ((0.0, 0.0), 0.9666666666666667), ((0.0, 0.0), 1.0), ((0.0, 0.0), 1.0333333333333334), ((0.0, 0.0), 1.0666666666666667), ((0.0, 0.0), 1.1), ((0.0, 0.0), 1.1333333333333333), ((0.0, 0.0), 1.1666666666666667), ((0.0, 0.0), 1.2), ((0.0, 0.0), 1.2333333333333334), ((0.0, 0.0), 1.2666666666666666), ((0.0, 0.0), 1.3), ((0.0, 0.0), 1.3333333333333333), ((0.0, 0.0), 1.3666666666666667), ((0.0, 0.0), 1.4), ((0.0, 0.0), 1.4333333333333333), ((9.0, 230.0), 1.4666666666666666), ((36.0, 229.0), 1.5), ((74.0, 228.0), 1.5333333333333334), ((120.0, 227.0), 1.5666666666666667), ((174.0, 226.0), 1.6), ((239.0, 227.0), 1.6333333333333333), ((317.0, 228.0), 1.6666666666666667), ((0.0, 0.0), 1.7), ((0.0, 0.0), 1.7333333333333334), ((0.0, 0.0), 1.7666666666666666), ((0.0, 0.0), 1.8), ((0.0, 0.0), 1.8333333333333333), ((0.0, 0.0), 1.8666666666666667), ((0.0, 0.0), 1.9), ((0.0, 0.0), 1.9333333333333333), ((0.0, 0.0), 1.9666666666666666), ((0.0, 0.0), 2.0), ((0.0, 0.0), 2.033333333333333), ((0.0, 0.0), 2.066666666666667), ((0.0, 0.0), 2.1), ((0.0, 0.0), 2.1333333333333333), ((0.0, 0.0), 2.1666666666666665), ((0.0, 0.0), 2.2)]
dis_conversion = 0.1

speeds = calculate_speeds(trajectory, dis_conversion)
accelerations = calculate_accelerations(trajectory, dis_conversion)

plot_fig(trajectory, dis_conversion)
