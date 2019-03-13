
var today = new Date();
var lastMonth = (today - (28*24*60*60*1000))
var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
var currentYearCountData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var prevYearCountData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function clearCanvases() {
	$('#charts').show();
	$('.canvas').remove();
	$('#charts').append(`<canvas class="canvas" id="voteChart"></canvas>
								<hr class="canvas">
								<canvas class="canvas" id="byMonth"></canvas>
								<hr class="canvas">
								<canvas class="canvas" id="last28Days"></canvas>
								<hr class="canvas">
								<canvas class="canvas" id="last7Days"></canvas>`);
}

// BUGS
$('#bugDataset').click(function() {
	$('#featuresImplementedToday').hide();
	$('#staffFeatures').hide();
	$('#staffBugs').hide();
	$('#contributionsBoard').hide();
	$('#bugsFixedToday').show();
	clearCanvases()
	var voteChartContainer = $('#voteChart');
	var byMonthChartContainer = $('#byMonth');
	var last28DaysChartContainer = $('#last28Days');
	var last7DaysChartContainer = $('#last7Days');
	
	$.ajax({
	type: 'GET',
	url: '/tickets/api/bugtickets/?format=json',
	success: function(data) {

		// Gather datasets for bugsByVoteChart
		var openBugsDataset = [];
		var bugsByVoteLabels = [];
		var bugsByVoteDataset = [];
		var j = 0
		$.each(data, function(i, item) {
			if (data[i].status != 'Fixed') {
				openBugsDataset[j] = data[i];
				j++;
			}
		})
		j = 0
		$.each(openBugsDataset, function(i, item) {
			if (openBugsDataset[i].rating >= 0) {
				bugsByVoteLabels[j] = openBugsDataset[i].id;
				bugsByVoteDataset[j] = openBugsDataset[i].rating;
				j++;
			}
		})

		// Draw a bar chart showing bugs by number of votes
		var bugsByVoteChart = new Chart(voteChartContainer, {
			type: 'bar',
			data: {
				labels: bugsByVoteLabels,
				datasets: [
					{
						data: bugsByVoteDataset,
						backgroundColor: '#bada55'

					}]
			},
			options: {
				title: {
					display: true,
					text: 'Bug popularity'
				},
				legend: {
	            display: false
	         	},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Ticket ID'
						}
					}],
					yAxes: [{
						ticks: {
							beginAtZero: true
						},
						scaleLabel: {
							display: true,
							labelString: 'Number of votes'
						}
					}]
				}
			},
		}
		)

		// Gather data for fixed bugs charts
		j = 0
		var fixedBugsDataset = []
		$.each(data, function(i, item) {
			if (data[i].status == 'Fixed') {
				fixedBugsDataset[j] = data[i];
				j++;
			}
		}); 

		// Calculate number of bugs fixed this year and last year
		var fixedThisYear = []
		$.each(months, function(i, month) {
			$.each(fixedBugsDataset, function(j, bug) {
				dateFixed = new Date(bug.fixed_date);
				monthFixed = dateFixed.toLocaleString('en-gb', { month: 'short' });
				yearFixed = dateFixed.getFullYear();
				if (monthFixed == months[i] && yearFixed == today.getFullYear()) {
					currentYearCountData[i] ++;
				}
				if (monthFixed == months[i] && yearFixed == (today.getFullYear() - 1)) {
					prevYearCountData[i] ++;
				}
			})
		})

		// Draw a bar chart showing number of bugs fixed per month
		var bugsByMonthChart = new Chart(byMonthChartContainer, {
			type: 'bar',
			data: {
				labels: months,
				datasets: [
					{
						label: 'This year',
						data: currentYearCountData,
						backgroundColor: '#bada55'

					},
					{
						label: 'Last year',
						data: prevYearCountData,
						backgroundColor: '#DE9E36'
					}
					]
			},
			options: {

				title: {
					display: true,
					text: 'Bugs Fixed By Year'
				},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of bugs fixed'
								}
							

						}]
					
					}
				},
			})

		//Last 30 days stats
		var last28Days = []
		var last28DaysLabels = []
		for (i=27, j=0; i >= 0; i--) {
			date = new Date(today - (i*24*60*60*1000))
			last28Days[j] = date.getDate();
			last28DaysLabels[j] = date.getDate() + '/' + (date.getMonth() + 1);
			j++;
		}
		var bugsFixedLastMonth = []
		j = 0
		$.each(fixedBugsDataset, function(i, bug) {
			dateFixed = Date.parse(bug.fixed_date);
			if (dateFixed > lastMonth) {
				bugsFixedLastMonth[j] = bug;
				j++;
			}
		})
		var fixedLastMonthDataset = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		$.each(last28Days, function(i, day) {
			$.each(bugsFixedLastMonth, function(j, bug) {
				fixedDate = new Date(bug.fixed_date);
				fixedDay = fixedDate.toLocaleString('en-gb', { day: 'numeric' })
				if (fixedDay == last28Days[i]) {
					fixedLastMonthDataset[i] ++;
				}
			})
		})

		// Draw a bar chart showing number of bugs fixed in the last 28 days
		var bugsLast28DaysChart = new Chart(last28DaysChartContainer, {
			type: 'bar',
			data: {
				labels: last28DaysLabels,
				datasets: [
					{
						data: fixedLastMonthDataset,
						backgroundColor: '#bada55'

					}
					]
			},
			options: {
				legend: {
	            display: false
	         	},
				title: {
					display: true,
					text: 'Bugs Fixed in the Last 28 Days'
				},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of bugs fixed'
								}
							

						}]
					
					}
				},
			})

		var fixedLastWeekDataset = fixedLastMonthDataset.slice(21,28)
		var fixedLastWeekLabels = last28DaysLabels.slice(21,28)
		// Draw a bar chart showing number of bugs fixed in the last 7 days
		var bugsLast7DaysChart = new Chart(last7DaysChartContainer, {
			type: 'bar',
			data: {
				labels: fixedLastWeekLabels,
				datasets: [
					{
						data: fixedLastWeekDataset,
						backgroundColor: '#bada55'

					}
					]
			},
			options: {
				legend: {
	            display: false
	         	},
				title: {
					display: true,
					text: 'Bugs Fixed in the Last 7 Days'
				},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of bugs fixed'
								}
							

						}]
					
					}
				},
			})

} } )

})

