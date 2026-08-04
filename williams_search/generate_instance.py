#!/usr/bin/env python3
import argparse, hashlib, json, math, random, urllib.request
from pathlib import Path

URL='https://math-zhangzhx.ahnu.edu.cn/SET-1029-PRIMES.txt'
EXPECTED_SHA256='44f3fe6777a7a1bcb8847761961fcc70a0e5438e98540288bded5594d141d44a'

def small_primes(n=1000):
    out=[]
    for x in range(2,n+1):
        if all(x%p for p in out if p*p<=x): out.append(x)
    return out
SMALL=small_primes()

def factor_small(n):
    d={}
    for p in SMALL:
        if p*p>n: break
        while n%p==0:
            d[p]=d.get(p,0)+1; n//=p
    if n>1:
        # For this published instance all factors of p±1 are <=653.
        if n>1000:
            raise ValueError(f'unexpected large remaining factor {n}')
        d[n]=d.get(n,0)+1
    return d

def merge_lcm_factors(factors):
    D={}
    for f in factors:
        for p,e in f.items(): D[p]=max(D.get(p,0),e)
    return D

def phi_prime_power(q,e): return (q-1)*q**(e-1)

def prime_factors(n): return list(factor_small(n))

def primitive_root_prime_power(q,e):
    mod=q**e; phi=phi_prime_power(q,e); pf=prime_factors(phi)
    for g in range(2,mod):
        if math.gcd(g,mod)==1 and all(pow(g,phi//r,mod)!=1 for r in pf):
            return g
    raise RuntimeError(('primitive root not found',q,e))

def dlog_table(g,mod,order):
    t={}; x=1
    for k in range(order):
        if x in t: raise RuntimeError('short generator cycle')
        t[x]=k; x=(x*g)%mod
    if x!=1 or len(t)!=order: raise RuntimeError('bad generator')
    return t

def load_primes(cache):
    cache=Path(cache)
    if cache.exists(): raw=cache.read_bytes()
    else:
        raw=urllib.request.urlopen(URL,timeout=60).read()
        cache.parent.mkdir(parents=True,exist_ok=True); cache.write_bytes(raw)
    h=hashlib.sha256(raw).hexdigest()
    if h!=EXPECTED_SHA256: raise RuntimeError(f'list hash mismatch {h}')
    P=[int(x) for x in raw.split()]
    if len(P)!=1029 or len(set(P))!=1029: raise RuntimeError('bad prime list')
    if any(p%4!=3 for p in P): raise RuntimeError('unexpected residue mod 4')
    return P

def build_constraints(P):
    FM=[factor_small(p-1) for p in P]; FP=[factor_small(p+1) for p in P]
    LM=merge_lcm_factors(FM); LP=merge_lcm_factors(FP)
    rows=[]; mods=[]; targets=[]; meta=[]
    for typ,D in [('minus',LM),('plus',LP)]:
        for q,e in sorted(D.items()):
            if q==2: continue
            mod=q**e; order=phi_prime_power(q,e); g=primitive_root_prime_power(q,e)
            tab=dlog_table(g,mod,order)
            row=[]
            for p in P:
                a=p%mod
                if a not in tab: raise RuntimeError(('nonunit',typ,q,e,p))
                row.append(tab[a])
            rows.append(row); mods.append(order)
            targets.append(0 if typ=='minus' else order//2)
            meta.append({'type':typ,'q':q,'e':e,'unit_modulus':mod,'generator':g,'order':order})
    E=LP[2]
    if E<3: raise RuntimeError('2-adic component too small')
    mod=2**E; order=2**(E-2); tab=dlog_table(5,mod,order)
    rows.append([1]*len(P)); mods.append(2); targets.append(1)
    meta.append({'type':'2sign','q':2,'e':1,'unit_modulus':4,'generator':-1,'order':2})
    row=[]
    for p in P:
        a=(-p)%mod
        if a not in tab: raise RuntimeError(('bad 2-adic unit',p,a))
        row.append(tab[a])
    rows.append(row); mods.append(order); targets.append(0)
    meta.append({'type':'2exp','q':2,'e':E,'unit_modulus':mod,'generator':5,'order':order})
    return rows,mods,targets,meta,LM,LP

def write_matrix(path, rows):
    with open(path,'w',encoding='ascii') as f:
        f.write('[')
        for i,row in enumerate(rows):
            if i: f.write('\n ')
            f.write('['+' '.join(map(str,row))+']')
        f.write(']\n')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='work')
    ap.add_argument('--cache',default='williams_search/SET-1029-PRIMES.txt')
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--scale-bits',type=int,default=20)
    ap.add_argument('--embedding',action='store_true')
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    P=load_primes(args.cache)
    A,mods,target,meta,LM,LP=build_constraints(P)
    n=len(P); r=len(A); C=1<<args.scale_bits
    rng=random.Random(args.seed)
    complement=[rng.getrandbits(1) for _ in range(n)] if args.seed else [0]*n
    signs=[-1 if b else 1 for b in complement]
    target2=[]; A2=[]
    for row,m,t in zip(A,mods,target):
        shift=sum(a for a,b in zip(row,complement) if b)
        target2.append((t-shift)%m)
        A2.append([(s*a)%m for s,a in zip(signs,row)])
    d=n+r
    basis=[]
    for i in range(n):
        row=[0]*d; row[i]=2
        for j in range(r): row[n+j]=2*C*A2[j][i]
        basis.append(row)
    for j,m in enumerate(mods):
        row=[0]*d; row[n+j]=2*C*m
        basis.append(row)
    target_vec=[1]*n+[2*C*t for t in target2]
    write_matrix(out/'basis.lat',basis)
    (out/'target.txt').write_text('['+' '.join(map(str,target_vec))+']\n',encoding='ascii')
    info={
      'source_url':URL,'source_sha256':EXPECTED_SHA256,'n_primes':n,'n_constraints':r,
      'dimension':d,'seed':args.seed,'scale_bits':args.scale_bits,'scale':C,
      'complement':complement,'mods':mods,'target_original':target,'target_transformed':target2,
      'constraint_meta':meta,
      'Lminus_factorization':{str(k):v for k,v in sorted(LM.items())},
      'Lplus_factorization':{str(k):v for k,v in sorted(LP.items())},
      'Lminus':str(math.prod(q**e for q,e in LM.items())),
      'Lplus':str(math.prod(q**e for q,e in LP.items()))
    }
    (out/'meta.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print(json.dumps({k:info[k] for k in ['n_primes','n_constraints','dimension','seed','scale_bits']}))

if __name__=='__main__': main()
