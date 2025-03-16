#!/usr/bin/env python3
"""
GitHub Issues Creator for PodcastGenerator

This script creates all the necessary GitHub issues for the PodcastGenerator project.
To use this script:
1. Generate a GitHub Personal Access Token with 'repo' scope
2. Set your GitHub username, repository name, and token below
3. Run the script

Requirements: requests library (pip install requests)
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any, Optional

# ======== CONFIGURATION ========
# Replace these values with your own
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # Personal Access Token with 'repo' scope
GITHUB_USERNAME = "natalie-a-1"  # Your GitHub username
GITHUB_REPO = "PodcastGenerator"  # Your repository name
# ===============================

# API settings
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/issues"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Issue definitions
ISSUES = [
    # Core Functionality
    {
        "title": "Implement Basic Summarization Module",
        "body": "Create the Research Analyzer component using facebook/bart-large-cnn model to generate concise summaries of research articles. Focus on handling different article lengths and proper text chunking.",
        "labels": ["core-functionality", "ai", "summarization"]
    },
    {
        "title": "Develop Script Generation System",
        "body": "Build the Script Composer component using GPT-4 to convert article summaries into engaging dialogue between two hosts (Alex and Sam). Include proper prompt engineering for natural conversation flow.",
        "labels": ["core-functionality", "ai", "script-generation"]
    },
    {
        "title": "Create Fact Verification Engine",
        "body": "Implement the Fact-Checker component using sentence-transformers/roberta-large-nli-stsb-mean-tokens to verify all script content against the original article, ensuring accuracy and preventing fabrication.",
        "labels": ["core-functionality", "ai", "fact-checking"]
    },
    {
        "title": "Build Audio Generation Pipeline",
        "body": "Develop the Audio Producer component to convert scripts into 5-minute MP3 files with distinct voices using either gTTS or AWS Polly. Include speaker differentiation and timing control.",
        "labels": ["core-functionality", "audio", "text-to-speech"]
    },
    {
        "title": "Design Main Module Interface",
        "body": "Create a clean, intuitive interface for the main module that orchestrates the four components and provides a simple API for integration into larger projects.",
        "labels": ["core-functionality", "api-design", "integration"]
    },
    
    # Improvements & Optimization
    {
        "title": "Optimize Memory Usage",
        "body": "Analyze and improve memory efficiency across all components, particularly for handling large research articles with limited resources.",
        "labels": ["optimization", "performance", "resource-efficiency"]
    },
    {
        "title": "Enhance Voice Quality and Naturalness",
        "body": "Improve the quality of generated voices by fine-tuning TTS parameters and implementing better speaker transitions for more natural conversation flow.",
        "labels": ["enhancement", "audio-quality", "user-experience"]
    },
    {
        "title": "Refine Fact-Checking Accuracy",
        "body": "Improve the accuracy of the fact-checking component by tuning similarity thresholds and implementing better text chunking strategies for comparison.",
        "labels": ["enhancement", "accuracy", "fact-checking"]
    },
    {
        "title": "Streamline API for Integration",
        "body": "Simplify the integration process by creating helper functions, clear documentation, and standardized input/output formats for the module.",
        "labels": ["enhancement", "api-design", "integration"]
    },
    
    # Testing & Documentation
    {
        "title": "Create Comprehensive Test Suite",
        "body": "Develop tests for each component and the integrated system, including unit tests and integration tests with sample articles of varying lengths and complexities.",
        "labels": ["testing", "quality", "reliability"]
    },
    {
        "title": "Write Clear API Documentation",
        "body": "Create detailed documentation for all module functions, including examples, parameter descriptions, and integration guidelines for developers.",
        "labels": ["documentation", "developer-experience"]
    },
    {
        "title": "Add Usage Examples",
        "body": "Provide practical examples of using the module with different types of research articles and configuration options.",
        "labels": ["documentation", "examples", "user-experience"]
    },
    
    # Configuration & Deployment
    {
        "title": "Implement Environment Configuration",
        "body": "Create a flexible configuration system to manage API keys, model selection, and output parameters through environment variables or config files.",
        "labels": ["configuration", "security", "deployment"]
    },
    {
        "title": "Add Error Handling and Logging",
        "body": "Implement robust error handling throughout the module with informative error messages and appropriate logging for troubleshooting.",
        "labels": ["reliability", "error-handling", "developer-experience"]
    },
    {
        "title": "Create Package Installation Script",
        "body": "Develop a proper setup.py and requirements specification to ensure easy installation and dependency management.",
        "labels": ["packaging", "deployment", "developer-experience"]
    }
]

def create_labels_if_needed(labels: List[str]) -> None:
    """Create any labels that don't already exist in the repository."""
    existing_labels_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/labels"
    response = requests.get(existing_labels_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to fetch existing labels: {response.status_code}")
        print(response.json())
        return
    
    existing_labels = {label["name"] for label in response.json()}
    
    # Collect unique labels from all issues
    all_labels = set()
    for issue in ISSUES:
        all_labels.update(issue["labels"])
    
    # Create labels that don't exist
    for label in all_labels:
        if label not in existing_labels:
            label_data = {
                "name": label,
                "color": generate_label_color(label)
            }
            create_label_response = requests.post(
                existing_labels_url, 
                headers=HEADERS, 
                json=label_data
            )
            
            if create_label_response.status_code == 201:
                print(f"Created new label: {label}")
            else:
                print(f"Failed to create label {label}: {create_label_response.status_code}")
                print(create_label_response.json())

def generate_label_color(label: str) -> str:
    """Generate a consistent color based on the label text."""
    # Simple hash function to generate a color
    hash_value = sum(ord(c) for c in label)
    # Use the hash to generate a hue (0-360)
    hue = hash_value % 360
    
    # Convert HSL to RGB (simplified version)
    # Using a fixed saturation and lightness for good readability
    # Returns a hex color code
    import colorsys
    rgb = colorsys.hls_to_rgb(hue/360, 0.6, 0.8)
    return '%02x%02x%02x' % tuple(int(c*255) for c in rgb)

def validate_config() -> bool:
    """Validate the configuration settings."""
    if GITHUB_TOKEN == "your_github_token_here":
        print("Error: Please set your GitHub token in the script.")
        return False
    
    if GITHUB_USERNAME == "your_github_username":
        print("Error: Please set your GitHub username in the script.")
        return False
    
    return True

def test_api_connection() -> bool:
    """Test the connection to the GitHub API."""
    test_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}"
    response = requests.get(test_url, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"Successfully connected to repository: {GITHUB_USERNAME}/{GITHUB_REPO}")
        return True
    else:
        print(f"Failed to connect to repository: {response.status_code}")
        print(response.json())
        return False

