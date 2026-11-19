"""Turn the full graph (build_graph.py output) into the compact graph.json the page reads."""
import json, sys
g = json.load(open(sys.argv[1]))
N = [dict(id=n['id'], k=n['kind'], t=n['title'], s=n['short'], o=n['state'] == 'open', sdo=n['sdo'],
          dom=n['domain'], cat=n['cat'], art=n['arts'], wf=n['wontfix'], ess=n['essential'], er=n['hasErrata'],
          sl=[l for l in n['labels'] if (l.startswith('sts:') or l.startswith('gap')) and 'milestone' not in l.lower()], sum=n['sum'],
          c=n['created'], u=n['updated']) for n in g['nodes']]
E = [[e['s'], e['t'], e['type']] for e in g['edges']]
json.dump(dict(generated=g['generated'], repo=g['repo'], nodes=N, edges=E), open(sys.argv[2], 'w'),
          separators=(',', ':'), ensure_ascii=False)
