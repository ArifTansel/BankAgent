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
            inputField.disabled = true;
            const response = await fetch("/send_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage.content })
            });

            if (response.ok) {
                const data = await response.json();
                jsonData = JSON.parse(data)
                addMessage("AI Asistan", jsonData.message);
                inputField.disabled = false ;
            } 
            else {

                addMessage("AI Asistan", {'content' : 'mesaj alınamadı'});
                inputField.disabled = false;
            }
        } catch (error) {
            inputField.disabled = false;

            console.error("Hata:", error);
            addMessage("AI Asistan", "Bir hata oluştu.");
        }
    });
});