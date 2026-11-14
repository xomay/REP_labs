ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "lab3.py", "/out"]