#!/bin/bash

echo "Диагностика окружения:"
echo "Текущая директория: $(pwd)"
echo "Содержимое текущей директории: $(ls -la)"
echo "Содержимое корневой директории: $(ls -la /)"

echo "Ожидание базы данных..."
until netcat -z -v -w30 db 5432; do
  echo "Ждём PostgreSQL..."
  sleep 1
done

echo "База данных доступна!"

if [ ! -d "alembic/versions" ]; then
  echo "Создание папки миграций..."
  mkdir -p alembic/versions
  alembic revision --autogenerate -m "Initial revision"
fi

echo "Применение миграций..."
alembic upgrade head

echo "Запуск бота..."
exec python3 start.py
