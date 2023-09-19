FROM python:3.10-slim as builder

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python -m pip install -U pip \
  && python -m pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry export -o requirements.txt

FROM python:3.10-slim as runtime

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

COPY . /app

RUN python -m pip install -U pip \
  && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "./handwriting_ocr/app.py"]
