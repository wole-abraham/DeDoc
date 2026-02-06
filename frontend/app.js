const ALL_SYMPTOMS = new Set([
    "fever", "cough", "headache", "chills", "fatigue",
    "body_pain", "nausea", "sweating",
    // Qualifiers & Subtypes
    "high_fever", "intermittent_fever",
    "dry_cough", "productive_cough",
    "retro_orbital_pain", "joint_pain", "muscle_pain",
    "abdominal_pain", "diarrhea", "vomiting", "rash",
    // New Advanced Facts (Expansion Phase)
    "shortness_of_breath", "chest_pain", "congestion",
    "sensitivity_light", "stiff_neck", "facial_pressure",
    "loss_of_smell", "severe_diarrhea",
    // Temporal & Context
    "sudden_onset", "gradual_onset",
    "mosquito_exposure", "recent_travel", "unsafe_food_exposure", "sick_contact"
]);

let collectedSymptoms = new Set();
let currentNodeId = 'root';

// --- Progress Mapping ---
const NODE_PROGRESS = {
    'root': 10,
    // Fever Branch
    'fever_q1': 20, 'fever_pattern': 35, 'fever_sweat': 50, 'fever_chills': 65,
    // Cough Branch
    'cough_q1': 20, 'cough_type': 35, 'resp_distress': 50, 'chest_pain_q': 65, 'neuro_smell': 75,
    // Other Branches
    'chills_q1': 25, 'general_q1': 25,
    // Convergence - Pain/Head
    'pain_head': 60,
    'head_neuro_1': 70, 'head_neuro_2': 80, 'pain_head_retro': 80,
    // Body Pain
    'pain_body': 70, 'pain_body_type': 80, 'fatigue_check': 85,
    // GI
    'stomach_check': 75, 'stomach_check_2': 85,
    // Context
    'context_onset': 90, 'context_exposure': 95, 'context_food': 98,
    'final_review': 99,
    'diagnose': 100
};

