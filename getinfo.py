from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
def getinfo(hashurl):
  if "*" in hashurl or '$' in hashurl:
    return {}
  html = urlopen(hashurl).read()
  soup = BeautifulSoup(html, features="html.parser")
  finaldict={}
  if 'graph' in json.loads(soup.body['data-load-data']).keys():
    for key in [x for x in ['hash','parent_hash','thumbUrl','stateUrl','title','access','created'] if x in json.loads(soup.body['data-load-data'])['graph'].keys()]:
      finaldict[key]=json.loads(soup.body['data-load-data'])['graph'][key]
    finaldict['version']='null'
    dastate=json.loads(soup.body['data-load-data'])['graph']['state']
    if 'version' in dastate.keys():
      finaldict['version']=dastate['version']
    if 'expressions' in dastate.keys():
      expr=dastate['expressions']['list']
      finaldict['expressions'] = expr
      finaldict['notes'], finaldict['folders']=[],[]
      finaldict['notes']=[expr[i] for i in range(len(expr)) if expr[i]['type' if 'type' in expr[i] else 'id']=='text']
      finaldict['folders']=[expr[i] for i in range(len(expr)) if expr[i]['type' if 'type' in expr[i] else 'id']=='folder']
      patternvar = re.compile(r"([A-Za-z](?:_{?\w*}?)?)=")
      finaldict['variables']=list(set([ii.group(1) for ii in patternvar.finditer(str(expr))]))
  return (finaldict)