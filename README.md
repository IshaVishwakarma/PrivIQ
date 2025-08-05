# 🔐 PrivIQ - Privacy Policy Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/Live-Demo-brightgreen)](https://myapp-pndu.onrender.com/)

**PriviQ** is an AI-powered web application that intelligently analyzes privacy policies to identify risk factors, highlight sensitive clauses, provide multilingual summaries, and assess compliance with India's **DPDP Act**. Built using Python and Streamlit, it simplifies privacy awareness and legal checks for users and developers.

---

## 🚀 Live Demo

👉 **[Try it here](https://myapp-pndu.onrender.com/)**

---

## 📌 Features

- **📝 Multiple Input Methods**
  - Upload `.txt` files
  - Paste policy text
  - Fetch privacy policy from a URL

- **🔍 Risk Keyword Classification**
  - Identifies keywords indicating High, Moderate, and Low privacy risks
  - Weighted scoring mechanism

- **📊 Risk Category Analysis**
  - Categorizes keywords under themes such as:
    - Tracking
    - Third-Party Sharing
    - Data Retention
    - User Data
    - Advertising
    - Cookies

- **🧠 AI-Based Summarization**
  - Extracts the most relevant risky content
  - Generates a concise summary

- **🌐 Multilingual Translation**
  - Supports summaries in Hindi, French, Spanish, Chinese, Arabic, and more
  - Automatic translation using Google Translate API

- **🔊 Text-to-Speech (TTS)**
  - Converts summary to voice using gTTS
  - Plays audio directly in the browser

- **🧯 Visual Risk Highlighting**
  - Color-coded highlights of risky sentences:
    - 🔴 High
    - 🟠 Moderate
    - 🟢 Low

- **📜 DPDP Act Compliance Checker**
  - Verifies the presence of critical clauses like:
    - Consent
    - Grievance Redressal
    - Data Deletion
    - Data Retention
    - Security
    - Access Rights

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **NLP Engine**: spaCy (`en_core_web_sm`)
- **Similarity & Text Vectorization**: scikit-learn (CountVectorizer, Cosine Similarity)
- **Text Summarization**: Extractive summarization using sentence ranking
- **Translation**: `googletrans`
- **Text-to-Speech**: `gTTS` (Google Text-to-Speech)
- **Web Scraping**: `BeautifulSoup` for extracting text from URLs
- **Visualization**: Matplotlib (Pie Charts)

---

## 📷 Screenshots



- **Risk Analysis Overview**
- <img width="1904" height="783" alt="image" src="https://github.com/user-attachments/assets/14b57249-ccb9-4da5-8b98-38da8cde8ffb" />

- **Summary with Audio Playback**
- <img width="1828" height="380" alt="image" src="https://github.com/user-attachments/assets/215e2664-5232-4d71-9a86-be08e9946497" />

- **DPDP Act Compliance Results**
- <img width="1901" height="494" alt="image" src="https://github.com/user-attachments/assets/a2cb4703-a27e-4a37-bd4e-62ab067ccb97" />

- **Highlight Policy by Risk**
- <img width="1874" height="848" alt="image" src="https://github.com/user-attachments/assets/154a1702-deef-4441-a4e0-e7639cba6bd1" />


---

## 👩‍💻 Author

**Isha Vishwakarma**  
🔗 [LinkedIn](https://www.linkedin.com/in/ishavishwakarma)

---

## 💡 Future Enhancements

- Integrate abstractive summarization using Pegasus/BART
- Add PDF upload and parsing
- Create a user dashboard with policy history
- Implement feedback/rating system
- Extend support for global data privacy laws (e.g., GDPR, CCPA)

---

## 🙋‍♀️ Feedback & Contributions

Have suggestions or improvements?  
👉 [Open an issue](https://github.com/your-username/priviq/issues) or submit a pull request! Contributions are always welcome 💙
