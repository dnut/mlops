# python docs

## animal_classifier

The `animal_classifier` folder is a namespace package which can be distributed in its entirety as a wheel. Alternatively, each contained module can be distributed independently.
- pyproject.toml in the repo root defines a single python distribution via poetry that contains all code in animal_classifier as a single distribution. This is useful to get all the code and dependencies in one place, mainly for development.
- dists.toml defines how each module in the folder (app, client, common, etc.) can be distributed separately as its own wheel, which is more practical to use for real-world deployments, since you can deploy exclusively the components you need, rather than requiring unnecessary dependencies. This is built with dist.py, which I intend to eventually flesh out as a more general tool and publish to pypi.

## test

The `test` folder is a collection of pytest tests. They are configured with the pytest configuration in the repository root's pyproject.toml.
