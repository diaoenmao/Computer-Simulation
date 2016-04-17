from parameters import parameters
import os
import re
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from Point import *
from mayavi import mlab

def picker_callback(picker):
    global vessels, lastSelected
    if 'lastSelected' not in globals():
        lastSelected = None
    
    picked = picker.actors
    for (top, bottom, node) in vessels:
        #if picker.actor in top.actor.actors or picker.actor in bottom.actor.actors:
            if top.actor.actor._vtk_obj in [o._vtk_obj for o in picked] or bottom.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
                if lastSelected != None:
                    lastSelected.remove()
                lastSelected = mlab.text(node.start.x, node.start.y, node.name, width=0.2, z=node.start.z)
            

def draw_body(nodes):
    assert(nodes is not None)
    global body_model
    global vessels
    if 'vessels' not in globals():
        vessels = []
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
    figure = mlab.gcf()
    mlab.clf()
    figure.scene.disable_render = True
    mlab.triangular_mesh(body_model['x'], body_model['y'], body_model['z'], body_model['triangles'], color=(1,0.8,0.8), opacity=0.2)
    #Blood vessels
    for node in nodes:
        top, bottom = draw_blood_vessel(node.start, node.end, node.radius / 100 * parameters.visualization_factor)
        vessels.append((top, bottom, node))
    figure.scene.disable_render = False
    picker = figure.on_mouse_pick(picker_callback)
    picker.tolerance = 0.01

    mlab.show()

def draw_blood_vessel(p1, p2, r, color=(1,0,0)):
    assert(isinstance(p1, Point))
    assert(isinstance(p2, Point))
    if(p2.y - p1.y) < 0:
        tmp = p2
        p2 = p1
        p1 = tmp
    u = np.linspace(0, 2 * np.pi, 100)
    l = p2.y - p1.y
    x = r * np.outer(np.cos(u), np.sin(u))
    y = np.empty((len(x),len(x)))
    y.fill(p1.y)
    z = r * np.outer(np.sin(u), np.sin(u))
    #p1
    mlab.mesh(p1.x + x, y, p1.z + z, color=color)
    #p2
    mlab.mesh(p2.x + x, l+y, p2.z + z, color=color)
    
    #sides
    x = r * np.linspace(-1, 1, 40)
    y = np.linspace(p1.y, p2.y, 40)

    x, y = np.meshgrid(x, y)
    z = np.sqrt(r**2-x**2)
    neg_z = -z
    diff = np.linspace(p1.x, p2.x, 40)
    diffz = np.linspace(p1.z, p2.z, 40)
    for (row, dx ) in zip(x, diff):
        row += dx
    for (row, dz ) in zip(z, diffz):
        row += dz
    for (row, dz ) in zip(neg_z, diffz):
        row += dz 
    top = mlab.mesh(x,y,neg_z, color=color)
    bottom = mlab.mesh(x,y,z, color=color)
    return (top, bottom)