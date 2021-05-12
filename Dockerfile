FROM python:slim

LABEL authors = "Kirill Leontyev, Maksim Apenyshev, Andrew Aleynikov"
LABEL version = "1.0.0"

# Скачиваем зависимости проекта
RUN pip3 install vk_api==11.9.3

# Создаем директорию для приложения
WORKDIR bot_app
# Копируем файлы из директории Dockerfile в bot_app
COPY . .

# Точка запуска контейнера
ENTRYPOINT ["python3", "bot.py"]
