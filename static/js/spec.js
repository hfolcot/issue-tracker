describe("Statistics", function() {
	describe("Clear Canvas", function() {
		it("should reset the canvases within the charts div to blank canvases", function() {
			var charts = $('#charts');
			clearCanvases();			
			expect(charts.html()).toBe(`
		<canvas class="canvas" id="voteChart"></canvas>
		<canvas class="canvas" id="byMonth"></canvas>
		<canvas class="canvas" id="last28Days"></canvas>
		<canvas class="canvas" id="last7Days"></canvas>
	`);
	});
	
	});

});