#!/usr/bin/env bash
set -e

ENVIRONMENT=${1:-dev}
PORT=${2:-8000}
WORKERS=${3:-4}

if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "test" && "$ENVIRONMENT" != "prod" ]]; then
    echo "Usage: $0 [dev|test|prod] [port] [workers]"
    exit 1
fi

echo "Environment: $ENVIRONMENT, Port: $PORT, Workers: $WORKERS"

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
# pip install gunicorn
pip install "pydantic[email]" fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv gunicorn

# Set environment
export ENV=$ENVIRONMENT
mkdir -p logs

# Initialize DB for dev/test
if [[ "$ENVIRONMENT" != "prod" ]]; then
    python - <<END
from app.db.session import create_db_and_tables
create_db_and_tables()
END
fi

# Run server
if [[ "$ENVIRONMENT" == "prod" ]]; then
    gunicorn -w $WORKERS -k uvicorn.workers.UvicornWorker app.main:app \
             --bind 0.0.0.0:$PORT \
             --access-logfile logs/gunicorn_access.log \
             --error-logfile logs/gunicorn_error.log
else
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
fi
