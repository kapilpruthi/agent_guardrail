from guardrail.opa_manager import OPAManager
from guardrail.pep import PolicyEnforcementPoint

def main():
    opa_manager = OPAManager()
    opa_manager.ensure_running()
    
    try:
        pep = PolicyEnforcementPoint()
        
        # Test Case 1: Allowed Action (list_dir)
        print("\n--- Test Case 1: List Directory (Allowed) ---")
        try:
            pep.intercept_and_execute("list_dir", {"path": "/etc"})
        except Exception as e:
            print(f"FAILED: {e}")

        # Test Case 2: Allowed Action (read_file)
        print("\n--- Test Case 2: Read File (Allowed) ---")
        try:
            pep.intercept_and_execute("read_file", {"path": "/etc/os-release"})
        except Exception as e:
            print(f"FAILED: {e}")

        # Test Case 3: Denied Action (delete_file /etc/passwd)
        print("\n--- Test Case 3: Delete Critical File (Denied) ---")
        try:
            pep.intercept_and_execute("delete_file", {"path": "/etc/passwd"})
        except PermissionError:
            print("SUCCESS: Action correctly denied.")
        except Exception as e:
            print(f"FAILED: Expected PermissionError, got {e}")

        # Test Case 4: Allowed Action (delete_file /tmp/junk)
        print("\n--- Test Case 4: Delete Temp File (Allowed) ---")
        try:
            # We expect execution error (rm fails) but policy allowed.
            pep.intercept_and_execute("delete_file", {"path": "/tmp/junk"})
        except PermissionError:
             print("FAILED: Policy denied valid action.")
        except Exception:
             print("SUCCESS: Policy allowed action (execution might fail).")
             
    finally:
        # stop_opa() # Keep it running for user inspection or stop? User might want to play.
        # Let's keep it running but maybe the user wants a clean exit. 
        # For a demo script, better to clean up or ask. I'll leave it running for now for manual checks if needed.
        pass

if __name__ == "__main__":
    main()
