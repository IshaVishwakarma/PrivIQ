
# app.py

# app.py

import streamlit as st
import matplotlib.pyplot as plt
import spacy
import spacy.cli
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from googletrans import Translator
from gtts import gTTS
import tempfile
import os

# Download spaCy model
spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Initialize translator
translator = Translator()

# --- Risk Keywords & Categories ---
risk_keywords = {
    "High": ["share", "third-party", "sale", "disclose", "sell", "transfer", "advertising"],
    "Moderate": ["collect", "store", "analyze", "process", "track", "monitor", "retain"],
    "Low": ["secure", "encrypt", "protect", "comply", "consent", "opt-out", "privacy"]
}

risk_categories = {
    "Tracking": ["track", "tracking", "location", "gps", "geolocation", "monitor"],
    "Third Party Sharing": ["third party", "affiliates", "partners", "external", "vendors"],
    "Data Retention": ["retain", "retention", "store", "storage duration", "archived"],
    "User Data": ["personal data", "email", "phone", "name", "dob", "address"],
    "Advertising": ["ads", "advertising", "targeted", "marketing", "campaign"],
    "Cookies": ["cookie", "cookies", "browser", "session", "cache"]
}

dpdp_clauses = {
    "grievance": "No grievance redressal clause found.",
    "consent": "No consent clause found.",
    "retention": "No data retention period mentioned.",
    "access": "No clause for user data access or correction.",
    "deletion": "No clause for data deletion/right to be forgotten.",
    "purpose": "Purpose of data collection not clearly stated.",
    "disclosure": "No mention of data disclosure practices.",
    "security": "No mention of data security practices."
}

# --- Functions ---
def classify_risk_keywords(policy_text):
    found_keywords = {"High": [], "Moderate": [], "Low": []}
    lower_text = policy_text.lower()
    for level, keywords in risk_keywords.items():
        for word in keywords:
            if word in lower_text:
                found_keywords[level].append(word)
    return found_keywords

def calculate_risk_score(text):
    text = text.lower()
    score = 0
    max_score = 0
    for level, keywords in risk_keywords.items():
        weight = {"High": 3, "Moderate": 2, "Low": 1}[level]
        count = sum(text.count(word) for word in keywords)
        score += count * weight
        max_score += len(keywords) * weight
    return score / max_score if max_score else 0

def display_risk_highlights(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    scores = [calculate_risk_score(sentence) for sentence in sentences]
    max_score = max(scores) if scores else 1

    for sentence, score in zip(sentences, scores):
        normalized = score / max_score
        if normalized >= 0.7:
            color = "rgba(255, 99, 71, 0.25)"  # red
        elif normalized >= 0.4:
            color = "rgba(255, 215, 0, 0.25)"  # orange
        else:
            color = "rgba(144, 238, 144, 0.25)"  # green
        st.markdown(
            f"<div style='background-color:{color}; padding:8px; margin-bottom:4px; border-radius:4px'>{sentence}</div>",
            unsafe_allow_html=True
        )

def categorize_risks(text):
    category_hits = {}
    for category, keywords in risk_categories.items():
        hits = [kw for kw in keywords if kw.lower() in text.lower()]
        if hits:
            category_hits[category] = hits
    return category_hits

def summarize_policy(text, risky_keywords):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    risky_sentences = [s for s in sentences if any(k in s.lower() for k in risky_keywords)]
    if not risky_sentences:
        return "✅ No risky content found."
    vectorizer = CountVectorizer().fit_transform(risky_sentences)
    sim_matrix = cosine_similarity(vectorizer)
    scores = sim_matrix.sum(axis=1)
    ranked = [s for _, s in sorted(zip(scores, risky_sentences), reverse=True)]
    return " ".join(ranked[:3])

def extractive_summary(text, num_sentences=3):
    doc = nlp(text)
    sentences = list(doc.sents)
    words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    word_freq = Counter(words)
    sentence_scores = {}
    for sent in sentences:
        for word in sent:
            if word.text.lower() in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word.text.lower()]
    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    return " ".join([s.text for s in ranked])

def get_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join(p.get_text() for p in paragraphs)
        return text
    except Exception as e:
        st.error(f"Failed to extract text from URL: {e}")
        return ""

def check_dpdp_compliance(text):
    missing = []
    lower_text = text.lower()
    for keyword, message in dpdp_clauses.items():
        if keyword not in lower_text:
            missing.append(message)
    return missing

