// app.js
const chatHistory = document.getElementById("chatHistory");

// Add this function
function showInitialMessage() {
    const initialMessage = "I am Bennett Bot. What do you want to know about Bennett?";
    const botMessageElement = createBotMessage(initialMessage);
    chatHistory.appendChild(botMessageElement);
}

// Call the function when the page loads
showInitialMessage();

document.getElementById("sendMessage").addEventListener("click", sendMessage);
document.getElementById("inputMessage").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
    const input = document.getElementById('inputMessage');
    const message = input.value.trim();

    if (message) {
        // Show user message
        const userMessageElement = createUserMessage(message);
        chatHistory.appendChild(userMessageElement);
        input.value = '';

        // Add loading animation
        const loadingElement = createLoadingElement();
        chatHistory.appendChild(loadingElement);

        // Scroll to the bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Get bot response and update UI
        const botResponse = await getBotResponse(message);
        chatHistory.removeChild(loadingElement);
        const botMessageElement = createBotMessage(botResponse);
        chatHistory.appendChild(botMessageElement);

        // Scroll to the bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

function createUserMessage(text) {
    const message = document.createElement('div');
    message.classList.add('message', 'user');
    message.innerHTML = text + ' <img src="programmer.png" class="user-icon">'; // Add the user icon
    return message;
}

function createBotMessage(text) {
    const message = document.createElement('div');
    message.classList.add('message', 'bot');
    message.innerHTML = '<img src="bot.png" class="bot-icon"> ' + text; // Add the bot icon
    return message;
}

function createLoadingElement() {
    const loadingElement = document.createElement('div');
    loadingElement.classList.add('loading');
    loadingElement.innerHTML = `
        <span class="loading-dot"></span>
        <span class="loading-dot"></span>
        <span class="loading-dot"></span>
    `;
    return loadingElement;
}

async function getBotResponse(message) {
    // Simulate a delay for the bot response
    const response = await fetch("https://13.127.235.246/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        return data.reply;

    // Replace this part with the actual API call to get the bot response
    return `Your message was: ${message}`;
}


    const sendMessageToBackend = async (message) => {
        const response = await fetch("https://13.127.235.246/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        return data.reply;
    };

   