const questions = {

    // --- ROOT ---
    'root': {
        text: "What is your primary concern today?",
        options: [
            { label: "High Temperature / Fever", symptom: "fever", next: 'fever_q1' },
            { label: "Persistent Coughing", symptom: "cough", next: 'cough_q1' },
            { label: "Shaking / Chills", symptom: "chills", next: 'chills_q1' },
            { label: "Feeling Weak or General Pain", next: 'general_q1' }
        ]
    },

    // --- FEVER BRANCH ---
    'fever_q1': {
        text: "Have you measured your body temperature?",
        options: [
            { label: "Yes, High (>39°C)", symptoms: ["fever", "high_fever"], next: 'fever_pattern' },
            { label: "Yes, Moderate", symptom: "fever", next: 'fever_pattern' },
            { label: "No, but I feel hot", symptom: "fever", next: 'fever_pattern' },
            { label: "No, strictly normal", next: 'fever_pattern' }
        ]
    },
    'fever_pattern': {
        text: "Does the fever come and go (intermittent) or stay constant?",
        options: [
            { label: "Intermittent (Comes and goes)", symptom: "intermittent_fever", next: 'fever_sweat' },
            { label: "Constant / Continuous", next: 'fever_sweat' }
        ]
    },
    'fever_sweat': {
        text: "Are you sweating profusely, even when not exerting yourself?",
        options: [
            { label: "Yes, heavy sweating", symptom: "sweating", next: 'fever_chills' },
            { label: "No", next: 'fever_chills' }
        ]
    },
    'fever_chills': {
        text: "Do you experience shivering or shaking sensations (chills)?",
        options: [
            { label: "Yes, uncontrollably", symptom: "chills", next: 'pain_head' },
            { label: "No", next: 'pain_head' }
        ]
    },

    // --- COUGH BRANCH ---
    'cough_q1': {
        text: "Is your cough accompanied by a fever?",
        options: [
            { label: "Yes, I have a fever", symptom: "fever", next: 'cough_type' },
            { label: "No fever", next: 'cough_type' }
        ]
    },
    'cough_type': {
        text: "Is the cough dry or does it produce phlegm?",
        options: [
            { label: "Dry (No phlegm)", symptom: "dry_cough", next: 'resp_distress' },
            { label: "Productive (Phlegm)", symptom: "productive_cough", next: 'resp_distress' }
        ]
    },
    'resp_distress': {
        text: "Are you experiencing shortness of breath or difficulty breathing?",
        options: [
            { label: "Yes, struggling to breathe", symptom: "shortness_of_breath", next: 'chest_pain_q' },
            { label: "No", next: 'chest_pain_q' }
        ]
    },
    'chest_pain_q': {
        text: "Do you feel pain or tightness specifically in your chest?",
        options: [
            { label: "Yes", symptom: "chest_pain", next: 'neuro_smell' },
            { label: "No", next: 'neuro_smell' }
        ]
    },
    'neuro_smell': {
        text: "Have you noticed a sudden loss of taste or smell?",
        options: [
            { label: "Yes", symptom: "loss_of_smell", next: 'pain_head' },
            { label: "No", next: 'pain_head' }
        ]
    },

    // --- CHILLS BRANCH ---
    'chills_q1': {
        text: "Do you also feel hot or feverish alongside the chills?",
        options: [
            { label: "Yes", symptom: "fever", next: 'fever_sweat' },
            { label: "No, just cold/shaking", next: 'pain_head' }
        ]
    },

    // --- GENERAL / PAIN BRANCH ---
    'general_q1': {
        text: "Do you feel any specific fatigue or tiredness?",
        options: [
            { label: "Yes, exhausted", symptom: "fatigue", next: 'pain_head' },
            { label: "No", next: 'pain_head' }
        ]
    },

    // --- CONVERGENCE POINT 1: PAIN & HEADACHE ---
    'pain_head': {
        text: "Are you experiencing a headache or facial pressure?",
        options: [
            { label: "Yes, Severe Headache", symptoms: ["headache", "severe_headache"], next: 'head_neuro_1' },
            { label: "Yes, Facial Pressure/Sinus", symptoms: ["headache", "facial_pressure", "congestion"], next: 'head_neuro_1' },
            { label: "Yes, Mild", symptom: "headache", next: 'head_neuro_1' },
            { label: "No", next: 'pain_body' }
        ]
    },
    'head_neuro_1': {
        text: "Does bright light hurt your eyes? Or is your neck stiff?",
        options: [
            { label: "Light Sensitivity", symptom: "sensitivity_light", next: 'head_neuro_2' },
            { label: "Stiff Neck", symptom: "stiff_neck", next: 'head_neuro_2' },
            { label: "Both", symptoms: ["sensitivity_light", "stiff_neck"], next: 'head_neuro_2' },
            { label: "Neither", next: 'pain_head_retro' }
        ]
    },
    'head_neuro_2': {
        // If they have stiff neck/light sensitivity, check retro orbital just in case
        text: "Do you also have pain specifically BEHIND your eyes?",
        options: [
            { label: "Yes", symptom: "retro_orbital_pain", next: 'pain_body' },
            { label: "No", next: 'pain_body' }
        ]
    },
    'pain_head_retro': {
        text: "Is the pain located specifically BEHIND your eyes?",
        options: [
            { label: "Yes, behind eyes", symptom: "retro_orbital_pain", next: 'pain_body' },
            { label: "No", next: 'pain_body' }
        ]
    },

    'pain_body': {
        text: "Do you have generalized body aches or muscle pain?",
        options: [
            { label: "Yes, body hurts", symptom: "body_pain", next: 'pain_body_type' },
            { label: "No", next: 'fatigue_check' }
        ]
    },
    'pain_body_type': {
        text: "Is the pain mostly in your joints or your muscles?",
        options: [
            { label: "Joints (Knees/Elbows)", symptom: "joint_pain", next: 'fatigue_check' },
            { label: "Muscles (Aches)", symptom: "muscle_pain", next: 'fatigue_check' },
            { label: "Both", symptoms: ["joint_pain", "muscle_pain"], next: 'fatigue_check' }
        ]
    },
    'fatigue_check': {
        text: "How severe is your fatigue or tiredness?",
        options: [
            { label: "Extreme / Prostrated", symptoms: ["fatigue", "severe_fatigue"], next: 'stomach_check' },
            { label: "Moderate", symptom: "fatigue", next: 'stomach_check' },
            { label: "Normal Energy", next: 'stomach_check' }
        ]
    },

    // --- CONVERGENCE POINT 2: STOMACH & CONTEXT ---
    'stomach_check': {
        text: "Do you have any stomach pain, diarrhea, or nausea?",
        options: [
            { label: "Nausea/Vomiting", symptoms: ["nausea", "vomiting"], next: 'stomach_check_2' },
            { label: "Stomach Pain", symptom: "abdominal_pain", next: 'stomach_check_2' },
            { label: "No", next: 'context_onset' }
        ]
    },
    'stomach_check_2': {
        text: "Are you also experiencing diarrhea?",
        options: [
            { label: "Yes, Severe/Watery", symptoms: ["diarrhea", "severe_diarrhea"], next: 'context_onset' },
            { label: "Yes, Mild", symptom: "diarrhea", next: 'context_onset' },
            { label: "No", next: 'context_onset' }
        ]
    },


    'context_onset': {
        text: "Did these symptoms appear suddenly or gradually?",
        options: [
            { label: "Suddenly (Rapid onset)", symptom: "sudden_onset", next: 'context_exposure' },
            { label: "Gradually (Over days)", symptom: "gradual_onset", next: 'context_exposure' }
        ]
    },

    'context_exposure': {
        text: "Have you had any recent travel or mosquito exposure?",
        options: [
            { label: "Mosquito Bites / Area", symptom: "mosquito_exposure", next: 'context_food' },
            { label: "Recent Travel", symptom: "recent_travel", next: 'context_food' },
            { label: "Both", symptoms: ["mosquito_exposure", "recent_travel"], next: 'context_food' },
            { label: "No", next: 'context_food' }
        ]
    },
    'context_food': {
        text: "Have you consumed any street food or potentially unsafe water recently?",
        options: [
            { label: "Yes", symptom: "unsafe_food_exposure", next: 'final_review' },
            { label: "No", next: 'final_review' }
        ]
    },

    // --- FINAL ---
    'final_review': {
        text: "We have gathered your symptoms. Ready to diagnose?",
        options: [
            { label: "Analyze Symptoms", next: 'diagnose' },
            { label: "Start Over", next: 'root' }
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
const logicContainer = document.querySelector('.logic-container');

logicBtn.addEventListener('click', () => {
    logicModal.classList.remove('hidden');
});

closeLogicModal.addEventListener('click', () => {
    logicModal.classList.add('hidden');
});

logicModal.addEventListener('click', (e) => {
    if (e.target === logicModal) {
        logicModal.classList.add('hidden');
    }
});

function init() {
    setTimeout(() => {
        loaderOverlay.classList.add('fade-out');
        setTimeout(() => {
            loaderOverlay.style.display = 'none';
            factBaseContainer.classList.add('content-visible');
            factBaseContainer.classList.remove('hidden-initially');
            logicContainer.classList.add('content-visible');
            logicContainer.classList.remove('hidden-initially');
        }, 1500);

        renderNode('root');
        updateFactDisplay();
        updateProgressBar('root');


    }, 2500);
}

function renderNode(nodeId) {
    updateProgressBar(nodeId);

    if (nodeId === 'diagnose') {

        runDiagnosis();
        return;
    }

    const node = questions[nodeId];
    questionText.textContent = node.text;
    actionsContainer.innerHTML = '';

    node.options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-no';
        if (option.label.toLowerCase() === 'yes' || option.label.includes('Fever') || option.label.includes('Cough')) {
            btn.className = 'btn btn-yes';
        }

        btn.textContent = option.label;
        btn.onclick = () => handleAnswer(option);
        actionsContainer.appendChild(btn);
    });
}

function handleAnswer(option) {
    if (option.symptom) collectedSymptoms.add(option.symptom);
    if (option.symptoms) option.symptoms.forEach(s => collectedSymptoms.add(s));

    updateFactDisplay();

    questionCard.classList.add('fade-up');
    setTimeout(() => {
        currentNodeId = option.next;
        renderNode(currentNodeId);
        questionCard.classList.remove('fade-up');
    }, 400);
}

function updateFactDisplay(trace = null) {
    const symList = Array.from(collectedSymptoms).map(s => `<li>User reports: ${s}</li>`).join('');
    factsList.innerHTML = symList || "<li>No symptoms reported yet</li>";

    if (trace) {
        deducedList.innerHTML = trace.map(t => `<li>${t}</li>`).join('');
    } else {
        deducedList.innerHTML = "<li>Waiting for analysis...</li>";
    }
}

async function runDiagnosis() {
    questionText.textContent = "Analyzing Reasoning...";
    actionsContainer.innerHTML = '<div class="loader">Processing...</div>';

    try {
        const response = await fetch('https://dedoc.devwole.space/diagnose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: Array.from(collectedSymptoms) })
        });

        const data = await response.json();

        // New Display Logic for Derived Facts
        if (data.inferred_diseases.length > 0 || data.clinical_states.length > 0) {
            let msg = "";

            if (data.inferred_diseases.length > 0) {
                msg += `<strong>POSSIBLE DIAGNOSES:</strong><br>${data.inferred_diseases.join(", ").toUpperCase().replace(/_/g, " ")}<br><br>`;
            }

            if (data.clinical_states.length > 0) {
                msg += `<strong>CLINICAL STATES:</strong><br>${data.clinical_states.join(", ").toUpperCase().replace(/_/g, " ")}`;
            }

            questionText.innerHTML = msg;

        } else {
            questionText.textContent = "No specific disease or clinical state inferred.";
        }

        updateFactDisplay(data.explanation);

        factBaseContent.classList.remove('hidden');

        actionsContainer.innerHTML = '';
        const restartBtn = document.createElement('button');
        restartBtn.className = 'btn btn-yes';
        restartBtn.textContent = "Start Over";
        restartBtn.onclick = () => {
            collectedSymptoms.clear();
            renderNode('root');
            updateFactDisplay();
            factBaseContent.classList.add('hidden');
        };
        actionsContainer.appendChild(restartBtn);

    } catch (error) {
        questionText.textContent = "Error connecting to expert system.";
        console.error(error);
    }
}

factBaseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    factBaseContent.classList.toggle('hidden');
});

document.addEventListener('click', (e) => {
    if (!factBaseContainer.contains(e.target)) {
        factBaseContent.classList.add('hidden');
    }
});

function updateProgressBar(nodeId) {
    const progress = NODE_PROGRESS[nodeId] || 10;
    progressBar.style.width = `${progress}%`;
}

init();

