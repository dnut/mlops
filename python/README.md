# python docs

## animal_classifier

The `animal_classifier` folder is a namespace package which can be distributed as a wheel, as can each of its files.
- pyproject.toml in the repo root defines a single python distribution via poetry that contains all code in animal_classifier as a single distribution. This is useful just to get all the code and dependencies in one place, mainly for development.
- dists.toml defines how each module in the folder (app, common, etc.) can be distributed separately as its own wheel, which is more practical to use for real-world deployments, since you can deploy exclusively the components you need, rather than requiring unnecessary dependencies. build-dists


## test

The `test` folder is a collection of pytest tests. They are configured with the pytest configuration in the repository root's pyproject.toml.
