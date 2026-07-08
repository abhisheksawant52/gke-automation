# Slim single-stage image packaging the gke-automate CLI.
FROM python:3.12-slim

# Do not write .pyc files; flush stdout/stderr immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the package first (leverages layer caching).
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir .

# Run as a non-root user.
RUN useradd --create-home --uid 10001 automation
USER automation

ENTRYPOINT ["gke-automate"]
CMD ["--help"]
