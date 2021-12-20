FROM python:3

WORKDIR /home/bobor16/pesticides-warning-system-server/test

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./producer.py" ]