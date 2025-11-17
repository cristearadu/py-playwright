# Python Playwright Test Framework

End-to-end UI test framework built with **Playwright** + **pytest**, packaged for local runs, **Docker** runs, and **CI** via GitHub Actions.

---

## ✨ Features

- **Playwright + pytest** with Page Object Model (POM)
- **Parallel execution** via `pytest-xdist`
- **Typed helpers** & a shared **BasePage**
- **Testing Managers** (e.g., `SauceDemoTestingManager`) with a `UserCredentials` dataclass
- **Deterministic selectors & readiness helpers**
- **Color scheme checks** using CSS assertions
- **First-class Docker support** (no host deps needed)
- **GitHub Actions** matrix (Chrome / Firefox / Safari*), scheduled + manual dispatch

\* Safari uses Playwright **WebKit** (headless in containers).

---

## 🗂 Project structure (high level)

```
py-playwright/
├─ constants/
│  ├─ browser_types.py
│  ├─ saucedemo_constants.py
│  └─ ...
├─ pages/
│  └─ saucedemo_pages/
│     └─ saucedemo_login_page.py
├─ project_utils/
│  ├─ browser_factory.py
│  ├─ logger.py
│  └─ settings.py
├─ testing_managers/
│  ├─ base_testing_manager.py
│  └─ saucedemo_testing_manager.py
├─ tests/
│  └─ tests_saucedemo/
│     └─ test_login.py
├─ logs/
├─ pyproject.toml
├─ dockerfile
└─ .github/workflows/ci.yml
```

The framework is **multi‑app ready**. Each app gets its own `pages/<app>_pages/` and `tests/tests_<app>/` folders. For base URLs, each app owns an env variable (e.g., current app uses `SAUCEDEMO_BASE_URL`).

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
# Base URL used by the Sauce Demo suite
export SAUCEDEMO_BASE_URL="https://www.saucedemo.com/"

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
docker run --rm -e RUN_BROWSER=firefox -e PYTEST_MARKERS="login" -e PYTEST_HEADLESS=1 py-playwright:local

# Safari (WebKit; forced headless in container)
docker run --rm -e RUN_BROWSER=safari  -e PYTEST_MARKERS="login" -e PYTEST_HEADLESS=1 py-playwright:local
```

Artifacts:
- `logs/` (mounted from the container)
- `pytest.log`

---

## ⚙️ Runtime configuration (env vars)

| Variable              | Description                                                            | Example                          |
|-----------------------|------------------------------------------------------------------------|----------------------------------|
| `SAUCEDEMO_BASE_URL`  | Base URL for the Sauce Demo app under test                             | `https://www.saucedemo.com/`     |
| `RUN_BROWSER`         | `chrome` \| `firefox` \| `safari` (`safari` = WebKit)                  | `chrome`                         |
| `PYTEST_MARKERS`      | Pytest `-m` expression to filter tests                                 | `smoke or regression`            |
| `PYTEST_WORKERS`      | Parallel workers for `xdist` (`auto` or an integer)                    | `auto`                           |
| `PYTEST_HEADLESS`     | `1` to run headless, `0` for headed                                    | `1`                              |
| `PYTEST_TESTS`        | Test path/pattern                                                      | `tests`                          |

The Docker entrypoint maps these to pytest flags and to the internal `BrowserFactory`.

---

## 🏗 Architecture

The code is organized into clear layers to keep tests **readable**, **maintainable**, and **extensible** across multiple apps/pages.

### 1) Constants
- `constants/` holds enumerations and values specific to apps (e.g., selectors, color schemes).
- Example: `saucedemo_constants.py` defines stable selectors and expected UI CSS (RGB values for color assertions).

### 2) Testing Managers
- `testing_managers/` encapsulates **test data composition**.
- `UserCredentials` (`@dataclass`) is a simple, printable value object.
- `SauceDemoTestingManager` exposes:
  - Predefined users (e.g., `STANDARD`, `LOCKED_OUT`)
  - A small **compose** API for dynamic users (`compose_user(username=..., password=...)`)

### 3) Pages (POM)
- `project_utils/base_page.py` (BasePage) provides small, **synchronous** wrappers for Playwright actions and asserts:
  - navigation, typing, clicking
  - `is_visible / is_enabled / exists / attribute_equals / wait_for_disappear`
  - helpers like `check_element_is_present_and_enabled`
- App‑specific pages live under `pages/<app>_pages/`.
  - `SauceDemoLoginPage` centralizes locators, actions (e.g., `login` / `login_with_user`) and **expectations** (e.g., header visible, login button green, error banner red).

### 4) Tests
- Tests live under `tests/tests_<app>/` and **only** talk to Page Objects and managers.
- Heavily use `@pytest.mark.parametrize` for coverage and **DRY** cases (e.g., login permutations, color schemes).
- Assertions prefer **page‑level** methods over raw locators to keep tests expressive and resilient.

### 5) Utilities & Settings
- `BrowserFactory` launches the proper channel:
  - `chrome` → Chromium channel `"chrome"`
  - `firefox` → `playwright.firefox`
  - `safari` → `playwright.webkit` (forced headless in containers)
- `settings.py` reads environment (e.g., `SAUCEDEMO_BASE_URL`); `conftest.py` wires fixtures:
  - CLI/env reading
  - `playwright_instance` / `browser` / `context` / `page`
  - `base_url` fixture per app (currently Sauce Demo)
- `logger.py` configures unified console + file logging, worker‑aware when running with xdist.

### 6) Parallelization
- `pytest-xdist` with `-n auto` for speed.
- Safari/WebKit is forced to a **single worker** when required (containers / WebKit constraints).

---

## ✅ What’s covered right now

- **Sauce Demo – Login page**
  - Presence & readiness of **username**, **password**, **Login** button, and header (“Swag Labs”)
  - **Happy flow** login with a standard user (navigates away from login page)
  - **Negative** scenarios: locked out user, invalid username/password, username/password required
  - **Color scheme** checks via CSS:
    - Login button background: `#3ddc91` → `rgb(61, 220, 145)`
    - Error banner background: `#e2231a` → `rgb(226, 35, 26)`

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
