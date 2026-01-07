#!/usr/bin/env python3
"""
CV Creator script for generating tailored CVs using LLM API.

This script takes user profile information and job requirements,
then uses an LLM API to create a tailored CV.
"""

import sys
import json
from datetime import datetime
from pathlib import Path


def load_user_profile(profile_path):
    """Load user profile from JSON file."""
    try:
        with open(profile_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Profile file not found: {profile_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing profile JSON: {e}", file=sys.stderr)
        return None


def load_job_description(job_path):
    """Load job description from JSON file."""
    try:
        with open(job_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Job description file not found: {job_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing job JSON: {e}", file=sys.stderr)
        return None


def call_llm_api(profile, job_description):
    """
    Call LLM API to generate tailored CV.
    
    This is a placeholder for the actual API call.
    Replace with your preferred LLM API (OpenAI, Anthropic, etc.)
    """
    # Placeholder for actual API call
    print("Calling LLM API to generate CV...")
    
    # TODO: Replace with actual API call
    # Example:
    # import openai
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{
    #         "role": "system",
    #         "content": "You are a professional CV writer..."
    #     }, {
    #         "role": "user",
    #         "content": f"Create a CV for {profile} targeting {job_description}"
    #     }]
    # )
    # return response.choices[0].message.content
    
    # Mock response for demonstration
    cv_content = f"""
# {profile.get('name', 'Professional')}

## Professional Summary
Experienced professional with expertise in {', '.join(job_description.get('requirements', [])[:3])}.

## Skills
{', '.join(job_description.get('requirements', []))}

## Experience
[Tailored experience based on job requirements]

## Education
[Education details]

Generated for: {job_description.get('title', 'Position')} at {job_description.get('company', 'Company')}
"""
    
    return cv_content


def create_cv(profile_path, job_path, output_dir):
    """Create a tailored CV for the given job."""
    print("Starting CV creation process...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Load user profile and job description
    profile = load_user_profile(profile_path)
    if not profile:
        return False
    
    job_description = load_job_description(job_path)
    if not job_description:
        return False
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate CV using LLM API
    cv_content = call_llm_api(profile, job_description)
    
    # Save CV to file
    job_title = job_description.get('title', 'position').replace(' ', '_').lower()
    company = job_description.get('company', 'company').replace(' ', '_').lower()
    output_file = output_path / f"cv_{company}_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_file, 'w') as f:
        f.write(cv_content)
    
    print(f"CV created successfully: {output_file}")
    
    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python cv_creator.py <profile.json> <job.json> [output_dir]")
        print("\nExample:")
        print("  python cv_creator.py profile.json job_description.json ./output")
        return 1
    
    profile_path = sys.argv[1]
    job_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./output"
    
    try:
        success = create_cv(profile_path, job_path, output_dir)
        if success:
            print("\nCV creation completed successfully")
            return 0
        else:
            print("\nCV creation failed")
            return 1
    except Exception as e:
        print(f"Error during CV creation: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
