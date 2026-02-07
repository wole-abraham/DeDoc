
const API_URL = "http://127.0.0.1:8000"; // Assuming backend is on default port
let currentSymptoms = [];
let currentSymptomsNo = [];
let lastQuestionSymptom = null;

const messagesContainer = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const extractedInfo = document.getElementById('extracted-info');
const chatContainer = document.getElementById('chat-container');

function toggleChat() {
    chatContainer.classList.toggle('hidden');
    if (!chatContainer.classList.contains('hidden')) {
        chatInput.focus();
    }
}

document.getElementById('chat-toggle-btn').addEventListener('click', toggleChat);
document.getElementById('chat-close-btn').addEventListener('click', toggleChat);

function appendMessage(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', type);

    // Simple sanitization
    const sanitizedText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    msgDiv.innerHTML = sanitizedText;

    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateInfoDisplay() {
    if (extractedInfo) {
        let content = '';
        if (currentSymptoms.length > 0) {
            currentSymptoms.forEach(s => {
                content += `<span class="tag positive">${s.replace('_', ' ')}</span>`;
            });
        }
        if (currentSymptomsNo.length > 0) {
            currentSymptomsNo.forEach(s => {
                content += `<span class="tag negative">No ${s.replace('_', ' ')}</span>`;
            });
        }
        extractedInfo.innerHTML = content;
    }
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // 1. Display user message
    appendMessage(text, 'user');
    chatInput.value = '';
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // 2. Send to backend
    try {
        const payload = {
            message: text,
            symptoms: currentSymptoms,
            symptoms_no: currentSymptomsNo,
            last_question_symptom: lastQuestionSymptom
        };

        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // 3. Update state
        currentSymptoms = data.symptoms;
        currentSymptomsNo = data.symptoms_no;
        lastQuestionSymptom = data.last_question_symptom;

        // 4. Display bot response
        appendMessage(data.message, 'bot');
        updateInfoDisplay();

        // 5. If diagnosis found, maybe show a special UI or alert
        if (data.diagnosis_found) {
            const successMsg = document.createElement('div');
            successMsg.className = 'message bot success';
            successMsg.style.backgroundColor = '#d4edda';
            successMsg.style.color = '#155724';
            successMsg.innerText = "Diagnosis Process Complete. Check explanation above.";
            messagesContainer.appendChild(successMsg);
        }

    } catch (error) {
        console.error('Error:', error);
        appendMessage("Sorry, I encountered an error connecting to the medical logic server.", 'bot');
    } finally {
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Event Listeners
if (sendBtn) sendBtn.addEventListener('click', sendMessage);

if (chatInput) chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initial greeting only once
let hasGreeted = false;
function initChat() {
    if (!hasGreeted && messagesContainer) {
        appendMessage("Hello. I am your AI medical assistant. Describe your symptoms freely.", 'bot');
        hasGreeted = true;
    }
}

// Initialize on load
initChat();
