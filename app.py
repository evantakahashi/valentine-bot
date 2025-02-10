import streamlit as st
from valentine_bot import ValentineBot
import os

# Page configuration
st.set_page_config(
    page_title="Will You Be My Valentine?",
    page_icon="💝",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    /* Add pink background to the entire page */
    .stApp {
        background-color: #fff0f3;
    }
    
    .valentine-card {
        background-color: #ffe6e6;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid #ff6b6b;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: #000000;
    }
    .user-message {
        background-color: #e6f3ff;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #ffe6e6;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize session state for game
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'started': False,
        'q1_answered': False,
        'q2_answered': False,
        'game_completed': False
    }

# Add this near the other session state initializations
if 'has_said_yes' not in st.session_state:
    st.session_state.has_said_yes = False

# Title
st.title("💘hi allie")

# Game Section
if not st.session_state.game_state['game_completed']:
    #st.markdown("### 💝Answer these questions to unlock a special message!")
    
    # Question 1
    if not st.session_state.game_state['q1_answered']:
        q1_answer = st.text_input("who loves the other person more?").lower().strip()
        if q1_answer:
            if q1_answer == "evan":
                st.success("correct! that's pretty obvious")
                st.session_state.game_state['q1_answered'] = True
                st.rerun()
            else:
                st.error("nope!")
    
    # Question 2
    elif not st.session_state.game_state['q2_answered']:
        q2_answer = st.text_input("who is Evan's favorite person? 🥰").lower().strip()
        if q2_answer:
            if q2_answer == "allie":
                st.success("wow that was easy")
                st.session_state.game_state['q2_answered'] = True
                st.session_state.game_state['game_completed'] = True
                st.rerun()
            else:
                st.error("not quite! this is an easy question")

# Only show Valentine's card and chat after game completion
if st.session_state.game_state['game_completed']:
    # Valentine's Card (Expandable)
    with st.expander("💌 click me first 💌"):
        st.markdown("""
        <div class="valentine-card">
            <h2 style='text-align: center;'>My Dearest Allie ❤️</h2>
            <p style='text-align: center;'>
                Every moment with you is a gift that I cherish deeply.<br>
                You make my world brighter just by being in it.<br>
                I love you more than words can express.<br><br>
                With all my love,<br>
                Evan
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Initialize the bot
    if 'bot' not in st.session_state:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.bot = ValentineBot(api_key)

    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
            <div class="chat-message {'user-message' if message['role'] == 'user' else 'bot-message'}">
                {message['content']}
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("try typing here")

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Check for yes response and update state
        if any(word in user_input.lower() for word in ['yes', 'sure', 'okay', 'of course', 'definitely']):
            st.session_state.has_said_yes = True
            st.session_state.bot.has_said_yes = True
        
        # Get bot response
        bot_response = st.session_state.bot.get_response(user_input)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update the chat display
        st.rerun() 