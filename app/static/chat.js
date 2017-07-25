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
        if (data.uname != 'Owner') {
          $('.messages-wrapper ul').append(
            '<li class="message-item-new" align="center"> \
              <span class="new-user-name">'+data.uname+'@ucsc.edu</span> \
              <span class="new-user-sentence"> has entered.</span> \
             </li>')
         }
        break
      case 'msg':
        $('.messages-wrapper ul').append(
          '<li class="message-item"> \
            <span class="nickname">'+ data.uname + '</span> \
            <span class="timestamp">' + data.time + '</span> \
            <p class="message">' + data.msg + '</p> \
           </li>')
        break
    }
  })

  $('.emoji-icon').on('click', function() {
    var msg = $('.msg-input').val()
    if (msg != '') {
      socket.send({msg: msg, room: passcode, uname: uname, type: 'msg'})
      $('.msg-input').val('')
    }
  })
})
