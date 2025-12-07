# 使用官方的 Python 3.11 作為基礎映像
FROM python:3.11-slim


# 安裝系統相依套件 + Microsoft SQL Server ODBC Driver 17
ENV TZ=Asia/Taipei
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    libssl-dev \
    libffi-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* microsoft.gpg

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 先到容器中，安裝依賴
COPY requirements.txt  /app/

# 安裝 Python 依賴包
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案的所有檔案到容器中
COPY . /app/

# 開放容器的 8501 端口
EXPOSE 8501

# 設定容器啟動時執行的命令
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]

