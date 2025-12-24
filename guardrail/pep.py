from .opa_client import OPAClient
from .sandbox import Sandbox

class PolicyEnforcementPoint:
    def __init__(self):
        self.opa = OPAClient()
        self.sandbox = Sandbox()

    def intercept_and_execute(self, tool_name, args):
        print(f"[PEP] Intercepting tool: {tool_name} with args: {args}")
        
        allowed = self.opa.check(tool_name, args)
        
        if allowed:
            print("[PEP] Policy Check: ALLOWED")
            print("[PEP] Executing in Sandbox...")
            result = self.sandbox.execute(tool_name, args)
            print(f"[PEP] Execution Result:\n{result}")
            return result
        else:
            print("[PEP] Policy Check: DENIED")
            raise PermissionError(f"Action {tool_name} denied by policy.")
