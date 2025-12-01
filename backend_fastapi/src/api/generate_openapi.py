import json
import os

# Import application first to ensure all routers are registered before schema generation
from src.api.main import app  # noqa


def generate_and_write_openapi():
    """Generate the OpenAPI schema from the fully-initialized FastAPI app and write to interfaces/openapi.json."""
    openapi_schema = app.openapi()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)


if __name__ == "__main__":
    generate_and_write_openapi()
