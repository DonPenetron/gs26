docker build -t ml:1.2.7 . </br>
docker compose up

ENDOPOINTS
http://hostname:30001//ml/parse_video - получает id задачи и путь на файл в Minio. Возвращает все найденные инциденты, выгружаешь хайлайты в Minio
http://hostname:30001//ml/parse_video - получает id задачи, путь на файл в Minio и пользовательский промпт. Возвращает все найденные инциденты, выгружаешь хайлайты в Minio