def create_issues() -> None:
    """Create all the defined issues in the GitHub repository."""
    # First, create any missing labels
    create_labels_if_needed([label for issue in ISSUES for label in issue["labels"]])
    
    # Create each issue
    for i, issue in enumerate(ISSUES, 1):
        print(f"Creating issue {i}/{len(ISSUES)}: {issue['title']}...", end=" ")
        
        try:
            response = requests.post(API_URL, headers=HEADERS, json=issue)
            
            if response.status_code == 201:
                print("Success!")
                # Get the issue number from the response
                issue_number = response.json()["number"]
                print(f"  - Issue #{issue_number} created: {response.json()['html_url']}")
            else:
                print(f"Failed: {response.status_code}")
                print(f"  - Error: {response.json().get('message', 'Unknown error')}")
        
        except Exception as e:
            print(f"Exception: {e}")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)

def main() -> int:
    """Main function to run the script."""
    print("GitHub Issues Creator for PodcastGenerator")
    print("=========================================")
    
    if not validate_config():
        return 1
    
    print("\nTesting API connection...")
    if not test_api_connection():
        return 1
    
    print("\nReady to create the following issues:")
    for i, issue in enumerate(ISSUES, 1):
        print(f"{i}. {issue['title']}")
    
    confirmation = input("\nDo you want to proceed with creating these issues? (y/n): ")
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        return 0
    
    print("\nCreating issues...")
    create_issues()
    
    print("\nProcess completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())