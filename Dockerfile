FROM python:3.12-slim AS build
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
COPY --from=build /install /usr/local
RUN apt-get update

WORKDIR /app
COPY . .
CMD ["uvicorn", "app:application", "--host", "0.0.0.0", "--port", "8123", "--proxy-headers"]
