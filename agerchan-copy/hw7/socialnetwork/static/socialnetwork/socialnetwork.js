"use strict"

function getStream() {
  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState != 4) return
      updatePage(xhr)
  }

  xhr.open("GET", "socialnetwork/get-global", true)
  xhr.send()
}

function getFriendStream() {
  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState != 4) return
      updatePage(xhr)
  }

  xhr.open("GET", "socialnetwork/get-follower", true)
  xhr.send()
}

function updatePage(xhr) {
  if (xhr.status == 200) {
    let response = JSON.parse(xhr.responseText)
    updateStream(response)
    return
  }

  if (xhr.status == 0) {
    displayError("Cannot connect to server")
    return
  }


  if (!xhr.getResponseHeader('content-type') == 'application/json') {
    displayError("Received status=" + xhr.status)
    return
  }

  let response = JSON.parse(xhr.responseText)
  if (response.hasOwnProperty('error')) {
    displayError(response.error)
    return
  }

  displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateStream(posts) {
  let list = document.getElementById("post-stream")

  for (let i = 0; i < posts.length; i++) {
    let post = posts[i]
    let comments = post.comments;
    let oldpost = document.getElementById("id_post_div_" + post.id)
    if (typeof(oldpost) == 'undefined' || oldpost == null) {
      let comment_html = ''
      for (let j = 0; j < comments.length; j++) {
        let comment = comments[j];
        let comment_date = new Date(comment.date_time)

        comment_html += '<div id="id_comment_div_' + comment.id + 
          '" class="comment">' + '<span class="post_user"> <a href="/get_profile/' + 
          comment.author + '" id="id_comment_profile_' +
          comment.id + '" class="post_user_link">' + 
          comment.author_first_name + ' ' + comment.author_last_name + '</a>' + '</span>' +
          '<span id="id_comment_text_' + comment.id + '" class="post_content">' +
          comment.content + '</span>' + '<span id="id_comment_date_time_' +
          comment.id + '" class="post_time">' + 
          comment_date.toLocaleDateString() + ' ' + comment_date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) +
          '</span>' + '</div>'
      }

      // Builds a new HTML list item for the todo-list
      let element = document.createElement('div')
      let post_date = new Date(post.date_time)
      element.id = "id_post_div_" + post.id
      element.className = "post"
      element.innerHTML = '<span class="post_user"> <a href="/get_profile/' + 
        post.author + '" id="id_post_profile_' + post.id +
        '" class="post_user_link">' + post.author_first_name + ' ' + 
        post.author_last_name + '</a> </span>' + 
        '<span id="id_post_text_' + post.id + 
        '" class = "post_content">' + post.content + '</span>' +
        '<span id="id_post_date_time_' + post.id + '" class = "post_time">' +
        post_date.toLocaleDateString() + ' ' + post_date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) +
        '</span> <span id="id_comment_section_' + 
        post.id + '">' + comment_html + '</span>' +
        '<div class="post_input_text">' + '<label>new comment:</label>' + 
        '<input type="text" name="post_input_text" class="text"' + 
        'id="id_comment_input_text_' + post.id + '"></input>' +
        '<button onclick="addComment(' + post.id + ')" id="id_comment_button_' + 
        post.id + '">submit</button>' +
        '<input type="hidden" name="comment_post" value="' + post.id + '">' + 
        '<input name="csrfmiddlewaretoken" value="' + getCSRFToken() + '" type="hidden">' + 
        '</div>'

      // list.appendChild(element)
      list.prepend(element)
    } else {
      let comment_list = document.getElementById("id_comment_section_" + post.id)

      for (let j = 0; j < comments.length; j++) {
        let comment = comments[j];
        let comment_date = new Date(comment.date_time)

        let old_comment = document.getElementById("id_comment_profile_" + comment.id)
        if (typeof(old_comment) == 'undefined' || old_comment == null) {
          let comment_element = document.createElement('div')
          comment_element.id = "id_comment_div_" + comment.id
          comment_element.className = "comment"
          comment_element.innerHTML = '<span class="post_user"> <a href="/get_profile/' + 
            comment.author + '" id="id_comment_profile_' +
            comment.id + '" class="post_user_link">' + 
            comment.author_first_name + ' ' + comment.author_last_name + '</a>' + '</span>' +
            '<span id="id_comment_text_' + comment.id + '" class="post_content">' +
            comment.content + '</span>' + '<span id="id_comment_date_time_' +
            comment.id + '" class="post_time">' + 
            comment_date.toLocaleDateString() + ' ' + comment_date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) +
            '</span>'
          comment_list.appendChild(comment_element)
        }
      }

    }
  }
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addPost() {
  let postTextElement = document.getElementById("id_post_input_text")
  let postTextValue   = postTextElement.value

  // Clear input box and old error message (if any)
  postTextElement.value = ''
  displayError('')

  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (xhr.readyState != 4) return
    updatePage(xhr)
  }
  xhr.open("POST", addPostURL, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send("post_text="+sanitize(postTextValue)+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addComment(post_id) {
  let commentTextElement = document.getElementById("id_comment_input_text_" + post_id)
  let commentTextValue   = commentTextElement.value

  // Clear input box and old error message (if any)
  commentTextElement.value = ''
  displayError('')

  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
    if (xhr.readyState != 4) return
    updatePage(xhr)
  }
  xhr.open("POST", addCommentURL, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send("post_id="+post_id+"&comment_text="+sanitize(commentTextValue)+"&csrfmiddlewaretoken="+getCSRFToken());
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