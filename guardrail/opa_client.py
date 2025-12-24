import requests
import json

class OPAClient:
    def __init__(self, url="http://127.0.0.1:8181/v1/data/guardrail/allow"):
        self.url = url

    def check(self, tool_name, args):
        """
        Queries OPA to check if the tool execution is allowed.
        """
        payload = {
            "input": {
                "tool": tool_name,
                "args": args
            }
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            result = response.json().get("result", False)
            return result
        except requests.RequestException as e:
            print(f"Error connecting to OPA: {e}")
            return False
