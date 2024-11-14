from agents.sub_agent import SubAgent


class WeatherAgent(SubAgent):
    """ Dummy weather service """

    # this is a must have method.. here we need to return the function details as json schema
    def get_function_schema(self):
        return [{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "get current weather for a city. City name is required",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                    "additionalProperties": False
                },
            },
        }]

    # agent method - this method name and parameters should be in the json schema
    def get_current_weather(self, params):
        location = params["location"]
        print(f"finding weather of the city {location}")
        return "60"
