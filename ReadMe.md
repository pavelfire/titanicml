source .venv/bin/activate

python app_api.py

http://127.0.0.1:5000/docs#/default/predict_model_predict_model_post


docker build -t titanic-service:latest .

docker run -d --name titanic-service -p 5026:5026 titanic-service:latest