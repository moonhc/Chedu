$(document).ready(function() {
  passcode = $('#data').data('passcode')
  uname = $('#data').data('uname')
  socket = io.connect('http://52.53.49.26')

  socket.on('connect', function() {
    socket.emit('join', {room: passcode, uname: uname})
  })

  socket.on('message', function(data) {
    switch (data.type) {
      case 'new':
        $('.msg-log').append('<li><b>'+data.uname+'</b> has entered.</li>')
        break
      case 'msg':
        $('.msg-log').append('<li>' + data.msg +'</li>')
        break
    }

  })

  $('.msg-send').on('click', function() {
    var msg = $('.msg-input').val()
    if (msg != '') {
      socket.send({msg: msg, room: passcode, uname: uname, type: 'msg'})
      $('.msg-input').val('')
    }
  })
})
