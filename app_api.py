'''
Давайте создадим простое API  с тремя ручкамиЖ одна для предсказания выживания (/predict),
вторая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
pip install fastapi uvicorn pydantic scikit-learn pandas

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение: python app_api.py
Шаг 4: Тестирование API
Теперь вы можете тестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP запросов.

curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{"Pclass": 3, "Age": 22, "Fare": 7.25}"
'''

from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel
from train import predictions

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
def predict_model(input_data: PredictInput):
    global request_count
    request_count += 1

    #Создание DataFrame из данных
    new_data = pd.DataFrame({
        'Pclass': [input_data.Pclass],
        'Aga': [input_data.Age],
        'Fare': [input_data.Fare]
    })

    #Предсказание
    prediction = model.prdict(new_data)

    #Преобразование результата в человеко-читаемый формат
    result = "Survived" if predictions[0] == 1 else "Not Survived"

    return {"prediction": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)

    
