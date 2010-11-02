$(document).ready(function(){

	//Hide (Collapse) the toggle containers on load
	$(".toggle_container").hide(); 

	//Switch the "Open" and "Close" state per click
	$("h2.trigger").toggle(function(){
		$(this).addClass("active");
		}, function () {
		$(this).removeClass("active");
	});

	//Slide up and down on click
	$("h2.trigger").click(function(){
		$(this).next(".toggle_container").slideToggle("fast");
	});

});