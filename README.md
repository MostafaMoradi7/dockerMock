# DockerMock - Django REST API for Managing Docker Containers

DockerMock is a Django-based REST API project that provides endpoints for creating, managing, and monitoring Docker containers. It allows users to send JSON data to the server, which is then used to create, run, delete, modify containers, and execute Docker commands. This README provides an overview of the project, installation instructions, and usage examples.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## Features

- Create and manage Docker containers via REST API.
- View a list of all created containers.
- Start, stop, and delete containers.
- Retrieve container logs and historical actions.
- Customizable Docker container creation parameters.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Docker installed and running.

## Installation

Follow these steps to set up and run the DockerMock project locally:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/MostafaMoradi7/dockerMock.git
   cd DockerMock
   ```

2. Create a virtual environment and activate it (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Your DockerMock API should now be accessible at `http://localhost:8000/`.

## Usage

To use the DockerMock API, you can send JSON data to the server to create and manage Docker containers. Here's an example of creating a container:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "new-container", "image_address": "hub.hamdocker.ir/nginx:1:21", "envs": {"key1": "value1"}, "command": "sleep 1000"}' http://localhost:8000/apps/
```

For detailed API documentation and endpoints, please refer to the [API Endpoints](#api-endpoints) section below.

## API Endpoints

- `/api/apps/` (GET): Get a list of created containers.
- `/api/apps/` (POST): Post a json to the server and create a docker container.
- `/api/apps/<container_id>/` (GET): Retrieve a specific container.
- `/api/apps/<container_id>/` (PUT): Update a specific container (NAME must change).
- `/api/apps/<container_id>/` (PATCH): STOP or RUN a specific container.
- `/api/apps/<container_id>/` (DELETE): Delete a specific container.
- `/api/history/` (GET): List all historical actions.

For more details on request and response formats, refer to the spectaculare documentation in which is available through the api endpoints of the project.

## Contributing

Contributions to DockerMock are welcome! You can contribute by:

- Reporting issues or suggesting improvements by opening issues.
- Submitting pull requests for bug fixes or new features.
- Providing feedback and ideas to enhance the project.

Please follow the [Contributing Guidelines](CONTRIBUTING.md) for more information.
