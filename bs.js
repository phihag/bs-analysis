VCOL_NAMES = ["1", "2", "3", "4", "5"]

VOTE_COLORS = {
	"1": "#ff0000",
	"2": "#800000",
	"3": "#808080",
	"4": "#008000",
	"5": "#00ff00"
}

$(function() {
	$("tbody tr").each(function (i, el) {
		var canvas = document.createElement("canvas");
		var w = 400;
		canvas.setAttribute("width", w);
		canvas.setAttribute("height", "20");
		var ctx = canvas.getContext("2d");
		
		var voteCount = 0;
		for (var o in VOTE_COLORS) {
			voteCount += parseInt(el.getAttribute("data-votes-" + o));
		}

		var xvotes = 0;
		for (var i = 0;i < VCOL_NAMES.length;i++) {
			var o = VCOL_NAMES[i];
			var votes = parseInt(el.getAttribute("data-votes-" + o));
			var color = VOTE_COLORS[o];
			
			ctx.fillStyle = color;
			ctx.fillRect(w * xvotes / voteCount, 0, w * (xvotes + votes) / voteCount, 20);
			xvotes = xvotes + votes;
		}

		var td = document.createElement("td");
		td.appendChild(canvas);
		$(el).append(td);
	});
});