#!/usr/bin/env python3
"""
Progressive GitHub Activity Generator
Generates contributions with increasing frequency over time
"""

import os
import random
import subprocess
import argparse
from datetime import datetime, timedelta
import math

def run_command(command):
    """Run a shell command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return None

def create_commit(date, commit_count):
    """Create a commit for a specific date"""
    # Create or modify a file
    filename = "contributions.txt"
    
    # Add content to the file
    with open(filename, "a") as f:
        f.write(f"Contribution: {date.strftime('%Y-%m-%d %H:%M')} - Commit #{commit_count}\n")
    
    # Stage the file
    run_command("git add .")
    
    # Create commit with the specific date
    commit_message = f"Contribution: {date.strftime('%Y-%m-%d %H:%M')}"
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    
    run_command(f'git commit --date="{date_str}" -m "{commit_message}"')

def calculate_commits_per_day(date, start_date, end_date):
    """Calculate number of commits for a given date based on progression"""
    total_days = (end_date - start_date).days
    current_day = (date - start_date).days
    
    # Calculate progress (0 to 1)
    progress = current_day / total_days if total_days > 0 else 0
    
    # Use exponential growth: start with 1-3 commits, end with 8-15 commits
    min_commits = 1
    max_commits = 15
    
    # Exponential growth function
    commits = min_commits + (max_commits - min_commits) * (progress ** 1.5)
    
    # Add some randomness
    variation = random.uniform(0.7, 1.3)
    commits = int(commits * variation)
    
    # Ensure minimum and maximum bounds
    commits = max(1, min(20, commits))
    
    return commits

def generate_progressive_contributions(repository_url, start_date_str, end_date_str):
    """Generate progressive contributions over the specified period"""
    
    # Parse dates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    print(f"Generating progressive contributions from {start_date_str} to {end_date_str}")
    print(f"Repository: {repository_url}")
    
    # Initialize git repository
    if not os.path.exists(".git"):
        run_command("git init")
        print("Initialized git repository")
    
    # Create initial file
    with open("contributions.txt", "w") as f:
        f.write("GitHub Activity Contributions\n")
        f.write("=" * 30 + "\n\n")
    
    run_command("git add .")
    run_command('git commit -m "Initial commit"')
    
    # Generate contributions
    current_date = start_date
    total_commits = 0
    
    while current_date <= end_date:
        # Skip weekends if desired (uncomment the next line to skip weekends)
        # if current_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        #     current_date += timedelta(days=1)
        #     continue
        
        # Calculate number of commits for this day
        commits_today = calculate_commits_per_day(current_date, start_date, end_date)
        
        # Generate commits for this day
        for i in range(commits_today):
            # Random time between 9 AM and 11 PM
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            
            commit_time = current_date.replace(hour=hour, minute=minute)
            total_commits += 1
            
            create_commit(commit_time, total_commits)
            
            print(f"Created commit #{total_commits} for {commit_time.strftime('%Y-%m-%d %H:%M')}")
        
        current_date += timedelta(days=1)
    
    print(f"\nGenerated {total_commits} total commits")
    
    # Set up remote repository
    if repository_url:
        run_command(f"git remote add origin {repository_url}")
        print(f"Added remote origin: {repository_url}")
        
        # Push to repository
        print("Pushing to repository...")
        result = run_command("git push -u origin main")
        if result:
            print("Successfully pushed to repository!")
        else:
            print("Failed to push. You may need to force push with: git push --force origin main")
    
    print("\nProgressive contribution generation completed!")

def main():
    parser = argparse.ArgumentParser(description="Generate progressive GitHub contributions")
    parser.add_argument("--repository", help="GitHub repository URL")
    parser.add_argument("--start_date", default="2023-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", default="2025-08-30", help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if not args.repository:
        print("Please provide a repository URL")
        print("Usage: python progressive_contribute.py --repository=https://github.com/username/repo.git")
        return
    
    generate_progressive_contributions(args.repository, args.start_date, args.end_date)

if __name__ == "__main__":
    main()