// FEATURES
$('#featureDataset').click(function() {
	$('#bugsFixedToday').hide();
	$('#staffFeatures').hide();
	$('#staffBugs').hide();
	$('#contributionsBoard').hide();
	clearCanvases()
	$('#featuresImplementedToday').show();
	var voteChartContainer = $('#voteChart');
	var byMonthChartContainer = $('#byMonth');
	var last28DaysChartContainer = $('#last28Days');
	var last7DaysChartContainer = $('#last7Days');
	$.ajax({
		type: 'GET',
		url: '/tickets/api/featuretickets/?format=json',
		success: function(data) {

		// Gather datasets for featuresByVoteChart
		var openFeaturesDataset = [];
		var featuresByVoteLabels = [];
		var featuresByVoteDataset = [];
		var j = 0
		$.each(data, function(i, item) {
			if (data[i].status != 'Implemented') {
				openFeaturesDataset[j] = data[i];
				j++;
			}
		})
		j = 0
		$.each(openFeaturesDataset, function(i, item) {
			if (openFeaturesDataset[i].rating >= 0) {
				featuresByVoteLabels[j] = openFeaturesDataset[i].id;
				featuresByVoteDataset[j] = openFeaturesDataset[i].rating;
				j++;
			}
		})

		var featuresByVoteChart = new Chart(voteChartContainer, {
			type: 'bar',
			data: {
				labels: featuresByVoteLabels,
				datasets: [
					{
						data: featuresByVoteDataset,
						backgroundColor: '#bada55'

					}]
			},
			options: {
				title: {
					display: true,
					text: 'Feature popularity'
				},
				legend: {
	            display: false
	         	},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Ticket ID'
						}
					}],
					yAxes: [{
						ticks: {
							beginAtZero: true
						},
						scaleLabel: {
								display: true,
								labelString: 'Number of votes'
						}
					}]
				}
			},
		}
		)
		// Gather data for implemented features chart
		j = 0
		var fImplementedDataset = []
		$.each(data, function(i, item) {
			if (data[i].status == 'Implemented') {
				fImplementedDataset[j] = data[i];
				j++;
			}
		});
		$.each(months, function(i, month) {
			$.each(fImplementedDataset, function(j, feature) {
				dateImplemented = new Date(feature.implemented_date);
				monthImplemented = dateImplemented.toLocaleString('en-gb', { month: 'short' });
				yearImplemented = dateImplemented.getFullYear();
				if (monthImplemented == months[i] && yearImplemented == today.getFullYear()) {
					currentYearCountData[i] ++;
				}
				if (monthImplemented == months[i] && yearImplemented == (today.getFullYear() - 1)) {
					prevYearCountData[i] ++;
				}
			})
		})
		// Draw a bar chart showing number of features implemented per month
		var featuresByMonthChart = new Chart(byMonthChartContainer, {
			type: 'bar',
			data: {
				labels: months,
				datasets: [
					{
						label: 'This year',
						data: currentYearCountData,
						backgroundColor: '#bada55'

					},
					{
						label: 'Last year',
						data: prevYearCountData,
						backgroundColor: '#DE9E36'
					}
					]
			},
			options: {
				title: {
					display: true,
					text: 'Features Implemented / Year Comparison'
				},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of features implemented'
								}
							

						}]
					
					}
				},
			})
			//Last 30 days stats
			var last28Days = []
			var last28DaysLabels = []
			for (i=27, j=0; i >= 0; i--) {
				date = new Date(today - (i*24*60*60*1000))
				last28Days[j] = date.getDate();
				last28DaysLabels[j] = date.getDate() + '/' + (date.getMonth() + 1);
				j++;
			}
			var fImplementedLastMonth = []
			j = 0
			$.each(fImplementedDataset, function(i, feature) {
				dateFixed = Date.parse(feature.implemented_date);
				if (dateFixed > lastMonth) {
					fImplementedLastMonth[j] = feature;
					j++;
				}
			})
			var implementedLastMonthDataset = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			$.each(last28Days, function(i, day) {
				$.each(fImplementedLastMonth, function(j, feature) {
					fixedDate = new Date(feature.implemented_date);
					fixedDay = fixedDate.toLocaleString('en-gb', { day: 'numeric' })
					if (fixedDay == last28Days[i]) {
						implementedLastMonthDataset[i] ++;
					}
				})
			})
		// Draw a bar chart showing number of features implemented per month
		var featuresLast28DaysChart = new Chart(last28DaysChartContainer, {
			type: 'bar',
			data: {
				labels: last28DaysLabels,
				datasets: [
					{
						data: implementedLastMonthDataset,
						backgroundColor: '#bada55'

					}]
			},
			options: {
				title: {
					display: true,
					text: 'Features Implemented in the Last 28 Days'
				},
				legend: {
	            	display: false
	         	},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of features implemented'
								}
							

						}]
					
					}
				},
			})

		var implementedLastWeekDataset = implementedLastMonthDataset.slice(21,28)
		var implementedLastWeekLabels = last28DaysLabels.slice(21,28)

		// Draw a bar chart showing number of features implemented in the last 7 days
		var featuresLast28DaysChart = new Chart(last7DaysChartContainer, {
			type: 'bar',
			data: {
				labels: implementedLastWeekLabels,
				datasets: [
					{
						data: implementedLastWeekDataset,
						backgroundColor: '#bada55'

					}]
			},
			options: {
				title: {
					display: true,
					text: 'Features Implemented in the Last 7 Days'
				},
				legend: {
	            	display: false
	         	},
				scales: {
					xAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						
						scaleLabel: {
								display: true,
								labelString: 'Number of features implemented'
								}
							

						}]
					
					}
				},
			})
		}
	})

})

// STAFF
$('#staffDataset').click(function() {
	$('#charts').hide();
	$('#bugsFixedToday').hide();
	$('#featuresImplementedToday').hide();
	$('#contributionsBoard').hide();
	$('#staffFeatures').show();
	$('#staffBugs').show();
})

//CUSTOMERS
$('#customerDataset').click(function() {
	$('#charts').hide();
	$('#bugsFixedToday').hide();
	$('#featuresImplementedToday').hide();
	$('#staffFeatures').hide();
	$('#staffBugs').hide();
	$('#contributionsBoard').show();
})