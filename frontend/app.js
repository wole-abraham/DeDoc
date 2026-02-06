const ALL_SYMPTOMS = new Set(); // Not strictly needed anymore, backend handles it

let collectedSymptoms = new Set();
let collectedNo = new Set(); // Track negative facts
let recursionCount = 0; // For progress bar estimation

const questions = {
    // --- ROOT BOOTSTRAP ---
    'root': {
        text: "What is your primary concern today?",
        options: [
            { label: "High Temperature / Fever", symptom: "fever" },
            { label: "Persistent Coughing", symptom: "cough" },
            { label: "Shaking / Chills", symptom: "chills" },
            { label: "Feeling Weak / Tired", symptom: "fatigue" },
            { label: "Headache / Pain", symptom: "headache" }
        ]
    }
};

const loaderOverlay = document.getElementById('loader-overlay');
const questionCard = document.getElementById('question-card');
const questionText = document.getElementById('question-text');
const actionsContainer = document.getElementById('actions-container');
const progressBar = document.getElementById('progress-bar');

const factBaseContainer = document.querySelector('.fact-base-container');
const factBaseBtn = document.getElementById('fact-base-toggle');
const factBaseContent = document.getElementById('fact-base-content');
const factsList = document.getElementById('facts-list');
const deducedList = document.getElementById('deduced-list');

const logicBtn = document.getElementById('logic-btn');
const logicModal = document.getElementById('logic-modal');
const closeLogicModal = document.getElementById('close-logic-modal');
// const logicContainer = document.querySelector('.logic-container'); // Removed usage for simplicity if needed, but keeping existing ref

function init() {
    setTimeout(() => {
        loaderOverlay.classList.add('fade-out');
        setTimeout(() => {
            loaderOverlay.style.display = 'none';
            factBaseContainer.classList.add('content-visible');
            factBaseContainer.classList.remove('hidden-initially');
            document.querySelector('.logic-container').classList.add('content-visible');
            document.querySelector('.logic-container').classList.remove('hidden-initially');
        }, 1500);

        renderNode('root');
        updateFactDisplay();
        updateProgressBar(0);

    }, 2500);
}

function renderNode(nodeId) {
    if (!questions[nodeId]) {
        // Fallback or Error
        console.error("Node not found:", nodeId);
        return;
    }

    const node = questions[nodeId];
    questionText.textContent = node.text;
    actionsContainer.innerHTML = '';

    node.options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-no';
        // Style "Primary" choices as Yes buttons
        btn.className = 'btn btn-yes';

        btn.textContent = option.label;
        btn.onclick = () => handleBootstrapAnswer(option);
        actionsContainer.appendChild(btn);
    });
}

// Initial Static Answer Handler
function handleBootstrapAnswer(option) {
    if (option.symptom) collectedSymptoms.add(option.symptom);

    updateFactDisplay();
    recursionCount++;
    updateProgressBar(10); // Start of journey

    // Transition to Dynamic Mode
    runDynamicDiagnosis();
}

// Dynamic Answer Handler (Yes/No)
function handleDynamicAnswer(symptom, isYes) {
    if (isYes) {
        collectedSymptoms.add(symptom);
    } else {
        collectedNo.add(symptom);
    }

    recursionCount++;
    let prog = Math.min(10 + (recursionCount * 5), 95);
    updateProgressBar(prog);

    updateFactDisplay();
    runDynamicDiagnosis(); // Loop
}

