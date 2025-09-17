import argparse, json, os
from typing import List, Dict

def filter_entries(entries: List[Dict], domains: List[str]) -> List[Dict]:
    wanted = {d.lower() for d in domains}
    def ok(e):
        c = (e.get('Category') or '').lower()
        return any(w in c for w in wanted)
    return [e for e in entries if ok(e)]

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--domains', type=str, required=True)
    p.add_argument('--out', type=str, required=True)
    args = p.parse_args()
    src_json = 'apis.json' if os.path.exists('apis.json') else 'entries.json'
    with open(src_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get('entries', [])
    subset = filter_entries(entries, [s.strip() for s in args.domains.split(',')])
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(subset, f, indent=2, ensure_ascii=False)
