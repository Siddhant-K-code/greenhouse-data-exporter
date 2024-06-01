# Greenhouse Data Export Script 📊

This project provides a Python script to fetch and export candidate data from Greenhouse.io using their Harvest API. The script collects candidate details, notes, scorecards, attributes, and questions, then saves this data into a CSV file. Finally, the CSV file is converted into an Excel file for easy access and analysis.

## Features ✨

- Fetch candidate applications after a specific date 📅
- Retrieve detailed candidate information including email addresses 📧
- Collect candidate notes and activity feed 📝
- Fetch and combine scorecards, attributes, and questions 📋
- Save the data into a CSV file and convert it to an Excel file 📂

## Requirements 📦

- Python 3.6 or higher
- pandas
- requests
- openpyxl

## Setup and Usage 🚀

1. **Clone the repository**:

   ```bash
   git clone https://github.com/siddhant-k-code/greenhouse-data-exporter.git
   cd greenhouse-data-exporter
   ```

2. **Install dependencies**:

   ```bash
   pip install pandas requests openpyxl
   ```

3. **Set your Greenhouse API token**:
   Open the script `greenhouse_export.py` and set your API token in the `API_TOKEN` variable:

   ```python
   API_TOKEN = 'your_api_token_here'
   ```

4. **Run the script**:

   ```bash
   python greenhouse_export.py
   ```

   Then, you can convert the CSV file to an Excel file using the following command:

   ```bash
    python csv_to_excel.py greenhouse_candidates_after_<date>.csv
   ```

5. **Check the output**:
   The script will create two files:

   - `greenhouse_candidates_after_<date>.csv`
   - `greenhouse_candidates_after_<date>.xlsx`

   You can find these files in the project directory.

## Script Details 🔍

The script performs the following steps:

1. **Fetch Applications**:
   Retrieves candidate applications created after a specified date from Greenhouse.

2. **Fetch Candidate Details**:
   Collects email addresses and other candidate information.

3. **Fetch Notes**:
   Gathers notes and activity feed for each candidate.

4. **Fetch Scorecards**:
   Retrieves scorecards, attributes, and questions for each application.

5. **Combine Data**:
   Merges notes, scorecards, attributes, and questions into a single string.

6. **Save to CSV and Excel**:
   Writes the data into a CSV file and converts it to an Excel file.

## Example Output 📁

Here is an example of the output structure:

| Job opening id | Email address        | Activity date | Notes                                                                                                      |
| -------------- | -------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------- |
| 12345          | john.doe@example.com | 2024-03-24T00:00:00Z | Note 1 (Date: 2024-03-24T00:00:00Z) <br><br> Scorecard 1:<br> Overall Recommendation: yes                  |
|                |                      |                      | Attributes:<br> Communication: strong_yes <br> Questions:<br> Why do you want this job?: To make an impact |
| 67890          | jane.doe@example.com | 2024-03-25T00:00:00Z | Note 2 (Date: 2024-03-25T00:00:00Z)                                                                        |

## Acknowledgments 🙌

- Thanks to Greenhouse.io for their [comprehensive API documentation](https://developers.greenhouse.io/harvest.html).
