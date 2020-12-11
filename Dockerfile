FROM python:3.6
RUN python -m pip install --upgrade pip
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
