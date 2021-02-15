FROM gorialis/discord.py

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "roof_pool.py"]
