$("#please_login").click(function(){
    alert("you must be logged in to play zombie_search!");
  });

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
