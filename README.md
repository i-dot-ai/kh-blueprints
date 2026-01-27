# Knowledge Hub Components Repository

This repository provides templates for building reusable AI components, alongside example applications demonstrating their integration.
The goal is to facilitate rapid development of AI-powered solutions by leveraging modular, customisable, containerised services.

How you use this repo depends on what you wish to do:
* If you would like to make use of the template components and/or applications, please go straight to the [User Guide](#user-guide).
* If you would like more direct ability to customise the components, you might prefer to go to the [Development Guide](\development-guide) and run the modify the component and application code directly.
* If you have built a component or application that you would like to allow others to reuse, please consider contributing it back to the community by submitting a pull request. Go to [Development Guide](#development-guide) for how to get started.

## User Guide

In order to employ the components and template applications provided in this repository, it is not necessary to clone the entire repository. Instead, you have two options:
1. **Template Application**: You can directly use the template applications available in the `applications/` directory. These applications are designed to showcase how to integrate and utilize the components effectively. By simply copying the relevant `docker-compose.yaml` files from the desired application directory, you can set up and run the application in your own environment without needing the full repository.
2. **Individual Components**: If you are interested in using specific components, you can write your own `docker-compose.yaml` file that references the components you wish to use and pulls the docker images as required. This allows you to tailor the setup to your specific needs without the overhead of the entire repository.

### Applications

To get started with the template applications, navigate to the `applications/` directory and select the application you wish to use. Each application contains a `docker-compose.yaml` file that defines the services and components it utilizes.

Ensure you have Docker, Docker Desktop (or equivalent) and Docker Compose installed on your system. You can then run the application by executing the following command in the terminal from the application's directory:

```bash
docker compose up -d
```

This will initiate the process of pulling the necessary images and starting the services defined in the `docker-compose.yaml` file. When the containers run, they will write customisable code into the mounted volumes, allowing you to modify and extend the functionality as needed. For example:

```bash
$ cp applications/mcp_datastore/docker-compose.yaml .
$ docker compose up -d
$ ls data/*/*
data/vector_db/config:
config.yaml

data/vector_db/plugins:
example_plugin.py

data/data_ingestor/config:
config.yaml

data/data_ingestor/parsers:
base.py         html_parser.py  __init__.py

data/data_ingestor/embedders:
base.py         qdrant_embedder.py  __init__.py
```

Each component mounts a single `custom` directory where defaults are copied on first run. Users can modify these files to customize behaviour:
- **vector_db**: `config/` for Qdrant settings, `plugins/` for startup scripts
- **data_ingestor**: `config/` for settings, `parsers/` and `embedders/` for custom code

### Components

The following components are available:

| Component | Description | Documentation |
|-----------|-------------|---------------|
| [vector_db](components/vector_db/) | Qdrant vector database with plugin support | [README](components/vector_db/README.md) |
| [data_ingestor](components/data_ingestor/) | Content ingestion and embedding | [README](components/data_ingestor/README.md) |

Individual components can be used by creating a custom `docker-compose.yaml` file that references the desired component images. Below is an example of how to define a service using a component:

```yaml
version: '3.8'
services:
    my_component_service:
        image: ghcr.io/knowledge-hub/components/<component-a>:latest
        container_name: my_component_service
        ports:
            - "8080:8080"
        volumes:
            - ./data/my_component:/app/data
        environment:
            - CONFIG_PATH=/app/data/config.yaml
```

## Development Guide

If you wish to add or develop entirely new components or applications, or build off the source code directly, you can clone the entire repository. The structure is as follows:

```
.
├── applications/               # Application implementations using components
│   ├── <application-a>/        # Example application 1
│   │   ├── docker-compose.yaml # Application-specific service definitions
│   ├── <application-b>/        # Example application 2
├── components/                 # Independent service components
│   └── <component-a>/          # Example component service
│       ├── src/                # Application source code
│       ├── Dockerfile          # Component build definition
│       └── entrypoint.sh       # Container startup script
├── tests/                      # Test infrastructure
│   ├── applications/           # Application integration tests
│   │   └── test_<application-a>.py
│   ├── components/             # Component container tests (require Docker)
│   │   └── test_<component-a>.py
│   ├── unit/                   # Unit tests (no Docker needed)
│   │   └── test_<component-a>.py
│   ├── test_utils.py           # Shared testing utilities
│   └── conftest.py             # Pytest fixtures
├── .github/workflows/          # CI/CD pipeline definitions
├── docker-compose.yaml         # Local dev environment setup
└── LICENSE
```

The `components/` directory contains modular services that can be independently developed, tested, and deployed. The `applications/` directory showcases how these components can be orchestrated to build complete AI solutions.

### Quick Start

1. Ensure Docker and Docker Compose are installed on your system, along with Docker Desktop (or equivalent).

2. **Build and start services**:
   ```bash
   docker compose build <component-a>
   ```

3. **Launch the component**:
   ```bash
   docker compose up -d <component-a>
   ```

4. **Run tests**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   # Individual component tests
   ./run_tests.sh component <component-a>
   # Individual application tests
   ./run_tests.sh application <application-a>
   ```

5. **Customise/add new components**:
   - Create new services by adding `components/<component-new>/Dockerfile` and `entrypoint.sh`
   - Add/modify source code in `components/<component-a>/src/`
   - Add tests for new functionality under `tests/components/`

6. **Customise/add new application templates**:
   - Create new directories under `applications/`
   - Define services in `docker-compose.yaml` files
   - Add application-specific tests under `tests/applications/`


### Testing


#### Run tests locally

```bash
# Run unit tests (no Docker needed)
./run_tests.sh unit

# Run component tests (starts service automatically)
./run_tests.sh component vector_db

# Run application tests
./run_tests.sh application mcp_datastore
```

#### Adding new tests

Tests are written using `pytest`. To add new tests:
1. Add unit tests under `tests/unit/` named `test_<component_name>.py`
2. Add component tests under `tests/components/` named `test_<component_name>.py`
3. Add application tests under `tests/applications/` named `test_<application_name>.py`

### CI/CD Pipelines


The CI system runs three pipelines, each publishing test results directly on PRs:

1. **Unit Tests** (`.github/workflows/unit-tests.yml`):
   - Triggered on push to main and PRs
   - Runs all unit tests (no Docker needed)

2. **Component Build & Test** (`.github/workflows/component-build-test.yml`):
   - Triggered on push to main and PRs
   - Builds Docker images for all components
   - Runs component container tests

3. **Application Test** (`.github/workflows/application-test.yml`):
   - Runs after successful component builds
   - Tests full application stacks using built components

## Contributing

1. Create feature branches from `main`
2. Include tests for new functionality
3. Verify all GitHub Actions pass
4. Maintain documentation updates

See [LICENSE](LICENSE) for terms.
