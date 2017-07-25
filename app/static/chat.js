$(document).ready(function() {
  passcode = $('#data').data('passcode')
  uname = $('#data').data('uname')
  socket = io.connect('http://52.53.49.26')

  socket.on('connect', function() {
    socket.emit('join', {room: passcode, uname: uname})
    console.log('connect')
  })
  // socket.on('room test', function(msg) {
  //   console.log(msg)
  // })
  socket.on('message', function(data) {
    console.log(data)
    $('.msg-log').append('<li>' + data.msg +'</li>')
  })

  $('.msg-send').on('click', function() {
    var msg = $('.msg-input').val()
    if (msg != '') {
      socket.send({msg: msg, room: passcode, uname: uname})
      $('.msg-input').val('')
    }
  })
})
