- two stage docker image
- quart with thread pool for prediction
- client library used by server and client
- go and rust server and client
- pickle model and test pickled against onnx
- get onnx to work with multiple named inputs
- kubernetes pod
- monitoring and logging to service
- scale in kubernetes based on load from monitoring service
- setup.py for server and client library and deploy wheels
- type hinting and mypy
- any data types shared between trainer and service
- automate environment setup with k8s and everything, maybe github workflow?
- error handling


# done
- train model with sklearn
- run model with onnx in python
- flask server running model
- docker container with flask server
- run model with onnx in rust
