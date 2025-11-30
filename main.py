import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scientific_research_system.agents.main_adk import main

if __name__ == "__main__":
    asyncio.run(main())
