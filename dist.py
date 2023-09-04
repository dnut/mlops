import os
import tomllib
import sys
import shutil
from copy import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from build.__main__ import main as build


@dataclass
class Distribution:
    name: str
    internal: List[str] = field(default_factory=list)
    external: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(name: str, d: dict):
        return Distribution(
            name=name,
            internal=d.get("internal", []),
            external=d.get("external", {}),
        )


@dataclass
class DistConfig:
    python_requires: str
    package_dir: str = "."
    namespace: Optional[str] = None
    distributions: List[Distribution] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        d = copy(d)
        distributions = [
            Distribution.from_dict(name, dct) for name, dct in d["_"].items()
        ]
        del d["_"]
        return DistConfig(**d, distributions=distributions)


def setup_cfg(
    namespace,
    python_requires,
    name,
    internal,
    external,
):
    external = [f"\n    {k} {v}" for k, v in external.items()]
    internal = [f"\n    {namespace}.{k}" for k in internal]
    return f"""[metadata]
name = {namespace}.{name}

[options]
python_requires = {python_requires}
install_requires = {''.join(external + internal)}
"""

def find_file_up_tree(start: str, filename: str) -> (str, str):
    """returns the folder abs path followed by the """
    start = os.path.abspath(start)
    folder = start
    while True:
        for item in os.listdir(folder):
            if item == filename:
                return folder, os.path.join(folder, filename)
        next_folder = os.path.normpath(os.path.join(folder, os.pardir))
        if next_folder == folder:
            raise Exception('{filename} not found in {start} or its parents')
        folder = next_folder


if __name__ == "__main__":
    path = os.path.join
    cwd = os.path.abspath(".")
    root, dist_toml = find_file_up_tree(cwd, "pydist.toml")

    with open(path(root, dist_toml), "rb") as f:
        config = DistConfig.from_dict(tomllib.load(f))

    # create package structure (fast)
    paths_to_build = []
    build_dir = path(root, "build", "multi-dist")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    for dist in config.distributions:
        dist_path = path(build_dir, dist.name)
        paths_to_build.append(dist_path)
        os.makedirs(path(dist_path, config.namespace), exist_ok=True)
        # TODO: support packages, not just modules
        shutil.copyfile(
            path(config.package_dir, config.namespace, dist.name + ".py"),
            path(dist_path, config.namespace, dist.name + ".py"),
        )
        with open(path(dist_path, "pyproject.toml"), "w") as f:
            f.write("")
        with open(path(dist_path, "setup.cfg"), "w") as f:
            f.write(
                setup_cfg(
                    config.namespace,
                    config.python_requires,
                    dist.name,
                    dist.internal,
                    dist.external,
                )
            )

    # build distributions (slow)
    dist_dir = path(root, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    for path_to_build in paths_to_build:
        os.chdir(path_to_build)
        build(sys.argv[1:] + ["--no-isolation"])
        for dist in os.listdir(path(path_to_build, "dist")):
            shutil.move(path(path_to_build, "dist", dist), path(dist_dir, dist))
