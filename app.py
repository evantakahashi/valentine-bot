import streamlit as st
from valentine_bot import ValentineBot
import os

# Page configuration
st.set_page_config(
    page_title="hi allie",
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
        position: relative;
        background: linear-gradient(45deg, #ffe6e6, #ffb3b3);
        border-radius: 10px;
        padding: 20px;
        border: 2px solid #ff6b6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform-origin: center;
        transition: all 0.3s ease;
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
    
    .card-container {
        perspective: 1000px;
        margin: 20px auto;
        max-width: 600px;
    }
    
    .valentine-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .card-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .card-header {
        color: #ff4b6b;
        font-family: 'Brush Script MT', cursive;
        font-size: 2em;
        margin-bottom: 15px;
    }
    
    .card-message {
        font-family: 'Georgia', serif;
        line-height: 1.6;
        color: #333;
    }
    
    .signature {
        font-family: 'Brush Script MT', cursive;
        font-size: 1.5em;
        color: #ff4b6b;
        margin-top: 20px;
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
        q1_answer = st.text_input("does evan love allie more than allie loves evan?").lower().strip()
        if q1_answer:
            if q1_answer == "yes":
                st.success("correct! that's pretty obvious")
                st.session_state.game_state['q1_answered'] = True
                st.rerun()
            else:
                st.error("nope!")
    
    # Question 2
    elif not st.session_state.game_state['q2_answered']:
        q2_answer = st.text_input("who is evan's favorite person?").lower().strip()
        if q2_answer:
            if q2_answer == "allie":
                st.success("wow that was easy")
                st.session_state.game_state['q2_answered'] = True
                st.session_state.game_state['game_completed'] = True
                st.rerun()
            else:
                st.error("not quite! this is an easy question")

# Valentine's Card section
if st.session_state.game_state['game_completed']:
    with st.expander("💌 click me first 💌", expanded=False):
        st.markdown("""
        <div class="card-container">
            <div class="valentine-card">
                <div class="card-header">
                    Hi Allie,
                </div>
                <div class="card-content">
                    <div class="card-message">
                        I'm sorry that we can't spend Valentines day together. I would've loved to spend the day together,
                        even if we just got to sit inside and hug because it will be raining. I miss you sooooooooooo much. Words cannot
                        describe how much I miss you. I miss you more than you'll ever miss me. Thanks for sticking with me for the past 598 days.
                        Every time we hang out together, I think about how lucky I am for you to even be in my presence. I love to listen to you, 
                        to hear you laugh, and to look at you of course. You make me smile so much. You're like the barbecue sauce to my chicken nuggets
                        (I know how much you like chicken nuggets and bbq sauce). There is not one thing that I don't love about you. You are so funny
                        too. I love how you never have a set opinion on food lol. I also love how cute you look with your glasses. I don't think I could
                        fit all the things I love about you on this page. You are so special to me I don't know how I'm living without you rn because I think about you all day. Anyways, it's
                        still nice how we call every night before bed. I always look forward to talking to you even if we're both super tired. 
                        I love you sooooooooooo much. Obviously more than you'll ever love me, but I think I can live with that. You're the best gf I could've ever asked for.<br><br>
                        I know you were upset that I didn't ask you to be my valentine yet, but it's literally because I was in the process of 
                        making this!! I couldn't spoil my secret, so I hope the sacrifice of making you mad was worth it. You can chat with a virtual
                        version of me below, although he's a little cheesy. You can come back to this and chat with him if you ever get bored of the real life me.
                        I love you so much Allie.
                    </div>
                    <div class="signature">
                        Love,<br>
                        Evan
                    </div>
                </div>
            </div>
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
    user_input = st.chat_input("chat with virtual me")

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Check for yes response and update state
        if any(word in user_input.lower() for word in ['yes', 'yeah', 'sure', 'okay', 'of course', 'definitely']):
            st.session_state.has_said_yes = True
            st.session_state.bot.has_said_yes = True
        
        # Get bot response
        bot_response = st.session_state.bot.get_response(user_input)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update the chat display
        st.rerun()