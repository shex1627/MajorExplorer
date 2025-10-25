"""
Major & Career Explorer - Streamlit App
Help high school students explore college majors and career options
"""

import streamlit as st
import pandas as pd
from data_aggregator import aggregate_major_data, get_major_details
from major_occupation_mapping import MAJOR_TO_OCCUPATIONS, DEFAULT_TOP_MAJORS

# Page config
st.set_page_config(
    page_title="Major & Career Explorer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
BLS_DATA_PATH = '/Users/shadowclone/Desktop/Code/warcraftlogs/warcraftlogs/ai_code/bls_occupations_all.csv'


def format_salary(salary):
    """Format salary as currency."""
    return f"${salary:,.0f}"


def format_jobs(jobs):
    """Format job count with K/M suffix."""
    if jobs >= 1_000_000:
        return f"{jobs/1_000_000:.1f}M"
    elif jobs >= 1_000:
        return f"{jobs/1_000:.0f}K"
    return f"{jobs:,.0f}"


def format_growth(growth):
    """Format growth rate as percentage."""
    return f"{growth:+.1f}%"


@st.cache_data
def load_aggregated_data():
    """Load and cache aggregated major data."""
    return aggregate_major_data(BLS_DATA_PATH)


def main():
    # Header
    st.title("🎓 Major & Career Explorer")
    st.markdown("""
    Explore different college majors and their career paths. Compare salary, job openings,
    and growth outlook to make informed decisions about your future.
    """)

    # Load data
    all_majors_df = load_aggregated_data()

    # Sidebar for major selection
    st.sidebar.header("Customize Your Comparison")

    # Get list of all available majors
    all_majors_list = sorted(MAJOR_TO_OCCUPATIONS.keys())

    # Initialize session state for selected majors if not exists
    if 'selected_majors' not in st.session_state:
        st.session_state.selected_majors = DEFAULT_TOP_MAJORS.copy()

    # Multiselect for adding/removing majors
    selected_majors = st.sidebar.multiselect(
        "Select majors to compare:",
        options=all_majors_list,
        default=st.session_state.selected_majors,
        help="Add or remove majors from the comparison table"
    )

    # Update session state
    st.session_state.selected_majors = selected_majors

    # Quick action buttons
    st.sidebar.markdown("### Quick Actions")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Reset to Top 15"):
            st.session_state.selected_majors = DEFAULT_TOP_MAJORS.copy()
            st.rerun()
    with col2:
        if st.button("Select All"):
            st.session_state.selected_majors = all_majors_list
            st.rerun()

    # Filter data for selected majors
    if len(selected_majors) == 0:
        st.warning("⚠️ Please select at least one major to compare.")
        return

    comparison_df = all_majors_df[all_majors_df['Major'].isin(selected_majors)].copy()

    # Main comparison table section
    st.header("📊 Major Comparison")

    # Sorting options
    sort_col1, sort_col2, sort_col3 = st.columns([2, 2, 6])
    with sort_col1:
        sort_by = st.selectbox(
            "Sort by:",
            options=['Major', 'Avg Median Salary', 'Total Job Openings', 'Avg Growth Rate (%)', 'Number of Career Paths'],
            index=1  # Default to salary
        )
    with sort_col2:
        sort_order = st.selectbox(
            "Order:",
            options=['Descending', 'Ascending'],
            index=0
        )

    # Sort the dataframe
    ascending = (sort_order == 'Ascending')
    comparison_df = comparison_df.sort_values(sort_by, ascending=ascending)

    # Format the display dataframe
    display_df = comparison_df.copy()
    display_df['Avg Median Salary'] = display_df['Avg Median Salary'].apply(format_salary)
    display_df['Salary Range'] = display_df.apply(
        lambda row: f"{format_salary(row['Min Salary'])} - {format_salary(row['Max Salary'])}",
        axis=1
    )
    display_df['Total Job Openings'] = display_df['Total Job Openings'].apply(format_jobs)
    display_df['Avg Growth Rate (%)'] = display_df['Avg Growth Rate (%)'].apply(format_growth)
    display_df['Top 3 Careers'] = display_df['Top 3 Careers'].apply(lambda x: ', '.join(x[:3]))

    # Select columns to display
    final_display_df = display_df[[
        'Major',
        'Avg Median Salary',
        'Salary Range',
        'Total Job Openings',
        'Avg Growth Rate (%)',
        'Number of Career Paths',
        'Top 3 Careers'
    ]]

    # Display the table
    st.dataframe(
        final_display_df,
        use_container_width=True,
        hide_index=True,
        height=min(600, len(final_display_df) * 35 + 38)
    )

    # Statistics cards
    st.markdown("---")
    st.subheader("📈 Key Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        highest_salary_major = comparison_df.loc[comparison_df['Avg Median Salary'].idxmax()]
        st.metric(
            "Highest Avg Salary",
            highest_salary_major['Major'],
            format_salary(highest_salary_major['Avg Median Salary'])
        )

    with col2:
        most_jobs_major = comparison_df.loc[comparison_df['Total Job Openings'].idxmax()]
        st.metric(
            "Most Job Openings",
            most_jobs_major['Major'],
            format_jobs(most_jobs_major['Total Job Openings'])
        )

    with col3:
        fastest_growth_major = comparison_df.loc[comparison_df['Avg Growth Rate (%)'].idxmax()]
        st.metric(
            "Fastest Growth",
            fastest_growth_major['Major'],
            format_growth(fastest_growth_major['Avg Growth Rate (%)'])
        )

    with col4:
        most_paths_major = comparison_df.loc[comparison_df['Number of Career Paths'].idxmax()]
        st.metric(
            "Most Career Paths",
            most_paths_major['Major'],
            f"{most_paths_major['Number of Career Paths']} careers"
        )

    # Detailed view section
    st.markdown("---")
    st.header("🔍 Explore Career Details")

    selected_major_detail = st.selectbox(
        "Select a major to see detailed career information:",
        options=selected_majors,
        index=0 if len(selected_majors) > 0 else None
    )

    if selected_major_detail:
        careers_df, stats = get_major_details(selected_major_detail, BLS_DATA_PATH)

        if not careers_df.empty:
            # Display stats for selected major
            st.subheader(f"Career Paths for {selected_major_detail}")

            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Average Salary", format_salary(stats['avg_salary']))
                st.caption(f"Range: {format_salary(stats['min_salary'])} - {format_salary(stats['max_salary'])}")
            with stat_col2:
                st.metric("Total Job Openings", format_jobs(stats['total_jobs']))
            with stat_col3:
                st.metric("Average Growth Rate", format_growth(stats['weighted_avg_growth']))

            st.markdown("### All Career Options")

            # Display careers with expandable details
            for idx, row in careers_df.iterrows():
                with st.expander(f"**{row['occupation_name']}** - {row['median_pay_annual']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Median Annual Salary:** {row['median_pay_annual']}")
                        st.write(f"**Number of Jobs:** {format_jobs(row['number_of_jobs'])}")
                    with col_b:
                        st.write(f"**Job Outlook:** {row['job_outlook']}")
                        st.write(f"**Entry Level Education:** {row['entry_level_education']}")

                    st.write("**What they do:**")
                    st.write(row['what_they_do'][:500] + "..." if len(str(row['what_they_do'])) > 500 else row['what_they_do'])

    # Footer
    st.markdown("---")
    st.caption("Data source: U.S. Bureau of Labor Statistics (BLS) Occupational Outlook Handbook")


if __name__ == "__main__":
    main()
