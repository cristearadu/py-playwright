# Python Playwright Test Framework

End-to-end UI test framework built with **Playwright** + **pytest**, packaged for local runs, **Docker** runs, and **CI** via GitHub Actions.

---

## ✨ Features

- **Playwright + pytest** with Page Object Model (POM)
- **Parallel execution** via `pytest-xdist` (`-n auto`)
- **Typed helpers** & a shared **BasePage**
- **Testing Managers** (e.g., `SauceDemoTestingManager`) with a `UserCredentials` dataclass
- **Deterministic selectors & readiness helpers**
- **Color scheme checks** using CSS assertions
- **First-class Docker support** (no host deps needed)
- **GitHub Actions** matrix (Chrome / Firefox / Safari\*), scheduled + manual dispatch
- **Multi‑app ready**: Sauce Demo, Rahul Shetty **Practice**, and The Internet (**Herokuapp**) — *currently implemented: Drag &amp; Drop, Dynamic Controls*

\* Safari uses Playwright **WebKit** (headless in containers).

---

## 🗂 Project structure (high level)

```
py-playwright/
├─ constants/
│  ├─ browser_types.py
│  ├─ timeouts.py
│  └─ saucedemo_constants.py
├─ pages/
│  ├─ base_page.py
│  ├─ heroku_app_pages/
│  │  ├─ __init__.py
│  │  ├─ heroku_home_page.py
│  │  ├─ heroku_app_drag_and_drop_page.py
│  │  └─ heroku_app_dynamic_controlls_page.py
│  ├─ practice_pages/
│  │  └─ practice_home_page.py
│  └─ saucedemo_pages/
│     ├─ saucedemo_base_page.py
│     ├─ saucedemo_inventory_page.py
│     └─ saucedemo_login_page.py
├─ project_utils/
│  ├─ browser_factory.py
│  ├─ logger.py
│  └─ settings.py
├─ testing_managers/
│  ├─ base_testing_manager.py
│  └─ saucedemo_testing_manager.py
├─ tests/
│  ├─ tests_saucedemo/
│  │  ├─ conftest.py
│  │  ├─ test_login.py
│  │  └─ test_cases/
│  │     └─ login_cases.py
│  ├─ tests_practice_home/
│  │  ├─ conftest.py
│  │  ├─ test_practice.py
│  │  └─ test_cases/
│  │     └─ practice_cases.py
│  └─ tests_heroku_app/
│     ├─ conftest.py
│     ├─ test_drag_and_drop.py
│     ├─ test_dynamic_controls.py
│     └─ test_cases/
│        └─ heroku_cases.py
├─ .env
├─ logs/
├─ pyproject.toml
├─ dockerfile
└─ .github/workflows/ci.yml
```

Each app has its own `pages/<app>_pages/` and `tests/tests_<app>/` folders. Base URLs are configured per app via env vars (see below).

---

## 🚀 Quick start

### 1) Local (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip

# Install the project (uses pyproject.toml)
pip install -e .

# Optional: install playwright browsers if not already present
python -m playwright install
```

Run tests:

```bash
# Base URLs used by the suites
export SAUCEDEMO_BASE_URL="https://www.saucedemo.com/"
export PRACTICE_BASE_URL="https://rahulshettyacademy.com/AutomationPractice/"
export HEROKU_BASE_URL="https://the-internet.herokuapp.com/"

# Pick a browser: chrome | firefox | safari  (safari = webkit)
export RUN_BROWSER=chrome

# Headless mode: 1 to enable, 0 to disable
export PYTEST_HEADLESS=1

# Run a selection (examples)
pytest -m "login" -n auto
pytest -m "regression" -n auto
```

> The suite relies on env vars (see **Runtime configuration** below).

#### Parallel runs (`pytest -n auto`)

Common commands:
```bash
# Run everything in parallel
pytest -n auto

# Only smoke tests in parallel
pytest -m "smoke" -n auto

# Regression suite in parallel
pytest -m "regression" -n auto

# Specific file in parallel
pytest tests/tests_saucedemo/test_login.py -n auto

