
import app

ENVVAR_KEY_API_ENDPOINT_BRANCH = 'API_ENDPOINT_BRANCH'

DEFAULT_API_ENDPOINT_BRANCH = 'http://localhost:8080'


def get_branch_api_endpoint():
    try:
        return app.app.config.from_envvar(ENVVAR_KEY_API_ENDPOINT_BRANCH)
    except RuntimeError as e:
        print('WARNING: API_ENDPOINT_BRANCH loading failed, details:', e)
        return DEFAULT_API_ENDPOINT_BRANCH
