"""
Mapping of college majors to BLS occupation names.
Each major maps to a list of relevant occupations from the BLS data.
Note: Jobs can appear in multiple majors as many careers are suitable for various educational backgrounds.
"""

MAJOR_TO_OCCUPATIONS = {
    "Computer Science": [
        "Software developers",
        "Computer programmers",
        "Web and digital interface designers",
        "Computer systems analysts",
        "Database administrators",
        "Computer network architects",
        "Information security analysts",
        "Computer and information research scientists",
        "Data scientists",
        "Network and computer systems administrators",
    ],

    "Data Science/Analytics": [
        "Data scientists",
        "Statisticians",
        "Operations research analysts",
        "Computer systems analysts",
        "Database administrators",
        "Market research analysts and marketing specialists",
    ],

    "Computer/Software Engineering": [
        "Software developers",
        "Computer hardware engineers",
        "Computer network architects",
        "Information security analysts",
        "Electronics engineers, except computer",
    ],

    "Nursing": [
        "Registered nurses",
        "Nurse anesthetists",
        "Licensed practical and licensed vocational nurses",
        "Nursing assistants",
        "Medical assistants",
    ],

    "Business Administration/Management": [
        "Management analysts",
        "Project management specialists",
        "Human resources specialists",
        "Training and development specialists",
        "Buyers and purchasing agents",
        "Logisticians",
        "Compliance officers",
        "Operations research analysts",
        "Market research analysts and marketing specialists",
    ],

    "Psychology": [
        "Industrial-organizational psychologists",
        "Marriage and family therapists",
        "Recreational therapists",
        "Survey researchers",
        "Human resources specialists",
        "Training and development specialists",
        "Market research analysts and marketing specialists",
    ],

    "Mechanical Engineering": [
        "Mechanical engineers",
        "Mechanical engineering technologists and technicians",
        "Industrial engineers",
        "Aerospace engineers",
        "Bioengineers and biomedical engineers",
    ],

    "Electrical Engineering": [
        "Electronics engineers, except computer",
        "Electrical and electronic engineering technologists and technicians",
        "Computer hardware engineers",
        "Electro-mechanical and mechatronics technologists and technicians",
    ],

    "Civil Engineering": [
        "Civil engineers",
        "Civil engineering technologists and technicians",
        "Surveyors",
        "Surveying and mapping technicians",
        "Urban and regional planners",
    ],

    "Chemical Engineering": [
        "Chemical engineers",
        "Materials scientists",
        "Petroleum engineers",
    ],

    "Biomedical Engineering": [
        "Bioengineers and biomedical engineers",
        "Medical scientists, except epidemiologists",
    ],

    "Environmental Engineering": [
        "Environmental engineers",
        "Environmental engineering technologists and technicians",
        "Environmental scientists and specialists, including health",
    ],

    "Biology/Biological Sciences": [
        "Biological technicians",
        "Medical scientists, except epidemiologists",
        "Biochemists and biophysicists",
        "Microbiologists",
        "Zoologists and wildlife biologists",
        "Bioengineers and biomedical engineers",
        "Environmental scientists and specialists, including health",
    ],

    "Chemistry": [
        "Chemical technicians",
        "Chemists",
        "Chemical engineers",
        "Materials scientists",
        "Biochemists and biophysicists",
        "Medical scientists, except epidemiologists",
    ],

    "Physics": [
        "Physicists",
        "Materials scientists",
        "Atmospheric and space scientists",
    ],

    "Mathematics (Pure)": [
        "Statisticians",
        "Data scientists",
        "Operations research analysts",
        "Actuaries",
        "Financial risk specialists",
    ],

    "Applied Mathematics": [
        "Operations research analysts",
        "Actuaries",
        "Data scientists",
        "Statisticians",
    ],

    "Statistics": [
        "Statisticians",
        "Data scientists",
        "Operations research analysts",
        "Actuaries",
        "Epidemiologists",
    ],

    "Finance": [
        "Financial risk specialists",
        "Personal financial advisors",
        "Financial examiners",
        "Budget analysts",
        "Accountants and auditors",
        "Loan officers",
        "Actuaries",
    ],

    "Accounting": [
        "Accountants and auditors",
        "Budget analysts",
        "Tax examiners and collectors, and revenue agents",
        "Cost estimators",
        "Financial examiners",
    ],

    "Economics": [
        "Economists",
        "Survey researchers",
        "Market research analysts and marketing specialists",
        "Financial risk specialists",
        "Management analysts",
        "Data scientists",
        "Operations research analysts",
    ],

    "Marketing": [
        "Market research analysts and marketing specialists",
        "Meeting, convention, and event planners",
        "Fundraisers",
    ],

    "Communications/Media Studies": [
        "Writers and authors",
        "Editors",
        "Film and video editors",
        "Public relations specialists",
    ],

    "English/Literature": [
        "Writers and authors",
        "Editors",
        "Technical writers",
    ],

    "Education (Teaching)": [
        "Kindergarten teachers, except special education",
        "Middle school teachers, except special and career/technical education",
        "Secondary school teachers, except special and career/technical education",
        "Special education teachers, middle school",
        "Preschool teachers, except special education",
        "Instructional coordinators",
        "Training and development specialists",
    ],

    "Pre-Medicine": [
        "Physicians and surgeons",
        "General internal medicine physicians",
        "Medical scientists, except epidemiologists",
    ],

    "Public Health": [
        "Epidemiologists",
        "Occupational health and safety specialists",
        "Health information technologists and medical registrars",
    ],

    "Pharmacy": [
        "Pharmacists",
        "Pharmacy technicians",
    ],

    "Physical Therapy/Kinesiology": [
        "Physical therapists",
        "Physical therapist assistants",
        "Occupational therapists",
        "Exercise physiologists",
        "Athletic trainers",
    ],

    "Political Science/Government": [
        "Political scientists",
        "Urban and regional planners",
        "Survey researchers",
    ],

    "Sociology": [
        "Sociologists",
        "Survey researchers",
        "Urban and regional planners",
    ],

    "History": [
        "Historians",
        "Archivists",
        "Museum technicians and conservators",
    ],

    "Environmental Science": [
        "Environmental scientists and specialists, including health",
        "Environmental science and protection technicians, including health",
        "Urban and regional planners",
        "Foresters",
    ],

    "Criminal Justice": [
        "Police and sheriff's patrol officers",
        "Detectives and criminal investigators",
        "Forensic science technicians",
    ],

    "Graphic Design": [
        "Graphic designers",
        "Web and digital interface designers",
    ],

    "Performing Arts (Theater/Music)": [
        "Actors",
        "Musicians and singers",
        "Music directors and composers",
    ],
}

# Top 15 majors to display by default in the comparison table
DEFAULT_TOP_MAJORS = [
    "Computer Science",
    "Nursing",
    "Business Administration/Management",
    "Psychology",
    "Mechanical Engineering",
    "Biology/Biological Sciences",
    "Finance",
    "Accounting",
    "Marketing",
    "Communications/Media Studies",
    "Education (Teaching)",
    "Electrical Engineering",
    "Civil Engineering",
    "Mathematics (Pure)",
    "Economics",
]
