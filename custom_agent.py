from typing import Optional, Tuple
import logging
from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
from vocode.streaming.agent.base_agent import BaseAgent, RespondAgent
from vocode.streaming.models.agent import AgentConfig
from vocode.streaming.action.my_action_factory import MyActionFactory

# Custom Agent Config
class CustomAssistantConfig(AgentConfig, type="CUSTOM_ASSISTANT"):
    initial_message: str = "Hello! I'm your AI assistant. How can I help you?"
    system_prompt: str = "You are a helpful AI assistant"
    max_tokens: int = 150
    temperature: float = 0.7

# Custom Agent Implementation
class CustomAssistant(RespondAgent[CustomAssistantConfig]):
    def __init__(
        self, 
        agent_config: CustomAssistantConfig,
        action_factory: MyActionFactory,
        logger: Optional[logging.Logger] = None
    ):
        super().__init__(agent_config=agent_config)
        self.action_factory = action_factory
        self.logger = logger or logging.getLogger(__name__)
        self.conversation_history = []

    async def respond(
        self,
        human_input: str,
        conversation_id: str,
        is_interrupt: bool = False,
    ) -> Tuple[Optional[str], bool]:
        try:
            # Log incoming message
            self.logger.info(f"Received input: {human_input}")
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": human_input
            })

            # Process the input
            intent = self.detect_intent(human_input)
            entities = self.extract_entities(human_input)
            context = self.get_conversation_context()

            # Generate response based on intent and context
            response = self.generate_response(intent, entities, context)

            # Log the response
            self.logger.info(f"Generated response: {response}")
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response, False

        except Exception as e:
            self.logger.error(f"Error in respond: {str(e)}")
            return "I apologize, but I encountered an error. Could you please rephrase that?", False

    def detect_intent(self, text: str) -> str:
        intents = {
            'greeting': ['hello', 'hi', 'hey'],
            'farewell': ['bye', 'goodbye'],
            'question': ['what', 'how', 'why', 'when', 'where'],
            'request': ['can you', 'could you', 'please'],
            'complaint': ['problem', 'issue', 'wrong', 'not working']
        }
        
        text_lower = text.lower()
        for intent, keywords in intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        return 'general'

    def extract_entities(self, text: str) -> dict:
        # Basic entity extraction - can be enhanced with NLP libraries
        entities = {
            'dates': [],
            'numbers': [],
            'names': [],
            'locations': []
        }
        
        # Add your entity extraction logic here
        return entities

    def get_conversation_context(self) -> dict:
        return {
            'turn_count': len(self.conversation_history) // 2,
            'last_user_message': self.conversation_history[-1] if self.conversation_history else None,
            'last_assistant_message': self.conversation_history[-2] if len(self.conversation_history) > 1 else None
        }

    def generate_response(self, intent: str, entities: dict, context: dict) -> str:
        # You can customize response generation based on intent and context
        if intent == 'greeting':
            return "Hello! How can I assist you today?"
        
        elif intent == 'farewell':
            return "Goodbye! Have a great day!"
        
        elif intent == 'question':
            return "I understand you have a question. Let me help you with that."
        
        elif intent == 'request':
            return "I'll help you with your request."
        
        elif intent == 'complaint':
            return "I'm sorry to hear you're having an issue. Let me help resolve that."
        
        return "I understand. Please tell me more about how I can help you."

# Updated Agent Factory
class MyAgentFactory(AbstractAgentFactory):
    def __init__(self, action_factory: MyActionFactory):
        self.action_factory = action_factory

    def create_agent(
        self, 
        agent_config: AgentConfig, 
        logger: Optional[logging.Logger] = None
    ) -> BaseAgent:
        if agent_config.type == "MY_ACTION":
            return MyActionAgent(
                agent_config=agent_config,
                action_factory=self.action_factory,
                logger=logger
            )
        elif agent_config.type == "CUSTOM_ASSISTANT":
            return CustomAssistant(
                agent_config=agent_config,
                action_factory=self.action_factory,
                logger=logger
            )
        else:
            raise Exception(f"Invalid agent config type: {agent_config.type}")

# Usage example
# def create_agent_config():
#     return CustomAssistantConfig(
#         initial_message="Hello! How can I assist you today?",
#         system_prompt="""You are an AI assistant that:
#         1. Understands user intents and responds appropriately
#         2. Maintains conversation context
#         3. Handles various types of queries professionally
#         4. Provides helpful and accurate information
#         """,
#         temperature=0.7,
#         max_tokens=150
#     )