// Function to fetch the received messages from the server and update the webpage
function fetchMessages() {
    fetch('/').then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    }).then(function(data) {
        updateMessages(data.messages);
    }).catch(function(error) {
        console.error('Error:', error);
    });
}

// Function to update the message content in the webpage
function updateMessages(messages) {
    var messageContainer = document.getElementById('messages');
    messageContainer.innerHTML = ''; // Clear the existing messages
    
    for (var i = 0; i < messages.length; i++) {
        var message = messages[i];
        var clientBox = document.createElement('div');
        clientBox.className = 'client-box';
        
        var idElement = document.createElement('h2');
        if (message.id == "not connected") {
            idElement.textContent = "Node " + (i+1) + " " + message.id;
        } else {
            idElement.textContent = "Node " + message.id + ":";
        }
        
        var dataElement = document.createElement('p');
        if (message.data !== 0) {
            var roundedData = message.data.toFixed(2);
            dataElement.textContent = "Value predicted: " + roundedData.toString();
        }
        
        clientBox.appendChild(idElement);
        clientBox.appendChild(dataElement);
        messageContainer.appendChild(clientBox);
    }
    


    
    // Calculate and display the decision
    var decisionContainer = document.getElementById('decision-container');
    var dangerTriangle = document.getElementById('danger-triangle');
    
    decisionContainer.innerHTML = ''; // Clear the decision
    var decision = document.createElement('h2');
    dec = calculateDecision(messages)
    if (dec === "Alarm!") {
        text = "Alarm! High fire risk"
        decisionContainer.classList.remove('decision-container-no-alarm');
        decisionContainer.classList.add("decision-container-alarm");
        dangerTriangle.style.display = 'block';
        
    } else {
        text = "No fire detected"
        decisionContainer.classList.remove('decision-container-alarm');
        decisionContainer.classList.add("decision-container-no-alarm");
        dangerTriangle.style.display = 'none';
    }
    decision.textContent = text;
    decisionContainer.appendChild(decision);
}

// Function to calculate the decision value based on the received data
function calculateDecision(messages) {
    var count = 0;
    var vote = 0;
    for (var i = 0; i < messages.length; i++) {
        if (messages[i] && messages[i].data && messages[i].data !== 0) {
            if (messages[i].data > 0.7) {
                vote++;
            }
            count++;
        }
    }
    if (count == 0)
        return "No Alarm"
    if (vote >= (count / 2)) {
        return "Alarm!";
    } 
    return "No Alarm";
}

// Function to periodically fetch the received messages every second
function startFetching() {
    fetchMessages();
    setInterval(fetchMessages, 1500);
}