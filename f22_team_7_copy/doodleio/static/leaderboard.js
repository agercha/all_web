function checkUsersLeaderboard() {
  let xhr = new XMLHttpRequest()

  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return
    updatePageWaitLeaderboard(xhr)
  }

  xhr.open("GET", "get-users-leaderboard", true)
  xhr.send()
}

function updatePageWaitLeaderboard(xhr) {

  if (xhr.status == 200) {
    updateButtonLeaderboard(xhr.responseText)
    return
  }
}

function updateButtonLeaderboard(users) {
  if (users == "True") {
    document.getElementById("next_box").style.display = "block"
  } else {
    document.getElementById("next_box").style.display = "none"
  }
}