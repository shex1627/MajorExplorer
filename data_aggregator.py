"""
Aggregates BLS occupation data by college major.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple
from major_occupation_mapping import MAJOR_TO_OCCUPATIONS


def parse_salary(salary_str: str) -> float:
    """Convert salary string like '$131,450' to float."""
    if pd.isna(salary_str) or salary_str == '':
        return 0.0
    # Remove $ and commas
    cleaned = re.sub(r'[$,]', '', str(salary_str))
    try:
        return float(cleaned)
    except:
        return 0.0


def parse_job_outlook(outlook_str: str) -> float:
    """Extract percentage from job outlook string like '15% (Much faster than average)'."""
    if pd.isna(outlook_str) or outlook_str == '':
        return 0.0
    # Extract the percentage number
    match = re.search(r'(-?\d+)%', str(outlook_str))
    if match:
        return float(match.group(1))
    return 0.0


def parse_job_count(job_count_str) -> int:
    """Convert job count to integer."""
    if pd.isna(job_count_str) or job_count_str == '':
        return 0
    try:
        return int(job_count_str)
    except:
        return 0


def aggregate_major_data(bls_csv_path: str) -> pd.DataFrame:
    """
    Aggregate BLS occupation data by major.

    Returns a DataFrame with columns:
    - Major
    - Avg Median Salary
    - Min Salary
    - Max Salary
    - Total Job Openings
    - Avg Growth Rate (%)
    - Number of Career Paths
    - Top Careers (list of top 3 by job count)
    """
    # Load BLS data
    bls_df = pd.read_csv(bls_csv_path)

    # Parse numeric columns
    bls_df['salary_numeric'] = bls_df['median_pay_annual'].apply(parse_salary)
    bls_df['growth_rate'] = bls_df['job_outlook'].apply(parse_job_outlook)
    bls_df['job_count'] = bls_df['number_of_jobs'].apply(parse_job_count)

    # Aggregate data for each major
    aggregated_data = []

    for major, occupation_names in MAJOR_TO_OCCUPATIONS.items():
        # Filter BLS data for this major's occupations
        major_occupations = bls_df[bls_df['occupation_name'].isin(occupation_names)].copy()

        if len(major_occupations) == 0:
            # No matching occupations found
            continue

        # Calculate statistics
        avg_salary = major_occupations['salary_numeric'].mean()
        min_salary = major_occupations['salary_numeric'].min()
        max_salary = major_occupations['salary_numeric'].max()
        total_jobs = major_occupations['job_count'].sum()

        # Weighted average growth rate (weighted by number of jobs)
        total_weighted_growth = (major_occupations['growth_rate'] * major_occupations['job_count']).sum()
        weighted_avg_growth = total_weighted_growth / total_jobs if total_jobs > 0 else 0

        num_career_paths = len(major_occupations)

        # Get top 3 careers by job count
        top_careers = major_occupations.nlargest(3, 'job_count')['occupation_name'].tolist()

        aggregated_data.append({
            'Major': major,
            'Avg Median Salary': avg_salary,
            'Min Salary': min_salary,
            'Max Salary': max_salary,
            'Total Job Openings': total_jobs,
            'Avg Growth Rate (%)': weighted_avg_growth,
            'Number of Career Paths': num_career_paths,
            'Top 3 Careers': top_careers,
        })

    return pd.DataFrame(aggregated_data)


def get_major_details(major: str, bls_csv_path: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Get detailed information for a specific major.

    Returns:
    - DataFrame of all occupations for this major
    - Dictionary with aggregated statistics
    """
    # Load BLS data
    bls_df = pd.read_csv(bls_csv_path)

    # Parse numeric columns
    bls_df['salary_numeric'] = bls_df['median_pay_annual'].apply(parse_salary)
    bls_df['growth_rate'] = bls_df['job_outlook'].apply(parse_job_outlook)
    bls_df['job_count'] = bls_df['number_of_jobs'].apply(parse_job_count)

    # Get occupations for this major
    occupation_names = MAJOR_TO_OCCUPATIONS.get(major, [])
    major_occupations = bls_df[bls_df['occupation_name'].isin(occupation_names)].copy()

    if len(major_occupations) == 0:
        return pd.DataFrame(), {}

    # Calculate aggregate stats
    stats = {
        'avg_salary': major_occupations['salary_numeric'].mean(),
        'min_salary': major_occupations['salary_numeric'].min(),
        'max_salary': major_occupations['salary_numeric'].max(),
        'total_jobs': major_occupations['job_count'].sum(),
        'weighted_avg_growth': (major_occupations['growth_rate'] * major_occupations['job_count']).sum() / major_occupations['job_count'].sum() if major_occupations['job_count'].sum() > 0 else 0,
        'num_careers': len(major_occupations),
    }

    # Sort by job count first, then select relevant columns for display
    major_occupations_sorted = major_occupations.sort_values('job_count', ascending=False)
    display_df = major_occupations_sorted[[
        'occupation_name',
        'median_pay_annual',
        'number_of_jobs',
        'job_outlook',
        'entry_level_education',
        'what_they_do'
    ]]

    return display_df, stats


if __name__ == "__main__":
    # Test the aggregation
    bls_path = '/Users/shadowclone/Desktop/Code/warcraftlogs/warcraftlogs/ai_code/bls_occupations_all.csv'

    print("Aggregating major data...")
    aggregated = aggregate_major_data(bls_path)

    print(f"\nAggregated data for {len(aggregated)} majors")
    print("\nTop 5 majors by average salary:")
    print(aggregated.nlargest(5, 'Avg Median Salary')[['Major', 'Avg Median Salary', 'Total Job Openings']])

    print("\nTop 5 majors by total job openings:")
    print(aggregated.nlargest(5, 'Total Job Openings')[['Major', 'Total Job Openings', 'Avg Median Salary']])
