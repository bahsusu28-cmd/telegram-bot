# 🚀 Деплой бота на Railway

## Быстрый старт (5 минут)

### 1. Подготовка

1. Зарегистрируйтесь на https://railway.app (через GitHub)
2. Создайте репозиторий на GitHub для вашего бота

### 2. Загрузка кода на GitHub

```bash
# Инициализируйте git (если еще не сделали)
git init

# Добавьте все файлы
git add .

# Сделайте коммит
git commit -m "Initial commit"

# Подключите GitHub репозиторий (замените на свой)
git remote add origin https://github.com/ВАШ_USERNAME/ВАШ_РЕПОЗИТОРИЙ.git

# Загрузите код
git push -u origin main
```

### 3. Деплой на Railway

1. Откройте https://railway.app
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Выберите ваш репозиторий
5. Railway автоматически определит Python проект

### 4. Настройка переменных окружения

В Railway:
1. Откройте ваш проект
2. Перейдите в "Variables"
3. Добавьте переменные:
   - `BOT_TOKEN` = `7749933756:AAFf4pLJX0Kll80CbvUb8yzmg9yofxH_2XU`
   - `CHANNEL_USERNAME` = `@verised`

### 5. Готово!

Бот автоматически запустится и будет работать 24/7!

## Альтернатива: Render.com

1. Зарегистрируйтесь на https://render.com
2. New → Web Service
3. Подключите GitHub репозиторий
4. Настройки:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Добавьте переменные окружения
6. Deploy!

## Мониторинг

- Railway: Логи доступны в разделе "Deployments"
- Render: Логи в разделе "Logs"

## Обновление бота

Просто сделайте `git push` - Railway автоматически обновит бота!

```bash
git add .
git commit -m "Update bot"
git push
```

## Бесплатные лимиты

- **Railway**: 500 часов/месяц (достаточно для 1 бота 24/7)
- **Render**: 750 часов/месяц

## Проблемы?

Если бот не запускается:
1. Проверьте логи в Railway/Render
2. Убедитесь что все переменные окружения добавлены
3. Проверьте что бот добавлен в канал как администратор
