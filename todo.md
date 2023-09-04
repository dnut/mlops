# in progress
- rust env vars
- rust Dockerfile

# backlog
- kubernetes pod
- go server
- go client
- configurable listening port number
- python: investigate multi-stage docker images in
- python: consider/test quart with thread pool for prediction - yes it is cpu bound, but we can improve GIL usage, also this actually could go to the gpu instead.
- pickle model and test pickled against onnx
- get onnx to work with multiple named inputs, requires training with names
- monitoring and logging to central services
- scale in kubernetes based on load from monitoring service
- python: type hinting and lint with mypy or comparable
- automate environment setup with k8s and everything, maybe github workflow?
- improve error handling
- reconsider: language-specific project config in root or lang folders?
