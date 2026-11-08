'''
Sends existing conversation to the model, replaces with a summary of conversation history that is no more then five lines
'''
from chat import llm

def compact(chat):
    '''
    >>> from unittest.mock import patch
    >>> from chat import Chat, client
    >>> chat = Chat(system='Be brief.')
    >>> chat.messages = [
    ...     {'role': 'system', 'content': 'Be brief.'},
    ...     {'role': 'user', 'content': 'Hi'},
    ...     {'role': 'assistant', 'content': 'Hello!'}
    ... ]
    >>> with patch.object(client.chat.completions, 'create') as request:
    ...     request.return_value.choices[0].message.content = 'The user greeted the assistant.'
    ...     compact(chat)
    >>> chat.messages
    [{'role': 'system', 'content': 'The user greeted the assistant.'}]
    '''
    messages_to_summarize = [
        {
            "role": "system",
            "content": "Summarize this conversation in no more than five lines."
        }
    ] + chat.messages

    reply = llm(messages_to_summarize, temperature=0)

    chat.messages = [
        {
            "role": "system",
            "content": reply.content
        }
    ]