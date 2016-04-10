from parameters import parameters
import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
def draw_body():
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
	plt.show()
