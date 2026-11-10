'''
ChatGPT Wrapper with some tool functionality.
'''
import os
import json
import sys
from dotenv import load_dotenv
from groq import Groq
from tools.ls import ls
from tools.cat import cat
from tools.calculate import calculate
from tools.grep import grep


load_dotenv()
# Map function names to implementations
available_functions = {
    "calculate": calculate,
    "cat": cat,
    "grep": grep,
    "ls": ls
}
# Define the tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Find lines matching a regex in files",
            "parameters": {
                "type": "object",
                "properties": {
                    "regex": {
                        "type": "string",
                        "description": "The regular expression to search for"
                    },
                    "path": {
                        "type": "string",
                        "description": "The file path or glob pattern to search"
                    }
                },
                "required": ["regex", "path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in the current or specified folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Folder to list; defaults to the current folder"
                    }
                },
                "required": []
            }
        }
    }
]


def execute_tool_call(tool_call):
    """Parse and execute a single tool call
    >>> from unittest.mock import Mock
    >>> tool_call = Mock()
    >>> tool_call.function.name = "calculate"
    >>> tool_call.function.arguments = '{"expression": "12*12"}'
    >>> execute_tool_call(tool_call)
    '144'
    """
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    # Call the function with unpacked arguments
    return function_to_call(**function_args)


def llm(messages, temperature=1):
    """Sets parameters for the LLM passthrough.

    >>> from unittest.mock import patch
    >>> messages = [{'role': 'user', 'content': 'Hi'}]
    >>> with patch('chat.Groq') as mock_groq:
    ...     request = mock_groq.return_value.chat.completions.create
    ...     request.return_value.choices[0].message.content = 'Hello!'
    ...     reply = llm(messages, temperature=0)
    ...     print(reply.content)
    ...     print(request.call_args.kwargs['temperature'])
    ...     print(request.call_args.kwargs['messages'] == messages)
    ...     print(request.call_args.kwargs['model'])
    Hello!
    0
    True
    openai/gpt-oss-20b
    """
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
    completion = client.chat.completions.create(
        messages=messages,
        model='openai/gpt-oss-20b',
        temperature=temperature,
        tools=tools
        
    )
    return completion.choices[0].message


class Chat:
    '''Uses chat history, system instructions, and tool execution calls.
    >>> from unittest.mock import patch
    >>> chatNew = Chat(system='act like a five year old')
    >>> with patch('chat.Groq') as mock_groq:
    ...     request = mock_groq.return_value.chat.completions.create
    ...     request.return_value.choices[0].message.content = 'Hiii!'
    ...     request.return_value.choices[0].message.tool_calls = None
    ...     request.return_value.choices[0].message.model_dump.return_value = {
    ...         'role': 'assistant',
    ...         'content': 'Hiii!'
    ...     }
    ...     reply = chatNew.send_message('Hiee', temperature=0)
    >>> print(reply)
    Hiii!
    >>> print(chatNew.messages)
    [{'role': 'system', 'content': 'act like a five year old'}, {'role': 'user', 'content': 'Hiee'}, {'role': 'assistant', 'content': 'Hiii!'}]
    '''
    def __init__(self, system='You are a helpful assistant.'):
        '''
        This provides an argument to set the system parameters.
        '''
        self.messages = [{'role': 'system', 'content': system}]

    def send_message(self, message, temperature=0.8, debug=False):
        """Send a message, check if groq should call on a tool and if so, execute and retain the reply.
        >>> from unittest.mock import patch
        >>> with patch('chat.Groq') as mock_groq:
        ...     request = mock_groq.return_value.chat.completions.create
        ...     request.return_value.choices[0].message.tool_calls = None
        ...     request.return_value.choices[0].message.content = 'Hello!'
        ...     request.return_value.choices[0].message.model_dump.return_value = {
        ...         'role': 'assistant',
        ...         'content': 'Hello!'
        ...     }
        ...     chat = Chat(system='Be brief.')
        ...     print(chat.send_message('Hi', temperature=0))
        Hello!
        >>> expected = [
        ...     {'role': 'system', 'content': 'Be brief.'},
        ...     {'role': 'user', 'content': 'Hi'},
        ...     {'role': 'assistant', 'content': 'Hello!'},
        ... ]
        >>> chat.messages == expected
        True
        >>> from unittest.mock import MagicMock, Mock, patch
        >>> first = MagicMock()
        >>> second = MagicMock()
        >>> calculator = Mock()
        >>> calculator.id = "call_123"
        >>> calculator.function.name = "calculate"
        >>> calculator.function.arguments = '{"expression": "12*12"}'
        >>> first.choices[0].message.tool_calls = [calculator]
        >>> first.choices[0].message.content = None
        >>> first.choices[0].message.model_dump.return_value = {
        ...     "role": "assistant",
        ...     "tool_calls": [
        ...         {
        ...             "id": "call_123",
        ...             "type": "function",
        ...             "function": {
        ...                 "name": "calculate",
        ...                 "arguments": '{"expression": "12*12"}'
        ...             }
        ...         }
        ...     ]
        ... }
        >>> second.choices[0].message.tool_calls = None
        >>> second.choices[0].message.content = "144"
        >>> second.choices[0].message.model_dump.return_value = {
        ...     "role": "assistant",
        ...     "content": "144"
        ... }
        >>> with patch('chat.Groq') as mock_groq:
        ...     request = mock_groq.return_value.chat.completions.create
        ...     request.side_effect = [first, second]
        ...     chat = Chat(system='Be brief.')
        ...     print(chat.send_message('What is 12*12', temperature=0))
        144
        >>> expected = [
        ...     {'role': 'system', 'content': 'Be brief.'},
        ...     {'role': 'user', 'content': 'What is 12*12'},
        ...     {'role': 'assistant', 'tool_calls': [
        ...     {
        ...       "type": "function",
        ...       "id": "call_123",
        ...       "function": {
        ...       "name": "calculate",
        ...       "arguments": '{"expression": "12*12"}'
        ...         }
        ...        }
        ...        ]
        ...      },
        ...     {'role': "tool", "tool_call_id": 'call_123', "name": "calculate", "content": "144"},
        ...     {'role': 'assistant', 'content': '144'},
        ... ]
        >>> chat.messages == expected
        True
        """
        self.messages.append({'role': 'user', 'content': message})
        reply = llm(self.messages, temperature=temperature)
        self.messages.append(reply.model_dump(exclude_none=True))
        if reply.tool_calls:
            # 3. Execute each tool call (using the helper function from step 2)
            for tool_call in reply.tool_calls:
                if debug:
                    print("Tool:", tool_call.function.name)
                    print("Arguments:", tool_call.function.arguments)
                function_response = execute_tool_call(tool_call)
            # Add tool result to messages
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(function_response)
                })
            reply = llm(self.messages, temperature=temperature)
            self.messages.append(reply.model_dump(exclude_none=True))
        return reply.content


