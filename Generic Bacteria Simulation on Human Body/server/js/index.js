var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, $("#left").innerWidth() / $("#left").innerHeight(), 0.1, 1000);

var CANVAS_WIDTH = 80,
	CANVAS_HEIGHT = 80,
	CAM_DISTANCE = 300,
	VISUALIZATION_FACTOR = 13;


var renderer = new THREE.WebGLRenderer();
renderer.setSize($("#left").innerWidth(), $("#left").innerHeight());
$("#left").append(renderer.domElement);

//axes
var container = $("#axes");
var renderer2 = new THREE.WebGLRenderer();
renderer2.setSize(CANVAS_WIDTH, CANVAS_HEIGHT);
container.append(renderer2.domElement);
var scene2 = new THREE.Scene();
var camera2 = new THREE.PerspectiveCamera(50, CANVAS_WIDTH / CANVAS_HEIGHT, 1, 1000);
camera2.up = camera.up;
var axes = new THREE.AxisHelper(100);
scene2.add(axes);

var bodyMeshOpacity = 0.4;
var material = new THREE.MeshPhongMaterial({
	color: 0xFEB786,
	transparent: true,
	opacity: bodyMeshOpacity
});
var bodyMesh;

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
	bodyMesh = object;
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

var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
var objects = [];

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
	camera.aspect = $("#left").innerWidth() / $("#left").innerHeight();
	camera.updateProjectionMatrix();
	renderer.setSize($("#left").innerWidth(), $("#left").innerHeight());
}

function render() {
	renderer.render(scene, camera);
	renderer2.render(scene2, camera2);
}

var lastSelection;
var lastSelectionColor;

function onDocumentMouseDown(event) {

	event.preventDefault();

	mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
	mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;

	raycaster.setFromCamera(mouse, camera);

	var intersects = raycaster.intersectObjects(objects);
	if (intersects.length > 0 && lastSelection != intersects[0]) {
		//Show div
		$("#objectLabel").text(intersects[0].object.node.name);
		$("#right").css('display', 'block');
		$("#left").css('width', '60%');
		$("#arrow").css('display', 'block');
		onWindowResize();
		if (lastSelection) {
			lastSelection.object.material.color.setHex(lastSelectionColor);
		}
		lastSelection = intersects[0]
		lastSelectionColor = intersects[0].object.material.color.getHex();
		intersects[0].object.material.color.setHex(0xf2cd00);
	}
}

window.addEventListener('resize', onWindowResize, false);
document.addEventListener('mousedown', onDocumentMouseDown, false);

animate();
$("#reset").click(function() {
	controls.reset();
});

$("#arrow").mouseenter(function() {
	controls.enabled = false;
	console.log("asadsad");
}).mouseleave(function() {
	controls.enabled = true;
});

$(document).keypress(function(event) {
	if (!bodyMesh) {
		return;
	}
	if (event.which == 43) {
		bodyMeshOpacity += 0.1;
		if (bodyMeshOpacity > 1) {
			bodyMeshOpacity = 1;
			return;
		}
		bodyMesh.traverse(function(child) {
			if (child instanceof THREE.Mesh) {
				child.material.opacity = bodyMeshOpacity;
			}
		});
		event.preventDefault();
	} else if (event.which == 95) {
		bodyMeshOpacity -= 0.1;
		if (bodyMeshOpacity < 0) {
			bodyMeshOpacity = 0;
			return;
		}
		bodyMesh.traverse(function(child) {
			if (child instanceof THREE.Mesh) {
				child.material.opacity = bodyMeshOpacity;
			}
		});
		event.preventDefault();
	}
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
		cylinder.node = data[i];
		objects.push(cylinder);
		scene.add(cylinder);
	}
});

var config = {
	type: 'line',
	data: {
		datasets: [{
			label: "",
			data: [2, 3, 5, 1],
			fill: true
		}]
	},
	options: {
		responsive: true,
		title: {
			display: true,
			text: "Chart.js Time Point Data"
		},
		scales: {
			xAxes: [{
				type: "time",
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Date'
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'value'
				}
			}]
		}
	}
};

// $.each(config.data.datasets, function(i, dataset) {
// 	dataset.borderColor = randomColor(0.4);
// 	dataset.backgroundColor = randomColor(0.5);
// 	dataset.pointBorderColor = randomColor(0.7);
// 	dataset.pointBackgroundColor = randomColor(0.5);
// 	dataset.pointBorderWidth = 1;
// });


// $('#addData').click(function() {
// 	if (config.data.datasets.length > 0) {
// 		var lastTime = myLine.scales['x-axis-0'].labelMoments[0].length ? myLine.scales['x-axis-0'].labelMoments[0][myLine.scales['x-axis-0'].labelMoments[0].length - 1] : moment();
// 		var newTime = lastTime
// 			.clone()
// 			.add(1, 'day')
// 			.format('MM/DD/YYYY HH:mm');

// 		for (var index = 0; index < config.data.datasets.length; ++index) {
// 			config.data.datasets[index].data.push({
// 				x: newTime,
// 				y: randomScalingFactor()
// 			});
// 		}

// 		window.myLine.update();
// 	}
// });
$(document).ready(function() {
	var socket = null;
	var isopen = false;
	socket = new WebSocket("ws://127.0.0.1:8080/ws");

	socket.onopen = function() {
		console.log("Connected!");
		isopen = true;
		$("#mask").hide();
	};

	socket.onclose = function(e) {
		console.log("Connection closed.");
		socket = null;
		isopen = false;
		$("#mask").show();
	};

	socket.onmessage = function(e) {
		if (typeof e.data == "string") {
			var payload = JSON.parse(e.data);
			$("#timer").text("Time: " + payload.time);
		}
	};
	var ctx = $("#chart");
	window.myLine = new Chart(ctx, config);
});