$(document).ready(function(){
$(function () {
  $( "#dialog" ).dialog({
    autoOpen: false,
	width: 500, 
	height: 250
  });
  
  $("#ingame_about").click(function() {
    $("#dialog").dialog('open');
  });
});
});