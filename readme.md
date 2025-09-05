# 📧 AI-Powered Email Assistant

An intelligent **Streamlit-based email management tool** that helps support teams process, prioritize, and respond to emails efficiently using AI.

This app automatically analyzes uploaded emails, classifies them by **sentiment** and **urgency**, extracts useful details, computes a **priority score**, and drafts personalized replies. It’s designed to **reduce manual workload**, speed up customer response times, and ensure no critical emails slip through the cracks.

---

## 🚀 Features

* **Upload & Process Emails**
  Upload a CSV file containing emails (`sender`, `subject`, `body`, `sent_date`) and let the app handle the rest.

* **Sentiment Analysis**
  Automatically detects whether an email is **positive**, **neutral**, or **negative**.

* **Urgency Detection**
  Distinguishes between **urgent** and **non-urgent** requests.

* **Information Extraction**
  Pulls out structured details (e.g., order IDs, issue categories, or keywords) from email content.

* **Personalized AI Draft Replies**
  Generates contextual responses, automatically greeting the sender by name.

* **Priority Scoring**
  Combines sentiment, urgency, and sent date to compute a **priority ranking**—so the most important emails surface first.

* **Interactive Dashboard**

  * Expandable email cards with metadata and extracted details
  * Editable draft replies
  * One-click **Approve & Send** buttons (mock action for now)
  * Sidebar filters by **urgency** and **sentiment**

---

## ✨ Unique Features

Unlike many AI email tools, this assistant is designed with **customer support workflows** in mind:

1. **Smart Prioritization** – Not just classification, but ranking emails so that urgent and negative ones don’t get lost.
2. **Personalized Replies** – Names are extracted from email addresses, making responses feel **human and personal**.
3. **Explainable Insights** – Extracted entities and classifications are shown transparently so agents can trust AI decisions.
4. **Streamlit UI** – Simple, interactive, and team-friendly without needing complex setup.

---

## 🔍 How It’s Different

* Most email tools stop at **sentiment or urgency detection** → this app **combines multiple factors** into a single **priority score**.
* Instead of generic canned replies, it generates **context-aware drafts** tailored to each sender.
* Built with **transparency** → users can see extracted information, sentiment, and urgency before approving a reply.
* Focused on **augmenting human agents**, not replacing them. The AI drafts, humans approve.

---

## 📂 Input Format

Upload a **CSV file** with the following columns:

| sender                                      | subject             | body                | sent\_date |
| ------------------------------------------- | ------------------- | ------------------- | ---------- |
| [alice@xyz.com](mailto:alice@xyz.com)       | Order Delay         | My order is late... | 2023-09-01 |
| [john.doe@abc.com](mailto:john.doe@abc.com) | Password Reset Help | I can't log in...   | 2023-09-02 |

---

## ▶️ How to Run

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/email-assistant.git
   cd email-assistant
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   streamlit run app.py
   ```
4. Upload your **CSV file** of emails and start exploring the dashboard.

---

## 🛠️ Tech Stack

* **Python** – Core logic
* **Streamlit** – UI and dashboard
* **Pandas** – Data handling
* **Custom NLP Modules** – `analyze.py` and `priority.py` handle sentiment, urgency, extraction, and reply drafting
