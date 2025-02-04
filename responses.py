from random import choice, randint
from classes import Score


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    # Chat responses
    if lowered == '':
        return 'Nothing?'
    if 'hello' in lowered:
        return 'Hello there fellow banana!'
    if 'how are you' in lowered:
        return 'Good, thanks!'
    if 'bye' in lowered:
        return 'See ya!'


    # Commands
    if '!addwin' in lowered:
        return f"command {lowered.split(' ')[1]} won"
    if '!addloss' in lowered:
        return f"command {lowered.split(' ')[1]} lost"
    if '!printwins' in lowered:
        return f"command rankbywins"
    if '!printwinrate' in lowered:
        return f"command rankbywinrate"
    if '!roll' in lowered:
        return f"You rolled a {randint(1, 6)}"