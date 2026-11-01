#!/usr/bin/env python3
"""用真正的多页 PDF 注入缺陷，逐项证明检查能抓到第二页/续页错误。"""
import json
from pathlib import Path
import fitz
import checks

OUT=Path(__file__).resolve().parent/'out'/'negative'

def base():
    d=fitz.open()
    for i in range(3):
        p=d.new_page(width=595.276,height=841.89)
        p.insert_text((200,70),'Fictional Thesis Header',fontsize=10.5)
        p.insert_text((290,792.28),['I','1','2'][i],fontsize=9)
        if i!=2:
            for j in range(4):p.insert_text((100,160+20*j),'Long fictional body paragraph for line spacing verification.',fontsize=12)
    return d

def clear(d,page,rect):
    d[page].add_redact_annot(fitz.Rect(rect),fill=(1,1,1));d[page].apply_redactions()

def test():
    OUT.mkdir(parents=True,exist_ok=True)
    profile=dict(kind='thesis');summary=[]
    def save(d,name):
        f=OUT/(name+'.pdf');d.save(f);d.close();return checks.inspect(f,profile)
    positive=save(base(),'positive')
    assert not positive['issues'],positive
    mutations={
        'ink':lambda d:d[1].insert_text((10,200),'OUTSIDE',fontsize=12),
        'pagination':lambda d:(clear(d,1,(270,780,320,810)),d[1].insert_text((290,792.28),'4',fontsize=9)),
        'header':lambda d:clear(d,1,(0,45,595,80)),
        'blank':lambda d:(clear(d,2,(0,45,595,80)),clear(d,2,(270,780,320,810))),
        'references':lambda d:d[1].insert_text((100,300),'Unresolved ?? reference []',fontsize=12),
        'numbering':lambda d:(d[1].insert_text((200,320),'(1)',fontsize=12),d[1].insert_text((470,340),'(1-2)',fontsize=12)),
        'spacing':lambda d:(clear(d,1,(85,140,580,240)),*[d[1].insert_text((100,160+24*j),'Long fictional body paragraph for line spacing verification.',fontsize=12) for j in range(4)]),
    }
    for name,mutate in mutations.items():
        d=base();mutate(d);r=save(d,name);key='pagination' if name=='header' else name
        assert r['counts'][key]>0,(name,r)
        summary.append(dict(test=name,caught=r['counts'][key],page=2 if name!='blank' else 3))
    # 独立目录样本：文字在目的页存在，页码故意写错。
    d=base();clear(d,0,(85,140,580,260));d[0].insert_text((250,125),'目录',fontname='china-s',fontsize=16)
    d[0].insert_text((100,170),'Target Heading',fontsize=12);d[0].insert_text((490,170),'9',fontsize=12)
    d[1].insert_text((100,280),'Target Heading',fontsize=16)
    d[0].insert_link(dict(kind=fitz.LINK_GOTO,from_=fitz.Rect(98,155,520,176),page=1,to=fitz.Point(100,280))) if False else None
    d[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(98,155,520,176),'page':1,'to':fitz.Point(100,280)})
    r=save(d,'toc');assert r['counts']['toc']>0,r;summary.append(dict(test='toc',caught=r['counts']['toc']))
    # 对该样本改回正确页码后，目录检查应通过，防止一个只会报错的检查。
    d=fitz.open(OUT/'toc.pdf');clear(d,0,(480,153,530,178));d[0].insert_text((490,170),'1',fontsize=12)
    r=save(d,'toc-positive');assert r['counts']['toc']==0,r
    (OUT.parent.parent/'negative-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print('8项故障注入全部检出；正常多页与正确目录通过。')

if __name__=='__main__':test()
