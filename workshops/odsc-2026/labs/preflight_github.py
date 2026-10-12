"""Check the public PR endpoint before timing a read-only GitHub lab."""
import json
import urllib.error
import urllib.request
import sys
import os
url='https://api.github.com/repos/OpenHands/OpenHands/pulls/16860'
try:
    headers={'User-Agent':'harness-workshop-preflight','Accept':'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'): headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    req=urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req,timeout=30) as response:
        data=json.load(response)
        print(json.dumps({'number':data['number'],'url':data['html_url'],'remaining_public_requests':response.headers.get('X-RateLimit-Remaining')}))
except (urllib.error.URLError, KeyError) as exc:
    print(f'GitHub preflight failed: {exc}. Use saved evidence if access or quota is unavailable.',file=sys.stderr)
    sys.exit(1)
