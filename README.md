# Play with apache-nifi
Проект - демонстрация возможностей API Apache-NIFI

## Стек:
Pyhon, Docker, Apache-NIFI, Streamlit
## Запуск:
1. Создание виртуального окружения
```commandline
python -m venv venv
```
2. Активация виртуального окружения
```commandline
source venv\Scripts\activate 
```
3. Установка зависимостей
```commandline
pip install -r requirements.txt
```
4. Запуск докер контейнера с apache-nifi
```commandline
docker compose up
```
Apache-nifi доступен по адресу http://127.0.0.1:8080/nifi  
5. Запуск проекта
```commandline
streamlit run app.py
```
Проект доступен по ссылке http://127.0.0.1:8501