async function runDynamicDiagnosis() {
    // UI Loading State
    questionText.classList.add('fade-up');

    setTimeout(async () => {
        questionText.textContent = "Thinking...";
        questionText.classList.remove('fade-up');
        actionsContainer.innerHTML = '<div class="loader">Logically deducing...</div>';

        try {
            const response = await fetch('http://127.0.0.1:8000/diagnose', { // CHANGED from hardcoded URL to localhost for dev
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symptoms: Array.from(collectedSymptoms),
                    symptoms_no: Array.from(collectedNo)
                })
            });

            const data = await response.json();

            // 1. Check for Diagnosis
            if (data.inferred_diseases.length > 0) {
                showDiagnosis(data);
                updateProgressBar(100);
                return;
            }

            // 2. Check for Next Question
            if (data.next_question) {
                renderDynamicQuestion(data.next_question);
            } else {
                // No diagnosis, no more questions
                showInconclusive(data);
            }

            updateFactDisplay(data.explanation);

        } catch (error) {
            questionText.textContent = "Error connecting to expert system.";
            actionsContainer.innerHTML = '<button class="btn btn-no" onclick="location.reload()">Retry</button>';
            console.error(error);
        }
    }, 400); // Small UI delay for smoothness
}

function renderDynamicQuestion(symptomRaw) {
    // Format text
    const fmt = symptomRaw.replace(/_/g, " ");
    questionText.textContent = `Do you have ${fmt}?`;

    actionsContainer.innerHTML = '';

    // Yes Button
    const btnYes = document.createElement('button');
    btnYes.className = 'btn btn-yes';
    btnYes.textContent = "Yes";
    btnYes.onclick = () => handleDynamicAnswer(symptomRaw, true);

    // No Button
    const btnNo = document.createElement('button');
    btnNo.className = 'btn btn-no';
    btnNo.textContent = "No";
    btnNo.onclick = () => handleDynamicAnswer(symptomRaw, false);

    actionsContainer.appendChild(btnYes);
    actionsContainer.appendChild(btnNo);
}

function showDiagnosis(data) {
    let msg = "";
    if (data.inferred_diseases.length > 0) {
        msg += `<strong>DIAGNOSIS CONFIRMED:</strong><br>${data.inferred_diseases.join(", ").toUpperCase().replace(/_/g, " ")}<br><br>`;
    }
    if (data.clinical_states.length > 0) {
        msg += `<small>Clinical States: ${data.clinical_states.join(", ").replace(/_/g, " ")}</small>`;
    }
    questionText.innerHTML = msg;

    actionsContainer.innerHTML = '';
    const restartBtn = document.createElement('button');
    restartBtn.className = 'btn btn-yes';
    restartBtn.textContent = "Start Over";
    restartBtn.onclick = () => location.reload();
    actionsContainer.appendChild(restartBtn);

    factBaseContent.classList.remove('hidden');
}

function showInconclusive(data) {
    questionText.innerHTML = "No specific diagnosis could be confirmed.<br><small>We have exhausted relevant questions.</small>";

    actionsContainer.innerHTML = '';
    const restartBtn = document.createElement('button');
    restartBtn.className = 'btn btn-yes';
    restartBtn.textContent = "Start Over";
    restartBtn.onclick = () => location.reload();
    actionsContainer.appendChild(restartBtn);
}

function updateFactDisplay(trace = null) {
    let symList = Array.from(collectedSymptoms).map(s => `<li class="yes-fact">YES: ${s}</li>`).join('');
    symList += Array.from(collectedNo).map(s => `<li class="no-fact" style="color:#ef4444">NO: ${s}</li>`).join('');

    factsList.innerHTML = symList || "<li>No symptoms reported yet</li>";

    if (trace) {
        deducedList.innerHTML = trace.map(t => `<li>${t}</li>`).join('');
    } else {
        deducedList.innerHTML = "<li>Waiting for analysis...</li>";
    }
}

// Logic Modal Event Listeners
logicBtn.addEventListener('click', () => { logicModal.classList.remove('hidden'); });
closeLogicModal.addEventListener('click', () => { logicModal.classList.add('hidden'); });
logicModal.addEventListener('click', (e) => { if (e.target === logicModal) logicModal.classList.add('hidden'); });
factBaseBtn.addEventListener('click', (e) => { e.stopPropagation(); factBaseContent.classList.toggle('hidden'); });
document.addEventListener('click', (e) => { if (!factBaseContainer.contains(e.target)) factBaseContent.classList.add('hidden'); });

function updateProgressBar(val) {
    progressBar.style.width = `${val}%`;
}

init();
