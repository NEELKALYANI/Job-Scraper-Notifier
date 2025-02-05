import requests
from bs4 import BeautifulSoup
import hashlib
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Configuration
URLS_TO_MONITOR = [
    'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=python&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&pDate=I&sequence=2&startPage=1',
    'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=marketing&txtLocation=',
]
CHECK_INTERVAL = 1  # in minutes
EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',
    'sender_password': '',
    'recipient_email': ''
}
HASH_STORAGE = 'hashes.txt'

def fetch_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    job_list = []
    
    for job in jobs:
        posted = job.find('span', class_='sim-posted').text.strip()
        if 'few days ago' in posted:
            job_title = job.find('h2', class_='heading-trun').text.strip()
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            job_description = job.find('li', class_='job-description__').text.strip()
            location = job.find('li', class_='srp-zindex location-tru').text.strip()
            salary_tag = job.find('i', class_='srp-icons salary')
            salary_low = salary_tag.get('data-lowsalary') if salary_tag else 'N/A'
            salary_high = salary_tag.get('data-highsalary') if salary_tag else 'N/A'
            skills_tag = job.find('div', class_='more-skills-sections')
            skills = [skill.strip().lower() for skill in skills_tag.stripped_strings] if skills_tag else []
            apply_link = job.find('a', class_='posoverlay_srp')['href']
            
            job_list.append(f"""
            Job Title: {job_title}
            Company Name: {company_name}
            Job Description: {job_description}
            Job Location: {location}
            Salary: {salary_low} - {salary_high}
            Skills: {', '.join(skills)}
            Posted: {posted}
            Apply Here: {apply_link}
            """)
    
    return '\n'.join(job_list)

def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_hashes():
    try:
        with open(HASH_STORAGE, 'r') as file:
            return dict(line.strip().split(' ') for line in file)
    except FileNotFoundError:
        return {}

def save_hashes(hashes):
    with open(HASH_STORAGE, 'w') as file:
        for url, hash_value in hashes.items():
            file.write(f"{url} {hash_value}\n")

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SETTINGS['sender_email']
    msg['To'] = EMAIL_SETTINGS['recipient_email']
    
    try:
        with smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_SETTINGS['sender_email'], EMAIL_SETTINGS['sender_password'])
            server.send_message(msg)
        print("Notification email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_websites():
    print("Starting website monitoring...")
    stored_hashes = load_hashes()
    current_hashes = {}
    
    for url in URLS_TO_MONITOR:
        content = fetch_page_content(url)
        if content:
            current_hash = compute_hash(content)
            current_hashes[url] = current_hash
            
            if url in stored_hashes:
                if current_hash != stored_hashes[url]:
                    print(f"Change detected at {url}")
                    send_email(
                        subject=f"Website Change Detected: {url}",
                        body=f"New job postings detected:\n{content}"
                    )
            else:
                print(f"Monitoring new URL: {url}")
                send_email(
                    subject=f"Started Monitoring: {url}",
                    body=f"Now monitoring {url} for changes."
                )
    
    save_hashes(current_hashes)
    print("Website monitoring completed.")

if __name__ == "__main__":
    schedule.every(CHECK_INTERVAL).minutes.do(monitor_websites)
    print(f"Scheduled monitoring every {CHECK_INTERVAL} minutes.")
    monitor_websites()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(1)
