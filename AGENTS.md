# Agent Instructions

When modifying code in this repository:

- Always run `pytest -q` after changes.
- Attempt to build and run the Docker image to ensure the server starts:
  ```bash
  docker build -t powerbi-mcp .
  docker run --rm -e OPENAI_API_KEY=dummy powerbi-mcp timeout 5 python src/server.py
  ```
  It's OK if these commands fail in the sandbox, but make a best effort.
