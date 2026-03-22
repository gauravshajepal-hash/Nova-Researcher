import time
import subprocess
import sys
import os
import threading
from src.reactor.event_bus import ArtifactReactor
from src.pi_agent.orchestrator import PIOrchestrator

def lab_heartbeat(pi):
    """Background thread to run the PI and trigger workers."""
    print("[System] Lab Heartbeat Started.")
    try:
        while True:
            # 1. PI Cycle
            pi.run_cycle()
            
            # 2. Trigger a worker cycle (simulate swarm activity)
            # In a real distributed system, workers would be separate processes
            subprocess.run(f"{sys.executable} -m src.swarm.literature_worker", shell=True, timeout=10, capture_output=True)
            
            time.sleep(10)
    except Exception as e:
        print(f"[System] Heartbeat Error: {e}")

def start_lab():
    print("\n" + "="*50)
    print("--- NOVA RESEARCHER LAB: INTERACTIVE STEERING ---")
    print("="*50)
    print("Commands: /steer <msg>, /question <msg>, /status, /exit\n")
    
    reactor = ArtifactReactor()
    pi = PIOrchestrator(agent_id="Lab_PI", reactor=reactor)
    
    # Start the background lab processes
    threading.Thread(target=lab_heartbeat, args=(pi,), daemon=True).start()
    
    while True:
        cmd = input("Lab Console > ").strip()
        
        if not cmd:
            continue
            
        if cmd.lower() == "/exit":
            print("[Lab Manager] Shutting down lab. Goodbye.")
            break
            
        elif cmd.lower() == "/status":
            plan = pi._load_plan()
            print("\n--- Current Research Plan ---")
            for step in plan:
                print(f"[{step['status'].upper()}] Step {step['step']}: {step['task']}")
            print("----------------------------\n")
            
        elif cmd.startswith("/steer "):
            directive = cmd[7:]
            pi.handle_steering(directive)
            pi.ask(
                need_type="steering_directive",
                description=directive,
                context={"target_id": "all", "origin": "Human_User"}
            )
            print(f"[System] Steering directive broadcasted to the entire swarm.")

        elif cmd.startswith("/question "):
            question = cmd[10:]
            print(f"\n[PI] Responding to Human Question: '{question}'")
            # In a real implementaiton, use LLM to answer based on DAG
            print("[PI] Analysis: Our current results indicate strong correlation between the variables. We are pivoting to verify Step 2.")

        else:
            print("[System] Unknown command. Use /steer, /question, or /status.")

if __name__ == "__main__":
    start_lab()
