#!/usr/bin/env python3
"""用本轮实际虚构姓名复核盲审，而不是依赖现有尺内固定的张三。"""
import json
from pathlib import Path
import re
import fitz

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def compact(s):return re.sub(r'\s+','',s)
def inspect(doc,names):
    text=compact(''.join(p.get_text() for p in doc))
    return dict(metadata_author=doc.metadata.get('author',''),visible_names=[n for n in names if n and compact(n) in text])
def main():
    # 真实PDF故障注入：文字层和Author元数据同时故意泄漏。
    d=fitz.open();p=d.new_page();positive=inspect(d,['测试作者']);assert not positive['visible_names'] and not positive['metadata_author']
    p.insert_text((100,100),'测试作者',fontname='china-s');d.set_metadata({'author':'测试作者'});negative=inspect(d,['测试作者']);assert negative['visible_names']==['测试作者'] and negative['metadata_author']=='测试作者';d.close()
    results=[]
    for rn in (1,2,3):
        batch=json.loads((HERE/f'results-r{rn:02}.json').read_text())
        for c in batch['cases']:
            if not c['blind'] or c['compile_rc']:continue
            source=(ROOT/c['source']).read_text();names=[]
            for key in ('author','author-en','student-id'):
                m=re.search(r'(?m)^  '+key+r': ("(?:[^"\\]|\\.)*"),',source)
                if m:names.append(json.loads(m[1]))
            for key in ('supervisor','supervisor-en'):
                m=re.search(r'(?m)^  '+key+r': \(("(?:[^"\\]|\\.)*"),',source)
                if m:names.append(json.loads(m[1]))
            with fitz.open(HERE/'out'/(c['name']+'.pdf')) as doc:result=inspect(doc,names)
            results.append(dict(name=c['name'],expected_names=names,**result))
    errors=[r for r in results if r['metadata_author'] or r['visible_names']]
    (HERE/'blind-results.json').write_text(json.dumps(dict(positive_control=positive,negative_control=negative,cases=results,failed=errors),ensure_ascii=False,indent=2)+'\n')
    print('盲审实际姓名验证',len(results),'份，失败',len(errors),'；文字/元数据泄漏负向测试通过。')
    for e in errors:print(e)
    raise SystemExit(bool(errors))
if __name__=='__main__':main()
