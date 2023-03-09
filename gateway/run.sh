python -m grpc_tools.protoc -I ./../protos/ --python_out=./ --pyi_out=./ --grpc_python_out=./ ./../protos/account.proto
echo "grpc files created"
python manage.py migrate
python manage.py runserver 0.0.0.0:7777 | python manage.py grpcrunserver