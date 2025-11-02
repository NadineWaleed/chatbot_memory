#!/usr/bin/env python3
"""
Modern project entry: Launch via python main.py or uvicorn chatbot.main:app --reload
"""
import sys
import os
from pathlib import Path

def check_env_and_instructions():
    """Check for required files and env, and print next launch steps."""
    root = Path(__file__).parent
    # Check key files/folders
    checks = [
        (root / "combined_markdown.txt").exists(),
        (root / "requirements.txt").exists(),
    ]
    if not all(checks):
        print("Missing core requirements or markdown. Run data/processing step first if needed.")
        sys.exit(1)

    # Warn if API key is not set
    if not os.environ.get("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY not set in environment. The app may not work in production.")
    print("\nUsage: python main.py (Gradio launch) or:")
    print("       uvicorn chatbot.main:app --reload    # For ASGI mode")
    print("\nReview README.md for more!")

if __name__ == "__main__":
    check_env_and_instructions() 