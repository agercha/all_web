function checkTargetWord(can_draw, target_word, hidden_target_word) {
    let timer = parseInt(document.getElementById('timer').innerHTML)
    if (can_draw) {
        document.getElementById('target').innerHTML = String(target_word)
        document.getElementById('target').style.letterSpacing = "normal"
    } else if (timer <= 0) {
        document.getElementById('target').innerHTML = String(target_word)
        document.getElementById('target').style.letterSpacing = "normal"
    } else {
        document.getElementById('target').innerHTML = hidden_target_word
        document.getElementById('target').style.letterSpacing = "1em"
    }
}

function securityCheck() {
    let status = "Error: "
    if (document.getElementById("players") == null) {
        status += 'players required '
    }
    if (document.getElementById("my-canvas") == null) {
        status += 'canvas required '
    }
    if (document.getElementById("pencil") == null) {
        status += 'pencil required '
    }
    if (document.getElementById("penColor") == null) {
        status += 'penColor required '
    }
    if (document.getElementById("eraser") == null) {
        status += 'eraser required '
    }
    if (document.getElementById("stroke") == null) {
        status += 'stroke required '
    }
    if (document.getElementById("lineWidth") == null) {
        status += 'lineWidth required '
    }
    if (document.getElementById("fill") == null) {
        status += 'fill required '
    }
    if (document.getElementById("clear") == null) {
        status += 'clear required '
    }
    if (document.getElementById("timer") == null) {
        status += 'timer required '
    }
    if (document.getElementById("chatbox") == null) {
        status += 'chatbox required '
    }
    if (document.getElementById("guess_box") == null) {
        status += 'guess_box required '
    }
    if (document.getElementById("item") == null) {
        status += 'item required '
    }
    if (document.getElementById("guessbutton") == null) {
        status += 'guessbutton required '
    }

    if (status != "Error: ") {
        document.getElementById('status-message').innerHTML = status
    } else {
        document.getElementById('status-message').innerHTML = ""
    }
}

function setUpCanvas(){
    let canvas = document.getElementById('my-canvas')
    canvas.style.width = '100%'
    canvas.style.height = '100%'
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
}

function getChat() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
      if (this.readyState != 4) return
      updatePageChat(xhr)
    };
  
    xhr.open("GET", "get-chat", true)
    xhr.send()
}

function displayColorInput(display) {
    if (display) {
        document.getElementById('penColor').type = 'color'
    } else {
        document.getElementById('penColor').type = 'hidden'
    }        
}

function displayLineWidth(display) {
    if (display) {
        document.getElementById('lineWidth').type = 'range'
    } else {
        document.getElementById('lineWidth').type = 'hidden'
    }
}

function setUpSocket() {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/ws/socket-server/';
    const socket = new WebSocket(ws_path);

    let currentlyDrawing = false
    let erasing = false
    let lastknowncolor = '#000000'

    socket.onopen = function () {
        console.log("Websocket connected! Welcome to doodle.io!");
    }

    let canvas = document.getElementById("my-canvas")
    let context = canvas.getContext("2d")
    canvas.style.width = '100%'
    canvas.style.height = '100%'
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
    if (can_draw_bool) {
        canvas.addEventListener("mousedown", getStartData)
        canvas.addEventListener("mousemove", getMoveData)
        canvas.addEventListener("mouseup", getStopData)    
    }


    socket.onmessage = function (e) {
        let data = JSON.parse(e.data)
        let message = data['message']
        let x1 = data['x1']
        let y1 = data['y1']
        let color = data['color']
        let linewidth = data['linewidth']

        if(message == "start data"){
            context.beginPath()
        } else if (message == 'fill data') {
            context.beginPath()
            context.strokeStyle = color
            context.rect(0, 0, canvas.width, canvas.height)
            context.fillStyle = color
            context.fill()
        } else {
            context.strokeStyle = color
            context.lineWidth = linewidth
            context.lineTo(x1, y1)
            context.stroke()
        }

    }

    socket.onclose = function (e) {
        console.log("connection closed");
    }

    function getStartData() {
        currentlyDrawing = true

        let message = "start data"
        let x1 = event.offsetX
        let y1 = event.offsetY
        let color = document.getElementById('penColor').value
        let linewidth = document.getElementById("lineWidth").value

        if (lastknowncolor != color) {
            erasing = false
        }
        if (erasing) {
            color = "#FFFFFF"
        } else {
            lastknowncolor = color
        }

        socket.send(JSON.stringify({
            'message': message,
            'x1': x1,
            'y1': y1,
            'color': color,
            "linewidth": linewidth

        }))
        displayColorInput(false)
        displayLineWidth(false)
    }

    function getMoveData(event) {
        if (!currentlyDrawing) {
            return
        }
        let message = "move data"
        let x1 = event.offsetX
        let y1 = event.offsetY
        let color = document.getElementById('penColor').value
        let linewidth = document.getElementById("lineWidth").value

        if (lastknowncolor != color) {
            erasing = false
        }
        if (erasing) {
            color = "#FFFFFF"
        } else {
            lastknowncolor = color
        }

        socket.send(JSON.stringify({
            'message': message,
            'x1': x1,
            'y1': y1,
            'color': color,
            "linewidth": linewidth

        }))
    }

    function getStopData() {
        currentlyDrawing = false
    }

    eraserbutton = document.getElementById('eraser')
    eraserbutton.addEventListener('click', erase)

    function erase() {
        erasing = true
    }

    fillbutton = document.getElementById('fill')
    fillbutton.addEventListener('click', fill)

    function fill() {
        socket.send(JSON.stringify({
            'message': "fill data",
            'x1': 0,
            'y1': 0,
            'color': document.getElementById('penColor').value,
            "linewidth": 0

        }))
        displayColorInput(false)
        displayLineWidth(false)
    }

    clearbutton = document.getElementById('clear')
    clearbutton.addEventListener('click', clear)

    function clear() {
        socket.send(JSON.stringify({
            'message': "fill data",
            'x1': 0,
            'y1': 0,
            'color': "#FFFFFF",
            "linewidth": 0

        }))
        displayColorInput(false)
        displayLineWidth(false)
    }

}

function setUpGame(can_draw) {
    getChat()
    if (can_draw) setUpCanvas()
    setUpSocket()
}
