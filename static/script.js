// ------------ SHOW/HIDE SCREENS -------------
function showLogin(e) {
    if (e) e.preventDefault();
    document.getElementById("register-box").classList.add("hidden");
    document.getElementById("login-box").classList.remove("hidden");
    document.getElementById("assistant").classList.add("hidden");
}

function showRegister(e) {
    if (e) e.preventDefault();
    document.getElementById("register-box").classList.remove("hidden");
    document.getElementById("login-box").classList.add("hidden");
    document.getElementById("assistant").classList.add("hidden");
}


// ------------ REGISTER -------------
async function registerUser() {
    const username = document.getElementById("reg-name").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-pass").value;

    const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();

    if (res.ok && data.message === "registered") {
        alert("Registration successful. Please login.");
        showLogin();
    } else {
        alert(data.error || "Registration failed.");
    }
}


// ------------ LOGIN -------------
async function loginUser() {
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-pass").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.message === "login_success") {
        document.getElementById("username").innerText = data.username;

        document.getElementById("register-box").classList.add("hidden");
        document.getElementById("login-box").classList.add("hidden");
        document.getElementById("assistant").classList.remove("hidden");

        if (data.greeting) speak(data.greeting);
    } else {
        alert(data.error || "Login failed.");
    }
}


// ------------ LOGOUT -------------
async function logout() {
    await fetch("/logout", { method: "POST", credentials: "same-origin" });
    showRegister();
}



// ------------ SPEECH RECOGNITION -------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onresult = async (event) => {
        const text = event.results[0][0].transcript;
        document.querySelector(".content").textContent = text;

        const res = await fetch("/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        // If backend says to open a link
        if (data.action === "open" && data.url) {
            window.open(data.url, "_blank");
        }

        if (data.reply) {
            speak(data.reply);
            document.querySelector(".content").textContent = data.reply;
        }
    };

} else {
    alert("Speech Recognition not supported in your browser.");
}


// ------------ MIC BUTTON CLICK -------------
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("talk") || e.target.classList.contains("mic-btn")) {
        if (!recognition) return;
        document.querySelector(".content").textContent = "Listening...";
        recognition.start();
    }
});


// ------------ TEXT-TO-SPEECH -------------
function speak(text) {
    if (!text) return;
    const speech = new SpeechSynthesisUtterance(text);
    speech.rate = 1;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
}
