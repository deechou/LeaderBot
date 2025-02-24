from random import choice, randint
from classes import Score

#generates a response based on user input
def get_response(user_input: str) -> str:
    user_input_lowered: str = user_input.lower()

    # Chat responses
    if user_input_lowered == '':
        return 'Nothing?'
    if 'hello' in user_input_lowered:
        return 'Hello there fellow banana!'
    if 'how are you' in user_input_lowered:
        return 'Good, thanks!'
    if 'bye' in user_input_lowered:
        return 'See ya!'
    if '!roll' in user_input_lowered:
        return f"You rolled a {randint(1, 6)}"