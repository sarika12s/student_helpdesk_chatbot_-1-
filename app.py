from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time
import os

from utils.retriever import Retriever
from utils.qa_reader import QAReader
from utils.convo_manager import ConversationManager


# ---------------- FLASK SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ----------------
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
READER_MODEL = "distilbert-base-uncased-distilled-squad"
DOCS_FOLDER = "data/docs"

CONF_THRESHOLD = 0.18


# ---------------- INIT COMPONENTS ----------------
retriever = Retriever(EMBED_MODEL, docs_folder=DOCS_FOLDER)
qa_reader = QAReader(READER_MODEL)
convo_mgr = ConversationManager()


# ---------------- ROUTES ----------------
@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/chatbot")
def chatbot_page():
    return render_template("index.html")


# ---------------- CHAT ROUTE ----------------
@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}

    session_id = payload.get("session_id") or str(int(time.time() * 1000))
    user_msg = payload.get("message", "").strip()

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    # Save message
    convo_mgr.add_user_message(session_id, user_msg)

    # Conversation context
    conversation_context = convo_mgr.get_context(session_id)

    # --- STEP 1: Retrieve top documents ---
    top_docs = retriever.get_top_k(user_msg, k=8)
    docs_context = "\n\n".join([d["text"] for d in top_docs]) if top_docs else ""

    # --- Combine conversation + docs ---
    combined_context = conversation_context + "\n\n" + docs_context

    # --- STEP 2: Run QA Model ---
    answer, confidence = qa_reader.answer(
        question=user_msg,
        context=combined_context
    )

    # Clean answer
    if answer:
        answer = answer.replace("[CLS]", "").replace("[SEP]", "").strip()

    # Bad answer detection
    bad_answer = (
        not answer or
        len(answer) < 3 or
        confidence < CONF_THRESHOLD
    )

    # ---- FALLBACK ANSWERS ----
    if bad_answer:
        msg = user_msg.lower()

        if "time" in msg or "timing" in msg or "when" in msg:
            answer = "College operates from 9:00 AM to 5:00 PM, Monday to Saturday."
        elif "fee" in msg or "fees" in msg:
            answer = "Tuition Fee is ₹95,000 per year. Hostel Fee is ₹55,000–₹68,000."
        elif "hostel" in msg:
            answer = "Hostel entry closes at 9:00 PM."
        elif "scholar" in msg:
            answer = "Scholarships include Merit, Girl Student Merit, SC/ST, EWS, and NSP schemes."
        elif "exam" in msg:
            answer = "Internal exams occur twice per semester. University exams are in December & May."
        elif "library" in msg:
            answer = "Library timings are 8:30 AM to 7:00 PM."
        elif "event" in msg or "fest" in msg:
            answer = "Major events include TechNova Fest, Cultural Carnival, Hackathon, and Sports Week."
        else:
            answer = "I'm not fully sure about that. Please ask the helpdesk for accurate details."

        confidence = 0.70

    # Save bot reply
    convo_mgr.add_bot_message(session_id, answer)

    return jsonify({
        "session_id": session_id,
        "response": answer,
        "confidence": float(confidence),
        "top_docs": [
            {"meta": d.get("meta", ""), "score": d.get("score", 0)}
            for d in top_docs
        ]
    })


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    # Load college docs into retriever
    retriever.load_all_documents()
    print("📘 Documents loaded into FAISS index:", len(retriever.documents))

    print("🚀 Starting Flask server...")
    app.run(debug=True)
