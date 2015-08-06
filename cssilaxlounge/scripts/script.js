$(document).ready(function() {
  $('#logo').fadeIn(2000, MoveUpAndDown);
});

function MoveUpAndDown() {
  $('#logo').animate({
    bottom: 0
  }, 2000 ).animate ({
    bottom: -30
  }, 2000, MoveUpAndDown)
}
