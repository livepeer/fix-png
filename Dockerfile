FROM python:3
RUN pip install Pillow requests
ADD fix.py fix.py
EXPOSE 80
ENTRYPOINT ["python3", "fix.py"]
