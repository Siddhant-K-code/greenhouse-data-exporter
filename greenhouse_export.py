import requests
import csv
import base64

# Your Greenhouse API key
API_TOKEN = 'YOUR_API_KEY'
CREDENTIAL = base64.b64encode(f"{API_TOKEN}:".encode('utf-8')).decode('utf-8')
BASE_URL = 'https://harvest.greenhouse.io/v1/'

# Headers for the API request
headers = {
    'Authorization': f'Basic {CREDENTIAL}'
}

# Function to get applications after a specific date
def get_applications_after(date):
    applications = []
    page = 1
    while True:
        response = requests.get(
            f"{BASE_URL}applications",
            headers=headers,
            params={'created_after': date, 'page': page, 'per_page': 100}
        )
        if response.status_code != 200:
            print(f"Error fetching applications: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        applications.extend(data)
        page += 1
        print(f"Fetched {len(data)} applications on page {page}")
    return applications

# Function to get candidate details including emails
def get_candidate_details(candidate_id):
    response = requests.get(f"{BASE_URL}candidates/{candidate_id}", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching candidate {candidate_id}: {response.status_code}")
        return None
    candidate_details = response.json()
    print(f"Candidate details for {candidate_id}: {candidate_details}")  # Debugging line
    return candidate_details

# Function to get candidate activity feed (notes)
def get_candidate_notes(candidate_id):
    response = requests.get(f"{BASE_URL}candidates/{candidate_id}/activity_feed", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching activity feed for candidate {candidate_id}: {response.status_code}")
        return [], "No Activity Date"
    activity_feed = response.json()
    print(f"Activity feed for candidate {candidate_id}: {activity_feed}")  # Debugging line
    notes = sorted(activity_feed.get('notes', []), key=lambda x: x['created_at'], reverse=True)
    notes_str = '\n'.join([f"{note['body']} (Date: {note['created_at']})" for note in notes])
    latest_note_date = notes[0]['created_at'] if notes else "No Activity Date"
    return notes_str, latest_note_date

# Function to get job scorecards
def get_application_scorecards(application_id):
    response = requests.get(f"{BASE_URL}applications/{application_id}/scorecards", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching scorecards for application {application_id}: {response.status_code}")
        return []
    scorecards = response.json()
    print(f"Scorecards for application {application_id}: {scorecards}")  # Debugging line

    scorecards_details = []
    for scorecard in scorecards:
        scorecard_info = {
            'overall_recommendation': scorecard.get('overall_recommendation', 'N/A'),
            'submitted_at': scorecard.get('submitted_at', 'N/A'),
            'attributes': [],
            'questions': []
        }
        # Collect attributes
        for attribute in scorecard.get('attributes', []):
            scorecard_info['attributes'].append(f"{attribute['name']}: {attribute['rating']}")
        
        # Collect questions and answers
        for question in scorecard.get('questions', []):
            scorecard_info['questions'].append(f"{question['question']}: {question['answer']}")
        
        scorecards_details.append(scorecard_info)
    
    return scorecards_details

# Date to filter candidates
date = '2022-01-01T00:00:00Z'

# Fetch applications
print("Fetching applications...")
applications = get_applications_after(date)
print(f"Total applications fetched: {len(applications)}")

# Prepare CSV file
output_path = './greenhouse_candidates_after_2022-01-01.csv'
with open(output_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Job opening id', 'Email address', 'Latest activity date', 'Notes'])
    writer.writeheader()

    for i, application in enumerate(applications):

        application_id = application.get('id')
        candidate_id = application.get('candidate_id')
        job_opening_id = application.get('job_post_id')

        print(f"Processing application for candidate ID: {candidate_id}, job opening ID: {job_opening_id}")

        candidate = get_candidate_details(candidate_id)
        if not candidate:
            print(f"Skipping candidate ID: {candidate_id} due to missing details")
            continue
        
        # Collect email addresses
        emails = [email['value'] for email in candidate.get('email_addresses', []) if email.get('value')]
        if not emails:
            # Skip candidates without email addresses
            print(f"Skipping candidate ID: {candidate_id} due to missing email addresses")
            continue
        emails_str = ', '.join(emails)

        # Collect notes and latest activity date
        notes_str, latest_note_date = get_candidate_notes(candidate_id)
        if not notes_str:
            notes_str = "No Notes"

        # Collect scorecards
        scorecards_details = get_application_scorecards(application_id)
        if scorecards_details:
            scorecards_str = '\n\n'.join([
                f"Scorecard {index + 1}:\nOverall Recommendation: {scorecard['overall_recommendation']} (Date: {scorecard['submitted_at']})\nAttributes:\n" +
                '\n'.join([f"  - {attribute}" for attribute in scorecard['attributes']]) +
                "\nQuestions:\n" + 
                '\n'.join([f"  - {question}" for question in scorecard['questions']])
                for index, scorecard in enumerate(scorecards_details)
            ])
            combined_str = f"{notes_str}\n\n{scorecards_str}"
        else:
            combined_str = notes_str

        # Log a row with the combined notes and scorecards
        writer.writerow({
            'Job opening id': job_opening_id if job_opening_id else "No Job ID",
            'Email address': emails_str,
            'Latest activity date': latest_note_date,
            'Notes': combined_str
        })

print(f"Data saved to {output_path}")