def repl(temperature=0.8):
    """
    >>> from unittest.mock import patch, MagicMock
    >>> first = MagicMock()
    >>> first.choices[0].message.content = 'Hello!'
    >>> first.choices[0].message.tool_calls = None
    >>> first.choices[0].message.model_dump.return_value = {
    ...     'role': 'assistant',
    ...     'content': 'Hello!'
    ... }
    >>> second = MagicMock()
    >>> second.choices[0].message.content = "Your last message was 'Hi'."
    >>> second.choices[0].message.tool_calls = None
    >>> second.choices[0].message.model_dump.return_value = {
    ...     'role': 'assistant',
    ...     'content': "Your last message was 'Hi'."
    ... }
    >>> with patch('chat.Groq') as mock_groq:
    ...     request = mock_groq.return_value.chat.completions.create
    ...     request.side_effect = [first, second]
    ...     chat = Chat(system='Be brief.')
    ...     print(chat.send_message('Hi', temperature=0))
    ...     print(chat.send_message('What was my last message', temperature=0))
    Hello!
    Your last message was 'Hi'.
    >>> with patch.object(sys, 'argv', ['chat']):
    ...  with patch('builtins.input', side_effect=['Ahoy', EOFError]):
    ...     with patch('chat.Groq') as mock_groq:
    ...         request = mock_groq.return_value.chat.completions.create
    ...         request.return_value.choices[0].message.content = 'Hello!'
    ...         request.return_value.choices[0].message.tool_calls = None
    ...         repl(temperature=0)
    Hello!
    <BLANKLINE>
    >>> with patch.object(sys, 'argv', ['chat']):
    ...  with patch('builtins.input', side_effect=['Ahoy', KeyboardInterrupt]):
    ...     with patch('chat.Groq') as mock_groq:
    ...         request = mock_groq.return_value.chat.completions.create
    ...         request.return_value.choices[0].message.content = 'Hello!'
    ...         request.return_value.choices[0].message.tool_calls = None
    ...         repl(temperature=0)
    Hello!
    <BLANKLINE>
    
    """
    chat = Chat(system='You are a helpful assistant. You always speak like Emperor Palpatine.')
    debug = "--debug" in sys.argv[1:]
    
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)

                function_name = parts[0][1:]
                argument = parts[1] if len(parts) > 1 else ""

                function_to_call = available_functions[function_name]

                result = function_to_call(argument)
                
                print(result)
                chat.messages.append({
                    "role": "user",
                    "content": user_input
                    })
                chat.messages.append({
                    "role": "assistant",
                    "tool": str(function_name),
                    "content": str(result)                 
                })
            else:
                print(chat.send_message(user_input, temperature=temperature, debug=debug))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
