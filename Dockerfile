FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install fastapi sqlalchemy pydantic starlette jose passlib python-decouple

EXPOSE 8000

CMD ["uvicorn", "main:app"]

ENTRYPOINT ["uvicorn", "main:app"]