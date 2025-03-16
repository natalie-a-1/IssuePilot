#!/usr/bin/env python3
"""
GitHub Issues Generator

This script uses OpenAI to generate GitHub issues based on a project description,
and then creates those issues in a specified GitHub repository.
"""

import requests
import json
import time
import sys
import os
import openai
from typing import Dict, List, Any, Optional

def validate_config(config: Dict[str, str]) -> bool:
    """Validate the configuration settings."""
    required_fields = ['githubToken', 'openaiApiKey', 'username', 'repo', 'projectDescription']
    
    for field in required_fields:
        if not config.get(field):
            print(f"Error: Missing required field '{field}' in configuration.")
            return False
    
    return True

def test_api_connection(config: Dict[str, str]) -> bool:
    """Test the connection to the GitHub API."""
    github_url = f"https://api.github.com/repos/{config['username']}/{config['repo']}"
    headers = {
        "Authorization": f"token {config['githubToken']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(github_url, headers=headers)
        
        if response.status_code == 200:
            print(f"Successfully connected to repository: {config['username']}/{config['repo']}")
            return True
        else:
            print(f"Failed to connect to repository: {response.status_code}")
            print(response.json())
            return False
    except Exception as e:
        print(f"Error connecting to GitHub API: {str(e)}")
        return False

def generate_issues_with_ai(config: Dict[str, str]) -> List[Dict[str, Any]]:
    """Generate GitHub issues using OpenAI based on the project description."""
    openai.api_key = config['openaiApiKey']
    
    print("Generating issues with AI based on project description...")
    
    # Prepare the prompt for OpenAI
    prompt = f"""
You are an expert project manager who specializes in creating GitHub issues for software projects.
Based on the following project description, generate 5-10 well-structured GitHub issues.

Project Description: {config['projectDescription']}

For each issue, include:
1. A clear, concise title
2. A detailed description that explains what needs to be done
3. 2-3 relevant labels (like "feature", "bug", "enhancement", "documentation", etc.)

Format the response as a JSON array of objects, where each object has the following structure:
{{
  "title": "Issue title",
  "body": "Detailed description",
  "labels": ["label1", "label2"]
}}

Only provide the JSON array, with no additional text.
"""

    try:
        # Call OpenAI API to generate issues
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates GitHub issues for software projects."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract and parse the response
        content = response.choices[0].message.content.strip()
        
        # Find the start and end of the JSON array if there's additional text
        content = content.replace("```json", "").replace("```", "").strip()
        
        issues = json.loads(content)
        print(f"Successfully generated {len(issues)} issues")
        return issues
    
    except Exception as e:
        print(f"Error generating issues with AI: {str(e)}")
        return []

def create_labels_if_needed(config: Dict[str, str], labels: List[str]) -> None:
    """Create any labels that don't already exist in the repository."""
    github_url = f"https://api.github.com/repos/{config['username']}/{config['repo']}/labels"
    headers = {
        "Authorization": f"token {config['githubToken']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Get existing labels
        response = requests.get(github_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch existing labels: {response.status_code}")
            print(response.json())
            return
        
        existing_labels = {label["name"] for label in response.json()}
        
        # Create labels that don't exist
        for label in labels:
            if label not in existing_labels:
                label_data = {
                    "name": label,
                    "color": generate_label_color(label)
                }
                
                create_response = requests.post(github_url, headers=headers, json=label_data)
                
                if create_response.status_code == 201:
                    print(f"Created new label: {label}")
                else:
                    print(f"Failed to create label {label}: {create_response.status_code}")
                    if create_response.status_code != 422:  # Skip "already exists" errors
                        print(create_response.json())
    
    except Exception as e:
        print(f"Error creating labels: {str(e)}")

def generate_label_color(label: str) -> str:
    """Generate a consistent color based on the label text."""
    # Simple hash function to generate a color
    hash_value = sum(ord(c) for c in label)
    # Use the hash to generate a hue (0-360)
    hue = hash_value % 360
    
    # Convert HSL to RGB
    import colorsys
    rgb = colorsys.hls_to_rgb(hue/360, 0.6, 0.8)
    return '%02x%02x%02x' % tuple(int(c*255) for c in rgb)

def create_issues(config: Dict[str, str], issues: List[Dict[str, Any]]) -> None:
    """Create the generated issues in the GitHub repository."""
    # GitHub API settings
    github_url = f"https://api.github.com/repos/{config['username']}/{config['repo']}/issues"
    headers = {
        "Authorization": f"token {config['githubToken']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Collect unique labels from all issues
    all_labels = set()
    for issue in issues:
        all_labels.update(issue.get("labels", []))
    
    # Create any missing labels
    create_labels_if_needed(config, all_labels)
    
    # Create each issue
    for i, issue in enumerate(issues, 1):
        print(f"Creating issue {i}/{len(issues)}: {issue['title']}...", end=" ")
        
        try:
            response = requests.post(github_url, headers=headers, json=issue)
            
            if response.status_code == 201:
                print("Success!")
                issue_number = response.json()["number"]
                print(f"  - Issue #{issue_number} created: {response.json()['html_url']}")
            else:
                print(f"Failed: {response.status_code}")
                print(f"  - Error: {response.json().get('message', 'Unknown error')}")
        
        except Exception as e:
            print(f"Exception: {str(e)}")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)

def main() -> int:
    """Main function to run the script."""
    print("GitHub Issues Generator")
    print("=======================")
    
    if len(sys.argv) != 2:
        print("Usage: python issue_generator.py <config_file_path>")
        return 1
    
    config_file_path = sys.argv[1]
    
    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading configuration file: {str(e)}")
        return 1
    
    if not validate_config(config):
        return 1
    
    print("\nTesting API connection...")
    if not test_api_connection(config):
        return 1
    
    # Generate issues with AI
    issues = generate_issues_with_ai(config)
    
    if not issues:
        print("Failed to generate issues. Exiting.")
        return 1
    
    print("\nReady to create the following issues:")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['title']}")
        
    print("\nCreating issues...")
    create_issues(config, issues)
    
    print("\nProcess completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 