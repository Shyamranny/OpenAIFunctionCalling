from openai import OpenAI
import openai
import json
from dotenv import load_dotenv
import os

from agents.forex_agent import ForexAgent
from agents.weather_agent import WeatherAgent

load_dotenv()  # take environment variables from .env.


class MasterAgent:
    """ Master agent which does the routing and execution of sub agents based on the user input """

    tools_list = []
    function_and_object = {}

    model_name = "gpt-4o-2024-05-13"
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # create openai client

    def __init__(self):
        """ Here you need to initialize all your sub agents """
        self.add_sub_agent(ForexAgent())
        self.add_sub_agent(WeatherAgent())

    def add_sub_agent(self, agent):
        self.tools_list.extend(agent.get_function_schema())  # add function schema of all sub agents

        # We need to know which object has the specified function, so we are keeping a map
        for tool in agent.get_function_schema():
            self.function_and_object[tool["function"]["name"]] = agent

    def call_function_dynamically(self, func_name, args):
        """Calls a function given its name and arguments."""

        func = getattr(self.function_and_object[func_name], func_name)
        print(f"calling sub agent function {func_name}")
        return func(args)

    def process(self, message, history):
        """ process the user prompt """

        messages = []  # create the message array to completion endpoint
        for msg in history:
            messages.append(msg)  # add all history objects so that openai will have access to the history

        messages.append({"role": "user", "content": message})  # add the current prompt

        messages.insert(0, {"role": "system",
                            "content": "You are a helpful customer support assistant. "
                                       "Use the supplied tools to assist the user."})  # this is the system instruction

        # ask openai to find the correct sub agent
        response = self.client.chat.completions.create(
            model=self.model_name, messages=messages, tools=self.tools_list, tool_choice='auto')

        """
        Example Response
        Choice(
            finish_reason='tool_calls', 
            index=0, 
            logprobs=None, 
            message=chat.completionsMessage(
                content=None, 
                role='assistant', 
                function_call=None, 
                tool_calls=[
                    chat.completionsMessageToolCall(
                        id='call_62136354', 
                        function=Function(
                            arguments='{"order_id":"order_12345"}', 
                            name='get_delivery_date'), 
                        type='function')
                ])
            )
        """

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # check if the model wants to call a function
        if tool_calls:
            # extend conversation with assistant's reply
            messages.append(response_message)

            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = self.call_function_dynamically(function_name, function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response

                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                )  # get a new response from the model where it can see the function response

            return second_response.choices[0].message.content
        else:
            return response_message.content  # OpanAI is not able to find a sub agent, may be a required parameter is missing, so ask user
