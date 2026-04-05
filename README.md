# JobFlow AI

JobFlow AI is a Python-based job application tracker and follow-up assistant designed to help job seekers manage applications, monitor progress, organize notes, and stay on top of recruiter communication from one place.

## Overview

Job searching often becomes messy across spreadsheets, emails, sticky notes, and scattered reminders. JobFlow AI is being built to solve that problem through a simple product that combines application tracking, workflow visibility, and communication support in one dashboard.

The goal of this project is twofold:

1. build a practical product with real user value
2. learn professional GitHub workflows through small, structured feature releases

## Current Features

- Streamlit-based dashboard UI
- Overview metrics for:
  - total applications
  - interviews
  - offers
  - follow-ups due
- Job application input form
- Session-based application tracking
- Interactive application table
- Clean starter structure for future backend and database integration
- Edit existing job applications
- Delete job applications
- Full basic CRUD workflow for application tracking

## Planned Features

- SQLite database integration
- Persistent application storage
- Edit and delete application entries
- Recruiter contact management
- Follow-up reminder tracking
- Thank-you and follow-up email draft generation
- Application status timeline
- FastAPI backend endpoints
- AI-powered writing assistance for outreach and follow-ups
- Deployment for public access

## Tech Stack

### Frontend

- Streamlit

### Backend

- FastAPI

### Database

- SQLite
- SQLAlchemy

### Language

- Python

### Version Control

- Git
- GitHub

## Project Structure

```text
jobflow-ai/
├── app/
│   ├── backend/
│   ├── frontend/
│   │   └── streamlit_app.py
│   ├── database/
│   └── models/
├── README.md
├── requirements.txt
├── .gitignore
└── main.py #python code
```
