# 📧 Secure Email Listing

This project enables users to securely view their Gmail inbox with a seamless login process using Google OAuth2. After successful authentication, users can view emails and download any attachments directly from their inbox.

## Features

- Google OAuth2 login
- Secure email listing with attachment support
- FastAPI backend for fetching emails
- Streamlit frontend for displaying emails
- JWT token-based authentication for secure access

## Prerequisites

Before running this project, ensure that you have the following:

- Python 3.8 or higher
- Google Cloud API credentials (Client ID and Client Secret) for OAuth2
- MongoDB for storing user tokens
- Streamlit for the frontend

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/secure-email-listing.git
cd secure-email-listing
```

### 2. Set up a virtual environment and install dependencies:

   - **On Windows**:
     ```bash
     py -3 -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```

   - **On macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

### 3. Configure environment variables:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     DATABASE_URL=mongo_url_from_cloud
     ```

### 4. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
### 4. Run Streamlit:
   ```bash
   streamlit run frontend/app.py
   ```
