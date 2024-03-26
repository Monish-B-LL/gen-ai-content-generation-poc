import requests
from base64 import b64encode
import os
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)

def create_jira_task(html_content, title):
    jira_url = os.environ['JIRA_URL']
    username = os.environ['USER_NAME']
    api_token = os.environ['JIRA_API_TOKEN']

    project_key = os.environ['JIRA_PROJECT_KEY']
    story_key = os.environ['JIRA_STORY_KEY']

    auth_header = ('%s:%s' % (username, api_token)).encode('utf-8')
    auth_header = 'Basic %s' % b64encode(auth_header).decode('utf-8')
    # auth_header = HTTPBasicAuth(username, api_token)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
    }

    issue_data = {
        "fields": {
            "project": {"key": project_key},
            "parent": {"key": story_key},
            "summary": title,
            "description": html_content,
            "issuetype": {"name": "Sub-task"}
        }
    }

    response = requests.post(jira_url, headers=headers, json=issue_data)
    if response.status_code == 201:
        logger.info("Issue created successfully.")
        print('Issue created successfully.')
    else:
        logger.error(f'Failed to update issue. Error: {response.text}')
        print('Failed to update issue. Error:', response.text)
