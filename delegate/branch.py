import requests


def get(branch_id, endpoint):
    r = requests.get(endpoint + '/branch/{}'.format(branch_id))
    if r.status_code == 200:
        return r.json() if r.content else None

    raise "Request wrong, status_code={}".format(r.status_code)
