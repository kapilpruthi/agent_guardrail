import docker
import os
import time

class OPAManager:
    def __init__(self, container_name="opa-guardrail", port=8181):
        self.container_name = container_name
        self.port = port
        self.client = docker.from_env()

    def ensure_running(self):
        """
        Ensures the OPA container is running. Starts it if it's not.
        """
        try:
            container = self.client.containers.get(self.container_name)
            if container.status != "running":
                container.restart()
                print("OPA container restarted.")
            else:
                print("OPA already running.")
        except docker.errors.NotFound:
            print("Starting new OPA container...")
            policy_dir = os.path.abspath("policy")
            self.client.containers.run(
                "openpolicyagent/opa:latest",
                command=f"run --server --log-level debug --addr 0.0.0.0:{self.port} /policy",
                volumes={policy_dir: {'bind': '/policy', 'mode': 'ro'}},
                ports={f'{self.port}/tcp': self.port},
                name=self.container_name,
                detach=True
            )
            print("OPA container started.")
            time.sleep(3) # Wait for startup
        except Exception as e:
            print(f"Error managing OPA container: {e}")
            raise

    def stop(self):
        """
        Stops and removes the OPA container.
        """
        try:
            container = self.client.containers.get(self.container_name)
            container.stop()
            container.remove()
            print("OPA container stopped.")
        except docker.errors.NotFound:
            print("OPA container not found, nothing to stop.")
        except Exception as e:
            print(f"Error stopping OPA container: {e}")
