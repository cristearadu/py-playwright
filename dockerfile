FROM mcr.microsoft.com/playwright/python:latest

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    BASE_URL=https://www.saucedemo.com/

WORKDIR /app

COPY pyproject.toml ./
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -e . allure-pytest

COPY . .

RUN python -m playwright install --with-deps

ENV PYTEST_TESTS="tests" \
    PYTEST_WORKERS="auto" \
    RUN_BROWSER="chrome" \
    PYTEST_HEADLESS="1" \
    PYTEST_MARKERS="" \
    PYTEST_EXTRA_ARGS=""

# A small entrypoint that builds pytest CLI from env vars
RUN printf '%s\n' '#!/usr/bin/env bash' \
    'set -euo pipefail' \
    'HEADLESS_FLAG=""' \
    'if [[ "${PYTEST_HEADLESS:-}" == "1" || "${PYTEST_HEADLESS:-}" == "true" ]]; then' \
    '  HEADLESS_FLAG="--headless"' \
    'fi' \
    'MARKER_ARGS=()' \
    'if [[ -n "${PYTEST_MARKERS:-}" ]]; then' \
    '  MARKER_ARGS=(-m "${PYTEST_MARKERS}")' \
    'fi' \
    'exec pytest "${PYTEST_TESTS:-tests}" -n "${PYTEST_WORKERS:-auto}" --run-browser="${RUN_BROWSER:-chrome}" ${HEADLESS_FLAG} "${MARKER_ARGS[@]}" --alluredir=/allure-results ${PYTEST_EXTRA_ARGS:-}' \
    > /usr/local/bin/pytest-entrypoint && chmod +x /usr/local/bin/pytest-entrypoint

ENTRYPOINT ["/usr/local/bin/pytest-entrypoint"]