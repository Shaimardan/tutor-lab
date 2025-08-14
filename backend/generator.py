import json
import sys

from fastapi import FastAPI
from uvicorn.importer import import_from_string


def main() -> None:
    sys.path.insert(0, ".")

    fastapi: FastAPI = import_from_string("main:app")

    if not isinstance(fastapi, FastAPI):
        raise Exception("The given object is not a FastAPI application")

    with open("{}/{}".format("../common/", "open_api.json"), "w+") as openapi:
        openapi.write(json.dumps(fastapi.openapi(), indent=2))
        openapi.close()


if __name__ == "__main__":
    main()
