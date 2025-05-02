import os
from dotenv import load_dotenv

from .config import load_yaml_config

load_dotenv()

app_config = {
    "opensearch_config": os.environ.get("OPENSEARCH_CONFIG"),
    "llm_config": os.environ.get("LLM_CONFIG"),
    "database_config": os.environ.get("DATABASE_CONFIG")
}

LLM_CONFIG = load_yaml_config(os.path.join(os.path.dirname(__file__), "llm_config.yaml"),
                              app_config["llm_config"])
OPENSEARCH_CONFIG = load_yaml_config(os.path.join(os.path.dirname(__file__), "opensearch_config.yaml"),
                                     app_config["opensearch_config"])
DATABASE_CONFIG = load_yaml_config(os.path.join(os.path.dirname(__file__), "database_config.yaml"),
                                   app_config["database_config"])