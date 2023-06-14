# Menggunakan image Python sebagai base image
FROM python:3.9

# Menentukan direktori kerja di dalam container
ENV APP_HOME /app
WORKDIR $APP_HOME

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstal dependensi yang diperlukan
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Menyalin seluruh isi direktori proyek ke dalam container
COPY . ./

# Menjalankan perintah untuk menjalankan aplikasi Flask
CMD ["python", "main.py"]

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
