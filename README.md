# Saauzi Automation Framework

[![Saauzi Automation CI/CD](https://github.com/anilchaudhary449/Saauzi/actions/workflows/cicd.yml/badge.svg)](https://github.com/anilchaudhary449/Saauzi/actions/workflows/cicd.yml)

A professional, industry-grade Selenium automation framework designed for the Saauzi E-commerce platform. This framework leverages the Page Object Model (POM) pattern and integrates with the Gmail API for automated OTP authentication.

---

## 🚀 Key Features

- **Automated Authentication**: Seamless login using the Gmail API (OAuth 2.0) to fetch and enter OTPs automatically.
- **Page Object Model (POM)**: Highly maintainable and scalable architecture separating page logic from test scripts.
- **Comprehensive Test Suite**: Covers Category Management, Product Creation, Order Processing, Shipping Settings, Customer Management, and more.
- **Advanced Reporting**: Generates detailed Allure reports, including a consolidated standalone HTML report for easy distribution.
- **CI/CD Ready**: Fully integrated with GitHub Actions for automated regression testing on every push and schedule.
- **Discord Integration**: Real-time notifications and test reports sent directly to your team's Discord channel.

---

## 🛠 Technology Stack

- **Language**: [Python 3.12+](https://www.python.org/)
- **Automation Tool**: [Selenium WebDriver](https://www.selenium.dev/)
- **Test Runner**: [Pytest](https://docs.pytest.org/)
- **Reporting**: [Allure Framework](https://docs.qameta.io/allure/)
- **API**: [Google Gmail API](https://developers.google.com/gmail/api)
- **CI/CD**: [GitHub Actions](https://github.com/features/actions)

---

## 📁 Project Structure

```text
SaauziAutomation/
├── .github/workflows/      # CI/CD pipeline configurations (cicd.yml)
├── pages_ecom/             # Page Object Model (POM) implementation
├── locators_ecom/          # Central repository for element locators
├── tests/                  # Test suites and execution logic
│   └── test_saauzi.py      # Main end-to-end automation tests
├── utils/                  # Utility functions
│   ├── gmail_api.py        # Gmail API OAuth 2.0 integration
│   └── security.py         # Encryption/Decryption utilities
├── resources/              # Test data and assets
│   ├── credentials.json    # Gmail API Client Credentials (local only)
│   ├── token.json          # Gmail API Access Token (local only)
│   ├── resources.py        # Central data management
│   └── images/             # Product and profile images repository
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── secret.key              # Encryption key for sensitive data (local only)
```

## 🏗 Architecture In-Depth

This framework is built using a **Multi-Layered Page Object Model (POM)** architecture to ensure high maintainability, reusability, and scalability.

### 1. Layered Design Pattern
- **Test Layer (`tests/`)**: Contains the test scenarios. It focuses on *what* to test rather than *how* to interact with the UI. Leverages Pytest fixtures for setup and teardown.
- **Page Object Layer (`pages_ecom/`)**: Contains the business logic and actions for each page (e.g., `login()`, `create_product()`). These classes do not contain hardcoded locators.
- **Locator Layer (`locators_ecom/`)**: A centralized repository of XPaths and CSS selectors. This allows UI changes to be updated in a single file without touching the page logic.
- **Data & Resource Layer (`resources/`)**: Centralized management of test data via `resources.py`. It provides randomized, localized data (using Faker) and manages paths for images and credentials.
- **Utility Layer (`utils/`)**: Provides low-level technical services like OAuth 2.0 authentication for Gmail, encryption, and custom logging.

### 2. Automated Authentication Workflow
The framework solves the "OTP problem" in automation through a sophisticated API bridge:
1. **Trigger**: Test requests a login.
2. **Action**: Page object enters email and triggers the "Send OTP" button.
3. **Bridge**: `GmailAPI` utility connects to Google via OAuth 2.0.
4. **Retrieval**: `OTPHandler` polls the inbox, finds the latest message from Saauzi, and extracts the 6-digit code using RegEx.
5. **Completion**: The code is returned to the test, and the Page Object enters it to complete login.

### 3. CI/CD Pipeline Flow
The GitHub Actions workflow (`cicd.yml`) orchestrates the entire lifecycle:
1. **Environment Setup**: Provisions a Linux runner, installs Python, and configures Firefox.
2. **Secret Injection**: Dynamically creates `credentials.json`, `token.json`, and `secret.key` from GitHub Repository Secrets to maintain security.
3. **Parallel Execution**: Uses `pytest-xdist` to run tests across multiple threads.
4. **Resilience**: Uses `pytest-rerunfailures` to automatically retry flaky tests.
5. **Artifact Generation**: Consolidates results into a single Standalone HTML Allure report.
6. **Notification**: Dispatches the report and status to Discord via webhooks.

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Python**: Ensure Python 3.12 or later is installed.
- **Firefox Browser**: The framework is optimized for Firefox.
- **Geckodriver**: Selenium 4+ manages this automatically, but ensure Firefox is installed in default locations.

### 2. Environment Setup
Clone the repository and create a virtual environment:

```powershell
# Create Virtual Environment
python -m venv .venv

# Activate Virtual Environment (Windows)
.\.venv\Scripts\Activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Gmail API Configuration
To automate OTP login, you need a Google Cloud Project with the Gmail API enabled.
1. Place your `credentials.json` in the `resources/` directory.
2. Run a test locally once to complete the OAuth 2.0 flow:
   ```powershell
   python -m pytest tests/test_saauzi.py -k test_verify_login
   ```
3. A browser will open for authentication. Once authorized, `resources/token.json` will be generated.

---

## 🧪 Running Tests

### Execute All Smoke Tests
```powershell
pytest -m smoke -v
```

### Run a Specific Test Case
```powershell
pytest tests/test_saauzi.py -k test_product -v -s
```

### Run Tests in Parallel (Fast Execution)
```powershell
pytest -n auto --dist loadscope -v
```

---

## 📊 Reporting

### Generate Allure Report
1. Run tests with the allure flag:
   ```powershell
   pytest --alluredir=allure-results
   ```
2. Serve the report locally:
   ```powershell
   allure serve allure-results
   ```

### Standalone HTML Report
The CI pipeline generates a `standalone-report.html` which is a self-contained HTML file viewable in any browser without requiring an Allure server.

---

## ☁️ CI/CD Integration

The project uses GitHub Actions for continuous testing.

### Required GitHub Secrets
To run tests in CI, you must add the following secrets in your Repository Settings (**Settings > Secrets and variables > Actions**):

| Secret Name | Description |
| :--- | :--- |
| `GMAIL_CREDENTIALS_JSON` | Content of your `resources/credentials.json` |
| `GMAIL_TOKEN_JSON` | Content of your `resources/token.json` |
| `SECRET_KEY` | Content of your `secret.key` |
| `DISCORD_WEBHOOK` | (Optional) Your Discord channel webhook URL |

---

## 🛠 Troubleshooting

- **OAuth Client Disabled**: If you see a `RefreshError: disabled_client`, your Google OAuth client needs reactivation in the [Google Cloud Console](https://console.cloud.google.com/).
- **Tests Skipping on Windows**: Ensure Firefox is installed. The framework handles path resolution automatically for standard installations.
- **Clean Workspace**: To clear temporary cache files, run:
  ```powershell
  Remove-Item -Path ".pytest_cache", "__pycache__" -Recurse -Force
  ```

---

## 📄 License
This project is for internal automation purposes. All rights reserved.

---
**Developed with ❤️ for Saauzi Automation**
