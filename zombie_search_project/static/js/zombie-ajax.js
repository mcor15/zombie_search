function gethtml(){
    $.get('/zombie_search/game/', {"action":parameters[0],
                                            "houseNumber":parameters[1],
                                            "roomNumber":parameters[2]}, function(data){
                        document.getElementById("posthere").innerHTML = data[0];
                        document.getElementById("update_state").innerHTML = data[1];
                        document.getElementById("stats").innerHTML = data[2];
                        document.getElementById("picture").innerHTML = data[3];

                        setupList();
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

}
$(document).ready(function(){
  $.get('/zombie_search/game/', {}, function (data) {
      document.getElementById("posthere").innerHTML = data[0];
      document.getElementById("update_state").innerHTML = data[1];
      document.getElementById("stats").innerHTML = data[2];
      document.getElementById("picture").innerHTML = data[3];
        setupList();
    });

  });

