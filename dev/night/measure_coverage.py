#!/usr/bin/env python3
"""记录长表、索引、文献的实际可提取条目数，供人工复核内容完整性。"""
import json
from pathlib import Path
import re
import fitz
HERE=Path(__file__).resolve().parent

def main():
    result=[]
    for rn in (1,2,3):
        batch=json.loads((HERE/f'results-r{rn:02}.json').read_text())
        for c in batch['cases']:
            if c['compile_rc'] or c['scenario'] not in ('bib300','bib_types','many_figures','long_table','long_indexes'):continue
            doc=fitz.open(HERE/'out'/(c['name']+'.pdf'));text='\n'.join(p.get_text() for p in doc)
            row=dict(name=c['name'],scenario=c['scenario'],kind=c['kind'])
            if c['scenario'] in ('bib300','bib_types'):
                ids=[]
                for page in doc:
                    for b in page.get_text('dict')['blocks']:
                        for line in b.get('lines',[]):
                            for s in line['spans']:
                                m=re.match(r'^\[(\d+)\]',s['text'].strip())
                                if m and s['size']>=9.5 and s['origin'][0]<116:ids.append(int(m[1]))
                row.update(reference_labels=sorted(set(ids)),expected=300 if c['scenario']=='bib300' else 14,english_etal_occurrences=text.count('et al'),chinese_deng_occurrences=text.count('等'))
            elif c['scenario']=='long_table':row.update(table_rows=sorted(set(map(int,re.findall(r'(\d+)\s*虚构长表内容',text)))),expected=150+(rn-1)*5)
            elif c['scenario']=='many_figures':row.update(figure_captions=len(set(re.findall('图题测试(\d+)',text))),table_captions=len(set(re.findall('表题测试(\d+)',text))),expected=70+(rn-1)*3)
            elif c['scenario']=='long_indexes' and c['kind']=='thesis':row.update(symbols=len(set(re.findall(r'\bS(\d+)\b',text))),abbreviations=len(set(re.findall(r'ABC(\d+)',text))),expected=140+(rn-1)*3)
            result.append(row);doc.close()
    (HERE/'coverage-measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    for r in result:
        if 'reference_labels' in r:
            if r['reference_labels']!=list(range(1,r['expected']+1)):print('文献标签待复核',r['name'],len(r['reference_labels']))
        if 'table_rows' in r and r['table_rows']!=list(range(r['expected'])):print('长表内容待复核',r['name'],len(r['table_rows']))
        if 'figure_captions' in r and (r['figure_captions']!=r['expected'] or r['table_captions']!=r['expected']):print('图表内容待复核',r['name'],r)
        if 'symbols' in r and (r['symbols']!=r['expected'] or r['abbreviations']!=r['expected']):print('索引内容待复核',r['name'],r)
    print('测量样本数',len(result))
if __name__=='__main__':main()
