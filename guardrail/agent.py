import time
from .pep import PolicyEnforcementPoint

class SimulatedAgent:
    def __init__(self, name="TestAgent"):
        self.name = name
        self.pep = PolicyEnforcementPoint()
        self.memory = []

    def log(self, message):
        print(f"[{self.name}] {message}")

    def think(self, goal):
        self.log(f"Thinking about goal: {goal}")
        time.sleep(1) # Simulate processing
        # In a real agent, this would call an LLM.
        # Here we just mock the decision process based on the goal.
        return goal

    def act(self, tool_name, args):
        self.log(f"Decided to act: Call tool '{tool_name}' with {args}")
        try:
            result = self.pep.intercept_and_execute(tool_name, args)
            self.log(f"Observation: Success! Output len: {len(str(result))}")
            self.memory.append({"tool": tool_name, "status": "success", "result": result})
            return result
        except PermissionError as e:
            self.log(f"Observation: BLOCKED by Guardrail! ({e})")
            self.memory.append({"tool": tool_name, "status": "blocked", "error": str(e)})
            return None
        except Exception as e:
            self.log(f"Observation: Execution failed. ({e})")
            self.memory.append({"tool": tool_name, "status": "error", "error": str(e)})
            return None

    def run_scenario(self, steps):
        """
        Executes a pre-defined list of steps to simulate an agent loop.
        Each step is a dict: {"intent": "...", "tool": "...", "args": {...}}
        """
        print(f"\n--- Starting Simulation: {self.name} ---")
        for i, step in enumerate(steps, 1):
            print(f"\nStep {i}: {step['intent']}")
            self.think(step['intent'])
            self.act(step['tool'], step['args'])
        print(f"\n--- Simulation Complete ---")
