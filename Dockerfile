FROM python:3.10


RUN apt-get update
RUN apt-get install poppler-utils ffmpeg libsm6 libxext6 -y
RUN apt-get install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
COPY . /code/
