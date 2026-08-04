#!/usr/bin/env python3
import argparse, hashlib, json, math, re
from pathlib import Path

URL='https://math-zhangzhx.ahnu.edu.cn/SET-1029-PRIMES.txt'
EXPECTED_SHA256='44f3fe6777a7a1bcb8847761961fcc70a0e5438e98540288bded5594d141d44a'

def load_primes(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA256: raise RuntimeError('prime-list hash mismatch')
    return [int(x) for x in raw.split()]

def parse_vector(path):
    text=Path(path).read_text(errors='replace')
    # fplll normally emits exactly one vector; use final bracketed nonempty line.
    candidates=re.findall(r'\[\s*[-+0-9][^\[\]]*\]',text)
    if not candidates: raise RuntimeError('no vector in output')
    return [int(x) for x in re.findall(r'-?\d+',candidates[-1])]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',default='work')
    ap.add_argument('--prime-list',default='williams_search/SET-1029-PRIMES.txt')
    ap.add_argument('--closest',default=None)
    args=ap.parse_args()
    w=Path(args.work); meta=json.loads((w/'meta.json').read_text())
    P=load_primes(args.prime_list); n=len(P); r=meta['n_constraints']; C=meta['scale']
    closest=Path(args.closest) if args.closest else w/'closest.txt'
    v=parse_vector(closest)
    if len(v)!=n+r: raise RuntimeError(f'wrong vector length {len(v)} != {n+r}')
    desired=[2*C*t for t in meta['target_transformed']]
    constraint_delta=[a-b for a,b in zip(v[n:],desired)]
    z=[]; bad=[]
    for i,a in enumerate(v[:n]):
        if a not in (0,2): bad.append((i,a))
        z.append(a//2)
    diag={
      'vector_length':len(v),'binary_coordinates':n-len(bad),'bad_coordinate_count':len(bad),
      'bad_coordinate_examples':bad[:30],
      'constraint_mismatch_count':sum(x!=0 for x in constraint_delta),
      'max_abs_constraint_mismatch':max(map(abs,constraint_delta),default=0),
      'squared_distance':sum((a-1)**2 for a in v[:n])+sum(x*x for x in constraint_delta)
    }
    (w/'diagnostics.json').write_text(json.dumps(diag,indent=2))
    print(json.dumps(diag))
    if bad or any(constraint_delta): raise SystemExit(2)
    comp=meta['complement']; x=[(1-zi) if b else zi for zi,b in zip(z,comp)]
    selected=[p for p,b in zip(P,x) if b]
    indices=[i for i,b in enumerate(x) if b]
    N=math.prod(selected)
    ok_minus=all((N-1)%(p-1)==0 for p in selected)
    ok_plus=all((N+1)%(p+1)==0 for p in selected)
    # Strong global checks used to construct the instance.
    Lm=int(meta['Lminus']); Lp=int(meta['Lplus'])
    ok_global=(N-1)%Lm==0 and (N+1)%Lp==0
    result={
      'source_url':URL,'source_sha256':EXPECTED_SHA256,'seed':meta['seed'],'scale_bits':meta['scale_bits'],
      'number_of_prime_factors':len(selected),'odd_number_of_factors':len(selected)%2==1,
      'indices_zero_based':indices,'indices_one_based':[i+1 for i in indices],'prime_factors':selected,
      'N':str(N),'N_decimal_digits':len(str(N)),
      'squarefree':len(selected)==len(set(selected)),
      'korselt_divisibilities':ok_minus,'williams_plus_divisibilities':ok_plus,
      'global_Lminus_congruence':(N-1)%Lm==0,'global_Lplus_congruence':(N+1)%Lp==0,
      'verified':bool(selected and len(selected)%2==1 and ok_minus and ok_plus and ok_global)
    }
    (w/'solution.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (w/'N.txt').write_text(str(N)+'\n')
    (w/'factors.txt').write_text('\n'.join(map(str,selected))+'\n')
    print(json.dumps({k:result[k] for k in ['number_of_prime_factors','N_decimal_digits','verified']}))
    if not result['verified']: raise SystemExit(3)

if __name__=='__main__': main()
