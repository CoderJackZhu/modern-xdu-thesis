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
        'empty_reference':lambda d:d[1].insert_text((100,300),'Empty reference []',fontsize=12),
        'question_reference':lambda d:d[1].insert_text((100,300),'?',fontsize=12),
        'missing_prefix':lambda d:d[1].insert_text((470,340),'(1)',fontsize=12),
        'chapter_switch':lambda d:d[0].insert_text((100,280),'第一章',fontname='china-s',fontsize=16),
        'numbering':lambda d:(d[1].insert_text((200,320),'(1)',fontsize=12),d[1].insert_text((470,340),'(1-2)',fontsize=12)),
        'spacing':lambda d:(clear(d,1,(85,140,580,240)),*[d[1].insert_text((100,160+24*j),'Long fictional body paragraph for line spacing verification.',fontsize=12) for j in range(4)]),
    }
    for name,mutate in mutations.items():
        d=base();mutate(d);r=save(d,name);key={'header':'pagination','empty_reference':'references','question_reference':'references','missing_prefix':'numbering','chapter_switch':'pagination'}.get(name,name)
        assert r['counts'][key]>0,(name,r)
        summary.append(dict(test=name,caught=r['counts'][key],page=2 if name!='blank' else 3))
    # 本科附录有明确的字母编号口径，与研究生附录缺实测坐标是两件事。
    for sequence,expected in [(1,0),(2,1)]:
        d=base();d[1].insert_text((200,125),'附录 A',fontname='china-s',fontsize=16)
        d[1].insert_text((200,310),f'图 A{sequence} 测试',fontname='china-s',fontsize=10.5)
        d[1].insert_text((470,340),f'(A-{sequence})',fontsize=12)
        result=checks.numbering([checks.lines(p) for p in d],dict(kind='bachelor'))
        assert bool(result)==bool(expected),result
        d.close()
    summary.append(dict(test='undergraduate-appendix-numbering',caught=len(result)))
    # 本科使用独立23.4pt口径，不能套用研究生20pt。
    for step,expected in [(23.4,0),(20,1)]:
        d=base()
        for i in range(3):
            clear(d,i,(0,140,595,260))
            d[i].insert_text((530 if i%2==0 else 58,61.51),['i','1','2'][i],fontsize=9)
            if i!=2:
                for j in range(4):d[i].insert_text((120,160+step*j),'Long fictional undergraduate paragraph for line spacing verification.',fontsize=12)
        f=OUT/f'undergrad-{step}.pdf';d.save(f);d.close()
        result=checks.inspect(f,dict(kind='bachelor'))
        assert bool(result['counts']['spacing'])==bool(expected),result
    summary.append(dict(test='undergraduate-spacing',caught=result['counts']['spacing']))
    # 跨表格行的内边距不应被当作正文基线间距。
    d=base();clear(d,1,(85,140,580,260))
    for j in range(4):
        d[1].insert_text((100,160+25*j),'Long fictional table cell contents for validation.',fontsize=12)
        d[1].draw_line((90,165+25*j),(540,165+25*j))
    r=save(d,'table-positive');assert r['counts']['spacing']==0,r
    # 独立目录样本：文字在目的页存在，页码故意写错。
    d=base();clear(d,0,(85,140,580,260));d[0].insert_text((250,125),'目录',fontname='china-s',fontsize=16)
    d[0].insert_text((100,170),'Target Heading',fontsize=12);d[0].insert_text((490,170),'9',fontsize=12)
    d[1].insert_text((100,280),'Target Heading',fontsize=16)
    d[0].insert_link(dict(kind=fitz.LINK_GOTO,from_=fitz.Rect(98,155,520,176),page=1,to=fitz.Point(100,280))) if False else None
    d[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(98,155,520,176),'page':1,'to':fitz.Point(100,280)})
    r=save(d,'toc');assert r['counts']['toc']>0,r;summary.append(dict(test='toc',caught=r['counts']['toc']))
    # 同时证明目录标题不匹配会被检出。
    d=fitz.open(OUT/'toc.pdf');clear(d,1,(85,260,580,300));r=save(d,'toc-title');assert any('目录文字' in i['detail'] for i in r['issues']),r
    summary.append(dict(test='toc-title',caught=r['counts']['toc']))
    # 对该样本改回正确页码后，目录检查应通过，防止一个只会报错的检查。
    d=fitz.open(OUT/'toc.pdf');clear(d,0,(480,153,530,178));d[0].insert_text((490,170),'1',fontsize=12)
    r=save(d,'toc-positive');assert r['counts']['toc']==0,r
    (OUT.parent.parent/'negative-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(summary)}项故障注入全部检出；正常多页、表格行距与正确目录通过。')

if __name__=='__main__':test()
