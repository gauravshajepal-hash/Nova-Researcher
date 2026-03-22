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
    
    reactor = ArtifactReactor() # 1. Initialize PI
    pi = PIOrchestrator(agent_id="Lab_PI", reactor=reactor)
    
    # 2. Optimized Multi-Role Swarm Scaling
    # Priority: Postdoc (3) > PhD Student (3) > Intern (2)
    max_agents = int(os.getenv("MAX_CONCURRENT_AGENTS", 8))
    
    target_inventory = [
        ("Postdoc", 3),
        ("PhD_Student", 3),
        ("Intern", 2)
    ]
    
    active_team = []
    for role, count in target_inventory:
        for i in range(count):
            if len(active_team) >= max_agents:
                print(f"[Lab Manager] Resource Limit Reached ({max_agents}). Skipping remaining {role}s.")
                break
            agent_id = f"{role}_{i+1}"
            active_team.append({"id": agent_id, "role": role})
            
    print(f"[Lab Manager] Successfully scaled lab to {len(active_team)} active staff members.")
    
    # ... launch logic continues ...
    
    # Start the background lab processes
    threading.Thread(target=lab_heartbeat, args=(pi,), daemon=True).start()
    
    # Start the API Dashboard Server
    from src.reactor.server import app
    import uvicorn
    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
    threading.Thread(target=run_server, daemon=True).start()
    
    print("[System] Dashboard Live at: http://localhost:8000/ui/index.html")
    print("[System] Lab Heartbeat Started.")
    
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
