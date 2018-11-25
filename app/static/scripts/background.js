/**
 * Particleground demo
 * @author Jonathan Nicol - @mrjnicol
 */

$(document).ready(function() {
  $('#particles').particleground({
    dotColor: '#dedede',
    lineColor: '#dedede'
  });
  $('.intro').css({
    'margin-top': -($('.intro').height() / 2)
  });
});