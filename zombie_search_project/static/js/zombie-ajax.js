$('#get_leaderboard').click(function(){
  var OrderBy;
  next = $(this).attr("data-next")
  $.get('zombie_search/get_leaderboard', {n: next}, )
}
