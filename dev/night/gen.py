#!/usr/bin/env python3
"""生成虚构用户输入；不改模板，不依赖全局本地包软链。"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCENARIOS = 'baseline long_titles long_fields multiple_supervisors optional_empty required_empty required_none mixed long_abstract many_keywords abstract_math heading4 heading5 one_chapter twenty_chapters long_chapter heading_math heading_footnote many_figures long_table sub_parallel equations code_notes_lists long_indexes bib0 bib1 bib300 bib_types appendices long_back'.split()
PROFILES = [{'id':'bachelor','kind':'bachelor','degree':'academic','blind':False,'graduate':'bachelor'}]
for g in ('master','doctor'):
    for d in ('academic','professional'):
        for blind in (False,True):
            PROFILES.append(dict(id=f'{g}-{d}'+('-blind' if blind else ''),kind='thesis',graduate=g,degree=d,blind=blind))
for kind in ('proposal','interim'):
    for g in ('master','doctor'):
        for d in ('academic','professional'):
            PROFILES.append(dict(id=f'{kind}-{g}-{d}',kind=kind,graduate=g,degree=d,blind=False))
for kind in ('bachelor-proposal','bachelor-interim','course-report'):
    PROFILES.append(dict(id=kind,kind=kind,graduate='bachelor' if kind.startswith('bachelor') else 'master',degree='academic',blind=False))

ZH = '本段研究虚构系统的性能与验证方法，说明实验条件、数据来源和适用边界。所有人物、数据与成果均为虚构，不包含真实论文内容。'
EN = 'This fictional experiment studies reliable modeling under controlled conditions. All names and results are synthetic and the assumptions are explicitly stated. '
def q(x):
    return json.dumps(x,ensure_ascii=False)
def repeated(n):
    return '\n\n'.join([ZH]*n)
def bibliography(n):
    types = ['article','inproceedings','phdthesis','patent','standard','online','incollection']
    result=[]
    for i in range(n):
        chinese=i%2==0
        typ=types[i%len(types)]
        author='张甲 and 王乙 and 李丙 and 赵丁 and 钱戊' if chinese else 'Alpha, Alice and Beta, Bob and Gamma, Carol and Delta, David and Epsilon, Eve'
        title=f'虚构研究条目{i+1}' if chinese else f'Fictional Research Item {i+1}'
        result.append(f'@{typ}{{r{i},\n author = {{{author}}},\n title = {{{title}}},\n year = {{2025}},\n date = {{2025-06-01}},\n journal = {{{"虚构研究期刊" if chinese else "Fictional Research Journal"}}},\n booktitle = {{Fictional Collected Research}},\n publisher = {{Fictional Press}},\n institution = {{Fictional University}},\n school = {{Fictional University}},\n number = {{CN000000{i}}},\n pages = {{1--9}},\n url = {{https://example.com/paper/{i}}},\n urldate = {{2026-10-01}},\n langid = {{{"chinese" if chinese else "english"}}}\n}}')
    return '\n\n'.join(result)+'\n'

def content(s, v):
    body = ''
    n=v
    if s in ('heading4','heading5'):
        body='== 二级测试\n\n=== 三级测试\n\n==== 四级甲\n\n'+ZH+'\n\n==== 四级乙\n\n'+ZH
        if s=='heading5': body+='\n\n===== 五级深层测试\n\n'+ZH
    elif s=='twenty_chapters':
        nums=['二','三','四','五','六','七','八','九','十','十一','十二','十三','十四','十五','十六','十七','十八','十九','二十']
        body='\n\n'.join('= 第'+x+'章 测试章\n\n'+ZH for x in nums)
    elif s in ('many_figures','long_indexes'):
        count=70+v*3 if s=='many_figures' else 4
        body='\n\n'.join(f'#figure(rect(width: 35mm, height: 6mm), caption: [图题测试{i}]) <fig:many{i}>\n#figure(table(columns: 2, [项目], [数值], [测试{i}], [1]), caption: [表题测试{i}]) <tab:many{i}>' for i in range(count))
    elif s=='long_table':
        body='#show figure: set block(breakable: true)\n#figure(table(columns: (20mm, 1fr), table.header([行号], [观测数据]), ..range('+str(150+v*5)+').map(i => ([#i], [虚构长表内容])).flatten()), caption: [跨页观测记录]) <tab:long>\n\n表 @tab:long。\n\n'+repeated(3)
    elif s=='sub_parallel':
        body='#figure(grid(columns: (1fr, 1fr), gutter: 8pt, [#rect(width: 30mm, height: 20mm)\n(a) 子图甲], [#rect(width: 30mm, height: 20mm)\n(b) 子图乙]), caption: [两张并排子图]) <fig:sub>\n\n图 @fig:sub。'
    elif s=='equations':
        body='\n\n'.join(f'$ y_{i} &= a x + b \\ z_{i} &= c x + d $ <eq:multi{i}>\n\n式 @eq:multi{i}。\n\n'+ZH for i in range(12+v))
    elif s=='code_notes_lists':
        body='正文带脚注#footnote[脚注内容用于检查长文档。]。\n\n```python\ndef fictional(value):\n    return value + 1\n```\n\n- 一级列表\n  - 二级列表\n    - 三级列表\n- 第二个项目\n\n'+repeated(8)
    elif s in ('bib1','bib300','bib_types'):
        count=300 if s=='bib300' else (1 if s=='bib1' else 14)
        body='\n\n'.join(f'文献测试条目{i+1}#cite(<r{i}>)。' for i in range(count))
    elif s in ('long_abstract','many_keywords','abstract_math'):
        body=repeated(4)
    return body

def thesis(p,s,v):
    bachelor=p['kind']=='bachelor'
    entry='bachelor.typ' if bachelor else ('doctor.typ' if p['graduate']=='doctor' else 'lib.typ')
    info={
        'title':'("虚构系统验证研究",)', 'title-en':'("Fictional System Verification",)',
        'author':q('测试作者'), 'author-en':q('Fictional Author'),
        'department':q('电子工程学院'), 'major':q('电子信息工程'),
        'student-id':q('202600001'), 'discipline':q('电子科学与技术'),
        'subdiscipline':q('电路与系统'), 'supervisor':'("测试导师", "教授")',
        'supervisor-en':'("Fictional Advisor", "Professor")',
        'abstract':'['+repeated(4)+']','abstract-en':'['+EN*5+']',
        'acknowledgement':'['+ZH+']',
    }
    if bachelor: info['supervisor']='("测试导师甲", "测试导师乙")'
    if s=='long_titles':
        info['title']='('+q('面向多源异构数据的可靠系统建模及验证方法研究'* (5+v))+',)'
        info['title-en']='('+q('Reliable Modeling and Verification of Heterogeneous Complex Systems '*(6+v))+',)'
    if s=='long_fields':
        for k in ('author','department','major','discipline','subdiscipline'): info[k]=q('中英Mixed复杂联合研究'+k*3+'中心'*12)
        info['supervisor']='('+q('导师姓名很长'*8)+', "教授")'
        info['supervisor-en']='('+q('Very Long Advisor Name '*10)+', "Professor")'
    if s=='multiple_supervisors':
        info['supervisor']='("导师甲、导师乙、导师丙", "教授、副教授、高级工程师")'
        info['supervisor-en']='("Advisor Alpha, Advisor Beta, Advisor Gamma", "Professors")'
    if s=='optional_empty':
        info.update({'enterprise-supervisor':'(none, none)','enterprise-supervisor-en':'(none, none)','subdiscipline':'""'})
    if s in ('required_empty','required_none'):
        info['title']='""' if s=='required_empty' else 'none'
        info['author']='""' if s=='required_empty' else 'none'
        info['student-id']='""'
    if s=='mixed':
        info['title']='("中英 Mixed：验证（A/B）与测试, V2.0！",)'
        info['author']=q('阿卜杜拉·测试')
    if s=='long_abstract':
        info['abstract']='['+repeated(80+v*3)+']'
        info['abstract-en']='['+EN*(90+v*3)+']'
    if s=='many_keywords':
        info['keywords']='('+','.join(q(f'测试关键词{i}') for i in range(60+v))+',)'
        info['keywords-en']='('+','.join(q(f'fictional keyword {i}') for i in range(60+v))+',)'
    if s=='abstract_math':
        info['abstract-en']='[We study $alpha + beta = integral_0^1 x dif x$. Symbols: Ω, ±, ≤, ≥, 50%, A/B, and C++.]'
    if s=='long_indexes':
        info['notation']='('+','.join(f'("S{i}", "符号名称{i}及其解释")' for i in range(140+v*3))+',)'
        info['abbreviations']='('+','.join(f'("ABC{i:03}", "Fictional Long English Term {i}", "缩略语解释{i}")' for i in range(140+v*3))+',)'
    if s=='long_back':
        info['acknowledgement']='['+repeated(90+v)+']'
        info['bio']='(("基本情况", '+q(ZH*60)+'), ("研究成果", '+q('\n'.join(f'{i}. 第一作者：测试作者. 虚构研究成果。' for i in range(160)))+'))'
    args='' if bachelor else f'degree: "{p["degree"]}", blind: {str(p["blind"]).lower()}, '
    source=f'// 虚构测试：{p["id"]}/{s}，变体{v}\n#import "../../../{entry}": documentclass\n#let t = documentclass('+args+'info: (\n'+''.join('  '+k+': '+val+',\n' for k,val in info.items())+'))\n#show: t.doc\n'
    front=['cover'] if bachelor else ['cover','title-cn','title-en','declaration']
    for f in front: source+=f'#(t.{f})()\n#pagebreak(to: "odd")\n'
    source+='#counter(page).update(1)\n'
    front=['abstract','abstract-en','outline-page'] if bachelor else ['abstract','abstract-en','list-of-figures','list-of-tables','notation','abbreviations','outline-page']
    source+='\n#pagebreak(to: "odd")\n'.join(f'#(t.{f})()' for f in front)
    source+='\n#show: t.mainmatter\n\n'
    heading='第一章 测试绪论'
    if s=='long_chapter': heading='第一章 '+('复杂系统的鲁棒建模方法与验证 '* (9+v))
    if s=='heading_math': heading='第一章 $alpha + beta$ 模型'
    if s=='heading_footnote': heading='第一章 测试#footnote[章标题脚注测试]'
    if bachelor: heading=heading.replace('第一章 ', '', 1)
    source+='= '+heading+' <head:one>\n\n'+repeated(4)+'\n\n'
    extra_body=content(s,v)
    if bachelor and s=='twenty_chapters':
        import re
        extra_body=re.sub(r'(?m)^= 第[一二三四五六七八九十]+章 ', '= ', extra_body)
    source+=extra_body+'\n\n'
    if s not in ('twenty_chapters','one_chapter'):
        source+=('= 图表公式' if bachelor else '= 第二章 图表公式')+'\n\n'+ZH+'\n\n'
    source+='#figure(rect(width: 45mm, height: 12mm), caption: [系统框图]) <fig:model>\n#figure(table(columns: 2, [参数], [数值], [实验], [1]), caption: [参数设置]) <tab:model>\n$ y = a x + b $ <eq:model>\n图 @fig:model、表 @tab:model、式 @eq:model；见 @head:one。\n'
    if s=='appendices':
        for i in range(3):
            source+=f'\n#pagebreak(to: "odd")\n#(t.appendix)(title: "补充材料{chr(65+i)}", body: [\n'+ZH+f'\n#figure(rect(width: 30mm, height: 10mm), caption: [附录图{i}]) <fig:app{i}>\n#figure(table(columns: 2, [甲], [乙]), caption: [附录表{i}]) <tab:app{i}>\n$ z = x + {i} $ <eq:app{i}>\n图 @fig:app{i}、表 @tab:app{i}、式 @eq:app{i}。\n])\n'
    source+='\n#pagebreak(to: "odd")\n'
    if s in ('bib1','bib300','bib_types'):
        source+='#(t.references)(body: bibliography("../refs.bib", style: "gb-7714-2015-numeric", title: none))\n'
    else:
        source+='#(t.references)(entries: ())\n'
    source+='#pagebreak(to: "odd")\n#(t.acknowledgement)()\n'
    if not bachelor: source+='#pagebreak(to: "odd")\n#(t.bio)()\n'
    return source

SUPPORT = {
    'proposal':('proposal-thesis.typ','supporting/proposal.typ','proposal-documentclass','abstract'),
    'interim':('interim-thesis.typ','supporting/interim.typ','interim-documentclass','completed'),
    'bachelor-proposal':('bachelor-proposal.typ','supporting/bachelor-forms.typ','bachelor-proposal-documentclass','purpose'),
    'bachelor-interim':('bachelor-interim.typ','supporting/bachelor-forms.typ','bachelor-interim-documentclass','completed'),
    'course-report':('course-report.typ','supporting/course-report.typ','course-report-documentclass',None),
}
def supporting(p,s,v):
    filename,entry,func,key=SUPPORT[p['kind']]
    source=(ROOT/'examples'/filename).read_text()
    source=source.replace('"@preview/modern-xdu-thesis:0.3.1"',q('../../../'+entry))
    source=source.replace('sys.inputs.at("graduate", default: "master")',q(p['graduate'])).replace('sys.inputs.at("degree", default: "academic")',q(p['degree']))
    # 替换调用参数，不改变行政表的固定字段或章节。
    if s=='long_titles':
        start=source.index('    title: '); end=source.index('\n',start)
        source=source[:start]+'    title: '+q('多源异构系统验证方法研究'*(10+v)+' Reliable Modeling and Verification of Complex Systems '*(5+v))+','+source[end:]
    if s in ('long_fields','multiple_supervisors','optional_empty','required_empty','required_none','mixed'):
        import re
        changes={}
        if s=='long_fields':
            changes={k:q('复杂联合研究中心'*10) for k in ('author','department','major','supervisor','discipline')}
        if s=='multiple_supervisors': changes={'supervisor':q('导师甲 教授、导师乙 副教授、导师丙 高级工程师'),'instructor':q('导师甲、导师乙、导师丙')}
        if s=='optional_empty': changes={'enterprise-supervisor':'""','department':'""'}
        if s in ('required_empty','required_none'): changes={'title':'""' if s=='required_empty' else 'none','author':'""' if s=='required_empty' else 'none','student-id':'""'}
        if s=='mixed': changes={'title':q('Mixed：复杂系统（A/B）验证, V2.0！'),'author':q('测试·Alpha')}
        for k,val in changes.items():
            source=re.sub(r'(?m)^    '+k+r': .*$',lambda m:'    '+k+': '+val+',',source)
    extra=content(s,v)
    if s=='equations': extra='#set math.equation(numbering: "(1)")\n'+extra
    if s=='long_abstract': extra=repeated(100+v*3)+EN*(90+v*3)
    if s=='many_keywords': extra='关键词：'+'；'.join(f'关键词{i} / fictional keyword {i}' for i in range(60+v))
    if s=='abstract_math': extra='English abstract: $alpha + beta = integral_0^1 x dif x$. Ω ± ≤ ≥ 50% C++.'
    if s=='long_chapter': extra='= '+('长章节名称与混排测试 '*20)+'\n\n'+ZH
    if s=='heading_math': extra='= $alpha + beta$ 模型\n\n'+ZH
    if s=='heading_footnote': extra='= 标题#footnote[标题脚注测试]\n\n'+ZH
    if s=='long_indexes': extra='#table(columns: 3, ..range(140).map(i => ([ABC#i], [Fictional English Term], [中文全称])).flatten())'
    if s=='long_back': extra=repeated(130+v)+'\n\n'+'\n'.join(f'成果{i}：虚构成果。' for i in range(150))
    if s=='appendices': extra='\n\n'.join('= 附录'+x+'\n\n'+ZH for x in 'ABC')
    if s in ('bib1','bib300','bib_types'):
        extra+='\n#bibliography("../refs.bib", style: "gb-7714-2015-numeric")'
    if extra:
        if key: source=source.replace('  '+key+': [','  '+key+': [\n'+extra+'\n\n',1)
        else: source=source.replace('("实验原理", [','("实验原理", [\n'+extra+'\n\n',1)
    return '// 全部内容为虚构测试\n'+source

def generate(round_no, only=None):
    (HERE/'cases').mkdir(exist_ok=True)
    (HERE/'out').mkdir(exist_ok=True)
    (HERE/'refs.bib').write_text(bibliography(300))
    pairs=[(p,s) for p in PROFILES for s in SCENARIOS]
    if round_no>1:
        a,b=((1,23) if round_no%2==0 else (8,19))
        pairs=[(p,SCENARIOS[i]) for p in PROFILES for i in (a,b)]
    if only: pairs=[(p,s) for p,s in pairs if only in p['id']+'/'+s]
    manifest=[]
    for p,s in pairs:
        name=f'r{round_no:02}-{p["id"]}-{s}'
        src=thesis(p,s,round_no-1) if p['kind'] in ('thesis','bachelor') else supporting(p,s,round_no-1)
        path=HERE/'cases'/(name+'.typ');path.write_text(src)
        manifest.append(dict(p,scenario=s,name=name,source=str(path.relative_to(ROOT)),round=round_no))
    (HERE/f'manifest-r{round_no:02}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'第{round_no}轮：生成{len(manifest)}份文档')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--round',type=int,default=1);ap.add_argument('--only');a=ap.parse_args();generate(a.round,a.only)
