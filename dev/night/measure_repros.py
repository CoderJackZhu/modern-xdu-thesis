#!/usr/bin/env python3
"""重编最小复现，保存原始坐标；不修改任何模板。"""
import json
import os
from pathlib import Path
import subprocess
import fitz

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=HERE/'out'
def main():
    outside=subprocess.check_output(['git','diff','--name-only','origin/main','--','.',':(exclude)dev/night/**'],cwd=ROOT,text=True)
    assert not outside,'存在范围外修改，立即停止：'+outside
    base=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
    env=dict(os.environ,TYPST_PACKAGE_PATH=str(OUT/'packages'));results=[]
    for source in sorted((HERE/'repro').glob('*.typ')):
        p=subprocess.run(['typst','compile','--root',str(ROOT),str(source),str(OUT/(source.stem+'.pdf'))],cwd=ROOT,env=env,capture_output=True,text=True,timeout=120)
        (OUT/(source.stem+'.compile.log')).write_text(p.stderr)
        result=dict(file=str(source.relative_to(ROOT)),rc=p.returncode,errors=[l for l in p.stderr.splitlines() if l.startswith('error:')])
        if p.returncode==0:
            with fitz.open(OUT/(source.stem+'.pdf')) as doc:
                result['pages']=len(doc)
                result['lines']=[dict(page=i+1,text=''.join(s['text'] for s in l['spans']),spans=[dict(text=s['text'],size=round(s['size'],3),x=round(s['origin'][0],3),y=round(s['origin'][1],3)) for s in l['spans']]) for i,page in enumerate(doc) for b in page.get_text('dict')['blocks'] for l in b.get('lines',[])]
                doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(OUT/(source.stem+'.png'))
        results.append(result);print(source.stem,p.returncode,result.get('pages'),result['errors'])
    (HERE/'repro-results.json').write_text(json.dumps(dict(base=base,restricted_source_diff=[],results=results),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
