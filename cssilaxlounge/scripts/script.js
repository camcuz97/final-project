$(document).ready(function() {
  $('#logo').fadeIn(3500, MoveUpAndDown);
  $('h1').fadeIn(3500)
  $('#audio-player').fadeIn(3500)

});

function MoveUpAndDown() {
  $('#logo').animate({
    bottom: 0
  }, 2000 ).animate ({
    bottom: -35
  }, 2000, MoveUpAndDown)
}
