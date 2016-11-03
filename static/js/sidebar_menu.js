/**
 *
 */
$("#menu-toggle").click(function(e) {
	e.preventDefault();
	//$("#wrapper").toggleClass("toggled");

});
$("#menu-toggle-2").click(function(e) {
	e.preventDefault();
	$("#wrapper").toggleClass("toggled-2");
	$('#menu ul').hide();
});

function initMenu() {
	$('#menu ul:first').hide();
	 //$('#menu ul:first').hide();
	//$('#menu ul').children('.current').parent().show();


}
$(document).ready(function() {
	initMenu();
});
(document).ready(function() {
	initMenu();
});