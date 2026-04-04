FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

RUN apt update; apt install git -y

ADD . /app

WORKDIR /app

RUN uv sync --frozen --no-cache --no-group ruff --no-dev

ENV LLM_API_KEY=${LLM_API_KEY}
ENV USERNAME=${USERNAME}
ENV PASSWORD=${PASSWORD}
ENV SECRET=${SECRET}

ENV PATH="/app/.venv/bin:$PATH"

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
