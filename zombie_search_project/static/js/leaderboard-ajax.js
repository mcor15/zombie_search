  $(document).ready(function(){

    $.get('/zombie_search/leader/', {}, function (data) {
      if(typeof(Storage) !== "undefined") {
              if (sessionStorage.typeof) {
              } else {
                  sessionStorage.typeof = 0;
              }
          } else {
                alert("Sorry, your browser does not support web storage.");
          }
         $('#first_half').html(data);
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
          $('#type').html( data['stat']);
          $('#first_half').html(data['html']);
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
            $('#type').html( data['stat']);
            $('#first_half').html(data['html']);
        });
      });
