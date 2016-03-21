$(document).ready(function() {
    $.get('/zombie_search/game/', {}, function (data) {
        document.getElementById("posthere").innerHTML = data[0];
        document.getElementById("update_state").innerHTML = data[1];
        document.getElementById("stats").innerHTML = data[2];
        document.getElementById("picture").innerHTML = data[3];
        document.getElementById("update_state").innerHTML += data[4];
        setupList();


    });

});

function gethtml(){
    $.get('/zombie_search/game/', {"action":parameters[0],
                                            "houseNumber":parameters[1],
                                            "roomNumber":parameters[2]}, function(data){
                        alert(data.length)
                        if(data.length==5) {
                            document.getElementById("posthere").innerHTML = data[0];
                            document.getElementById("update_state").innerHTML = data[1];
                            document.getElementById("stats").innerHTML = data[2];
                            document.getElementById("update_state").innerHTML += data[4];
                            document.getElementById("picture").innerHTML = data[3];
                            setupList();
                        }
                        else{
                            window.location.href='/zombie_search/play'
                        }
              });
                $("#dialog").dialog({
            autoOpen: false,
            width: 500,
            height: 250
        });
}

function setupList(){
    $('li').on('click',function(){
        var my_var ;
        my_var = $(this).attr("id");
          if(my_var!=undefined){
              parameters=my_var.split("/");
            gethtml();
          }

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

}
