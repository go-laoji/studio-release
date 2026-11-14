import hashlib,json,os,pathlib,urllib.request,urllib.error,sys
username=os.environ.get('HUB_USERNAME') or 'golaoji'
secret=os.environ.get('HUB_TOKEN')
if not secret:
    print('Docker Hub repository secret DOCKERHUB_TOKEN is not configured; no metadata changed.',flush=True)
    raise SystemExit(78)
repo='https://hub.docker.com/v2/repositories/golaoji/trace-studio-server/'
content=pathlib.Path('.overview-sync/README.md').read_text()
def request(url,method='GET',data=None,token=None):
    headers={'Content-Type':'application/json','Accept':'application/json','User-Agent':'dockerhub-description-sync'}
    if token:headers['Authorization']='JWT '+token
    req=urllib.request.Request(url,headers=headers,data=json.dumps(data).encode() if data is not None else None,method=method)
    try:
        with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)
    except urllib.error.HTTPError as error:
        print('Docker Hub API '+method+' failed: HTTP'+str(error.code),flush=True)
        raise SystemExit(1)
auth=request('https://hub.docker.com/v2/users/login',method='POST',data={'username':username,'password':secret})
token=auth['token']
request(repo,method='PATCH',data={'full_description':content},token=token)
actual=request(repo,token=token)
assert actual['full_description']==content
print(json.dumps({'overview_updated':True,'repository':'golaoji/trace-studio-server','bytes':len(content.encode()),'sha256':hashlib.sha256(content.encode()).hexdigest()}),flush=True)
