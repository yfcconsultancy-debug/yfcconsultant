document.addEventListener("DOMContentLoaded", () => {
    const chatLauncher = document.getElementById("chat-launcher");
    const chatWindow = document.getElementById("chat-window");
    const closeChat = document.getElementById("close-chat");
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const quickButtonsContainer = document.getElementById("quick-buttons");
    const typingIndicator = document.getElementById("typing-indicator");

    let historyLoaded = false;

    // --- Event Listeners ---
    chatLauncher.addEventListener("click", toggleChatWindow);
    closeChat.addEventListener("click", toggleChatWindow);
    chatForm.addEventListener("submit", handleFormSubmit);
    quickButtonsContainer.addEventListener("click", handleQuickButtonClick);


    function toggleChatWindow() {
        chatWindow.classList.toggle("hidden");
        // Load history only on first open
        if (!chatWindow.classList.contains("hidden") && !historyLoaded) {
            loadChatHistory();
            sendMessage("Hello", true); // Start the conversation without user message
        }
    }

    async function loadChatHistory() {
        try {
            const response = await fetch("/history");
            const history = await response.json();
            history.forEach(msg => addMessage(msg.from, msg.text));
            historyLoaded = true;
        } catch (error) {
            console.error("Failed to load chat history:", error);
        }
    }

    function handleFormSubmit(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = "";
        }
    }

    function handleQuickButtonClick(event) {
        if (event.target.tagName === 'BUTTON') {
            const message = event.target.textContent;
            sendMessage(message);
        }
    }

    // --- Communication ---
    function sendMessage(message, isInitial = false) {
        if (!isInitial) {
            addMessage("user", message);
        }
        
        updateQuickButtons([]); // Clear buttons immediately
        typingIndicator.classList.remove("hidden");
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Wait for 1 second, then fetch and show the bot's reply
        setTimeout(async () => {
            try {
                const response = await fetch("/send", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message }),
                });
                const data = await response.json();
                
                typingIndicator.classList.add("hidden"); // Hide indicator
                addMessage("bot", data.text);
                updateQuickButtons(data.buttons);

            } catch (error) {
                console.error("Failed to send message:", error);
                typingIndicator.classList.add("hidden");
                addMessage("bot", "Sorry, something went wrong. Please try again later.");
            }
        }, 1000); // 1-second delay
    }

    // --- UI Updates ---
    function addMessage(sender, text) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);

        const bubble = document.createElement("div");
        bubble.classList.add("message-bubble");
        bubble.textContent = text;
        
        const timestamp = document.createElement('div');
        timestamp.classList.add('message-time');
        timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageElement.appendChild(bubble);
        messageElement.appendChild(timestamp);
        chatMessages.appendChild(messageElement);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateQuickButtons(buttons) {
        quickButtonsContainer.innerHTML = "";
        if (buttons && buttons.length > 0) {
            buttons.forEach(buttonText => {
                const button = document.createElement("button");
                button.textContent = buttonText;
                quickButtonsContainer.appendChild(button);
            });
        }
    }
});