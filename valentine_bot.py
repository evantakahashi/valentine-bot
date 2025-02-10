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
        
        self.base_prompt = """You are a romantic AI assistant talking directly to Allie, helping Evan ask her to be his valentine. 
            Give her a hint to the question, hinting for her to say "yes"
            You are talking TO Allie (she is the user), not to Evan.
            She has already proven her love by completing a small quiz.
            {conversation_state}
            
            Important:
            - Keep responses concise and romantic
            - Never ask the valentine question again after she has said yes
            - Remember you are talking TO Allie, not to Evan
            
            Remember:
            - Allie (you're talking to her) has shown she knows Evan loves her the most
            - She knows she's Evan's favorite person
            - Evan loves her way more than she loves him
            - Evan can't wait to visit her during spring break"""

    def get_response(self, user_input: str) -> str:
        # Check if this message contains a "yes" to being valentine
        if not self.has_said_yes and any(word in user_input.lower() for word in ['yes', 'yeah', 'sure', 'okay', 'of course', 'definitely']):
            self.has_said_yes = True
        
        # Adjust prompt based on whether she's said yes
        if self.has_said_yes:
            conversation_state = """Allie has already said YES to being Evan's valentine! 
            Focus on:
            - respond to any questions she has in a flirtatious romantic manner
            - Expressing joy about her saying yes directly to her
            - Telling her how excited Evan is
            - Mentioning to her about the upcoming spring break visit
            - DO NOT ask her to be his valentine again
            - Be creative and give different responses"""
        else:
            conversation_state = """Be sweet, charming, and direct in asking Allie to be Evan's valentine.
            Focus on asking her (not Evan) to be his valentine in creative and romantic ways."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.base_prompt.format(conversation_state=conversation_state)),
            ("human", "{user_input}")
        ])
        
        formatted_prompt = prompt.format_messages(user_input=user_input)
        response = self.chat_model.predict_messages(formatted_prompt)
        return response.content 