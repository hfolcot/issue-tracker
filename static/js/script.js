$(document).ready(function() {
	$(".article-content").each(function() {
		var article = $(this).text();
		var marked_article = marked(article)
		$(this).html(marked_article)
	});

})