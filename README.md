📌 Overview

The Job Scraper and Notifier is a Python-based automation script that monitors job listings from specified websites, detects updates, and notifies users via email when new job postings are found.
It is particularly useful for job seekers who want to stay updated with the latest job openings without manually checking websites. The script uses BeautifulSoup to extract job details, hashlib to track changes, and smtplib to send email notifications.

🚀 Features
✅ Automated Job Scraping – Fetches job listings from specified websites at regular intervals.
✅ Change Detection – Uses hashing to detect new job postings and avoids duplicate notifications.
✅ Email Notifications – Sends an email when new jobs are found, keeping users updated.
✅ Customizable Job Search – Modify URLs to track different job categories or keywords.
✅ Scheduled Execution – Runs automatically at defined time intervals using schedule.

🛠 Technologies Used

Python – Core programming language.
BeautifulSoup – Web scraping to extract job details.
Requests – Fetching web pages.
Hashlib – Tracking changes in job listings.
Smtplib – Sending email notifications.
Schedule – Automating script execution at set intervals.

🛠 How It Works

Scraping Websites: The script fetches job postings from predefined URLs.
Change Detection: It computes a hash of the job listings to detect updates.
Storing Hashes: Hashes are stored in hashes.txt to track changes.
Sending Notifications: If a change is detected, an email notification is sent.
Automated Execution: The script runs at regular intervals using schedule.
