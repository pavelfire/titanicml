'''
Давайте создадим простое API  с тремя ручкамиЖ одна для предсказания выживания (/predict),
вторая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
source .venv/bin/activate
pip3 install fastapi uvicorn pydantic scikit-learn pandas
pip3 install matplotlib   

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение:

В терминале перейдите в папку проекта и выполните:

cd /Users/pvdo/VScodeProjects/titanicml
source .venv/bin/activate
После активации в начале строки терминала появится (.venv):

(.venv) pvdo@MacBook-Pro-Pavel titanicml %
Теперь команды python и pip будут из виртуального окружения:

pip install fastapi uvicorn pydantic scikit-learn pandas
python app_api.py
Деактивация
deactivate
Если .venv ещё нет
Создайте и сразу активируйте:

python3 -m venv .venv
source .venv/bin/activate

 python3 app_api.py
Шаг 4: Тестирование API
Теперь вы можете тестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP запросов.

curl -X GET http://127.0.0.1:5026/health
curl -X GET http://127.0.0.1:5026/stats
curl -X POST http://127.0.0.1:5026/predict_model \
  -H "Content-Type: application/json" \
  -d '{"Pclass": 3, "Age": 22, "Fare": 7.25}'
'''

from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel
# from train import predictions

app = FastAPI()

#Загрузка модели из файла pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

#Счётчик запросов
request_count = 0

#Модель для валидации входных данных
class PredictionInput(BaseModel):
    Pclass: int
    Age: float
    Fare: float

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    #Создание DataFrame из данных
    new_data = pd.DataFrame({
        'Pclass': [input_data.Pclass],
        'Age': [input_data.Age],
        'Fare': [input_data.Fare]
    })

    #Предсказание
    prediction = model.predict(new_data)

    #Преобразование результата в человеко-читаемый формат
    result = "Survived" if prediction[0] == 1 else "Not Survived"

    return {"prediction": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5026)

    
