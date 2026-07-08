# Titanic ML API

Сервис для предсказания выживания пассажиров «Титаника» на основе обученной модели.

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Проверка работоспособности API |
| GET | `/stats` | Количество выполненных предсказаний |
| POST | `/predict_model` | Предсказание выживания |

Тело запроса для `/predict_model`:

```json
{
  "Pclass": 3,
  "Age": 22,
  "Fare": 7.25
}
```

Ответ:

```json
{
  "prediction": "Survived"
}
```

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app_api.py
```

API будет доступно на `http://127.0.0.1:5026`.

Документация Swagger: http://127.0.0.1:5026/docs

### Примеры запросов

```bash
curl http://127.0.0.1:5026/health

curl http://127.0.0.1:5026/stats

curl -X POST http://127.0.0.1:5026/predict_model \
  -H "Content-Type: application/json" \
  -d '{"Pclass": 3, "Age": 22, "Fare": 7.25}'
```

## Docker

```bash
docker build -t titanic-service:latest .

docker run -d --name titanic-service -p 5026:5026 titanic-service:latest
```

После запуска контейнера API доступно на `http://127.0.0.1:5026`.

## Обучение модели

Модель обучается в ноутбуке `train.ipynb` и сохраняется в `model.pkl`.
