FROM python:3.10  

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]