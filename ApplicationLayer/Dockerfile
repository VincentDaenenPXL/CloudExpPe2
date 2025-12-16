FROM python:3.9-slim-bullseye
WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY parameters.py ./
ENV PATH="/home/appuser/.local/bin:${PATH}"

EXPOSE 4000
CMD ["python", "app.py"]
