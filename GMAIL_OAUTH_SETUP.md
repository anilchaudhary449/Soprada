# Gmail OAuth 2.0 OTP Automation Setup Guide

## 📋 Prerequisites
- Python 3.8+
- Google Cloud Project with Gmail API enabled
- Test Gmail account

## 🔧 Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Library**
4. Search for "Gmail API" and click **Enable**

## 🔑 Step 2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External** (for testing) or **Internal** (for organization)
   - Add your test email to **Test users**
   - Scopes: Add `https://www.googleapis.com/auth/gmail.modify`
4. Application type: **Desktop app**
5. Name: `Soprada OTP Automation`
6. Click **Create**
7. Download the JSON file
8. Rename it to `credentials.json`
9. Place it in: `c:\Users\anilb\PycharmProjects\SopradaAutomation\resources\credentials.json`

## 🚀 Step 3: First-Time Authentication

Run the verification script:
```powershell
python verify_gmail_oauth.py
```

This will:
1. Open a browser window for Google OAuth consent
2. Ask you to sign in with your test Gmail account
3. Grant permissions to the application
4. Generate `token.json` automatically in the `resources` folder

**Note**: `token.json` will be auto-refreshed when expired. You only need to authenticate once.

## 📁 File Structure

```
SopradaAutomation/
├── resources/
│   ├── credentials.json  # OAuth client credentials (from Google Cloud)
│   ├── token.json        # Auto-generated after first auth (gitignored)
│   └── resources.py      # Configuration constants
├── utils/
│   ├── gmail_api.py      # Gmail API OAuth handler
│   └── gmail_otp.py      # Legacy IMAP (deprecated)
├── pages/
│   └── login_otp.py      # Page Object with trigger_resend_otp()
└── tests/
    └── test_soprada.py    # Centralized tests with OTP retry logic
```

## ⚙️ Configuration (resources/resources.py)

```python
# Gmail API Configuration (OAuth 2.0)
GMAIL_API_CREDENTIALS = os.path.join(RESOURCES_DIR, "credentials.json")
GMAIL_API_TOKEN = os.path.join(RESOURCES_DIR, "token.json")
GMAIL_OTP_QUERY = "subject:\"Verify your account\""
GMAIL_OTP_REGEX = r"\b\d{6}\b"
GMAIL_FETCH_TIMEOUT = 60
GMAIL_POLL_INTERVAL = 7
```

## 🧪 Usage in Tests

```python
from utils.gmail_api import GmailAPI, OTPHandler

# Initialize
gmail_api = GmailAPI(GMAIL_API_CREDENTIALS, GMAIL_API_TOKEN)

# Cleanup old OTPs
gmail_api.cleanup_inbox(GMAIL_OTP_QUERY)

# Fetch OTP with retry
status, otp = OTPHandler.fetch_with_retry(
    gmail_api, 
    GMAIL_OTP_QUERY, 
    GMAIL_OTP_REGEX, 
    max_attempts=2, 
    resend_callback=login_page.trigger_resend_otp
)

if status == "OTP_RECEIVED":
    login_page.enter_otp_direct(otp)
```

## 🔄 Retry Logic Flow

1. **Attempt 1**: Poll Gmail for OTP (60s timeout)
2. If failed → Trigger UI "Resend OTP" button
3. **Attempt 2**: Poll Gmail again (60s timeout)
4. If still failed → Return `OTP_BLOCKED` status

## 🛡️ Security Best Practices

- ✅ Use OAuth 2.0 (no passwords in code)
- ✅ `credentials.json` should be gitignored
- ✅ `token.json` auto-refreshes (no manual intervention)
- ✅ Use test Gmail accounts only
- ✅ Restrict OAuth scopes to `gmail.modify` only

## 🚫 What NOT to Do

- ❌ Do NOT commit `credentials.json` or `token.json` to Git
- ❌ Do NOT use production Gmail accounts
- ❌ Do NOT share OAuth credentials publicly
- ❌ Do NOT use IMAP/App Passwords (deprecated approach)

## 📊 OTP Status Codes

| Status | Meaning |
|--------|---------|
| `OTP_RECEIVED` | OTP successfully fetched and returned |
| `OTP_DELAYED` | OTP not received within timeout |
| `OTP_BLOCKED` | All retry attempts exhausted |
| `RATE_LIMITED` | Gmail API rate limit hit (future) |

## 🔍 Troubleshooting

### "credentials.json not found"
- Ensure you've downloaded OAuth credentials from Google Cloud
- Place it in `resources/credentials.json`

### "Invalid grant" error
- Delete `token.json` and re-authenticate
- Check if test user is added in OAuth consent screen

### "Insufficient permissions"
- Verify Gmail API is enabled in Google Cloud
- Check OAuth scope includes `gmail.modify`

### OTP not found
- Verify `GMAIL_OTP_QUERY` matches your email subject
- Check `GMAIL_OTP_REGEX` pattern
- Ensure email is actually sent to the test account

## 📈 Performance Metrics

- **Average OTP fetch time**: 5-10 seconds
- **Polling interval**: 7 seconds
- **Timeout**: 60 seconds per attempt
- **Max retry attempts**: 2 (configurable)

## 🔮 Future Enhancements

- [ ] SMS OTP integration
- [ ] Multi-account OTP handling
- [ ] OTP analytics dashboard
- [ ] CI/CD integration guide
- [ ] Rate limit detection
