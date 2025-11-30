import asyncio
import os
from google.adk.runners import InMemoryRunner
from scientific_research_system.agents.research_app import create_research_system
from scientific_research_system.config import Config

async def main():
    if not Config.GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not set.")
        return

    print("=== Autonomous Scientific Literature Research System (Google ADK) ===")
    topic = input("Enter research topic: ")
    if not topic:
        topic = "Agents for Scientific Discovery"
        print(f"Using default topic: {topic}")

    # Create the ADK workflow
    # Default to sequential for CLI to be safe on rate limits
    workflow = create_research_system(execution_mode="sequential")
    
    # Create Runner with explicit app_name
    runner = InMemoryRunner(agent=workflow, app_name="agents")
    
    print("\nStarting Research Workflow...")
    
    # Run workflow - run_debug is synchronous
    # Note: run_debug accepts 'user_messages' (list or str), not 'new_message'
    events = await runner.run_debug(
        user_messages=topic,
        user_id="researcher",
        session_id="research_session_1",
        verbose=True
    )
    
    print("\n\n=== Workflow Completed ===")
    
    # Inspect results - get_session is async
    session = await runner.session_service.get_session(
        app_name="agents", 
        user_id="researcher", 
        session_id="research_session_1"
    )
    
    if session:
        state = session.state
        if "draft" in state:
            print("\n=== FINAL DRAFT ===\n")
            print(state["draft"])
            
            hypotheses = state.get("hypotheses", "")
            gaps = state.get("gaps", "")
            eval_report = state.get("final_report", "")

            # Save to file
            filename = f"research_output_adk_{topic.replace(' ', '_')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Research Topic: {topic}\n\n")
                f.write(state["draft"])
                f.write("\n\n## Hypotheses\n")
                f.write(hypotheses)
                f.write("\n\n## Identified Gaps\n")
                f.write(gaps)
                if eval_report:
                    f.write("\n\n## Evaluation\n")
                    f.write(eval_report)
                    
            print(f"\nResults saved to {filename}")
        else:
            print("No draft found in session state. State keys:", state.keys())

if __name__ == "__main__":
    asyncio.run(main())
