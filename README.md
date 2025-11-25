# voice_assistant – Python-Based AI Voice Assistant

**voice_assistant** is a Python-powered AI Voice Assistant that supports real-time speech recognition, 
dynamic intelligent responses, user authentication, browser automation, and a custom Iron-Man-themed UI.

The system uses Flask as the backend, JSON for data storage, and the Web Speech API for live voice processing.

---

## 🚀 Features

### 🎤 Voice Interaction
- Speech recognition using Web Speech API  
- Natural text-to-speech responses  
- Live command processing  

### 🧠 Intelligent Command Handling
Supports smart voice commands such as:

- **Greetings**
  - “hi”, “hello”, “hey”
- **Identity**
  - “who are you?”
- **Website Automation**
  - “open google”
  - “open youtube”
  - “open facebook”
- **Time Information**
  - “what’s the time?”
- **Fallback Search**
  - Any unknown query (example: *“who is gandhi”*)  
    → Automatically opens Google Search in a new tab  
    → Assistant speaks: *“Searching Google for {query}”*

### 👤 User Authentication
- Login & Registration using **JSON file storage**
- Greets users by their name  
  - *“Good morning Krishna…”*  
  - *“Good evening Balu…”*

### 🎨 Iron-Man Style UI
- custom glowing theme  
- animated effects  
- circular Iron-Man image button instead of mic  
- clean, futuristic layout  

---

## 🛠 Tech Stack

- **Python (Flask)** – Backend  
- **HTML, CSS, JavaScript** – Frontend  
- **JSON** – User Database  
- **Web Speech API** – Voice recognition  
- **Speech Synthesis API** – Voice replies  

---

## 📁 Project Structure

