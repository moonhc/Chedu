$(document).ready(function() {
  var socket = io.connect('http://54.193.3.64')

  socket.on('connect', function() {
    socket.send('new user')
  })

  socket.on('message', function(msg) {
    $('.msg-log').append('<li>' + msg +'</li>')
  })

  $('.msg-send').on('click', function() {
    socket.send($('.msg-input').val())
    $('.msg-input').val('')
  })
})
