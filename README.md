# ResearchFlow AI

A small AI research assistant API. Submit a topic to receive a structured response with a summary, key points, assumptions, and suggested follow-up questions. The response is generated with Google Gemini and checked for completeness, with a retry if needed.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A Google AI API key

## Run locally

Install the project dependencies:

```bash
uv sync
```

Set your Google API key in the environment or in a `.env` file at the project root:

```dotenv
GOOGLE_API_KEY=your-api-key
```

Start the API:

```bash
uv run uvicorn app.main:app --reload
```

The server listens at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

## API

### `GET /health`

Returns `{"status":"ok"}` when the service is running.

### `POST /research`

Request:

```json
{
  "topic": "How do solar panels work?"
}
```

The `topic` must be between 3 and 500 characters. A successful response contains:

```json
{
  "topic": "How do solar panels work?",
  "summary": "A concise overview.",
  "key_points": ["A key finding."],
  "assumptions": "The requested overview is general.",
  "follow_up_questions": ["How are panels tested for efficiency?"]
}
```

The endpoint requires `GOOGLE_API_KEY`. Requests without a configured key return `500`; AI provider failures return `502`.

## Tests

```bash
uv run --group dev pytest
```

## Docker

Build and run the service from the repository root:

```bash
docker build -t researchflow-ai .
docker run --rm -p 8000:8000 --env-file .env researchflow-ai
```
