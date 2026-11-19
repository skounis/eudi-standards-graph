import json,re,sys
from collections import Counter
src,out=sys.argv[1],sys.argv[2]
d=[i for i in json.load(open(src)) if 'pull_request' not in i]
REPO='eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications'
nodes={};edges=[]
cirkey={}
def kind(i,L):
    if 'CIR' in L and re.match(r'CI[RD] \(EU\)',i['title']): return 'cir'
    if i['title'].startswith('Errata:'): return 'errata'
    t=i['title'].strip()
    if re.match(r'^\[|^TS\d+\b',t): return 'signal'
    if not any(l.startswith('sts:') for l in L) and not re.match(KNOWN,t): return 'signal'
    return 'sts'
KNOWN=r'(ETSI|ISO|IETF|CEN|prCEN|FprCEN|EC |W3C|OIDF|OpenID|GlobalPlatform|DILCIS|ITU|Common Criteria|ENISA|CSC|FIDO|Eurosmart|RFC|Data Catalog|DTS|IANA|TS 18170|Verifiable|Data Integrity)'
for i in d:
    L=[l['name'] for l in i['labels']]
    k=kind(i,L)
    t=i['title'].strip()
    if k=='cir':
        m=re.match(r'(CI[RD] \(EU\) \d{4}/\d+)',t); cirkey[m.group(1)]=i['number']
        short=m.group(1); 
    elif k=='errata':
        short=re.sub(r'^Errata:\s*','',t).split(' - ')[0]
    else:
        short=re.split(r'\s+-\s*|\s+–\s+|\)-\s*',t)[0]
        if short.count('(')>short.count(')'): short+=')'
        if k=='signal': short=t
    body=i.get('body') or ''
    sdo=(re.match(r'(ETSI|ISO/IEC|ISO|CEN|CENELEC|IETF|W3C|OpenID|EC|ENISA|IEC|NIST|ICAO|OIDF|EUDI|ITU)',t) or [None,None])[1] if k in ('sts','signal') else None
    if k in('sts','signal') and not sdo:
        sdo=t.split()[0].strip(':-') if t else 'Other'
    nodes[i['number']]=dict(id=i['number'],kind=k,title=t,short=short[:60],state=i['state'],
        labels=L,sdo=sdo,
        domain=[x[8:] for x in L if x.startswith('Domain: ')],
        cat=[x[5:] for x in L if x.startswith('Cat: ')],
        arts=[x for x in L if x.startswith('Art ')],
        wontfix='wontfix' in L or 'Withdrawn' in L,
        essential='Essential' in L,
        hasErrata='errata' in L and k=='sts',
        created=i['created_at'][:10],updated=i['updated_at'][:10],
        sum=re.sub(r'\s+',' ',re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',(body.split('### Overview')[1] if '### Overview' in body else body)))[:280].strip())
seen=set()
def add(a,b,t):
    if a==b or a not in nodes or b not in nodes: return
    key=(a,b,t)
    if key in seen: return
    seen.add(key); edges.append(dict(s=a,t=b,type=t))
linkre=re.compile(r'github\.com/'+re.escape(REPO)+r'/issues/(\d+)')
for i in d:
    n=nodes[i['number']]
    # label-based STS -> CIR
    for l in n['labels']:
        if l in cirkey: add(i['number'],cirkey[l],'cites' if n['kind']=='sts' else 'ref')
    body=i.get('body') or ''
    for m in set(linkre.findall(body)):
        m=int(m)
        if m not in nodes: continue
        a,b=n['kind'],nodes[m]['kind']
        if a=='errata' and b=='sts': t='corrects'
        elif a=='cir' and b=='cir': t='amends'
        elif {a,b}=={'cir','sts'}: t='cites'
        elif a=='signal': t='raises'
        else: t='ref'
        if t=='cites' and a=='cir': add(m,i['number'],t)
        else: add(i['number'],m,t)
rank={'corrects':0,'amends':1,'cites':2,'raises':3,'ref':4}
best={}
for e in edges:
    k=frozenset((e['s'],e['t']))
    if k not in best or rank[e['type']]<rank[best[k]['type']]: best[k]=e
edges=list(best.values())
SD={'Common':'Common Criteria','FprCEN/TS':'CEN','prCEN':'CEN','Data':'W3C','Verifiable':'W3C','VC':'W3C','Web':'W3C','RFC':'IETF','IANA':'IETF'}
for n in nodes.values():
    if n['sdo']:
        n['sdo']=SD.get(n['sdo'],n['sdo'])
        if n['sdo'] not in ('ETSI','ISO/IEC','ISO','IETF','CEN','EC','W3C','OIDF','GlobalPlatform','DILCIS','ITU','ENISA','Common Criteria','CSC','FIDO'): n['sdo']='Other'
# Article nodes
arts=Counter(a for n in nodes.values() for a in n['arts'])
c=Counter(e['type'] for e in edges)
deg=Counter();[deg.update([e['s'],e['t']]) for e in edges]
for n in nodes.values(): n['deg']=deg[n['id']]
json.dump(dict(generated=sys.argv[3],repo=REPO,nodes=list(nodes.values()),edges=edges,articles=arts),open(out,'w'))
print(Counter(n['kind'] for n in nodes.values()),c,len(arts),sum(1 for n in nodes.values() if n['deg']==0))
print(Counter(n['sdo'] for n in nodes.values() if n['kind']=='sts').most_common(25))
