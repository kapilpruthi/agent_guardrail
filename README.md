# Agent Guardrail

Agent Guardrail is a security framework designed to act as a **Policy Enforcement Point (PEP)** for AI agents. It intercepts tool calls made by an agent and validates them against a set of policies defined in **Open Policy Agent (OPA)** before allowing execution in a sandboxed environment.

## Features

-   **Interception**: Intercepts tool executions (e.g., `read_file`, `delete_file`).
-   **Policy Decision**: Queries an OPA server to check if an action is allowed based on Rego policies.
-   **Sandboxing**: Executes authorized actions within a Docker container to prevent harm to the host system.
-   **Configurable Policies**: Policies are defined in `policy/main.rego` and can be easily updated.

## Prerequisites

-   **Docker**: Required for running the OPA server and the execution sandbox.
-   **Python 3.8+**

## Setup

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Demo

The `run_demo.py` script demonstrates the system in action. It spins up the OPA container, runs several test cases (both allowed and denied actions), and prints the results.

```bash
python run_demo.py
```

### Running Simulated Agent

To demonstrate how an AI agent interacts with the guardrail, run the simulated agent script. This mimics an agent loop that attempts both allowed and malicious actions.

```bash
python run_agent_simulation.py
```

### Project Structure

-   `guardrail/`: Core package containing the PEP, OPA client, and Sandbox logic.
    -   `pep.py`: Main entry point for intercepting actions.
    -   `opa_client.py`: Client for communicating with the OPA server.
    -   `sandbox.py`: Handles execution of allowed actions in Docker.
-   `policy/`: Contains OPA policy definitions.
    -   `main.rego`: The Rego policy file.
-   `run_demo.py`: Demonstration script.

## Policy Example

Policies are written in Rego. Example from `policy/main.rego`:

```rego
package guardrail

default allow = false

# Allow reading files
allow if {
    input.tool == "read_file"
}

# Only allow deleting files in /tmp/
allow if {
    input.tool == "delete_file"
    startswith(input.args.path, "/tmp/")
}
```
