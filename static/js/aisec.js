document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.querySelector(".ai-input");
    const chatBox = document.querySelector(".chat-box");

    function addMessage(role, message) {
        const messageElem = document.createElement("p");
        messageElem.textContent = `${role}: ${message}`;
        chatBox.appendChild(messageElem);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
    }

    document.querySelector(".aibtn").addEventListener("click", async function () {
        userMessage= inputField.value.trim();
        if (!userMessage) return;
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
                body: JSON.stringify({ message: userMessage })
            });
            if (response.ok) {
                const data = await response.json();
                addMessage("AI Asistan", data);
                inputField.disabled = false;
            }
            else {

                addMessage("AI Asistan", 'mesaj alınamadı');
                inputField.disabled = false;
            }
        } catch (error) {
            inputField.disabled = false;

            console.error("Hata:", error);
            addMessage("AI Asistan", "Bir hata oluştu.");
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    receiverInputField = document.querySelector("#receiver_name");
    amountInputField = document.querySelector("#amount");

    document.querySelector("#transmission_submit").addEventListener("click", async function () {
        console.log("transmission")
        receiverName = receiverInputField.value.trim()
        amountInput = parseInt(amountInputField.value.trim())
        if (Number.isInteger((amountInput))) {
            try {
                const response = await fetch("/transform", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ receiver_name: receiverName, amount: amountInput })
                });
                console.log("fetching....")
                if (response.ok) {
                    console.log("transition completed");
                    receiverInputField.value = ""
                    amountInputField.value = ""
                }

            } catch (error) {
                console.log(error)
            }
        }
        
    })
});