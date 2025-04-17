import streamlit as st
import json
# from transformers import pipeline

# Set Streamlit page config
st.set_page_config(page_title="MSME Chatbot", page_icon="🤖", layout="centered")

# 💅 Custom CSS for styling
st.markdown("""
    <style>
        body, .main {
            background-color: #fff0f5;
        }
        .stTextInput > div > div > input {
            background-color: #fff5fa;
        }
        .stTextInput > label {
            color: #c71585;
            font-weight: bold;
        }
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #e6f7ff;
            text-align: right;
        }
        .bot-message {
            background-color: #f9f9f9;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

# Cache the model
# @st.cache_resource
# def load_model():
#     return pipeline("question-answering", model="deepset/roberta-base-squad2")

# qa_pipeline = load_model()

# Q&A + rule-based logic
def answer_question(question, scheme_name):
    selected_scheme = next((s for s in schemes if scheme_name.lower() in s["scheme_name"].lower()), None)
    if not selected_scheme:
        return "🚫 Scheme not found. Please try selecting another scheme."

    q_lower = question.lower()

    # Check for key intents
    keywords = ["subsidy", "benefit", "eligibility", "how to apply", "application", "description", "about"]
    if not any(kw in q_lower for kw in keywords):
        return (
            "🙏 Kindly ask more specific questions related to the scheme.\n\n"
            "For example:\n"
            "- What are the benefits under this scheme?\n"
            "- Who is eligible for this scheme?\n"
            "- How can I apply?\n"
            "- Give me a brief about the scheme.\n"
        )

    # Rule-based Q&A
    if "subsidy" in q_lower or "benefit" in q_lower:
        return selected_scheme["benefits"]
    elif "eligibility" in q_lower:
        return selected_scheme["eligibility"]
    elif "how to apply" in q_lower or "application" in q_lower:
        return selected_scheme["how_to_apply"]
    elif "description" in q_lower or "about" in q_lower:
        return selected_scheme["description"]

    # # Fallback to model
    # context = f"""
    # Scheme: {selected_scheme['scheme_name']}
    # Description: {selected_scheme['description']}
    # Eligibility: {selected_scheme['eligibility']}
    # Benefits: {selected_scheme['benefits']}
    # How to apply: {selected_scheme['how_to_apply']}
    # """
    # result = qa_pipeline(question=question, context=context)
    # return result["answer"]


# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Chat History
st.sidebar.title("🕐Chat History")
for i, chat in enumerate(st.session_state.chat_history):
    with st.sidebar.expander(f"Conversation {i+1}"):
        for entry in chat:
            role = "🧑‍💼 You" if entry["role"] == "user" else "🤖 Bot"
            st.markdown(f"**{role}:** {entry['content']}")

# Main UI
st.title("🤖 MSME Scheme Assistant")
st.success("Ask about subsidies, eligibility, and more!")

# Dropdown for scheme
scheme_names = [scheme["scheme_name"] for scheme in schemes]
selected_scheme = st.selectbox("🏢 Select a Scheme", scheme_names)

# Text input
user_question = st.text_input("💬 Your Question", placeholder="e.g., What is the subsidy?")

if user_question:
    # Create new chat if last one ended with assistant
    if not st.session_state.chat_history or st.session_state.chat_history[-1][-1]["role"] == "assistant":
        st.session_state.chat_history.append([])

    # Add user query
    st.session_state.chat_history[-1].append({"role": "user", "content": user_question})

    # Get response
    with st.spinner("Thinking..."):
        response = answer_question(user_question, selected_scheme)

    # Add bot response
    st.session_state.chat_history[-1].append({"role": "assistant", "content": response})

    # Display chat
    for entry in st.session_state.chat_history[-1]:
        role = "🧑‍💼 You" if entry["role"] == "user" else "🤖 Bot"
        css_class = "user-message" if entry["role"] == "user" else "bot-message"
        st.markdown(
            f'<div class="chat-message {css_class}"><strong>{role}:</strong><br>{entry["content"]}</div>',
            unsafe_allow_html=True
        )

# Optional: Show full scheme info
if st.checkbox("📄 Show full scheme details"):
    scheme_data = next((s for s in schemes if s["scheme_name"] == selected_scheme), None)
    if scheme_data:
        st.markdown(f"""
        ### 📝 {scheme_data["scheme_name"]}
        **📘 Description**: {scheme_data["description"]}
        
        **🧾 Eligibility**: {scheme_data["eligibility"]}
        
        **🏆 Benefits**: {scheme_data["benefits"]}
        
        **📝 How to Apply**: {scheme_data["how_to_apply"]}
        """)
# Sidebar information
st.sidebar.title("About")
st.sidebar.markdown("""
This chatbot helps you explore MSME-related schemes and information extracted from official documents.

""")