# Pick a browser + parallel
RUN_BROWSER=firefox pytest -n auto
```

---

### 2) Docker (recommended & reproducible)

Build:

```bash
docker build -t py-playwright:local .
```

Run:

```bash
docker run --rm \
  -e SAUCEDEMO_BASE_URL="https://www.saucedemo.com/" \
  -e PRACTICE_BASE_URL="https://rahulshettyacademy.com/AutomationPractice/" \
  -e HEROKU_BASE_URL="https://the-internet.herokuapp.com/" \
  -e RUN_BROWSER="chrome" \
  -e PYTEST_MARKERS="regression" \
  -e PYTEST_WORKERS="auto" \
  -e PYTEST_HEADLESS="1" \
  -e PYTEST_TESTS="tests" \
  -v "$PWD/logs:/app/logs" \
  -v "$PWD/pytest.log:/app/pytest.log" \
  py-playwright:local
```

Examples:

```bash
# Firefox
docker run --rm \
  -e RUN_BROWSER=firefox \
  -e PYTEST_MARKERS="login" \
  -e PYTEST_HEADLESS=1 \
  py-playwright:local

# Safari (WebKit; forced headless in container)
docker run --rm \
  -e RUN_BROWSER=safari \
  -e PYTEST_MARKERS="login" \
  -e PYTEST_HEADLESS=1 \
  py-playwright:local
```

Artifacts:
- `logs/` (mounted from the container)
- `pytest.log`

---

## ⚙️ Runtime configuration (env vars)

| Variable              | Description                                                            | Example                                      |
|-----------------------|------------------------------------------------------------------------|----------------------------------------------|
| `SAUCEDEMO_BASE_URL`  | Base URL for the Sauce Demo app under test                             | `https://www.saucedemo.com/`                 |
| `PRACTICE_BASE_URL`   | Base URL for Rahul Shetty Practice site                                | `https://rahulshettyacademy.com/AutomationPractice/` |
| `HEROKU_BASE_URL`     | Base URL for The Internet (Herokuapp)                                  | `https://the-internet.herokuapp.com/`        |
| `RUN_BROWSER`         | `chrome` \| `firefox` \| `safari` (`safari` = WebKit)                  | `chrome`                                     |
| `PYTEST_MARKERS`      | Pytest `-m` expression to filter tests                                 | `smoke or regression`                        |
| `PYTEST_WORKERS`      | Parallel workers for `xdist` (`auto` or an integer)                    | `auto`                                       |
| `PYTEST_HEADLESS`     | `1` to run headless, `0` for headed                                    | `1`                                          |
| `PYTEST_TESTS`        | Test path/pattern                                                      | `tests`                                      |

The Docker entrypoint maps these to pytest flags and to the internal `BrowserFactory`.

---

## 🏗 Architecture

Organized into clear layers to keep tests **readable**, **maintainable**, and **extensible** across multiple apps.

### 1) Constants
- `constants/` holds enums and app-specific values (selectors, color schemes).
- Example: `saucedemo_constants.py` defines stable selectors and expected UI CSS (RGB values for color assertions).

### 2) Testing Managers
- `testing_managers/` encapsulates **test data composition**.
- `UserCredentials` (`@dataclass`) is a simple, printable value object.
- `SauceDemoTestingManager` exposes:
  - Predefined users (e.g., `STANDARD`, `LOCKED_OUT`)
  - A small **compose** API for dynamic users (`compose_user(username=..., password=...)`)

### 3) Pages (POM)
- `pages/base_page.py` (BasePage) provides small, **synchronous** wrappers for Playwright actions and asserts:
  - navigation, typing, clicking, waiting
  - `is_visible / is_enabled / exists / attribute_equals / wait_for_disappear`
  - built-in helpers: `check_element_is_present_and_enabled`, `wait_until_editable`
  - ergonomic locator helpers: `by_role(...)`, `by_label(...)`, `by_placeholder(...)`, `by_test_id(...)`, `first(...)`, `nth(...)`, `filter_has_text(...)`
  - scroll helpers that work across browsers (fallbacks for Firefox when needed)
