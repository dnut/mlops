The goal of this project is to demonstrate a variety of practical approaches for deploying a machine learning model that was trained in python. The model and the problem it solves are not the focus of this project. The focus is productionalization and deployment of any arbitrary model.

I'd like to demonstrate best practices, but this is a work in progress. I am first focused on delivering each of the following:

1. Train a model using sklearn in python
2. Deploy model in an HTTP server, using various technologies:
   - pickled sklearn model in python
   - converted to an onnx model, and used in each language:
     - python
     - rust
     - go
3. Comprehensive automated test coverage
4. Containerize the apps using docker
5. Deploy the apps to a kubernetes cluster
6. Automate processes with github workflow

See [todo.md](todo.md) for more a more granular (and disorganized) set of tasks.
