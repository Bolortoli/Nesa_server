$(".pagination").paging(1337, { // make 1337 elements navigatable
	format: '[< ncnnn! >]', // define how the navigation should look like and in which order onFormat() get's called
	perpage: 10, // show 10 elements per page
	lapping: 0, // don't overlap pages for the moment
	page: 1, // start at page, can also be "null" or negative
	onSelect: function (page) {
		// add code which gets executed when user selects a page, how about $.ajax() or $(...).slice()?
		console.log(this);
	},
	onFormat: function (type) { // Gets called for each character of "format" and returns a HTML representation
		switch (type) {
		case 'block': // n and c
			return '<a href="#">' + this.value + '</a>';
		case 'next': // >
			return '<a href="#">&gt;</a>';
		case 'prev': // <
			return '<a href="#">&lt;</a>';
		case 'first': // [
			return '<a href="#">first</a>';
		case 'last': // ]
			return '<a href="#">last</a>';
		}
	}
});