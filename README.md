# Websocket example

## Requirements
Python 3

## Server
### Installation
```
pip install -r server/python_modules
```
### Run
```
./server/tornado_server.py --port=9500
```
### Tests
```
./server/test.py
```

## Client
### Installation
```
pip install -r client/python_modules
```
### Run
```
./client/client.py --host_ws localhost --port_ws 9500 --image_generator file --image_max_height 150 --image_gray
```
