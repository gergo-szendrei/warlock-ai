FROM python:3.12-slim AS build
COPY ./requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && python -m pip install --prefix=/install -r requirements.txt \
    && apt-get remove -y gcc libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /install /usr/local

WORKDIR /app
COPY . .

CMD ["uvicorn", "app:application", "--host", "0.0.0.0", "--port", "8123", "--proxy-headers"]
