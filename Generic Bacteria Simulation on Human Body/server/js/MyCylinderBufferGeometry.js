/**
 * @author Mugen87 / https://github.com/Mugen87
 */

THREE.MyCylinderBufferGeometry = function(radius, start, end, radialSegments, heightSegments) {

	THREE.BufferGeometry.call(this);

	this.type = 'MyCylinderBufferGeometry';

	this.parameters = {
		radius: radius,
		start: start,
		end: end,
		radialSegments: radialSegments,
		heightSegments: heightSegments
	};

	var scope = this;
	console.assert(radius);
	console.assert(start != null && start.x != null && start.y != null && start.z != null);
	console.assert(end != null && end.x != null && end.y != null && end.z != null);

	radialSegments = radialSegments !== undefined ? Math.floor(radialSegments) : 20;
	heightSegments = heightSegments !== undefined ? Math.floor(heightSegments) : 10;

	var nbCap = 2;

	var vertexCount = calculateVertexCount();
	var indexCount = calculateIndexCount();

	// buffers

	var indices = new THREE.BufferAttribute(new(indexCount > 65535 ? Uint32Array : Uint16Array)(indexCount), 1);
	var vertices = new THREE.BufferAttribute(new Float32Array(vertexCount * 3), 3);
	var normals = new THREE.BufferAttribute(new Float32Array(vertexCount * 3), 3);
	var uvs = new THREE.BufferAttribute(new Float32Array(vertexCount * 2), 2);

	// helper variables

	var index = 0,
		indexOffset = 0,
		indexArray = [],
		height = end.y - start.y;

	var halfHeight = height / 2;

	// group variables
	var groupStart = 0;

	// generate geometry

	generateTorso();
	generateCap();
	generateCap(true);
	// build geometry

	this.setIndex(indices);
	this.addAttribute('position', vertices);
	//this.addAttribute('normal', normals);
	//this.addAttribute('uv', uvs);

	// helper functions

	function calculateVertexCount() {
		var count = (radialSegments + 1) * (heightSegments + 1);
		count += ((radialSegments + 1) * nbCap) + (radialSegments * nbCap);
		return count;
	}

	function calculateIndexCount() {
		var count = radialSegments * heightSegments * 2 * 3;
		count += radialSegments * nbCap * 3;
		return count;
	}

	function generateTorso() {

		var x, y;
		var normal = new THREE.Vector3();
		var vertex = new THREE.Vector3();

		var groupCount = 0;

		// this will be used to calculate the normal
		var tanTheta = (end.x - start.x) / height;

		// generate vertices, normals and uvs
		var diff = (start.x - end.x) / heightSegments;
		var diffz = (start.z - end.z) / heightSegments;
		for (y = 0; y <= heightSegments; y++) {

			var indexRow = [];

			var v = y / heightSegments;

			// calculate the radius of the current row
			for (x = 0; x <= radialSegments; x++) {

				var u = x / radialSegments;

				// vertex
				vertex.x = start.x + radius * Math.sin(u * 2 * Math.PI) - diff * y;
				vertex.y = start.y + v * height;
				vertex.z = start.z + radius * Math.cos(u * 2 * Math.PI) - diffz * y;
				vertices.setXYZ(index, vertex.x, vertex.y, vertex.z);

				//normal
				normal.copy(vertex);
				normal.setY(Math.sqrt(normal.x * normal.x + normal.z * normal.z) * tanTheta).normalize();
				normals.setXYZ(index, normal.x, normal.y, normal.z);

				//uv
				uvs.setXY(index, u, 1 - v);

				// save index of vertex in respective row
				indexRow.push(index);

				// increase index
				index++;

			}

			// now save vertices of the row in our index array
			indexArray.push(indexRow);

		}

		// generate indices

		for (x = 0; x < radialSegments; x++) {

			for (y = 0; y < heightSegments; y++) {

				// we use the index array to access the correct indices
				var i1 = indexArray[y][x];
				var i2 = indexArray[y + 1][x];
				var i3 = indexArray[y + 1][x + 1];
				var i4 = indexArray[y][x + 1];

				// face one
				indices.setX(indexOffset, i1);
				indexOffset++;
				indices.setX(indexOffset, i2);
				indexOffset++;
				indices.setX(indexOffset, i4);
				indexOffset++;

				// face two
				indices.setX(indexOffset, i2);
				indexOffset++;
				indices.setX(indexOffset, i3);
				indexOffset++;
				indices.setX(indexOffset, i4);
				indexOffset++;

				// update counters
				groupCount += 6;

			}

		}

		// add a group to the geometry. this will ensure multi material support
		scope.addGroup(groupStart, groupCount, 0);

		// calculate new start value for groups
		groupStart += groupCount;

	}

	function generateCap(top) {

		var x, centerIndexStart, centerIndexEnd;

		var uv = new THREE.Vector2();
		var vertex = new THREE.Vector3();

		var groupCount = 0;
		var sign = top ? 1 : -1;
		// save the index of the first center vertex
		centerIndexStart = index;

		// first we generate the center vertex data of the cap.
		// because the geometry needs one set of uvs per face,
		// we must generate a center vertex per face/segment

		for (x = 1; x <= radialSegments; x++) {

			// vertex
			if (top) {
				vertices.setXYZ(index, start.x, start.y, start.z);
			} else {
				vertices.setXYZ(index, end.x, end.y, end.z);
			}
			normals.setXYZ(index, 0, sign, 0);

			// normal

			// uv
			uv.x = 0.5;
			uv.y = 0.5;

			uvs.setXY(index, uv.x, uv.y);

			// increase index
			index++;

		}

		// save the index of the last center vertex
		centerIndexEnd = index;

		// now we generate the surrounding vertices, normals and uvs

		for (x = 0; x <= radialSegments; x++) {

			var u = x / radialSegments;
			var theta = u * 2 * Math.PI;

			var cosTheta = Math.cos(theta);
			var sinTheta = Math.sin(theta);

			// vertex
			vertex.x = (top ? start.x : end.x) + radius * sinTheta;
			vertex.y = top ? start.y : end.y;
			vertex.z = (top ? start.z : end.z) + radius * cosTheta;
			vertices.setXYZ(index, vertex.x, vertex.y, vertex.z);

			// normal
			normals.setXYZ(index, 0, sign, 0);

			// uv
			uv.x = (cosTheta * 0.5) + 0.5;
			uv.y = (sinTheta * 0.5 * sign) + 0.5;
			uvs.setXY(index, uv.x, uv.y);

			// increase index
			index++;

		}

		// generate indices

		for (x = 0; x < radialSegments; x++) {

			var c = centerIndexStart + x;
			var i = centerIndexEnd + x;

			if (top === true) {

				// face top
				indices.setX(indexOffset, i);
				indexOffset++;
				indices.setX(indexOffset, i + 1);
				indexOffset++;
				indices.setX(indexOffset, c);
				indexOffset++;

			} else {

				// face bottom
				indices.setX(indexOffset, i + 1);
				indexOffset++;
				indices.setX(indexOffset, i);
				indexOffset++;
				indices.setX(indexOffset, c);
				indexOffset++;

			}

			// update counters
			groupCount += 3;

		}

		// add a group to the geometry. this will ensure multi material support
		scope.addGroup(groupStart, groupCount, top === true ? 1 : 2);

		// calculate new start value for groups
		groupStart += groupCount;

	}

};

THREE.MyCylinderBufferGeometry.prototype = Object.create(THREE.BufferGeometry.prototype);
THREE.MyCylinderBufferGeometry.prototype.constructor = THREE.MyCylinderBufferGeometry;