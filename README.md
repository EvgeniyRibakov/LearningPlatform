📚 LearningPlatform

Платформа для самообучения студентов, реализованная на Django и Django Rest Framework (DRF).
Поддерживает регистрацию, авторизацию, управление разделами, материалами, тестами и результатами тестирования.
API защищён JWT-токенами, доступ регулируется ролями: администратор, преподаватель, студент.



📋 Требования





Python: 3.8 или выше



PostgreSQL: 13 или выше



Redis: для Celery



Git



🚀 Установка

1. Клонирование репозитория

Склонируйте проект с GitHub и перейдите в папку:

git clone https://github.com/<your-username>/LearningPlatform.git
cd LearningPlatform

2. Создание виртуального окружения

Создайте и активируйте виртуальное окружение:

python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

3. Установка зависимостей

Установите необходимые пакеты из requirements.txt:

pip install -r requirements.txt

4. Настройка PostgreSQL

Создайте базу данных и обновите настройки:





Создайте базу:

CREATE DATABASE learningplatform_db;



Откройте LearningPlatform/settings.py и настройте:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learningplatform_db',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. Настройка Redis

Установите и запустите Redis:





Скачайте и установите Redis: redis.io/download



Запустите сервер Redis:

redis-server



Убедитесь, что в LearningPlatform/settings.py указаны настройки Redis:

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

6. Применение миграций

Создайте таблицы в базе данных:

python manage.py makemigrations
python manage.py migrate

7. Создание суперпользователя

Создайте администратора для доступа к админ-панели:

python manage.py createsuperuser



🏁 Запуск проекта

1. Запуск Celery

В отдельном терминале запустите Celery для обработки задач:

celery -A LearningPlatform worker --loglevel=info

2. Запуск сервера Django

Запустите сервер разработки:

python manage.py runserver

3. Доступ к API

Откройте API-документацию в браузере:
🔗 http://127.0.0.1:8000/swagger/



📂 Структура проекта





LearningPlatform/ — корневые настройки и Celery:





settings.py — настройки (база данных, JWT, CORS, Celery).



urls.py — маршруты API (регистрация, токены, Swagger).



tasks.py — Celery-задачи (уведомления о результатах тестов).



courses/ — управление разделами, материалами, тестами:





models.py — модели (Section, Material, Test, Question, TestResult).



views.py — ViewSet'ы и API-эндпоинты (CRUD, проверка ответов).



serializers.py — сериализаторы для API.



permissions.py — кастомные разрешения (роли).



tests.py — тесты API и прав доступа.



users/ — управление пользователями:





models.py — модель пользователя (CustomUser).



views.py — регистрация пользователей.



serializers.py — сериализаторы для регистрации.



tests.py — тесты регистрации.



🌟 Основные функции API







Эндпоинт



Метод



Описание



Доступ





/api/register/



POST



Регистрация пользователя



Все





/api/token/



POST



Получение JWT-токена



Все





/api/sections/



GET/POST



CRUD для разделов



Преподаватели





/api/materials/



GET/POST



CRUD для материалов



Преподаватели





/api/tests/



GET/POST



CRUD для тестов (фильтр по разделу)



Преподаватели





/api/test-results/



GET/POST



Отправка результатов тестов



Студенты/Преподаватели





/api/check-answer/



POST



Проверка ответа на вопрос



Студенты



👥 Роли и права





Администратор:
Полный доступ через админ-панель: /admin/.



Преподаватель:
Создание и редактирование своих разделов, материалов, тестов.



Студент:
Просмотр материалов, прохождение тестов, отправка ответов.



🧪 Тестирование





Покрытие кода: ~98%.



Запуск тестов:

coverage run manage.py test
coverage report



ℹ️ Дополнительно





API-документация: доступна через Swagger (/swagger/).



Логирование: Celery-задачи логируются в LearningPlatform/tasks.py.