# python docs

## animal_classifier

The `animal_classifier` folder is a namespace package which can be distributed in its entirety as a wheel. Alternatively, each contained module can be distributed independently.
- pyproject.toml in the repo root defines a single python distribution via poetry that contains all code in animal_classifier as a single distribution. This is useful to get all the code and dependencies in one place, for example during development.
- dists.toml defines how each module in the folder (app, client, common, etc.) can be distributed separately as its own wheel, which may be more practical to use for real-world deployments, since you can deploy exclusively the components you need, rather than requiring unnecessary dependencies. This is built with dist.py.

### Why the strange approach to packaging?

Typically, the best practice is to keep separate python distributions in separate directories, but this is unwieldy for the current scenario. There are several subsets of the namespace that are each worth deploying independently in order to minimize unnecessary dependencies. These subsets overlap, which means there are shared dependencies within the namespace.

The dependency complexity is managed cleanly by independently packaging each file as its own wheel. However, with each file in separately nested folders, it would be very inconvenient to navigate the code and to get it to run properly in a development environment. The current approach with dist.py is an attempt to balance the two competing ideals: ease of development and clean dependency management.

There is also utility in distributing the whole namespace as a single entity for a "batteries included" experience that does not require developers to identify exactly which components they need while they are trying to rapidly prototype something based on this code.

I would like to revisit this topic later to address whether the current approach is worth formalizing with more robust dependency management and testing, or if it should be abandoned in favor of a more practical way to smooth out the inconvenience of separation.

## test

The `test` folder is a collection of pytest tests. They are configured with the pytest configuration in the repository root's pyproject.toml.
