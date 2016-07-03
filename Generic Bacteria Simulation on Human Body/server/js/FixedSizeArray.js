function FixedSizeArray(n) {
	this.n = n;
	this.array = new Array(n);
	this.length = 0;
}

FixedSizeArray.prototype.push = function(o) {
	this.length++;
	if (this.length > this.n) {
		this.length = this.n;
		this.array.shift();
		this.array.push(o);
	} else {
		this.array[this.length - 1] = o;
	}
};