FROM python:3.9.7

# run plain container and check file structure
WORKDIR /usr/src/app

# copy requirements to workdir
COPY requirements.txt .

# install dependencies, don't redo this if req's unchanged
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]


