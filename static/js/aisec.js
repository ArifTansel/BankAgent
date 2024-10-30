
document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.querySelector(".form-control");
    const chatBox = document.querySelector(".chat-box");

    function addMessage(role, message) {
        const messageElem = document.createElement("p");
        messageElem.textContent = `${role}: ${message}`;
        chatBox.appendChild(messageElem);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
    }

    document.querySelector(".btn").addEventListener("click", async function() {
        const userMessage = inputField.value.trim();
        if (!userMessage) return;

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
                addMessage("AI Asistan", data.response);
            } else {
                addMessage("AI Asistan", "Yanıt alınamadı.");
            }
        } catch (error) {
            console.error("Hata:", error);
            addMessage("AI Asistan", "Bir hata oluştu.");
        }
    });
});