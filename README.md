# paas-cluster-test

A simple dockerized Python Flask application designed to test Kubernetes deployments with environment variables and persistent volumes (PVC).

## Features

- **Environment Variable Display**: Reads and displays the `TEST_ENV_VAR` environment variable
- **Interactive Message Form**: Allows users to write and update a custom message through the web interface
- **Persistent Volume Testing**: Writes and reads JSON data to/from the filesystem to test PVC functionality
- **Restart Counter**: Tracks how many times the application has been restarted
- **Interactive UI**: Clean web interface showing all relevant information

## Running the Application

### Using Docker

Build the Docker image:
```bash
docker build -t paas-cluster-test .
```

Run the container with environment variable:
```bash
docker run -p 8080:8080 -e TEST_ENV_VAR="Hello from Docker" paas-cluster-test
```

Run with mounted volume for persistence testing:
```bash
docker run -p 8080:8080 \
  -e TEST_ENV_VAR="Hello from Docker" \
  -e DATA_DIR=/data \
  -v $(pwd)/data:/data \
  paas-cluster-test
```

Access the application at: `http://localhost:8080/`

### Running Locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
export TEST_ENV_VAR="My Test Value"
python app.py
```

Access the application at: `http://localhost:8080/`

## Testing Persistent Volume Behavior

1. **Set a custom message**: Open the app in your browser and enter a message in the form
2. **Save the message**: Click the "Save Message" button
3. **Restart the pod/container**: Stop and restart the application
4. **Verify persistence**: The message should still be visible after restart, and the restart counter should increment

This workflow allows you to verify that your PVC is properly mounted and data persists across pod restarts.

## Kubernetes Deployment

When deploying to Kubernetes, you can test:

1. **Environment Variables**: Set `TEST_ENV_VAR` in your deployment manifest
2. **Persistent Volumes**: Mount a PVC to `/data` in the container

Example deployment snippet:
```yaml
env:
  - name: TEST_ENV_VAR
    value: "Kubernetes Test"
  - name: DATA_DIR
    value: "/data"
volumeMounts:
  - name: app-data
    mountPath: /data
```

The application will:
- Display the value of `TEST_ENV_VAR`
- Allow users to write/update a custom message via web form
- Create and persist `app_data.json` in the mounted volume
- Increment a restart counter each time the pod restarts
- Show the timestamp of first start and last restart

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `TEST_ENV_VAR` | `NOT SET` | A test environment variable to display |
| `DATA_DIR` | `./data` | Directory for persistent data storage |

## Data Persistence

The application stores data in `app_data.json` with the following structure:
```json
{
  "first_started": "2025-11-19T13:43:01.225768",
  "restart_count": 2,
  "last_restart": "2025-11-19T13:44:22.918563",
  "user_message": "Your custom message here",
  "message_updated": "2025-11-19T13:44:07.553996"
}
```

This allows you to verify that:
- Data persists across pod restarts
- PVC is properly mounted and writable
- Application state is maintained
- User-generated content survives container recreation