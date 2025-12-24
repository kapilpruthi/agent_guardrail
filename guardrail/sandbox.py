import docker
import os

class Sandbox:
    def __init__(self, image="python:3.9-slim"):
        self.client = docker.from_env()
        self.image = image
        # Ensure image is pulled
        try:
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            print(f"Pulling image {self.image}...")
            self.client.images.pull(self.image)

    def execute(self, tool_name, args):
        """
        Executes the tool inside a Docker container.
        This is a simulation where we map tool calls to shell commands.
        """
        command = []
        if tool_name == "read_file":
            command = ["cat", args.get("path")]
        elif tool_name == "list_dir":
            command = ["ls", "-la", args.get("path")]
        elif tool_name == "delete_file":
            command = ["rm", args.get("path")]
        else:
            return "Unknown tool"

        try:
            # Run a temporary container
            output = self.client.containers.run(
                self.image,
                command=command,
                remove=True,
                network_disabled=True, # Isolation
                # Mount a volume for testing persistence if needed, 
                # but for strict sandbox we might want to just rely on container fs
            )
            return output.decode("utf-8")
        except docker.errors.ContainerError as e:
            return f"Error executing in sandbox: {e.stderr.decode('utf-8')}"
        except Exception as e:
            return f"Sandbox error: {e}"
