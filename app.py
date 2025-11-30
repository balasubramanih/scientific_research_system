import streamlit as st
import os
import sys
import asyncio
import uuid
from dotenv import load_dotenv

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Autonomous Research Agent (ADK)", layout="wide", page_icon="🔬")

# Import ADK components
try:
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    from scientific_research_system.agents.research_app import create_research_system
    from scientific_research_system.config import Config
except ImportError as e:
    st.error(f"Configuration Error: Could not import required modules. Ensure 'google-adk' is installed.\nError: {e}")
    st.stop()

st.title("🔬 Autonomous Scientific Literature Research System")
st.markdown(f"""
This system leverages a **multi-agent architecture** (powered by Google ADK & {Config.MODEL_NAME}) to:
1.  **Mine** literature from ArXiv and the Web.
2.  **Construct** a knowledge graph of concepts.
3.  **Identify** research gaps.
4.  **Generate** novel hypotheses.
5.  **Draft** a comprehensive review.
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input("Google API Key", type="password", value=Config.GOOGLE_API_KEY or "")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        
    # Execution Mode Selection
    execution_mode = st.selectbox(
        "Execution Mode",
        ["sequential", "parallel"],
        index=0,
        help="Sequential: Slower but safer for rate limits. Parallel: Faster but may hit rate limits."
    )
    
    st.divider()
    st.success("System Ready (ADK Mode)")

# Main Interface
topic = st.text_input("Enter Research Topic:", placeholder="e.g., 'Multi-agent systems for climate modeling'", help="Be specific for better results.")

if st.button("🚀 Start Research", type="primary"):
    if not topic:
        st.warning("Please enter a research topic.")
    elif not Config.GOOGLE_API_KEY and not os.environ.get("GOOGLE_API_KEY"):
        # Config might load initially, but if set via UI, we check env
        st.error("Please provide a Google API Key.")
    else:
        # Initialize ADK Workflow
        try:
            # Create workflow based on selected execution mode
            workflow = create_research_system(execution_mode=execution_mode)
            runner = InMemoryRunner(agent=workflow, app_name="agents")
            
            session_id = str(uuid.uuid4())
            user_id = "researcher"
            
            # UI Containers
            progress_container = st.container()
            log_container = st.expander("📜 Execution Logs", expanded=True)
            result_container = st.container()

            with progress_container:
                st.info(f"Initializing agents ({execution_mode} mode)...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                
            # Run the agent
            # ADK's InMemoryRunner runs asynchronously. 
            # We'll display a generic spinner because we can't easily stream step-by-step progress 
            # without a custom event listener in this version of ADK/Streamlit integration.
            
            with st.spinner("Agents are collaborating... This may take 1-2 minutes."):
                # Run the workflow
                # We pass the topic as the user message
                try:
                    # Create session explicitly to avoid "Session not found" in threads
                    # Signature is: create_session(*, app_name: str, user_id: str, state: Optional[dict] = None, session_id: Optional[str] = None)
                    # We must pass kwargs
                    
                    # Define an async execution function to handle the entire flow
                    async def execute_research():
                        # 1. Create Session
                        await runner.session_service.create_session(
                             app_name="agents", 
                             user_id=user_id, 
                             session_id=session_id
                         )
                        
                        # 2. Run Workflow (debug mode is synchronous but wrapped as async in recent versions or we call it async if awaitable)
                        # Based on previous error, run_debug IS awaitable (returns coroutine).
                        events = await runner.run_debug(
                            user_messages=topic,
                            user_id=user_id,
                            session_id=session_id,
                            verbose=False
                        )
                        return events

                    # Run the complete async flow
                    events = asyncio.run(execute_research())
                    
                    # Display events in log container
                    with log_container:
                        st.write(f"Processed {len(events)} events.")
                        for event in events:
                            # Check event type and format accordingly
                            event_type = type(event).__name__
                            
                            if event_type == "ModelEvent":
                                st.markdown(f"**🤖 Agent Action:** `{event.agent_name}`")
                                st.text(f"Model: {event.model}")
                                
                            elif event_type == "ToolEvent":
                                st.markdown(f"**🛠️ Tool Call:** `{event.tool_name}`")
                                # Show tool input/output if available (ADK structure varies)
                                st.json(event.tool_args)
                                st.text(f"Output: {str(event.tool_output)[:500]}...") # Truncate long outputs
                                
                            elif hasattr(event, 'agent_name'):
                                st.markdown(f"**➡️ Step:** `{event.agent_name}`")
                                if hasattr(event, 'state_update'):
                                     st.json(event.state_update)
                            else:
                                # Fallback for unknown event types
                                st.code(str(event))

                    # Fetch final state (need another async run or include in execute_research)
                    async def fetch_state():
                         session = await runner.session_service.get_session(
                            app_name="agents", 
                            user_id=user_id, 
                            session_id=session_id
                        )
                         return session.state
                    
                    final_state = asyncio.run(fetch_state())

                    progress_bar.progress(1.0)
                    status_text.success("Research Completed Successfully!")
                    
                except Exception as e:
                    st.error(f"Error during ADK execution: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.stop()

            # Display Results in Tabs
            st.divider()
            st.header("📊 Research Results")
            
            # Extract data from state
            # The keys match what we defined in research_app.py
            draft = final_state.get("draft", "No draft generated.")
            final_report = final_state.get("final_report", "")
            if final_report:
                draft += f"\n\n## Evaluation\n{final_report}"
                
            hypotheses_text = final_state.get("hypotheses", "No hypotheses found.")
            gaps_text = final_state.get("gaps", "No gaps found.")
            kg_data = final_state.get("knowledge_graph", {})
            
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Literature Review", "💡 Hypotheses", "🔍 Gaps", "🕸️ Knowledge Graph"])
            
            with tab1:
                st.markdown(draft)
                
            with tab2:
                st.markdown("### Generated Hypotheses")
                st.markdown(hypotheses_text)
                    
            with tab3:
                st.markdown("### Identified Gaps")
                st.markdown(gaps_text)
                    
            with tab4:
                st.markdown("### Knowledge Graph Data")
                
                import json
                import re
                
                # Handle potential markdown wrapping from LLM
                kg_content = kg_data
                if isinstance(kg_content, str):
                    # Remove markdown code blocks
                    cleaned_json = re.sub(r'```json\s*', '', kg_content)
                    cleaned_json = re.sub(r'```\s*', '', cleaned_json)
                    cleaned_json = cleaned_json.strip()
                    try:
                        kg_display = json.loads(cleaned_json)
                        st.json(kg_display)
                    except json.JSONDecodeError:
                        st.warning("Could not parse JSON. Raw output:")
                        st.text(kg_content)
                else:
                    st.json(kg_content)
                
            # Download Button
            result_text = f"# {topic}\n\n## Review\n{draft}\n\n## Hypotheses\n{hypotheses_text}\n\n## Gaps\n{gaps_text}"
            
            st.download_button(
                label="Download Research Report",
                data=result_text,
                file_name=f"research_report_{topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Failed to initialize or run the research agent: {e}")
            import traceback
            st.code(traceback.format_exc())
