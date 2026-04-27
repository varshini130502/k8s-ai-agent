import sys
from core import K8sAgent

def main():
    print("======================================================")
    print("🧠 Kubernetes AI Copilot - Interactive Mode")
    print("Type 'exit' or 'quit' to end the session.")
    print("======================================================\n")

    try:
        agent = K8sAgent()
    except ValueError as e:
        print(f"ERROR: {e}")
        print("Get your free key at: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    while True:
        try:
            user_query = input("\n(k8s-copilot)> ").strip()
            if user_query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if not user_query:
                continue
            
            print("Thinking...")
            command = agent.generate_command(user_query)
            
            print("\n------------------------------------------------")
            print(f"🤖 Suggested command:\n> \033[92m{command}\033[0m")
            print("------------------------------------------------")
            
            confirm = input("\nExecute this command? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Skipping execution.")
                continue
                
            print("\n🚀 Executing (with Auto-Fix enabled)...")
            final_cmd, output, success = agent.execute_with_autofix(command)
            
            print("\n📦 Summarizing output...")
            summary = agent.summarize_output(user_query, final_cmd, output)
            
            print("\n================== SUMMARY ==================")
            print(summary)
            print("=============================================")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