- App‑specific pages live under `pages/<app>_pages/`.
  - **SauceDemo**: `saucedemo_login_page.py`, `saucedemo_inventory_page.py` (base page in `saucedemo_base_page.py`)
  - **Practice Home**: `practice_home_page.py`
  - **Herokuapp**: `heroku_home_page.py`, `heroku_app_drag_and_drop_page.py`, `heroku_app_dynamic_controlls_page.py`

### 4) Tests
- Tests live under `tests/tests_<app>/` and **only** talk to Page Objects and managers.
- Heavy `@pytest.mark.parametrize` usage for coverage and **DRY** scenarios (login permutations, color schemes, etc.).
- Assertions prefer **page‑level** methods over raw locators to keep tests expressive and resilient.

### 5) Utilities & Settings
- `BrowserFactory` launches the proper channel:
  - `chrome` → Chromium channel `"chrome"`
  - `firefox` → `playwright.firefox`
  - `safari` → `playwright.webkit` (forced headless in containers)
- `settings.py` reads environment (`SAUCEDEMO_BASE_URL`, `PRACTICE_BASE_URL`, `HEROKU_BASE_URL`); `conftest.py` wires fixtures:
  - `playwright_instance` / `browser` / `context` / `page`
  - per‑app base URL fixtures (e.g., `saucedemo_base_url`, `practice_base_url`, `heroku_base_url`)
  - ready‑to‑use page fixtures (e.g., `saucedemo_page`, `practice_home_page`, `heroku_home_page`)
- `logger.py` configures unified console + file logging, worker‑aware for xdist.

### 6) Parallelization
- `pytest-xdist` with `-n auto` for speed.
- Safari/WebKit is forced to a **single worker** when required (containers / WebKit constraints).

---

## ✅ What’s covered right now

- **Sauce Demo – Login page**
  - Presence & readiness of **username**, **password**, **Login** button, and header (“Swag Labs”)
  - **Happy flow** with a standard user (navigates away from login page)
  - **Negative** scenarios: locked out user, invalid username/password, username/password required
  - **Color scheme** checks via CSS:
    - Login button background: `#3ddc91` → `rgb(61, 220, 145)`
    - Error banner background: `#e2231a` → `rgb(226, 35, 26)`

- **Practice site – Examples**
  - Hide/Show text field scenario
  - Alert/Confirm dialog handling
  - Mouse hover menu
  - iFrame actions
  - Web tables parsing & assertions

- **Herokuapp – Implemented now**
  - Drag &amp; Drop
  - Dynamic Controls

---

## 🧪 Markers

Defined in `pyproject.toml`:

- `smoke` – quick sanity checks
- `regression` – full/extended checks
- `login` – login-related scenarios
- `color_scheme` – CSS/visual checks

Examples:

```bash
pytest -m "smoke"
pytest -m "login or color_scheme" -n auto
```

---

## 🤖 CI (GitHub Actions)

Workflow: `.github/workflows/ci.yml`

- **On push / PR to `main`** → runs **regression** in Docker across browsers (Chrome / Firefox / Safari).
- **Scheduled** 3× daily (UTC): `06:00`, `14:00`, `22:00`.
- **Manual dispatch** with inputs:
  - `browser` (chrome | firefox | safari)
  - `markers` (pytest `-m` expression)
  - `headless` (true/false)
  - `tests_path`
  - `workers` (e.g., `auto`)

Artifacts uploaded:
- `pytest.log`
- `logs/` directory

> Note: Safari = WebKit (forced headless).

---

## 🛠 Troubleshooting

- **“no tests ran”**  
  You probably filtered everything with `PYTEST_MARKERS` or a wrong `PYTEST_TESTS` path. Drop the filter and re-run.

- **Safari/WebKit: “cannot open display”**  
  You’re launching headed WebKit in a container. The `BrowserFactory` forces headless when `DISPLAY` is absent. Ensure `PYTEST_HEADLESS=1`.

- **Firefox didn’t scroll to element**  
  Use the BasePage’s scroll helpers (they add small fallbacks), or ensure the element is scrolled with `element.scroll_into_view_if_needed()` before interacting.