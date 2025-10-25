# 🎓 Major & Career Explorer

A Streamlit web application designed to help high school students explore different college majors and their associated career paths. The app provides comprehensive comparisons of salary, job openings, growth outlook, and career options based on real data from the U.S. Bureau of Labor Statistics (BLS).

## Features

### 📊 Major Comparison Table
- Compare 10-15 popular majors side-by-side
- View key metrics:
  - Average median salary
  - Salary range (min-max)
  - Total job openings
  - Average growth rate
  - Number of career paths
  - Top 3 career options

### 🔍 Interactive Filtering & Sorting
- Add or remove majors from the comparison
- Sort by any metric (salary, jobs, growth rate, etc.)
- Quick actions: Reset to top 15 or select all majors

### 📈 Key Statistics Dashboard
- Highest paying major
- Major with most job openings
- Fastest growing major
- Major with most career diversity

### 🔎 Detailed Career Information
- Explore all career paths for each major
- View occupation-specific details:
  - Salary information
  - Job outlook and growth
  - Entry-level education requirements
  - Job descriptions

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure BLS data is available:**
   - The app expects BLS occupation data at: `/Users/shadowclone/Desktop/Code/warcraftlogs/warcraftlogs/ai_code/bls_occupations_all.csv`
   - Update the `BLS_DATA_PATH` in `app.py` if your data is located elsewhere

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`

3. **Explore majors:**
   - Use the sidebar to select majors to compare
   - Sort the table by different metrics
   - Click on a major in the detailed view to see all career paths

## Project Structure

```
major_career_explorer/
├── app.py                          # Main Streamlit application
├── data_aggregator.py              # Data aggregation logic
├── major_occupation_mapping.py     # Mapping of majors to BLS occupations
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Files

### `major_occupation_mapping.py`
Contains the mapping of 36+ college majors to relevant BLS occupations. Each major can map to multiple occupations, and occupations can appear in multiple majors (e.g., "Data scientists" appears in Computer Science, Mathematics, Statistics, etc.).

**Majors included:**
- STEM: Computer Science, Engineering (Mechanical, Electrical, Civil, Chemical, Biomedical, Environmental), Biology, Chemistry, Physics, Mathematics, Statistics, Data Science
- Business: Business Administration, Finance, Accounting, Marketing, Economics
- Health: Nursing, Pre-Medicine, Public Health, Pharmacy, Physical Therapy
- Social Sciences: Psychology, Political Science, Sociology, History
- Humanities: Communications, English/Literature
- Other: Education, Criminal Justice, Environmental Science, Graphic Design, Performing Arts

### `data_aggregator.py`
Provides functions to:
- Parse BLS salary, job outlook, and employment data
- Aggregate statistics by major
- Generate comparison tables
- Retrieve detailed career information

## Data Source

All occupation data comes from the **U.S. Bureau of Labor Statistics (BLS) Occupational Outlook Handbook**.

The BLS data includes:
- Occupation names
- Median annual salary
- Number of jobs
- Job outlook (growth percentage)
- Entry-level education requirements
- Job descriptions

## Customization

### Adding More Majors

Edit `major_occupation_mapping.py` and add entries to the `MAJOR_TO_OCCUPATIONS` dictionary:

```python
MAJOR_TO_OCCUPATIONS = {
    "Your New Major": [
        "BLS Occupation Name 1",
        "BLS Occupation Name 2",
        # ...
    ],
}
```

### Changing Default Majors

Modify the `DEFAULT_TOP_MAJORS` list in `major_occupation_mapping.py`:

```python
DEFAULT_TOP_MAJORS = [
    "Computer Science",
    "Nursing",
    # ... add your preferred defaults
]
```

### Updating BLS Data Path

In `app.py`, update the `BLS_DATA_PATH` constant:

```python
BLS_DATA_PATH = '/path/to/your/bls_occupations_all.csv'
```

## Future Enhancements

Potential features to add:
- Quiz/questionnaire to suggest majors based on interests
- Geographic salary variations
- Education ROI calculations (salary vs. tuition costs)
- Career path visualizations (graphs/charts)
- Export comparison data to PDF/Excel
- Integration with additional data sources (e.g., O*NET)

## License

This project uses public data from the U.S. Bureau of Labor Statistics.

## Contributing

Feel free to submit issues or pull requests to improve the app!
