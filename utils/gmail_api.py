import os
import re
import time
import base64
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailAPI:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def __init__(self, credentials_path, token_path):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._get_service()

    def _get_service(self):
        """Authenticates and returns the Gmail API service."""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            print(f"Found token file at {self.token_path}")
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e: # Catch JSONDecodeError or other file issues
                print(f"Error loading token file (it corresponds to GMAIL_TOKEN_JSON secret): {e}")
                creds = None
        else:
            print(f"Token file NOT found at {self.token_path}")
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Token expired, attempting refresh with refresh_token...")
                try:
                    creds.refresh(Request())
                    print("Token refreshed successfully.")
                except Exception as e:
                    print(f"Token refresh failed: {e}")
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}. Please follow Gmail API setup guide.")
                
                # Check if running in a CI environment (like GitHub Actions)
                if os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true':
                    raise Exception(
                        "Gmail API token is expired or invalid, and cannot be refreshed. "
                        "Interactive authentication is not possible in a CI environment. "
                        "Please update your GMAIL_TOKEN_JSON secret with a fresh token containing a refresh_token."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            return None

    def cleanup_inbox(self, query):
        """Marks old OTP emails matching the query as read or removes them."""
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])

            if not messages:
                logger.info(f"No stale emails found for cleanup with query: {query}")
                return

            for message in messages:
                self.service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': [message['id']],
                        'removeLabelIds': ['UNREAD']
                    }
                ).execute()
            logger.info(f"Cleaned up {len(messages)} stale emails.")
        except HttpError as error:
            logger.error(f"An error occurred during cleanup: {error}")

    def get_otp(self, query, regex_pattern, timeout=60, poll_interval=7):
        """
        Polls for the latest OTP email matching the Gmail query.
        Returns (status, otp)
        """
        start_time = time.time()
        logger.info(f"Polling for OTP with query: {query} (Timeout: {timeout}s)")

        while time.time() - start_time < timeout:
            try:
                # Search for unread emails matching the query
                results = self.service.users().messages().list(userId='me', q=f"{query} is:unread").execute()
                messages = results.get('messages', [])

                if messages:
                    # Get the most recent one
                    msg_id = messages[0]['id']
                    message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                    
                    # Extract body
                    payload = message.get('payload', {})
                    parts = payload.get('parts', [])
                    body = ""

                    if not parts:
                        # Simple message
                        data = payload.get('body', {}).get('data', '')
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                    else:
                        # Multipart message
                        for part in parts:
                            if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                                data = part.get('body', {}).get('data', '')
                                body += base64.urlsafe_b64decode(data).decode('utf-8')
                    
                    # Strip HTML if needed for cleaner regex matching
                    clean_body = re.sub(r'<[^>]+>', ' ', body)
                    
                    # Match OTP
                    otp_match = re.search(regex_pattern, clean_body)
                    if otp_match:
                        otp = otp_match.group(0)
                        logger.info(f"OTP found: {otp}")
                        
                        # Mark as read
                        self.service.users().messages().batchModify(
                            userId='me',
                            body={
                                'ids': [msg_id],
                                'removeLabelIds': ['UNREAD']
                            }
                        ).execute()
                        
                        return "OTP_RECEIVED", otp
                    else:
                        logger.warning(f"Email found but OTP regex did not match. ID: {msg_id}")
                
            except HttpError as error:
                logger.error(f"Gmail API error: {error}")
                # Check for rate limiting or other specific API errors if needed
            
            time.sleep(poll_interval)

        logger.error("OTP retrieval timed out.")
        return "OTP_DELAYED", None

class OTPHandler:
    """Standardized handler for OTP operations with retry and fallback logic."""
    
    @staticmethod
    def fetch_with_retry(gmail_api, query, regex_pattern, max_attempts=2, resend_callback=None):
        """
        Fetches OTP with retry logic. 
        If first attempt fails, calls resend_callback and tries again.
        """
        for attempt in range(1, max_attempts + 1):
            logger.info(f"OTP Fetch Attempt {attempt}/{max_attempts}")
            status, otp = gmail_api.get_otp(query, regex_pattern)
            
            if status == "OTP_RECEIVED":
                return status, otp
            
            if attempt < max_attempts and resend_callback:
                logger.info("Triggering Resend OTP fallback...")
                resend_callback()
                # Brief wait after resend before starting next poll
                time.sleep(5)
            
        return "OTP_BLOCKED", None
