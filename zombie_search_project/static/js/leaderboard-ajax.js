  $(document).ready(function(){

    $.get('/zombie_search/leader/', {}, function (data) {
      if(typeof(Storage) !== "undefined") {
              if (sessionStorage.typeof) {
                  //sessionStorage.clickcount = Number(sessionStorage.clickcount)+1;
              } else {
                  sessionStorage.typeof = 0;
              }
          } else {
                alert("Sorry, your browser does not support web storage.");
          }
          //data = JSON.parse(data);
          //alert(data);
         $('#first_half').html(data);
         //$('#here').html(my_var);
         });


    });
  $('#right').click(function(){
        if (sessionStorage.typeof==2){
          sessionStorage.typeof=0
        }else{
        sessionStorage.typeof =Number(sessionStorage.typeof)+ 1;}
        var cookie = sessionStorage.typeof
        $.get('/zombie_search/render_players/', {"current": cookie}, function (data) {
          var data = jQuery.parseJSON(data);
          //alert(data['otherthing']);
          $('#type').html( data['stat']);
          $('#first_half').html(data['html']);

        //var x = document.getElementById("type").innerHTML;
      });
    });
    $('#left').click(function(){
          if (sessionStorage.typeof==0){
            sessionStorage.typeof=2
          }else{
          sessionStorage.typeof =Number(sessionStorage.typeof)- 1;}
          var cookie = sessionStorage.typeof
          $.get('/zombie_search/render_players/', {"current": cookie}, function (data) {
            var data = jQuery.parseJSON(data);
            //alert(data['otherthing']);
            $('#type').html( data['stat']);
            $('#first_half').html(data['html']);

          //var x = document.getElementById("type").innerHTML;
        });
      });
