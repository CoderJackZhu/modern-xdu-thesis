#!/usr/bin/env python3
"""独立 PDF 通用检查。只报告可测证据，不把候选自动判作模板缺陷。

页眉/页码按版式区分；目录通过 PDF 内部链接验证目标页和标题；
行距只判无结构对象打断的 12pt 连续文字行，不把公式高度当正文行距。
"""
import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path
import fitz

MM=72/25.4

def compact(s): return re.sub(r'\s+', '', s)
def lines(page):
    out=[]
    for bi,b in enumerate(page.get_text('dict')['blocks']):
        for line in b.get('lines',[]):
            ss=[s for s in line['spans'] if s['text'].strip()]
            if ss:
                out.append(dict(text=''.join(s['text'] for s in ss),spans=ss,y=ss[0]['origin'][1],x=min(s['bbox'][0] for s in ss),x1=max(s['bbox'][2] for s in ss),size=ss[0]['size'],block=bi,bbox=line['bbox']))
    return out

def roman(n):
    out=''
    for k,s in [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        while n>=k:out+=s;n-=k
    return out

def parse_number(s):
    if re.fullmatch(r'\d+',s):return ('arabic',int(s))
    s=s.upper()
    if not re.fullmatch('[IVXLCDM]+',s):return None
    for n in range(1,2000):
        if roman(n)==s:return ('roman',n)
    return None

def page_number(ls,kind):
    area=[l for l in ls if (l['y']<80 if kind=='bachelor' else l['y']>780) and abs(l['size']-9)<.2]
    nums=[(l,parse_number(compact(l['text']))) for l in area]
    return next(((l,n) for l,n in nums if n), (None,None))

def has_header(ls): return any(48<l['y']<80 and l['size']>=9.5 for l in ls)

def ink_in(page,rect):
    """按 stride 逐行切片，忽略填充字节，返回真实非白墨迹包围盒。"""
    rect=fitz.Rect(rect)&page.rect
    rect=fitz.Rect(math.ceil(rect.x0),math.ceil(rect.y0),math.floor(rect.x1),math.floor(rect.y1))
    if rect.is_empty:return None
    pm=page.get_pixmap(matrix=fitz.Matrix(1,1),clip=rect,colorspace=fitz.csGRAY,alpha=False,annots=False)
    samples=pm.samples
    xs=[];ys=[]
    for row in range(pm.height):
        data=samples[row*pm.stride:row*pm.stride+pm.width]
        if data and min(data)<200:
            nonwhite=[i for i,c in enumerate(data) if c<200]
            xs.extend((min(nonwhite),max(nonwhite)));ys.append(row)
    if not ys:return None
    return [pm.x+min(xs),pm.y+min(ys),pm.x+max(xs)+1,pm.y+max(ys)+1]

def geometry(doc,all_lines,profile):
    issues=[];kind=profile['kind'];thesis=kind in ('thesis','bachelor')
    for i,(page,ls) in enumerate(zip(doc,all_lines)):
        if abs(page.rect.width-595.276)>1 or abs(page.rect.height-841.89)>1:
            issues.append(dict(check='ink',page=i+1,detail='不是 A4'))
        numbered=page_number(ls,kind)[1] is not None
        if thesis and numbered:
            left=(40 if i%2==0 else 20) if kind=='bachelor' else (30 if i%2==0 else 25)
            right=(20 if i%2==0 else 40) if kind=='bachelor' else (25 if i%2==0 else 30)
            bottom=(277 if kind=='bachelor' else 270.93)*MM
            # 侧边包括页眉，允许2pt栅格化误差；底部检查截止页脚之上。
            rects=[(0,85,left*MM-2,page.rect.height if kind=='bachelor' else 780),((210-right)*MM+2,85,page.rect.width,780),(left*MM,bottom+2,(210-right)*MM,780)]
        elif thesis:
            # 封面/题名页有独立绝对定位规格，不能强套正文版心。
            cover_left=30 if kind=='bachelor' else (30 if i%2==0 else 25)
            cover_right=30 if kind=='bachelor' else (25 if i%2==0 else 30)
            rects=[(0,0,cover_left*MM-2,page.rect.height),((210-cover_right)*MM+2,0,page.rect.width,page.rect.height),(0,0,page.rect.width,12*MM),(0,292*MM,page.rect.width,page.rect.height)]
        else:
            margin=31.7 if kind=='bachelor-proposal' else (22 if kind=='course-report' else 25.4)
            vertical=22 if kind=='course-report' else 25.4
            rects=[(0,0,margin*MM-2,page.rect.height),((210-margin)*MM+2,0,page.rect.width,page.rect.height),(0,0,page.rect.width,vertical*MM-2),(0,(297-vertical)*MM+2,page.rect.width,page.rect.height)]
        for r in rects:
            hit=ink_in(page,r)
            if hit:issues.append(dict(check='ink',page=i+1,detail=f'版心/打印边界外墨迹 bbox(bp)={hit}'))
    return issues

def pagination(doc,all_lines,profile):
    issues=[];kind=profile['kind']
    if kind not in ('thesis','bachelor'):return issues
    numbers=[page_number(ls,kind)[1] for ls in all_lines]
    first=next((i for i,n in enumerate(numbers) if n is not None),None)
    if first is None:return [dict(check='pagination',page=1,detail='全文无可辨认页码')]
    if numbers[first] != ('roman',1):issues.append(dict(check='pagination',page=first+1,detail=f'前置页码未从罗马1开始：{numbers[first]}'))
    prev=None;arabic_started=False
    for i in range(first,len(doc)):
        n=numbers[i];ls=all_lines[i]
        blank=not any(85<l['y']<778 for l in ls)
        check='blank' if blank else 'pagination'
        if n is None:issues.append(dict(check=check,page=i+1,detail='编号区缺页码'))
        if not has_header(ls):issues.append(dict(check=check,page=i+1,detail='编号区缺页眉'))
        if n:
            if prev and n!=(prev[0],prev[1]+1):
                if not(prev[0]=='roman' and n==('arabic',1)):
                    issues.append(dict(check='pagination',page=i+1,detail=f'页码不连续：{prev} → {n}'))
            if arabic_started and n[0]=='roman':issues.append(dict(check='pagination',page=i+1,detail='正文后切回罗马页码'))
            if n[0]=='arabic':arabic_started=True
            prev=n
    # 从第一章的大标题位置判定切换，不能仅凭页码本身证明切换正确。
    chapter=next((i for i,ls in enumerate(all_lines) if any('第一章' in l['text'] and l['size']>=15 and l['y']>85 for l in ls)),None)
    if chapter is not None and numbers[chapter]!=('arabic',1):issues.append(dict(check='pagination',page=chapter+1,detail='第一章首页未切为阿拉伯1'))
    return issues

def unresolved(all_lines):
    out=[]
    for i,ls in enumerate(all_lines):
        for l in ls:
            if re.search(r'\?\?|？？|\[\s*\]|\(\s*\)',l['text']) or compact(l['text']) in ('?','？'):
                out.append(dict(check='references',page=i+1,detail=l['text'][:160]))
    return out

def numbering(all_lines,profile):
    if profile['kind'] not in ('thesis','bachelor'):return []
    out=[];found=defaultdict(list)
    appendix=False
    for i,ls in enumerate(all_lines):
        for l in ls:
            t=compact(l['text'])
            if l['y']<85:continue
            if l['size']>=15 and ('附录' in t or '补充材料' in t):appendix=True
            if appendix:continue  # 附录编号另按本科独立口径复核，不将其套入阿拉伯章号。
            if abs(l['size']-10.5)<.3:
                m=re.match(r'^(图|表)(\d+)\.(\d+)',t)
                if m:found[(m[1],int(m[2]))].append((int(m[3]),i+1))
                elif re.match(r'^[图表]\d',t):out.append(dict(check='numbering',page=i+1,detail='图表编号缺章前缀：'+t))
            for sp in l['spans']:
                st=compact(sp['text'])
                if sp['origin'][0]>440:
                    m=re.fullmatch(r'\((\d+)-(\d+)\)',st)
                    if m:found[('式',int(m[1]))].append((int(m[2]),i+1))
                    elif re.fullmatch(r'\(\d+\)',st):out.append(dict(check='numbering',page=i+1,detail='公式编号缺章前缀：'+st))
    for key,seq in found.items():
        # 同个PDF行若抽出重复span，仅保留一次；不同页重复编号仍是错误。
        for expected,(n,p) in enumerate(seq,1):
            if n!=expected:out.append(dict(check='numbering',page=p,detail=f'{key} 编号应为{expected}，实际{n}'))
    return out

def toc(doc,all_lines,profile):
    if profile['kind'] not in ('thesis','bachelor'):return []
    out=[];active=False;page_nums=[page_number(ls,profile['kind'])[1] for ls in all_lines]
    for i,(page,ls) in enumerate(zip(doc,all_lines)):
        if any(compact(l['text'])=='目录' and l['size']>=15 for l in ls):active=True
        elif active and any('第一章' in l['text'] and l['size']>=15 and l['y']>85 for l in ls):active=False
        if not active:continue
        # 一条目录的所有链接片段合并，含换行标题；链接目标必须落在正文标题页。
        groups=defaultdict(list)
        for link in page.get_links():
            if link.get('kind')==fitz.LINK_GOTO and link.get('page',-1)>=0 and link['from'].y0>85:
                groups[link['page']].append(link['from'])
        for target,rects in groups.items():
            rows=[l for l in ls if l['y']>85 and any(fitz.Rect(l['bbox']).intersects(r) for r in rects)]
            # 多标题同目标页时按基线分组，行尾页码与独立标题链接分别验证。
            text=''.join(l['text'] for l in sorted(rows,key=lambda z:(round(z['y'],1),z['x'])))
            nums=[parse_number(compact(l['text'])) for l in rows if re.fullmatch(r'[0-9IVXLCDMivxlcdm]+',compact(l['text']))]
            expected=page_nums[target] if target<len(doc) else None
            if nums and expected not in nums:out.append(dict(check='toc',page=i+1,detail=f'目录目标物理页{target+1}，显示页码{nums}，实际{expected}'))
            target_text=compact(doc[target].get_text()) if target<len(doc) else ''
            # 优先比较真实标题文字；节标题编号可能被 PDF 拆成单独 span。
            for l in rows:
                t=compact(l['text'])
                if len(t)<3 or re.fullmatch(r'[.·…0-9IVXLCivxlc]+',t):continue
                t=re.sub(r'^[0-9.]+','',t).strip(' .·…')
                if t and t not in target_text:
                    # 连续的页码/点线在同一 span 时，剥掉末尾目录装饰。
                    clean=re.sub(r'[.·…]+[0-9IVXLCivxlc]*$','',t)
                    if clean and clean not in target_text:out.append(dict(check='toc',page=i+1,detail=f'目录文字不在目标页{target+1}：{t[:100]}'))
    return out

def spacing(doc,all_lines,profile):
    out=[];expected=23.4 if profile['kind']=='bachelor' else 20.0
    for i,ls in enumerate(all_lines):
        if profile['kind'] in ('thesis','bachelor') and page_number(ls,profile['kind'])[1] is None:continue
        # 同一文字块中的连续长正文行，排除表格单元格、代码、短图题与数学字形。
        groups=defaultdict(list)
        rules=[float(it[1].y) for dr in doc[i].get_drawings() for it in dr['items'] if it[0]=='l' and abs(it[1].y-it[2].y)<.1 and abs(it[1].x-it[2].x)>10]
        for l in ls:
            if 85<l['y']<780 and len(l['text'])>=18 and all(abs(s['size']-12)<.15 and not(s['flags'] & 16) and 'Hei' not in s['font'] and 'Math' not in s['font'] for s in l['spans']):groups[0].append(l)
        for group in groups.values():
            ys=sorted(set(round(l['y'],3) for l in group))
            for a,b in zip(ys,ys[1:]):
                delta=b-a
                if 8<delta<30 and abs(delta-expected)>.08 and not any(a+.2 < z['y'] < b-.2 and z not in group for z in ls) and not any(a < y < b for y in rules):
                    out.append(dict(check='spacing',page=i+1,detail=f'相邻正文基线 {a:.3f}/{b:.3f}，差{delta:.3f}bp，应为{expected:.3f}bp'))
    return out

def inspect(path,profile):
    with fitz.open(path) as doc:
        ls=[lines(p) for p in doc]
        issues=geometry(doc,ls,profile)+pagination(doc,ls,profile)+unresolved(ls)+numbering(ls,profile)+toc(doc,ls,profile)+spacing(doc,ls,profile)
        return dict(pages=len(doc),issues=issues,counts={k:sum(x['check']==k for x in issues) for k in ('ink','pagination','blank','references','numbering','toc','spacing')})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf');p.add_argument('--kind',default='thesis');a=p.parse_args();r=inspect(a.pdf,dict(kind=a.kind));print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(bool(r['issues']))
