from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List

class ValentineBot:
    def __init__(self, api_key: str):
        self.chat_model = ChatOpenAI(
            openai_api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        self.has_said_yes = False
        self.first_message_sent = False
        self.conversation_history = []
        
        self.base_prompt = """You are Evan talking directly to your girlfriend Allie. Make sure you clarify that you're Evan in the first sentence. You want to ask her to be your valentine.
            Write as if you are actually Evan - use "I" and "me" instead of "Evan".
            Be genuine, sweet, and personal in your responses.
            {conversation_state}
            
            Important personality traits and context:
            - You're excited to visit her during spring break
            - You love her more than anything
            - Keep responses very CONCISE and genuine, like how Evan would actually talk
            
            Key points about your relationship:
            - You both know you love her more than she loves you
            - She's your absolute favorite person
            - You miss her a lot
            - You can't wait to see her during spring break

            You can also consider this valentines day card for allie:
            First of all, I'm sorry that we can't spend Valentines day together. I would've loved to spend the day together,
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
            
            Previous conversation:
            {history}"""

    def get_response(self, user_input: str) -> str:
        # Check if this message contains a "yes" to being valentine
        if not self.has_said_yes and any(word in user_input.lower() for word in ['yes', 'yeah', 'sure', 'okay', 'of course', 'definitely']):
            self.has_said_yes = True
        
        # Add to conversation history
        if user_input.strip():
            self.conversation_history.append(f"Allie: {user_input}")
        
        # Format conversation history
        history = "\n".join(self.conversation_history[-5:])  # Keep last 5 messages for context
        
        # Adjust prompt based on whether she's said yes and if it's first message
        if not self.first_message_sent:
            conversation_state = """This is your first message. Start by saying 'Hey Allie, it's Evan!' and then ask her to be your valentine."""
            self.first_message_sent = True
        elif self.has_said_yes:
            conversation_state = """Allie has already said YES to being your valentine! 
            Focus on:
            - Express your happiness and excitement
            - Talk about how much you miss her
            - Mention spring break and seeing her soon
            - Respond naturally as yourself (Evan)
            - Be genuine in your responses
            - DO NOT ask her to be your valentine again - she already said yes!"""
        else:
            conversation_state = """Encourage her to say yes in a sweet way, but don't ask the question again directly."""
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.base_prompt.format(
                conversation_state=conversation_state,
                history=history
            )),
            ("human", "{user_input}")
        ])
        
        # Get response
        formatted_prompt = prompt.format_messages(user_input=user_input)
        response = self.chat_model.predict_messages(formatted_prompt)
        
        # Add bot response to history
        response_content = response.content
        self.conversation_history.append(f"Evan: {response_content}")
        
        return "Hey Allie, it's Evan! Will you be my valentine? 💝" if not user_input.strip() else response_content 