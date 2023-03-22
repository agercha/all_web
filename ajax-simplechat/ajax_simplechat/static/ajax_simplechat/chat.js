"use strict"

// Sends a new request to update the to-do list
function getList() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/ajax_simplechat/get-list", true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
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

function updateList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("todo-list")

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        let olditem = document.getElementById("id_item_div_" + item.id)

        // Builds a new HTML list item for the todo-list
        if (typeof(olditem) == 'undefined' || olditem == null) {
            let element = document.createElement("div")
            element.id = "id_item_div_" + item.id
            element.className = "chatMessage"
            element.innerHTML = "<span class='username'>" + item.user + "</span>" + 
                                "<span> " + sanitize(item.text) + "</span>" 

            // Adds the todo-list item to the HTML list
            list.appendChild(element)
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

function addItem() {
    let itemTextElement = document.getElementById("item")
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addItemURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
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

