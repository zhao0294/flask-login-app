# CST8919 Lab 2 – Web App Threat Detection with Azure Monitor and KQL

## Lab Overview

This lab demonstrates how to detect suspicious login behaviors, such as brute-force attacks, by:

- Deploying a Python Flask web application on Azure App Service
- Enabling diagnostic logging to Azure Monitor via Log Analytics
- Writing KQL queries to analyze login patterns
- Creating alert rules that notify when excessive failed logins occur

---

## Project Structure

<pre>
flask-login-app/
├── app.py
├── requirements.txt
├── test-app.http
└── README.md
</pre>

---

## What I Learned

- How to deploy a basic Flask app with login logging functionality to Azure App Service
- How to create and link a Log Analytics Workspace to an App Service for real-time logging
- How to query structured log data using Kusto Query Language (KQL)
- How to configure an Azure Monitor alert based on query results and trigger email notifications

---

## Challenges Faced

- Initial confusion about where `logger.warning(...)` logs appear in Log Analytics (they are under `AppServiceConsoleLogs`)
- Delay between logging events and their appearance in the analytics table (up to 3–5 minutes)
- Diagnosing field name mismatches (e.g., using `ResultDescription` instead of `Message`)
- Ensuring the alert rule uses the correct granularity and frequency to be triggered

---

## Detection Logic and Future Improvements

Currently, detection is based on simple string matching of the phrase `"Login failed"` in logs. In a real-world application, I would:

- Add IP tracking and user-agent logging
- Use rate-limiting or CAPTCHA at the app level
- Store login attempts in a database for more persistent analysis
- Detect multiple failures from the same IP in a short time window using KQL aggregation

---

## KQL Query Used

```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(30m)
| where ResultDescription has "Login failed"
| project TimeGenerated, ResultDescription
| sort by TimeGenerated desc
```

Explanation:

- AppServiceConsoleLogs: The Azure table containing standard output logs from the Flask app
- ResultDescription has "Login failed": Filters logs for failed login attempts
- project: Only shows the timestamp and log message
- sort: Puts the newest entries on top

---

## Alert Rule Configuration

| Property              | Value                     |
|-----------------------|---------------------------|
| **Scope**             | Log Analytics Workspace   |
| **Condition (Measure)** | Table rows             |
| **Operator**          | Greater than              |
| **Threshold**         | 5                         |
| **Time Aggregation**  | 5 minutes                 |
| **Evaluation Frequency** | 1 minute              |
| **Action Group**      | Email notification        |
| **Severity**          | 2                         |

---

## Test File

I used the following .http file to test successful and failed login requests using the REST Client extension in VS Code:

```http
### ✅ Successful login
POST https://flask-lab-cong.azurewebsites.net/login
Content-Type: application/json

{
  "username": "admin",
  "password": "1234"
}

### ❌ Failed login
POST https://flask-lab-cong.azurewebsites.net/login
Content-Type: application/json

{
  "username": "admin",
  "password": "wrong"
}
```

---

## Demo Video

Here is the YouTube link to my 5-minute demo:

[Watch on YouTube](https://youtu.be/nLaG7GLz3FA)

---
