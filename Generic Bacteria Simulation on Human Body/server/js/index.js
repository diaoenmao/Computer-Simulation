var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

var CANVAS_WIDTH = 80,
	CANVAS_HEIGHT = 80,
	CAM_DISTANCE = 300,
	VISUALIZATION_FACTOR = 13;


var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

//axes
var container = document.getElementById('axes');
var renderer2 = new THREE.WebGLRenderer();
renderer2.setSize(CANVAS_WIDTH, CANVAS_HEIGHT);
container.appendChild(renderer2.domElement);
var scene2 = new THREE.Scene();
var camera2 = new THREE.PerspectiveCamera(50, CANVAS_WIDTH / CANVAS_HEIGHT, 1, 1000);
camera2.up = camera.up;
var axes = new THREE.AxisHelper(100);
scene2.add(axes);


var material = new THREE.MeshPhongMaterial({
	color: 0xFEB786,
	transparent: true,
	opacity: 0.4
});

var manager = new THREE.LoadingManager();
manager.onProgress = function(item, loaded, total) {
	console.log(item, loaded, total);
};

var onProgress = function(xhr) {
	if (xhr.lengthComputable) {
		var percentComplete = xhr.loaded / xhr.total * 100;
		console.log(Math.round(percentComplete, 2) + '% downloaded');
	}
};
var onError = function(xhr) {};


var loader = new THREE.OBJLoader(manager);
loader.load('assets/body_mesh.obj', function(object) {
	object.traverse(function(child) {
		if (child instanceof THREE.Mesh) {
			child.material = material;
		}
	});
	scene.add(object);
}, onProgress, onError);

var llight = new THREE.PointLight(0x404040, 8, 8.5);
var flight = new THREE.PointLight(0x404040, 5, 18);
var blight = new THREE.PointLight(0x404040, 5, 18);
var ambientLight = new THREE.AmbientLight(0x404040);
llight.position.set(0, 3, 6);
flight.position.set(0, 19, 5);
blight.position.set(0, 19, -5);
scene.add(blight);
scene.add(flight);
scene.add(llight);
scene.add(ambientLight);
scene.position.z = 0;
scene.position.y = -10;
scene.position.x = 0;
camera.position.z = 20;
var controls = new THREE.TrackballControls(camera);
controls.addEventListener('change', render);


function animate() {
	requestAnimationFrame(animate);
	camera.lookAt(scene.position);
	controls.update();

	camera2.position.copy(camera.position);
	camera2.position.sub(controls.target);
	camera2.position.setLength(CAM_DISTANCE);
	camera2.lookAt(scene2.position);

	render();
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}

function render() {
	renderer.render(scene, camera);
	renderer2.render(scene2, camera2);
}

window.addEventListener('resize', onWindowResize, false);
animate();
$("#reset").click(function() {
	controls.reset();
});

function setStartEndNodes(node) {
	var radians = function(deg) {
		return deg / 180 * Math.PI;
	};
	var children = node.edges;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		if (child.start == null) {
			child.start = {};
			child.start.x = node.end.x;
			child.start.y = node.end.y;
			child.start.z = node.end.z;
		}

		if (child.end == null) {
			child.end = {};
			child.end.x = child.start.x + Math.sin(radians(child.yaw)) * child.length * VISUALIZATION_FACTOR;
			child.end.y = child.start.y + Math.cos(radians(child.yaw)) * child.length * VISUALIZATION_FACTOR;
			child.end.z = child.start.z + Math.sin(radians(child.pitch));
		}
	}

	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		setStartEndNodes(child);
	}
}

function buildGraph(blood_vessels) {
	var start_node;
	for (var i = 0; i < blood_vessels.length; i++) {
		var node = blood_vessels[i];
		node.length = node.length / 100;
		node.radius = node.radius / 100;
		node.edges = [];
		if (node.start) {
			node.start = node.start.split(',');
			node.start = {
				x: parseFloat(node.start[0]),
				y: parseFloat(node.start[1]),
				z: parseFloat(node.start[2])
			};
			start_node = node;
		}

		if (node.end) {
			node.end = node.end.split(',');
			node.end = {
				x: parseFloat(node.end[0]),
				y: parseFloat(node.end[1]),
				z: parseFloat(node.end[2])
			};
		}
	}
	//Make node connections with its children.
	blood_vessels.sort(function(a, b) {
		return a.id - b.id;
	});
	var addEdge = function(host, client) {
		host.edges.push(client);
	};
	for (var i = 0; i < blood_vessels.length; i++) {
		var node = blood_vessels[i];
		if (typeof node.to === 'string' || node.to instanceof String) {

			var to = node.to.split(',');
			for (var j = 0; j < to.length; j++) {
				var index = parseInt(to[j]) - 1;
				if (index > 0) {
					addEdge(node, blood_vessels[index]);
				}
			}
		} else if (node.to > 0) {
			addEdge(node, blood_vessels[node.to - 1]);
		}
	}

	setStartEndNodes(start_node)
}

$.getJSON('assets/blood_vessels.json', function(data) {
	buildGraph(data);
	console.log(data[0]);
	for (var i = 0; i < data.length; i++) {
		var geometry = new THREE.MyCylinderBufferGeometry(data[i].radius * VISUALIZATION_FACTOR, data[i].start, data[i].end);
		var material = new THREE.MeshBasicMaterial({
			color: 0x8A0707,
			side: THREE.DoubleSide
		});
		var cylinder = new THREE.Mesh(geometry, material);

		scene.add(cylinder);
	}
});