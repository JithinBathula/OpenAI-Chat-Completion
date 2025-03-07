# OpenAI Chat Completion API Service

This is a Flask-based API service that acts as a middleman between clients and [OpenAI's Chat Completion API](https://platform.openai.com/docs/api-reference/chat). It processes incoming requests, communicates with OpenAI to generate completions, logs interactions in a SQLite database, and returns responses to the client. The service includes rate limiting to prevent abuse and supports session management with unique user IDs for conversation continuity.

---

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Set Up Environment Variables](#4-set-up-environment-variables)
- [Usage](#usage)
  - [1. Run the Application](#1-run-the-application)
  - [2. Interact with the API](#2-interact-with-the-api)
- [Rate Limiting](#rate-limiting)
- [Database](#database)
- [Additional Notes](#additional-notes)

---

## Features

- **API Endpoint**: A single POST endpoint `/openai-completion` that accepts a `prompt` and an optional `user_id`, returning a completion from OpenAI.
- **Session Management**: Maintains conversation history using a unique `user_id` (generated if not provided).
- **Database Logging**: Records all interactions (requests and responses) in a SQLite database with timestamps.
- **Rate Limiting**: Prevents abuse with configurable limits using Flask-Limiter.
- **Error Handling**: Validates input and handles OpenAI API errors gracefully.

---

## Setup Instructions

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

Download the project files by cloning the repository:

```bash
git clone <repository-url>
cd staple-ai
```

Replace `<repository-url>` with the actual URL of the repository.

### 2. Create a Virtual Environment

To keep dependencies isolated, create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
# On Windows, use `.venv\Scripts\activate`
```

After activation, your terminal prompt should indicate that the virtual environment is active (e.g., `(.venv)`).

### 3. Install Dependencies

The project relies on several Python packages listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

Common dependencies include:

- `Flask`: Web framework for the API.
- `openai`: Python client for OpenAI's API.
- `flask-limiter`: For rate limiting.
- `flask-sqlalchemy`: For database management.
- `python-dotenv`: For loading environment variables from `.env`.

If you encounter issues, ensure your Python version is compatible (e.g., Python 3.8+).

### 4. Set Up Environment Variables

The application requires an OpenAI API key, which should be stored securely in a `.env` file. Create this file in the root directory.

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

- Replace `your-openai-api-key-here` with your actual OpenAI API key from [OpenAI's dashboard](https://platform.openai.com/account/api-keys).
- The `.env` file is ignored by Git (via `.gitignore`) to prevent exposing sensitive data.

---

## Usage

### 1. Run the Application

Start the Flask application with:

```bash
python app.py
```

The API will be hosted at `http://localhost:5000`. You’ll see output indicating the server is running, typically:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 2. Interact with the API

The API provides a single endpoint: `/openai-completion` (POST).

#### Request Format

Send a JSON payload with:

- `prompt` (required): The message you want the chatbot to respond to.
- `user_id` (optional): A unique identifier for the user. If omitted, a new UUID is generated and returned.

#### Response Format

The API returns a JSON object with:

- `user_id`: The unique identifier for the user (either provided or newly generated).
- `completion`: The response from OpenAI's Chat Completion API.

#### Example: Initial Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Hello, how are you?"}' http://127.0.0.1:5000/openai-completion
```

**Response:**

```json
{
  "user_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
  "completion": "I'm doing well, thank you! How can I assist you today?"
}
```

#### Example: Continuing the Conversation

Reuse the `user_id` to maintain context:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv", "prompt": "Tell me a joke"}' http://127.0.0.1:5000/openai-completion
```

**Response:**

```json
{
  "user_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
  "completion": "Why don’t skeletons fight each other? Because they don’t have the guts!"
}
```

---

## Rate Limiting

To prevent abuse, the application uses [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) with the following default settings:

- **Global Limits**:
  - 200 requests per day per IP address.
  - 50 requests per hour per IP address.
- **Endpoint-Specific Limit**:
  - 10 requests per minute for `/openai-completion`.

If these limits are exceeded, the API returns a 429 (Too Many Requests) response.

### How to Change Rate Limits

You can adjust rate limits by modifying the configuration in the source code:

1. **Global Limits**  
   Edit the `default_limits` in `app.py` or `extensions.py` (depending on your setup):

   ```python
   limiter = Limiter(
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
       # Adjust these values
   )
   ```

   Examples:

   - `"500 per day", "100 per hour"`
   - `"50 per day", "10 per hour"`

2. **Endpoint-Specific Limit**  
   Modify the decorator in `routes/openai_routes.py`:

   ```python
   @bp.route('/openai-completion', methods=['POST'])
   @limiter.limit("10 per minute")
   # Change this, e.g., "20 per minute"
   def openai_completion_route():
       return openai_completion()
   ```

After making changes, restart the application (`python app.py`) for them to take effect.

---

## Database

When you first run the application, it automatically creates an `instance` folder in the project root. Inside this folder, a SQLite database named `chat_history.db` is initialized to log all API interactions. The database has a `messages` table with the following columns:

- `id` (INTEGER): A unique identifier for each message, automatically generated by the database.
- `user_id` (TEXT): The unique identifier for the user.
- `timestamp` (DATETIME): When the message was sent or received.
- `role` (TEXT): Either "user" (request) or "assistant" (response).
- `content` (TEXT): The message text.

NOTE: The id column is an auto-incrementing integer that ensures each message has a unique identifier. This is the primary key in the database and is managed automatically. The user_id links messages to a specific user, allowing the application to retrieve conversation history.

### Notes

- The `instance` folder is excluded from version control (via `.gitignore`) to avoid committing the database.
- The database is created only once; subsequent runs will use the existing file unless it’s deleted.

To inspect the database, you can use a SQLite client like [DB Browser for SQLite](https://sqlitebrowser.org/) or the SQLite CLI:

```bash
sqlite3 instance/chat_history.db
sqlite> SELECT * FROM message;
```

---

## Additional Notes

- **Session Management**: If you don’t provide a `user_id`, the API generates a new UUID and includes it in the response. Reuse this `user_id` in subsequent requests to maintain conversation history.
- **Error Handling**:
  - Missing `prompt`: Returns `{"error": "Prompt is required"}` with a 400 status.
  - OpenAI API errors: Returns a 500 status with an error message.
- **Troubleshooting**:
  - Ensure your OpenAI API key is valid and has sufficient credits.
  - Check the terminal for error messages if the server fails to start.
- **Testing**: Use tools like `curl`, Postman, or a custom script to test the endpoint. Verify rate limiting by sending rapid requests and observing 429 responses.
