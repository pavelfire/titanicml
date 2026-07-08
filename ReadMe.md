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

## Деплой на сервер (GitHub Actions + GHCR)

Образ собирается в GitHub Container Registry и автоматически выкатывается на сервер при пуше тега `v*`.

### 1. Подготовка сервера (один раз)

```bash
sudo mkdir -p /opt/titanicml
sudo chown $USER:$USER /opt/titanicml
cd /opt/titanicml

git clone https://github.com/pavelfire/titanicml.git .
cp .env.example .env
# отредактируй .env — домен и email для Let's Encrypt
nano .env
```

Если образ в GHCR приватный, залогинься на сервере:

```bash
echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USER --password-stdin
```

### 2. Секреты в GitHub (Settings → Secrets)

| Секрет | Описание |
|--------|----------|
| `SSH_HOST` | IP или домен сервера |
| `SSH_USER` | SSH-пользователь |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ |
| `DEPLOY_PATH` | Путь на сервере (по умолчанию `/opt/titanicml`) |

### 3. Выкатка новой версии

```bash
git tag v1.0.0
git push origin v1.0.0
```

Или вручную: Actions → Deploy → Run workflow → указать тег.

После успешного workflow API будет доступно на `https://ВАШ_ДОМЕН/health`.
docker compose -f docker-compose.prod.yml --env-file .env pull

## Обучение модели

Модель обучается в ноутбуке `train.ipynb` и сохраняется в `model.pkl`.
