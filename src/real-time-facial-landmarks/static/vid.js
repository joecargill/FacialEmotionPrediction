
    var v1 = document.querySelector("#v1");
    var v2 = document.querySelector("#v2");

    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

    if (navigator.getUserMedia) {
        navigator.getUserMedia({video: true}, handleVideo, videoError);
        navigator.getUserMedia({video: true}, handleVideo, videoError);
    }

    function handleVideo(stream) {
        v1.src = window.URL.createObjectURL(stream);
        v2.src = window.URL.createObjectURL(stream);
    }


    function videoError(e) {
        // do something
    }


    namespace = '/vid';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    // Event handler for new connections.
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    function send_frame() {
        var video  = document.getElementById("v1");
        var canvas = document.createElement('canvas');
        canvas.width  = video.videoWidth;
        canvas.height = video.videoHeight;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // quality ranges from 0.00-1.00
        var jpgQuality=0.60;

        // get the dataURL in .jpg format
        var vid_frame = canvas.toDataURL('image/jpeg',jpgQuality);
        socket.emit('vid_frame', {imageData: vid_frame});




    }

    socket.on('Emotion', function(e) {
            console.log(e.emotion);
            console.log("here");
            $('#vi').text(e.emotion)
            console.log("here too");
    });

    send_frame();
    setInterval(send_frame,3000);