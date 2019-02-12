$(document).ready(function() {

	//Render markdown where called
	$(".article-content").each(function() {
		var article = $(this).text();
		var marked_article = marked(article)
		$(this).html(marked_article)
	});

	//Store which tab is currently selected, in the session window
	$('.nav-link').click(function(){
   	sessionStorage.setItem("clickedTab", $(this).attr('id'));
   	sessionStorage.setItem("activePane", $(this).attr('href'));
	});

	if(typeof sessionStorage.getItem("activePane") != null && sessionStorage.getItem("clickedTab") != "undefined") {
		$("#feature-results").removeClass("show active");
		console.log("removed class from feature-results")
		$('#featuresTab').removeClass("active");
		console.log("removed class from featuresTab")
		console.log(sessionStorage.getItem("clickedTab"));
		activeTabId = "#" + sessionStorage.getItem("clickedTab")
		console.log(activeTabId);
		activePaneId = sessionStorage.getItem("activePane")
		console.log(activePaneId)
    	$(activeTabId).addClass("active");
    	console.log("added class to active tab");
    	$(activePaneId).addClass("show active");
    	console.log("added class to active pane")

	} else {
		$("#feature-results").addClass("show active");
		$('#featuresTab').addClass("active");
		console.log("no item to get")
	}

})