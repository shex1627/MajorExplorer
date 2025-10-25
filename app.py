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
    st.caption("Data source: U.S. Bureau of Labor Statistics (BLS) Occupational Outlook Handbook")

    # Load data
    all_majors_df = load_aggregated_data()

    # Sidebar for major selection
    st.sidebar.header("Customize Your Comparison")

    # Get list of all available majors
    all_majors_list = sorted(MAJOR_TO_OCCUPATIONS.keys())

    # Initialize session state for selected majors if not exists
    if 'selected_majors' not in st.session_state:
        st.session_state.selected_majors = DEFAULT_TOP_MAJORS.copy()

    # Quick action buttons
    st.sidebar.markdown("### Quick Actions")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Reset to Top 15", use_container_width=True):
            st.session_state.selected_majors = DEFAULT_TOP_MAJORS.copy()
            st.rerun()
    with col2:
        if st.button("Select All", use_container_width=True):
            st.session_state.selected_majors = all_majors_list.copy()
            st.rerun()

    st.sidebar.markdown("---")

    # Show currently selected majors
    st.sidebar.markdown("### Currently Selected Majors")
    st.sidebar.caption(f"{len(st.session_state.selected_majors)} majors selected")

    # Display selected majors as removable chips
    if len(st.session_state.selected_majors) > 0:
        # Create columns for remove buttons (2 per row)
        for i in range(0, len(st.session_state.selected_majors), 2):
            cols = st.sidebar.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(st.session_state.selected_majors):
                    major = st.session_state.selected_majors[idx]
                    with col:
                        if st.button(f"✕ {major[:20]}{'...' if len(major) > 20 else ''}",
                                   key=f"remove_{idx}",
                                   use_container_width=True):
                            st.session_state.selected_majors.remove(major)
                            st.rerun()

    # Filter data for selected majors
    selected_majors = st.session_state.selected_majors

    if len(selected_majors) == 0:
        st.warning("⚠️ Please select at least one major to compare.")
        return

    comparison_df = all_majors_df[all_majors_df['Major'].isin(selected_majors)].copy()

    # Main comparison table section
    st.header("📊 Major Comparison")

    # Add new major section at the top of main page
    st.markdown("### Add a Major to Compare")

    # Get available majors
    available_majors = [m for m in all_majors_list if m not in st.session_state.selected_majors]

    add_col1, add_col2, add_col3 = st.columns([3, 1, 6])

    with add_col1:
        if len(available_majors) > 0:
            selected_to_add = st.selectbox(
                "Search and select a major:",
                options=[""] + available_majors,
                index=0,
                help="Type to search for a major (e.g., 'chem' for Chemistry)",
                label_visibility="collapsed"
            )
        else:
            st.info("All majors are already selected!")
            selected_to_add = None

    with add_col2:
        if len(available_majors) > 0 and selected_to_add and selected_to_add != "":
            if st.button("➕ Add", use_container_width=True):
                if selected_to_add not in st.session_state.selected_majors:
                    st.session_state.selected_majors.append(selected_to_add)
                    st.rerun()

    st.markdown("---")

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

    # Create a dataframe for styling (keep numeric values)
    style_df = comparison_df.copy()
    style_df['Salary Range'] = style_df.apply(
        lambda row: f"{format_salary(row['Min Salary'])} - {format_salary(row['Max Salary'])}",
        axis=1
    )
    style_df['Top 3 Careers'] = style_df['Top 3 Careers'].apply(lambda x: ', '.join(x[:3]))

    # Keep numeric columns for gradient styling
    style_df_display = style_df[[
        'Major',
        'Avg Median Salary',
        'Salary Range',
        'Total Job Openings',
        'Avg Growth Rate (%)',
        'Number of Career Paths',
        'Top 3 Careers'
    ]].copy()

    # Apply styling with color gradients
    def style_dataframe(df):
        # Create styler
        styler = df.style

        # Apply gradient to numeric columns
        styler = styler.background_gradient(
            subset=['Avg Median Salary'],
            cmap='Greens',
            vmin=df['Avg Median Salary'].min(),
            vmax=df['Avg Median Salary'].max()
        )

        styler = styler.background_gradient(
            subset=['Total Job Openings'],
            cmap='Blues',
            vmin=df['Total Job Openings'].min(),
            vmax=df['Total Job Openings'].max()
        )

        styler = styler.background_gradient(
            subset=['Avg Growth Rate (%)'],
            cmap='Greens',  # Green gradient for growth rate
            vmin=df['Avg Growth Rate (%)'].min(),
            vmax=df['Avg Growth Rate (%)'].max()
        )

        styler = styler.background_gradient(
            subset=['Number of Career Paths'],
            cmap='Purples',
            vmin=df['Number of Career Paths'].min(),
            vmax=df['Number of Career Paths'].max()
        )

        # Format the numeric columns as text
        styler = styler.format({
            'Avg Median Salary': lambda x: format_salary(x),
            'Total Job Openings': lambda x: format_jobs(x),
            'Avg Growth Rate (%)': lambda x: format_growth(x),
        })

        return styler

    # Display the styled table
    st.dataframe(
        style_dataframe(style_df_display),
        use_container_width=True,
        hide_index=True,
        height=min(600, len(style_df_display) * 35 + 38)
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


if __name__ == "__main__":
    main()
