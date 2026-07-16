# 1. Base image
FROM python:3.10-slim

# 2. Working directory
WORKDIR /app

# 3. Copy project files
COPY . .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose Streamlit port
EXPOSE 8501

# 6. Launch Streamlit app
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]