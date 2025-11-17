FROM mcr.microsoft.com/playwright/python:latest

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    BASE_URL=https://www.saucedemo.com/

WORKDIR /app

COPY pyproject.toml ./
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -e .

COPY . .

RUN python -m playwright install --with-deps

# -------- Runtime-configurable defaults for pytest --------
# Leave PYTEST_TESTS empty to rely on pytest.ini/pyproject [tool.pytest.ini_options].
# You can still override it with e.g. PYTEST_TESTS="tests tests_extra"
ENV PYTEST_TESTS="" \
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
    'TARGETS=()' \
    'if [[ -n "${PYTEST_TESTS:-}" ]]; then' \
    '  # allow multiple, space-separated targets' \
    '  read -r -a TARGETS <<< "${PYTEST_TESTS}"' \
    'fi' \
    'exec pytest "${TARGETS[@]}" -n "${PYTEST_WORKERS:-auto}" --run-browser="${RUN_BROWSER:-chrome}" ${HEADLESS_FLAG} "${MARKER_ARGS[@]}" ${PYTEST_EXTRA_ARGS:-}' \
    > /usr/local/bin/pytest-entrypoint && chmod +x /usr/local/bin/pytest-entrypoint

ENTRYPOINT ["/usr/local/bin/pytest-entrypoint"]