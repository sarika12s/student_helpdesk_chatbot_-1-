const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const speakerBtn = document.getElementById("speakerBtn");

// Add message to UI
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "bot-msg";
    msg.textContent = text;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// SEND TEXT MESSAGE
sendBtn.onclick = async () => {
    const msg = userInput.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    userInput.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg })
    });

    const data = await response.json();
    addMessage(data.response, "bot");
};

// SPEECH TO TEXT
micBtn.onclick = () => {
    try {
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = "en-US";
        rec.start();

        rec.onresult = (e) => {
            userInput.value = e.results[0][0].transcript;
        };

        rec.onerror = () => alert("Microphone error. Check permissions.");
    } catch {
        alert("Speech recognition not supported in this browser.");
    }
};

// TEXT TO SPEECH
speakerBtn.onclick = () => {
    const lastBotMsg = [...document.querySelectorAll(".bot-msg")].pop();
    if (!lastBotMsg) return;

    const utter = new SpeechSynthesisUtterance(lastBotMsg.textContent);
    utter.lang = "en-US";
    utter.rate = 1;
    speechSynthesis.speak(utter);
};
