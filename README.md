# Django Online Judge

A web-based programming platform where users can write and submit code
in **C++**, **Java**, and **Python**, execute submissions in isolated
Docker containers, and view the results.

The project combines a Django-powered web application with containerized
code execution to provide a simple online coding and evaluation
workflow.

> **Project status:** Update the configuration, screenshots, repository
> links, and exact commands below to match your current codebase before
> publishing.

## Features

-   **Multi-language submissions** --- supports C++, Java, and Python.
-   **Docker-based execution** --- runs submitted programs inside
    language-specific containers rather than directly in the Django
    application process.
-   **Web-based coding workflow** --- users can write code, submit it,
    and inspect execution results.
-   **Django backend** --- handles application logic, submission
    processing, and communication between the web layer and execution
    environment.
-   **Persistent application data** --- uses a SQL database for
    application records (configure the database through Django
    settings).

## Architecture

The application separates the **web/application layer** from the **code
execution layer**. Django receives a submission and coordinates
execution in a Docker container configured for the selected language.

``` mermaid
flowchart TB
    U([User / Browser])

    subgraph WEB["Web application"]
        UI["Frontend<br/>HTML · CSS"]
        DJ["Django application"]
        AUTH["User & request handling"]
        SUB["Submission service"]
        DB[("SQL database<br/>Users · Problems · Submissions")]
    end

    subgraph EXEC["Code execution layer"]
        ORCH["Execution manager"]
        LANG{"Selected language"}
        CPP["C++ Docker container"]
        JAVA["Java Docker container"]
        PY["Python Docker container"]
        RESULT["Execution result<br/>stdout · stderr · exit code"]
    end

    U --> UI
    UI <--> DJ
    DJ --> AUTH
    AUTH --> SUB
    DJ <--> DB
    SUB --> ORCH
    ORCH --> LANG
    LANG -->|C++| CPP
    LANG -->|Java| JAVA
    LANG -->|Python| PY
    CPP --> RESULT
    JAVA --> RESULT
    PY --> RESULT
    RESULT --> ORCH
    ORCH --> SUB
    SUB --> DJ
    DJ --> UI
    UI --> U
```

### Submission lifecycle

1.  A user selects a problem, chooses a programming language, and
    submits source code through the web interface.
2.  Django validates the request and creates or updates the relevant
    submission record.
3.  The execution manager selects the appropriate language runtime.
4.  The source code is made available to a Docker container configured
    for that language.
5.  The container compiles the program when required and executes it
    against the supplied input.
6.  The execution layer captures the program's output and error
    information, along with its exit status.
7.  Django makes the result available to the user through the web
    interface.

### Why Docker?

Running untrusted user code directly inside the Django process or on the
host operating system is unsafe. Docker provides a separate execution
environment for each run and helps isolate submitted programs from the
web application.

For a production deployment, containers should also be configured with
appropriate security restrictions, including:

-   CPU, memory, process-count, and execution-time limits.
-   No privileged mode and no unnecessary Linux capabilities.
-   Restricted network access (ideally disabled for submitted programs).
-   Read-only base filesystems where practical and temporary
    per-submission workspaces.
-   Safe handling and cleanup of source files, binaries, and containers.
-   A non-root user inside the execution container.

**Important:** Docker is an isolation mechanism, not a complete security
boundary by itself. Do not run arbitrary submissions with unrestricted
host access.

## Technology stack

  Layer                 Technology
  --------------------- ---------------------------------------------
  Backend               Python, Django
  Frontend              HTML, CSS
  Database              SQL database (configure in Django settings)
  Code execution        Docker
  Supported languages   C++, Java, Python

## Getting started

### Prerequisites

Install the following before running the project:

-   Python 3
-   pip
-   Docker Engine or Docker Desktop
-   Git
-   A SQL database supported by your Django configuration

Verify the installations:

``` bash
python --version
pip --version
docker --version
docker info
```

### 1. Clone the repository

``` bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

### 2. Create and activate a virtual environment

``` bash
python -m venv .venv
```

Activate it:

**Linux / macOS**

``` bash
source .venv/bin/activate
```

**Windows PowerShell**

``` powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the project has a `requirements.txt` file:

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file (or configure the variables using your deployment
environment). Typical settings include:

``` env
SECRET_KEY=replace-with-a-secure-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Add the database settings required by your project.
# Never commit production credentials or secret keys.
```

Make sure Django is configured to load these values. The variable names
above are examples; use the names expected by your settings module.

### 5. Apply database migrations

``` bash
python manage.py migrate
```

If your project uses Django's admin interface, create an administrator
account:

``` bash
python manage.py createsuperuser
```

### 6. Start Docker

Ensure the Docker daemon is running and that the account executing
Django can access it.

``` bash
docker info
```

The execution component must be able to invoke Docker and access the
required language images. Build or pull the images expected by your
execution code before testing submissions.

### 7. Run the Django development server

``` bash
python manage.py runserver
```

Open:

``` text
http://127.0.0.1:8000/
```

> The commands above are a general Django setup. Your actual settings
> module, environment variable names, image names, and Docker invocation
> may differ.

## Example execution flow

A submission typically follows this pattern:

``` text
Source code + selected language
             |
             v
       Django backend
             |
             v
     Execution manager
             |
             v
   Language-specific Docker
       /      |       \
     C++    Java    Python
       \      |       /
             v
     Captured execution result
             |
             v
        Django response
             |
             v
        Result in UI
```

For compiled languages such as C++, the container generally compiles the
source before executing the resulting binary. Java submissions generally
require compilation before running the generated class. Python source
can be interpreted directly.

## Suggested repository structure

The exact structure depends on the current implementation. A typical
organization could look like this:

``` text
online-judge/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── <django_project>/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── <judge_app>/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   └── execution.py
│   └── templates/
├── static/
└── docker/
    ├── cpp/
    ├── java/
    └── python/
```

Replace the placeholders with the actual app and directory names in your
repository.

## Security and operational considerations

Because the platform executes user-provided code, execution safety is a
core design concern.

-   Never use `shell=True` with user-controlled input.
-   Pass arguments safely and validate the selected language against an
    allowlist.
-   Apply execution timeouts and terminate processes that exceed them.
-   Apply Docker resource limits and avoid privileged containers.
-   Do not mount sensitive host directories or expose the Docker socket
    to submitted code.
-   Keep application secrets and database credentials outside source
    control.
-   Clean up temporary files and containers after execution, including
    when execution fails.
-   Treat compiler output, standard output, and standard error as
    untrusted data when displaying them in the browser.

## Future improvements

-   Add per-test-case evaluation with expected-output comparison.
-   Return verdicts such as Accepted, Wrong Answer, Compilation Error,
    and Time Limit Exceeded.
-   Add configurable CPU and memory limits for each submission.
-   Move execution to a background task queue for better scalability.
-   Add submission history, execution metrics, and structured logs.
-   Add automated tests for language-specific compile and run workflows.

## Contributing

Contributions and suggestions are welcome.

1.  Fork the repository.
2.  Create a feature branch.
3.  Make your changes and add tests where appropriate.
4.  Open a pull request describing the change.

## License

Add the license applicable to this project (for example, MIT) before
distributing the repository.
