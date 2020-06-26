import os
import json
from django.conf import settings


def google_analytics(request):
    return {'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID}


def static_asset_hashes(request):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    hash_file = '{}/static_asset_hashes.json'.format(dir_path)

    try:
        with open(hash_file) as f:
            hashes = json.load(f)

    except Exception:
        hashes = {}

    res = {}

    # the asset manifest is in the format `{ 'styles.css': '928af98e' }`,
    # but jinja templates can only use simple dictionary accessors (e.g.
    # `{{ hash.css }}`, not `{{ hash['css'] }}` or `{{ hash|get('css') }}`).
    # this means we can't parse `styles.css` in the template, so convert
    # dots to underscores.
    for key, value in hashes.items():
        res[key.decode('utf-8').replace('.', '_')] = value

    return {'static_asset_hashes': res}
