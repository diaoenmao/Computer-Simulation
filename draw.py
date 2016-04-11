from parameters import parameters
import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from Point import *

def draw_body(nodes):
    assert(nodes is not None)
    global body_model
    if 'body_model' not in globals() or body_model is None:
        body_model = {'x': [], 'y': [], 'z': [], 'triangles': []}
        current_directory = os.path.dirname(os.path.realpath(__file__))
        with open(current_directory + parameters.body_mesh_file) as data_file:
            for line in data_file:
                if re.match('^v\s+', line):
                    #parse line
                    line = re.sub('^v\s*', '', line)
                    line = re.sub('\n', '', line)
                    parts = re.split('\s', line)
                    x = float(parts[0]); y = float(parts[1]); z = float(parts[2])
                    body_model['x'].append(x)
                    body_model['y'].append(y)
                    body_model['z'].append(z)
                elif re.match('^f\s+', line):
                    line = re.sub('^f\s*', '', line)
                    line = re.sub('\n', '', line)
                    parts = re.split('\s', line)
                    triangle = [ float(re.sub('\/\/.*', '', parts[0]))-1, float(re.sub('\/\/.*', '', parts[1]))-1, float(re.sub('\/\/.*', '', parts[2]))-1 ]
                    body_model['triangles'].append(triangle)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(body_model['x'], body_model['y'], triangles=body_model['triangles'], shade=False,alpha=0.2, Z=body_model['z'])

    #Blood vessels

    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')

    plt.show()

def draw_blood_vessel(p1, p2, r, color='g'):
    assert(isinstance(p1, Point))
    assert(isinstance(p2, Point))
    if(p2.y - p1.y) < 0:
        tmp = p2
        p2 = p1
        p1 = tmp
    u = np.linspace(0, 2 * np.pi, 100)
    l = p2.y - p1.y
    x = r * np.outer(np.cos(u), np.sin(u))
    y = p1.y * np.outer(1,1)
    z = r * np.outer(np.sin(u), np.sin(u))
    #p1
    ax.plot_surface(p1.x + x, y, z, color='g')
    #p2
    ax.plot_surface(p2.x + x, l+y, z, color='g')
    
    #sides
    x = r * np.linspace(-1, 1, 40)
    z = np.sqrt(r**2-x**2)
    y = np.linspace(p1.y, p2.y, 40)

    x, y = np.meshgrid(x, y)
    diff = np.linspace(p1.x, p2.x, 40)
    for (row, dx ) in zip(x, diff):
        row += dx
    ax.plot_surface(x,y,-z, color=color)
    ax.plot_surface(x,y,z, color=color)