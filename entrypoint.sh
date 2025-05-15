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

echo "Запуск Backend."
exec python3 tmp.py
