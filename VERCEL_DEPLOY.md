# 🚀 Деплой мини-приложения на Vercel

## Быстрый старт

1. **Зарегистрируйтесь на Vercel:**
   - Откройте https://vercel.com
   - Нажмите "Sign Up"
   - Войдите через GitHub

2. **Создайте новый проект:**
   - Нажмите "Add New" → "Project"
   - Выберите репозиторий `telegram-bot`
   - Нажмите "Import"

3. **Настройки проекта:**
   - Framework Preset: **Other**
   - Root Directory: оставьте пустым
   - Build Command: оставьте пустым
   - Output Directory: `webapp`
   - Install Command: оставьте пустым

4. **Deploy:**
   - Нажмите "Deploy"
   - Подождите 1-2 минуты

5. **Получите URL:**
   - После деплоя скопируйте URL (например, `https://telegram-bot-xxx.vercel.app`)

6. **Обновите бота:**
   - Откройте файл `bot.py`
   - Найдите строку с `WEBAPP_URL`
   - Замените на ваш Vercel URL

## Готово!

Теперь мини-приложение доступно по HTTPS и работает с ботом!

## Обновление

При каждом `git push` Vercel автоматически обновит приложение.
