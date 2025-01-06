# Household Services App - Neato

A full-stack web application for booking and managing household tasks like plumbing, AC servicing, and more. This app offers seamless user experience, robust authentication, booking management, and a fair scoring system for service professionals based on customer feedback using NLP sentiment analysis.

## Features

- **User Authentication & Authorization**: Secure login and role-based access control.
- **Admin Control**:  Verify professional by reviewing portfolio.
- **Service Booking Management**: Customers can book, track, and manage household tasks.
- **Task Tracking**: Real-time updates on task status.
- **Professional Scoring System**: NLP-based sentiment analysis on customer comments for fair scoring.
- **Asynchronous Task Management**: Implemented using Celery and Redis.

## Tools & Technologies

- **Frontend**: Vue.js, Bootstrap, HTML/CSS
- **Backend**: Flask-RESTful API, SQLite, JWT
- **Task Management**: Celery, Redis
- **Natural Language Processing**: Sentiment analysis for scoring system
- **Package Management**: Vue CLI, npm

## How to Run the Project

### Prerequisites

Ensure you have the following installed on your system:

- **Python** (>=3.8)
- **Node.js** (>=14.x) and **npm**
- **Redis**

### Steps to Run

#### 1. Clone the Repository

```bash
- git clone https://github.com/Ripu0902/Neato.git
- cd household-services-app

Backend Setup
- cd backend
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate
- pip install -r requirements.txt

Start Redis server
- redis-server   (in Windows Subsystem linux (WSL) )
- celery -A app.celery worker --loglevel=info
- celery -A app.celery beat --loglevel=info

Running the app
- python app.py


Frontend Setup
- cd ../frontend
- npm install
- npm run serve







