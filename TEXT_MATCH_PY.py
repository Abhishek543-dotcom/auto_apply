import pandas as pd
import re
from fuzzywuzzy import fuzz

# Load the CSV file into a DataFrame
df = pd.read_csv("linkedin_jobs_with_full_descriptions.csv")

# Define a function to extract email addresses from a text
def extract_email(description):
    # Regular expression for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, description)
    return ', '.join(matches) if matches else None

# Apply the function to the 'Job Description' column and create a new 'Email' column
df['Email'] = df['Job Description'].apply(lambda x: extract_email(x) if pd.notna(x) else None)

# Save the updated DataFrame with emails to a new CSV file
emails_csv_path = "linkedin_jobs_with_emails_test.csv"
df.to_csv(emails_csv_path, index=False)

print(f"Data with emails has been saved to {emails_csv_path}")

# Absolute path to the CSV files
jobs_csv_path = emails_csv_path
resumes_csv_path = "resume.csv"

# Load the CSV files into DataFrames
jobs_df = pd.read_csv(jobs_csv_path)
resumes_df = pd.read_csv(resumes_csv_path)

# Print column names for debugging
print("Columns in jobs_df:", jobs_df.columns)
print("Columns in resumes_df:", resumes_df.columns)

# Strip any leading/trailing spaces from column names
resumes_df.columns = resumes_df.columns.str.strip()

# Check if 'Resume' column exists; if not, create it and fill with empty strings
if 'Resume' not in resumes_df.columns:
    print("The 'Resume' column is missing. Creating and filling it with empty strings.")
    resumes_df['Resume'] = ""  # Create the 'Resume' column and initialize with empty strings

# Extract resumes as a list of strings
resumes = resumes_df['Resume'].astype(str).tolist()

# Define a function to compute similarity percentage
def compute_similarity(job_description, resumes):
    if pd.isna(job_description):
        return 0

    max_similarity = 0
    for resume in resumes:
        similarity = fuzz.partial_ratio(job_description, resume)
        if similarity > max_similarity:
            max_similarity = similarity

    return max_similarity

# Apply the similarity computation for each job description
jobs_df['Similarity Percentage'] = jobs_df['Job Description'].apply(lambda desc: compute_similarity(desc, resumes))

# Save the updated DataFrame with similarity percentages to a new CSV file
output_path = "linkedin_jobs_with_similarity.csv"
jobs_df.to_csv(output_path, index=False)

print(f"Data with similarity percentages has been saved to {output_path}")
