const { connect } = require("socket.io-client");

document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.querySelector(".ai-input");
    const chatBox = document.querySelector(".chat-box");

    function addMessage(role, message) {
        const messageElem = document.createElement("p");
        messageElem.textContent = `${role}: ${message.content}`;
        chatBox.appendChild(messageElem);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
    }

    document.querySelector(".aibtn").addEventListener("click", async function() {
        var userMessage = {
            'content' : ''
        }
        userMessage.content = inputField.value.trim();
        if (!userMessage.content) return;
        addMessage("Kullanıcı", userMessage);
        inputField.value = "";

        // API'ye mesaj gönder
        try {
            const response = await fetch("/send_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (response.ok) {
                const data = await response.json();
                jsonData = JSON.parse(data)
                addMessage("AI Asistan", jsonData.message);
            } else {
                addMessage("AI Asistan", {'content' : 'mesaj alınamadı'});
            }
        } catch (error) {
            console.error("Hata:", error);
            addMessage("AI Asistan", "Bir hata oluştu.");
        }
    });
});