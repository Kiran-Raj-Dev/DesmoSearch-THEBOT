from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import difflib
import pylatexenc
from pylatexenc.latex2text import LatexNodes2Text
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


def difference (graph1,graph2):
  getinfo1=getinfo(graph1)
  getinfo2=getinfo(graph2)
  Expressions = lambda getinf: [f"[#{exp['id']}] {exp['latex' if 'latex' in exp.keys() else ('text' if 'text' in exp.keys() else 'title')]}" for exp in getinf['expressions'] if ('latex' in exp.keys() or 'text' in exp.keys() or 'title' in exp.keys())]
  Expressions1 = [LatexNodes2Text().latex_to_text(exp) for exp in Expressions(getinfo1)]
  Expressions2 = [LatexNodes2Text().latex_to_text(exp) for exp in Expressions(getinfo2)]

  text1_lines, text2_lines = Expressions1, Expressions2
  diff = difflib.ndiff(text1_lines, text2_lines)
  sm = difflib.SequenceMatcher(a=text1_lines, b=text2_lines)
  diff2=[]
  getid=-1
  for change in diff:
    if change[0] in ["-","+","?"]:
      getid0 = re.match('[+-\?] (\[.*\])',change)
      if (getid0 is None):
        diff2[-1]=diff2[-1]+'\n'+change
      else:
        if getid==getid0.group(1):
          diff2[-1]=diff2[-1]+'\n'+change
        else:
          diff2.append(change)
          getid=getid0.group(1)
    else:
      diff2.append(change)
  diff2 = ['```'+dif+'```' for dif in diff2]
  return([sm.ratio(),diff2])