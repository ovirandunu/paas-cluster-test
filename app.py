from flask import Flask
import os
import json
from datetime import datetime

app = Flask(__name__)

# Path for persistent storage (can be mounted to PVC in k8s)
# Use /data for k8s deployments, or ./data for local development
DATA_DIR = os.getenv('DATA_DIR', './data')
DATA_FILE = os.path.join(DATA_DIR, 'app_data.json')

def ensure_data_dir():
    """Ensure the data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def read_persisted_data():
    """Read data from persistent storage"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        return {"error": f"Failed to read data: {str(e)}"}

def write_persisted_data(data):
    """Write data to persistent storage"""
    try:
        ensure_data_dir()
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        return False

def initialize_data():
    """Initialize data file if it doesn't exist"""
    existing_data = read_persisted_data()
    if existing_data is None:
        initial_data = {
            "first_started": datetime.now().isoformat(),
            "restart_count": 1,
            "last_restart": datetime.now().isoformat()
        }
        write_persisted_data(initial_data)
    else:
        # Increment restart count
        if "restart_count" in existing_data:
            existing_data["restart_count"] += 1
        else:
            existing_data["restart_count"] = 1
        existing_data["last_restart"] = datetime.now().isoformat()
        write_persisted_data(existing_data)

@app.route('/')
def hello_world():
    # Read environment variable
    test_env_var = os.getenv('TEST_ENV_VAR', 'NOT SET')
    
    # Read persisted data
    persisted_data = read_persisted_data()
    
    # Build HTML response
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PaaS Cluster Test App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
            }}
            .section {{
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
                border-left: 4px solid #4CAF50;
            }}
            .label {{
                font-weight: bold;
                color: #666;
            }}
            .value {{
                color: #333;
                margin-top: 5px;
            }}
            pre {{
                background-color: #eee;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 PaaS Cluster Test Application</h1>
            
            <div class="section">
                <div class="label">Environment Variable (TEST_ENV_VAR):</div>
                <div class="value">{test_env_var}</div>
            </div>
            
            <div class="section">
                <div class="label">Persistent Volume Data:</div>
                <div class="value">
                    <pre>{json.dumps(persisted_data, indent=2) if persisted_data else "No data found"}</pre>
                </div>
            </div>
            
            <div class="section">
                <div class="label">Data File Location:</div>
                <div class="value">{DATA_FILE}</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    # Initialize data on startup
    initialize_data()
    app.run(host='0.0.0.0', port=8080)
