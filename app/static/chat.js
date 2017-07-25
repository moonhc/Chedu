$(document).ready(function() {
  passcode = $('#data').data('passcode')
  uname = $('#data').data('uname')
  socket = io.connect('http://52.53.49.26')

  function send_message() {
    $('.msg-input').focus()
    var msg = $('.msg-input').val()
    if (msg != '') {
      socket.send({msg: msg, room: passcode, uname: uname, type: 'msg'})
      $('.msg-input').val('')
    }
  }

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
        if ($('.message-item:last .nickname').text() == data.uname) {
          $('.message-item:last').append(
            '<p class=message>' + data.msg + '</p>')
        }
        else if (data.uname == uname) {
          $('.messages-wrapper ul').append(
            '<li class="message-item reverse"> \
              <span class="nickname">'+ data.uname + '</span> \
              <span class="timestamp">' + data.time + '</span> \
              <p class="message">' + data.msg + '</p> \
             </li>')
        }
        else {
          $('.messages-wrapper ul').append(
            '<li class="message-item"> \
              <span class="nickname">'+ data.uname + '</span> \
              <span class="timestamp">' + data.time + '</span> \
              <p class="message">' + data.msg + '</p> \
             </li>')
         }
        break
    }
    $(".messages-wrapper").stop().animate(
      { scrollTop: $(".messages-wrapper")[0].scrollHeight}, 1000)
  })

  $('.emoji-icon').on('click', send_message)
  $('.msg-input').on('keypress', function(e) {
    if (e.keyCode==13) {
      send_message()
      return false
    }
  })
})
