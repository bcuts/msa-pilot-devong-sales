import requests

from delegate.exceptions import IntegrationException


def get(branch_id, endpoint):
    url = endpoint + '/branch/{}'.format(branch_id)
    r = requests.get(url)
    if r.status_code % 100 == 2:
        return r.json() if r.content else None

    raise IntegrationException("Branch Request wrong to {}, status_code={}".format(url, r.status_code))
