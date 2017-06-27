import requests

from delegate.exceptions import IntegrationException


def get(product_id, endpoint):
    url = endpoint + '/product/{}'.format(product_id)
    r = requests.get(url)
    if r.status_code % 100 == 2:
        return r.json() if r.content else None

    raise IntegrationException("Product Request wrong to {}, status_code={}".format(url, r.status_code))