# --- New translation function ---
def translate_text(text, dest_language):
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        return f"Translation failed: {e}"

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="PriviQ", page_icon="🔐", layout="wide")
    st.title("🔐 PriviQ - Privacy Policy Analyzer")

    st.subheader("📎 Upload / Paste / Fetch Privacy Policy")

    url_input = st.text_input("🔗 Or enter a URL to fetch the privacy policy text:")
    url_text = get_text_from_url(url_input) if url_input.strip() else ""

    uploaded_file = st.file_uploader("📁 Upload Privacy Policy (.txt only)", type=["txt"])
    file_text = ""
    if uploaded_file:
        try:
            file_text = uploaded_file.read().decode("utf-8")
            st.success(f"✅ Uploaded {uploaded_file.name}")
            with st.expander("📄 File Preview"):
                st.text_area("Preview", file_text, height=200)
        except Exception as e:
            st.error(f"Failed to read file: {e}")

    manual_text = st.text_area("✍️ Or Paste Text Manually:", height=250)

    final_input = url_text.strip() if url_text.strip() else (manual_text.strip() if manual_text.strip() else file_text.strip())

    if not final_input:
        st.warning("⚠️ Please upload a file, paste text, or enter a URL.")
        return

    st.markdown("---")

    # Language selector for summaries and TTS
    languages = {
        'English': 'en',
        'Hindi': 'hi',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Chinese (Simplified)': 'zh-cn',
        'Japanese': 'ja',
        'Arabic': 'ar',
        # add more if needed
    }
    selected_lang = st.selectbox("🌐 Select language for summary and voice:", options=list(languages.keys()))

    if st.button("🔍 Analyze Privacy Policy"):
        keyword_classification = classify_risk_keywords(final_input)
        category_results = categorize_risks(final_input)

        risk_weights = {"High": 3, "Moderate": 2, "Low": 1}
        risk_score = sum(len(set(keyword_classification[level])) * risk_weights[level] for level in risk_weights)

        risk_level = "🔴 High" if risk_score >= 15 else "🟠 Moderate" if risk_score >= 7 else "🟢 Low"

        st.subheader("📌 Risk Severity Breakdown")
        st.markdown(f"**🧮 Score:** {risk_score}  |  **Level:** {risk_level}")

        for level in ["High", "Moderate", "Low"]:
            keywords = keyword_classification[level]
            if keywords:
                st.markdown(f"**{level} Risk Keywords:**")
                st.write(", ".join(set(keywords)))

        if category_results:
            st.subheader("📊 Risk Category Insights")
            for cat, kws in category_results.items():
                st.markdown(f"**{cat}** ➤ {', '.join(kws)}")

            st.markdown("#### 🥧 Risk Category Distribution")
            labels = list(category_results.keys())
            sizes = [len(v) for v in category_results.values()]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
            st.pyplot(fig1)

    if st.button("📄 Summarize Risky Content"):
        st.subheader("🧠 Summary of Risky Content")
        summary = summarize_policy(final_input, sum(risk_keywords.values(), []))

        if selected_lang != "English":
            translated_summary = translate_text(summary, languages[selected_lang])
            st.markdown(f"**Translated Summary ({selected_lang}):**")
            st.write(translated_summary)
            tts_text = translated_summary
        else:
            st.write(summary)
            tts_text = summary

        # Voice summary playback using the text chosen above
        try:
            lang_code = languages[selected_lang]
            tts = gTTS(text=tts_text, lang=lang_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                audio_bytes = open(tmp_file.name, 'rb').read()
                st.audio(audio_bytes, format='audio/mp3')
            os.unlink(tmp_file.name)
        except Exception as e:
            st.error(f"Failed to generate voice summary: {e}")

    if st.button("📘 Full Extractive Summary"):
        st.subheader("📘 Full Summary")
        full_summary = extractive_summary(final_input)
        st.write(full_summary)
        if selected_lang != "English":
            translated_full_summary = translate_text(full_summary, languages[selected_lang])
            st.markdown(f"**Translated Full Summary ({selected_lang}):**")
            st.write(translated_full_summary)
        st.download_button("📥 Download Summary", data=full_summary, file_name="summary.txt")

    if st.button("🧯 Highlight Policy by Risk"):
        st.subheader("🧯 Risk Highlighting")
        display_risk_highlights(final_input)

    if st.button("📜 Check DPDP Compliance"):
        st.subheader("📜 DPDP Act Compliance Check")
        dpdp_issues = check_dpdp_compliance(final_input)
        if dpdp_issues:
            for issue in dpdp_issues:
                st.error(issue)
        else:
            st.success("✅ This policy includes all key DPDP clauses.")

if __name__ == "__main__":
    main()



