import requests


def get(branch_id, endpoint):
    url = endpoint + '/branch/{}'.format(branch_id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json() if r.content else None

    raise "Request wrong to {}, status_code={}".format(url, r.status_code)
