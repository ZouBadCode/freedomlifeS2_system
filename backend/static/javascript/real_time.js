var socket = io.connect(window.location.protocol + '//' + window.location.host);
socket.on('update_time', function (data) {
    document.getElementById('time').innerHTML = data.time;
});