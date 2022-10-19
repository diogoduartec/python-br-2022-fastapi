## Setup

### Set up venv (optional)
Install virtual env
```bash
pip install virtualenv
```

Creating virtual env
```bash
virtualenv venv
```

Activate virtual env
```bash
source venv/bin/activate
```

### Install dependencies
From requirements file
```bash
pip install -r requirements.txt
```

Or
```bash
pip install fastapi mongomock aiohttp pymongo uvicorn requests
```

### Run the project
```bash
uvicorn app:app --port 8080 --reload
```