#!/usr/bin/env python3
"""
Cover Letter Creator script for generating tailored cover letters using LLM API.

This script takes user profile information and job requirements,
then uses an LLM API to create a tailored cover letter.
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
    Call LLM API to generate tailored cover letter.
    
    This is a placeholder for the actual API call.
    Replace with your preferred LLM API (OpenAI, Anthropic, etc.)
    """
    # Placeholder for actual API call
    print("Calling LLM API to generate cover letter...")
    
    # TODO: Replace with actual API call
    # Example:
    # import openai
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{
    #         "role": "system",
    #         "content": "You are a professional cover letter writer..."
    #     }, {
    #         "role": "user",
    #         "content": f"Create a cover letter for {profile} applying to {job_description}"
    #     }]
    # )
    # return response.choices[0].message.content
    
    # Mock response for demonstration
    today = datetime.now().strftime("%B %d, %Y")
    cover_letter = f"""
{today}

{job_description.get('company', 'Hiring Manager')}
{job_description.get('location', '')}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_description.get('title', 'position')} role at {job_description.get('company', 'your company')}. 

With my background in {', '.join(job_description.get('requirements', [])[:2])}, I am confident in my ability to contribute effectively to your team.

[Tailored content highlighting relevant experience and skills]

Key qualifications I bring include:
{chr(10).join(f'- {req}' for req in job_description.get('requirements', [])[:3])}

I am excited about the opportunity to bring my expertise to {job_description.get('company', 'your organization')} and would welcome the chance to discuss how I can contribute to your team's success.

Thank you for considering my application. I look forward to the opportunity to discuss this position further.

Sincerely,
{profile.get('name', 'Applicant')}
"""
    
    return cover_letter


def create_cover_letter(profile_path, job_path, output_dir):
    """Create a tailored cover letter for the given job."""
    print("Starting cover letter creation process...")
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
    
    # Generate cover letter using LLM API
    cover_letter_content = call_llm_api(profile, job_description)
    
    # Save cover letter to file
    job_title = job_description.get('title', 'position').replace(' ', '_').lower()
    company = job_description.get('company', 'company').replace(' ', '_').lower()
    output_file = output_path / f"cover_letter_{company}_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(output_file, 'w') as f:
        f.write(cover_letter_content)
    
    print(f"Cover letter created successfully")
    print(f"Output saved to: {output_file}")
    
    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python cover_letter_creator.py <profile.json> <job.json> [output_dir]")
        print("\nExample:")
        print("  python cover_letter_creator.py profile.json job_description.json ./output")
        return 1
    
    profile_path = sys.argv[1]
    job_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./output"
    
    try:
        success = create_cover_letter(profile_path, job_path, output_dir)
        if success:
            print("\nCover letter creation completed successfully")
            return 0
        else:
            print("\nCover letter creation failed")
            return 1
    except Exception as e:
        print(f"Error during cover letter creation: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
