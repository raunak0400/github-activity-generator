#!/usr/bin/env python3
"""
Natural Progressive GitHub Activity Generator
Simulates realistic human contribution patterns with increasing activity over time
"""

import os
import random
import subprocess
import argparse
from datetime import datetime, timedelta

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
    filename = "contributions.txt"
    
    with open(filename, "a") as f:
        f.write(f"Contribution: {date.strftime('%Y-%m-%d %H:%M')} - Commit #{commit_count}\n")
    
    run_command("git add .")
    commit_message = f"Contribution: {date.strftime('%Y-%m-%d %H:%M')}"
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    run_command(f'git commit --date="{date_str}" -m "{commit_message}"')

def is_break_period(date):
    """Check if the date falls in a break period"""
    year = date.year
    month = date.month
    day = date.day
    
    # 2023: No contributions in March and April
    if year == 2023 and month in [3, 4]:
        return True
    
    # 2024: No contributions in April, May, and last 15 days of December
    if year == 2024:
        if month in [4, 5]:
            return True
        if month == 12 and day >= 16:
            return True
    
    # 2025: No contributions in first and last 15 days of February
    if year == 2025 and month == 2:
        if day <= 15 or day >= 16:
            return True
    
    return False

def calculate_commits_per_day(date, start_date, end_date):
    """Calculate number of commits for a given date based on natural progression"""
    total_days = (end_date - start_date).days
    current_day = (date - start_date).days
    progress = current_day / total_days if total_days > 0 else 0
    
    # Natural progression: very slow start, moderate middle, rapid end
    if progress < 0.3:  # First 30% of time (2023 mostly)
        base_commits = random.randint(0, 2)
    elif progress < 0.7:  # 30-70% of time (2024 mostly)
        base_commits = random.randint(1, 5)
    else:  # Last 30% of time (2025 mostly)
        base_commits = random.randint(3, 12)
    
    # Weekday/weekend patterns
    if date.weekday() < 5:  # Weekdays
        weekday_boost = random.uniform(1.0, 1.5)
        base_commits = int(base_commits * weekday_boost)
    else:  # Weekends
        weekend_reduction = random.uniform(0.3, 0.8)
        base_commits = int(base_commits * weekend_reduction)
    
    # Monthly patterns (more active in middle of month)
    if 5 <= date.day <= 25:
        monthly_boost = random.uniform(1.0, 1.3)
        base_commits = int(base_commits * monthly_boost)
    
    # Natural variation
    variation = random.uniform(0.5, 1.5)
    base_commits = int(base_commits * variation)
    base_commits = max(0, min(15, base_commits))
    
    return base_commits

def generate_natural_contributions(repository_url, start_date_str, end_date_str):
    """Generate natural progressive contributions over the specified period"""
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    print(f"Generating natural progressive contributions from {start_date_str} to {end_date_str}")
    print(f"Repository: {repository_url}")
    print("Break periods:")
    print("- 2023: March and April (no contributions)")
    print("- 2024: April, May, and last 15 days of December (no contributions)")
    print("- 2025: First and last 15 days of February (no contributions)")
    
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
    days_with_commits = 0
    total_days_processed = 0
    
    while current_date <= end_date:
        total_days_processed += 1
        
        # Check if this is a break period
        if is_break_period(current_date):
            print(f"Skipping {current_date.strftime('%Y-%m-%d')} (break period)")
            current_date += timedelta(days=1)
            continue
        
        # Calculate number of commits for this day
        commits_today = calculate_commits_per_day(current_date, start_date, end_date)
        
        if commits_today > 0:
            days_with_commits += 1
            
            # Generate commits for this day
            for i in range(commits_today):
                # Realistic time distribution
                time_choice = random.random()
                if time_choice < 0.6:
                    hour = random.randint(9, 18)  # 9 AM - 6 PM
                elif time_choice < 0.9:
                    hour = random.randint(18, 23)  # 6 PM - 11 PM
                else:
                    hour = random.randint(23, 2)  # 11 PM - 2 AM
                
                minute = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute)
                total_commits += 1
                
                create_commit(commit_time, total_commits)
                print(f"Created commit #{total_commits} for {commit_time.strftime('%Y-%m-%d %H:%M')}")
        
        current_date += timedelta(days=1)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total days processed: {total_days_processed}")
    print(f"Days with contributions: {days_with_commits}")
    print(f"Total commits generated: {total_commits}")
    if days_with_commits > 0:
        print(f"Average commits per active day: {total_commits/days_with_commits:.1f}")
    
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
    
    print("\nNatural progressive contribution generation completed!")

def main():
    parser = argparse.ArgumentParser(description="Generate natural progressive GitHub contributions")
    parser.add_argument("--repository", help="GitHub repository URL")
    parser.add_argument("--start_date", default="2023-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", default="2025-08-30", help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if not args.repository:
        print("Please provide a repository URL")
        print("Usage: python natural_contribute.py --repository=https://github.com/username/repo.git")
        return
    
    generate_natural_contributions(args.repository, args.start_date, args.end_date)

if __name__ == "__main__":
    main()
