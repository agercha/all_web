function updatePageChat(xhr) {

  if (xhr.status == 200) {
      let response = JSON.parse(xhr.responseText)
      updateChat(response)
      return
  }

  if (xhr.status == 0) {
      return
  }


  if (!xhr.getResponseHeader('content-type') == 'application/json') {
      return
  }

  let response = JSON.parse(xhr.responseText)
  if (response.hasOwnProperty('error')) {
      return
  }

  displayError(response)
}

function updateChat(items) {

  let chats = document.getElementById("chatbox")
  for (let i = 0; i < items['chats'].length; i++) {
      let message = items['chats'][i]
      let oldmessage = document.getElementById("id_message_div_" + message.id)
      if (typeof(oldmessage) == 'undefined' || oldmessage == null) {
          let element = document.createElement("div")
          element.id = "id_message_div_" + message.id
          element.className = "chatMessage"
          element.style.color = message.color
          element.style.fontWeight = message.weight
          element.innerHTML = "<span class='chat_username'>" + message.user + "</span>" + 
                              "<span> " + sanitize(message.text) + "</span>" 

          chats.appendChild(element)
      }
  }

  // https://stackoverflow.com/questions/40903462/how-to-keep-a-scrollbar-always-bottom
  chats.scrollTop = chats.scrollHeight;

  let players = document.getElementById("players")
  let players_guessed = 0
  while (players.hasChildNodes()) {
    players.removeChild(players.firstChild)
  }
  players.innerHTML = ""
  for (let i = 0; i < items['all_players'].length; i++) {
    let player = items['all_players'][i]
    if (player.color == '#98CC28') { players_guessed += 1 }
    let element = document.createElement("div")
    element.className = "player"
    element.style.backgroundColor = player.color
    element.innerHTML = player.name + ": " + player.score
    players.appendChild(element) 
  }


  all_in_game = items['all_players_in']
  let timer =  document.getElementById("timer")

  if (parseInt(timer.innerHTML) < items['time_left']) {
    location.reload();
  }

  if (timer.style.display == "none" & all_in_game) timer.style.display = "block"
  timer.innerHTML = items['time_left']

  if (parseInt(items['round']) >= ((items['all_players']).length - 1)) {
    // change form action to go to leaderboard
    document.getElementById("next_button").value = "leaderboard"
    document.getElementById("next_box").action = 'leaderboard'
  }

  if (items['time_left'] == "0" | players_guessed >= ((items['all_players']).length - 1)) {
    document.getElementById("guess_box").style.display = "none"
    if (items['can_draw'] == "true" | document.getElementById("next_button").value === "leaderboard") {
      document.getElementById("next_box").style.display = "block"
    }
  }
}

function sanitize(s) {
  return s.replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
}

function addChat() {
  let itemTextElement = document.getElementById("item")
  let itemTextValue   = itemTextElement.value

  itemTextElement.value = ''

  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (xhr.readyState != 4) return
      updatePageChat(xhr)
  }

  xhr.open("POST", addChatURL, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send("text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function getCSRFToken() {
  let cookies = document.cookie.split(";")
  for (let i = 0; i < cookies.length; i++) {
      let c = cookies[i].trim()
      if (c.startsWith("csrftoken=")) {
          return c.substring("csrftoken=".length, c.length)
      }
  }
  return "unknown"
}
