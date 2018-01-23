$(function() {
	$("#review-form").submit(function(e) {
		$("#rating-hidden").val($("#rating").val())
	});

	$(".stars").each(function() {
		switch ($(this).text()) {
			case "1":
				$(this).html("&#9733;&#9734;&#9734;&#9734;&#9734;")
				break
			case "2":
				$(this).html("&#9733;&#9733;&#9734;&#9734;&#9734;")
				break
			case "3":
				$(this).html("&#9733;&#9733;&#9733;&#9734;&#9734;")
				break
			case "4":
				$(this).html("&#9733;&#9733;&#9733;&#9733;&#9734;")
				break
			case "5":
				$(this).html("&#9733;&#9733;&#9733;&#9733;&#9733;")
				break
		}
	});
});