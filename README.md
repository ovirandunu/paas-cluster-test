# paas-cluster-test

A simple dockerized Python Flask application that returns "Hello World" at the root path.

## Running the Application

### Using Docker

Build the Docker image:
```bash
docker build -t hello-world-app .
```

Run the container:
```bash
docker run -p 8080:8080 hello-world-app
```

Access the application at: `http://localhost:8080/`

### Running Locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python app.py
```

Access the application at: `http://localhost:8080/`