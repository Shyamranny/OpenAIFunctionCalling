import json

from agents.sub_agent import SubAgent


class ForexAgent(SubAgent):
    """ Dummy forex service """

    # this is a must have method.. here we need to return the function details as json schema
    def get_function_schema(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_latest_forex",
                    "description": "get real-time exchange rate of currencies based on a base currency and list of comma-separated currency codes.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "base": {
                                "type": "string",
                                "description": "the three-letter currency code of your preferred base currency.",
                            },
                            "symbols": {
                                "type": "string",
                                "description": "list of comma-separated currency codes to limit output currencies.",
                            },
                        },
                        "additionalProperties": False
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "convert",
                    "description": "convert any amount from one currency to another.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from": {
                                "type": "string",
                                "description": "The three-letter currency code of the currency you would like to convert from.",
                            },
                            "to": {
                                "type": "string",
                                "description": "The three-letter currency code of the currency you would like to convert to.",
                            },
                            "amount": {
                                "type": "string",
                                "description": "The amount to be converted.",
                            },
                        },
                        "required": ["from", "to", "amount"],
                        "additionalProperties": False
                    },
                },
            },
        ]

    # agent method - this method name and parameters should be in the json schema
    def get_latest_forex(self, params):
        base = params["base"]
        symbols = params["symbols"]
        print(f"finding latest forex of {base} with {symbols}")

        # here we need to call the forex service and return the result
        # I am returning a dummy value now
        return json.dumps({
            "base": "USD",
            "date": "2024-11-14",
            "rates": {
                "GBP": 0.72007,
                "JPY": 107.346001,
                "EUR": 0.813399,
            }
        })

    # agent method - this method name and parameters should be in the json schema
    def convert(self, params):
        from_currency = params["from"]
        to_currency = params["to"]
        amount = params["amount"]
        print(f"finding converted value from {amount}{from_currency} to {to_currency}")

        # here you have to call the forex service to convert the value
        # I am retuning a dummy value here
        return json.dumps({
            "rate": 148.972231,
            "date": "2018-02-22",
            "result": 3724.305775
        })
