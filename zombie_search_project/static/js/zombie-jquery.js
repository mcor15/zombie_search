$(document).ready(function(){
  $( "#dialog" ).dialog({
    autoOpen: false,
	width: 500,
	height: 250
  });

  $("#ingame_about").click(function() {
    $("#dialog").dialog('open');
  });

$("#please_login").click(function(){
    alert("you must be logged in to play zombie_search!");
  });

$('#show_change_pw').click(function(){
  $('#change_pw').show()
  });

});
