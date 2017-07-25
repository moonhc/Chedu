$(document).ready(function() {
  var socket = io.connect('http://52.53.49.26')

  socket.on('connect', function() {
    socket.send('new user')
  })

  socket.on('message', function(msg) {
    $('.msg-log').append('<li>' + msg +'</li>')
  })

  $('.msg-send').on('click', function() {
    var msg = $('.msg-input').val()
    if (msg != '') {
      socket.send(msg)
      $('.msg-input').val('')
    }
  })
})
