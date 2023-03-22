function checkUsers() {
  let xhr = new XMLHttpRequest()

  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return
    updatePageWait(xhr)
  }

  xhr.open("GET", "get-users", true)
  xhr.send()
}

function updatePageWait(xhr) {

  if (xhr.status == 200) {
    updateButton(xhr.responseText)
    return
  }
}

function updateButton(users) {
  let players = document.getElementById("num_players");
  if (players != null) {
    players.innerHTML = users;
  }
  if (parseInt(users) > 2) {
    document.getElementById("go_button").style.display = "block";
    document.getElementById("wait_div").style.display = "none";
  } else {
    document.getElementById("go_button").style.display = "none";
    document.getElementById("wait_div").style.display = "block";
  }
}

function updateTime() {
  let timer = document.getElementById("timer")
  let old_time = parseInt(timer.innerHTML)
  if (old_time > 0) {
    timer.innerHTML = old_time - 1
  } else {
    timer.style.display = "none"
    if (parseInt(document.getElementById("num_players").innerHTML) > 2) {
      document.getElementById("go_button").style.display = "block";
    }
  }
}

function tryEnter() {
  let xhr = new XMLHttpRequest()
  xhr.open("POST", "try-enter", true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send("&csrfmiddlewaretoken="+getCSRFToken());
}