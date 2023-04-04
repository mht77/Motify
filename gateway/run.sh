python -m grpc_tools.protoc -I ./../protos/ --python_out=./ --pyi_out=./ --grpc_python_out=./ ./../protos/account.proto
python -m grpc_tools.protoc -I ./../protos/ --python_out=./ --pyi_out=./ --grpc_python_out=./ ./../protos/artist.proto
echo "grpc files created"