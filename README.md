# Health Recommendations Service

This service provides a comprehensive solution for analyzing health reports, researching health conditions, and generating personalized health recommendations. Built with Flask, MongoDB, and leveraging the CrewAI framework for orchestrating agents and tasks, it offers a REST API for user registration, login, and health recommendation generation.

## Features

- User registration and login with JWT authentication.
- Upload blood test reports for analysis.
- Automated generation of health recommendations based on the uploaded report.
- Email delivery of the health recommendations in PDF format on your registered email address.

## Prerequisites

- Python 3.11 or newer
- MongoDB running locally or remotely
- SMTP server credentials for sending emails

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables by creating a `.env` file in the project root with the content in `.env.example`:
   ```plaintext
   JWT_SECRET_KEY=your_jwt_secret_key
   SENDER_EMAIL=your_email@gmail.com
   EMAIL_PASSWORD=your_email_password
   ```
   Ensure to replace `your_jwt_secret_key`, `your_email@gmail.com`, and `your_email_password` with your actual data.

## Running the Application

1. Start the Flask application:
   ```bash
   python main.py
   ```
2. The server will start running on `http://localhost:5000`.

## Usage

### Register

- Endpoint: `/register`
- Method: `POST`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### Login

- Endpoint: `/login`
- Method: `POST`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- Successful login sets a secure HTTP-only cookie with the JWT token.

### Upload Report and Get Recommendations

- Endpoint: `/recommend`
- Method: `POST`
- Form-data: Attach the blood test report file with the key `file`.
- Requires: Login (JWT token as an HTTP-only cookie).

## Development

Refer to the provided code snippets for understanding the application structure and logic:

- Flask application setup and routes: `main.py`
- Task definitions using CrewAI: `src/tasks.py`
- Utility functions, including JWT token generation and email sending: `src/utils.py`
- Agent definitions for analyzing, researching, and recommending: `src/agents.py`
- Language model configurations: `src/llms.py`

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your proposed changes.