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
		$('#featuresTab').removeClass("active");
		activeTabId = "#" + sessionStorage.getItem("clickedTab")
		activePaneId = sessionStorage.getItem("activePane")
    	$(activeTabId).addClass("active");
    	$(activePaneId).addClass("show active");
	}

})