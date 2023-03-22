var target_text = ""
var current_row = 0

function makeWordDict(word) {
  var d = {}
  for (var i = 0; i < 5; i++) {
    var char = word[i]
    if (char in d) {
      d[char] ++
    } else {
      d[char] = 1
    }
  }
  return d
}

function decrementChar(d, char) {
  if (d[char] == 1) {
    delete d[char]
  } else {
    d[char] --
  }
  return d
}

function setRow(word) {
  word = word.toUpperCase()
  d = makeWordDict(target_text)
  for (var i = 0; i < 5; i++) {
    var char = word[i]
    cell_id = `cell_${current_row}_${i}`
    document.getElementById(cell_id).innerHTML = char
    if (char === target_text[i]) {
      document.getElementById(cell_id).style.backgroundColor = "greenyellow";
      decrementChar(d, char);
      console.log(d)
    }
  }
  for (var i = 0; i < 5; i++) {
    var char = word[i]
    cell_id = `cell_${current_row}_${i}`
    document.getElementById(cell_id).innerHTML = char
    if (char != target_text[i]) {
      if (char in d) {
        document.getElementById(cell_id).style.backgroundColor = "gold";
        decrementChar(d, char)
      } else {
        document.getElementById(cell_id).style.backgroundColor = "deeppink";
      }
    }
  }
  current_row ++
}

function checkValidWord(word) {
  if (word.length < 5) {
    document.getElementById("status").innerHTML = "Invalid Input: Too Short"
    return false
  } else if (word.length > 5) {
    document.getElementById("status").innerHTML = "Invalid Input: Too Long"
    return false
  }
  for (var i = 0; i < 5; i++) {
    let char = word[i]
    if (char.toUpperCase() === char.toLowerCase()) {
      document.getElementById("status").innerHTML = `Invalid Input: ${char }is not a Letter`
      return false
    }
  }
  return true
}

function setTarget() {
  target_text_temp = document.getElementById("target_text").value
  if (checkValidWord(target_text_temp)) {
    document.getElementById("status").innerHTML = "Start!"
    document.getElementById("target_text").value = ""
    target_text = target_text_temp.toUpperCase()
  }
}

function makeGuess() {
  if (target_text === "") {
    document.getElementById("status").innerHTML = "No target word set yet"
    return
  }
  guess_text = document.getElementById("guess_text").value
  if (checkValidWord(guess_text)) {
    setRow(guess_text)
    document.getElementById("guess_text").value = ""
    if (guess_text.toUpperCase() === target_text) {
      document.getElementById("status").innerHTML = "You Win!"
    } else if (current_row == 6) {
      document.getElementById("status").innerHTML = "You Lose!"
    } else {
      document.getElementById("status").innerHTML = "Good Guess!"
    }
  }
}