#!/usr/bin/env python3
"""编译真实 PDF 验证匿名、跨页与公开 API；所有生成文件均在临时目录。"""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import fitz

ROOT = Path(__file__).resolve().parents[1]
IMPORT = '#import "@preview/modern-xdu-thesis:0.1.0": documentclass\n'
failures = []

def check(name, fn):
    try:
        fn()
        print(f'通过：{name}', flush=True)
    except AssertionError as exc:
        failures.append(name)
        print(f'失败：{name}：{exc}', flush=True)

with tempfile.TemporaryDirectory(prefix='xdu-regression-') as tmp:
    work = Path(tmp)
    package = work / 'packages/preview/modern-xdu-thesis/0.1.0'
    package.mkdir(parents=True)
    # 仅复制发布实现，不读取私人论文或本地配置。
    for name in ('lib.typ', 'bachelor.typ', 'typst.toml', 'layouts', 'pages', 'utils', 'bachelor', 'assets'):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, package / name)
        elif src.exists():
            shutil.copy2(src, package / name)
    env = dict(os.environ, TYPST_PACKAGE_PATH=str(work / 'packages'))
    def compile_pdf(name, source, rejected=False):
        path = work / (name + '.typ')
        path.write_text(source)
        result = subprocess.run(['typst', 'compile', '--root', str(work), str(path), str(path.with_suffix('.pdf'))], env=env, capture_output=True, text=True)
        if rejected:
            assert result.returncode != 0 and 'unexpected argument: bib' in result.stderr, '已移除的 bib 参数仍被接受' if result.returncode == 0 else result.stderr
            return
        assert result.returncode == 0, result.stderr
        return fitz.open(path.with_suffix('.pdf'))

    blind_source = (ROOT / 'dev/test-blind.typ').read_text().replace('#import "../lib.typ": documentclass', IMPORT.strip())
    def blind_metadata():
        pdf = compile_pdf('blind', blind_source)
        assert not pdf.metadata.get('author'), repr(pdf.metadata.get('author'))
    check('盲审 PDF Author 为空', blind_metadata)
    def blind_visible():
        pdf = compile_pdf('blind-visible', blind_source)
        text = ''.join(p.get_text() for p in pdf)
        for secret in ('21011201234', '张三', '李四', '王五', 'Zhang San', 'Li Si', 'Wang Wu', '这里是一段很长的致谢文字'):
            assert secret not in text, f'泄漏 {secret}'
        assert '致谢' in text.replace(' ', '') and '第一作者' in text
    check('盲审可见内容匿名且保留成果排序', blind_visible)
    def author_case(value, expected, visible=None):
        pdf = compile_pdf('author', IMPORT + f'#let (doc, cover, title-cn) = documentclass(info: (author: {value},))\n#show: doc\n' + ('元数据测试' if value.startswith('(') else '#cover()\n#pagebreak(to: "odd")\n#title-cn()'))
        assert (pdf.metadata.get('author') or '') == expected, pdf.metadata
        if visible:
            assert all(visible in p.get_text().replace(' ', '') for p in (pdf[0], pdf[2]))
    check('content 作者可见且元数据为空', lambda: author_case('[自定义内容]', '', '自定义内容'))
    check('字符串作者元数据保留', lambda: author_case('"测试作者"', '测试作者'))
    check('字符串数组作者元数据保留', lambda: author_case('("Alpha", "Beta")', 'Alpha, Beta'))

    def long_index(kind):
        is_list = kind in ('list-of-figures', 'list-of-tables')
        count = 40 if is_list else 50
        prefix = {'list-of-figures': 'FIG', 'list-of-tables': 'TAB', 'notation': 'SYM', 'abbreviations': 'ABR'}[kind]
        source = IMPORT + '#let (doc, '+kind+', mainmatter) = documentclass()\n#show: doc\n'
        if is_list:
            source += '#'+kind+'()\n#pagebreak(to: "odd")\n#show: mainmatter\n= 测试章\n'
            for i in range(count):
                caption = f'{prefix}{i:03d}' + (' 长题注需要自动换行并保持不重叠' * 12 if i == 2 else '')
                typ = 'image' if kind == 'list-of-figures' else 'table'
                source += f'#figure(rect(width: 1mm, height: 1mm), kind: {typ}, caption: [{caption}])\n'
        else:
            rows = ','.join(f'("{prefix}{i:03d}", "说明"'+(', "中文"' if kind == 'abbreviations' else '')+')' for i in range(count))
            source += '#'+kind+'(rows: ('+rows+',))'
        pdf = compile_pdf(kind, source)
        pages = []
        for p in pdf:
            # 正文的图题为 10.5pt，索引数据为 12pt；只检查索引本身。
            spans = [s for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if abs(s['size']-12)<0.1 and 85 <= s['origin'][1] <= 768]
            if any(prefix in s['text'] for s in spans):
                pages.append((p, spans))
        text = ''.join(s['text'] for _, spans in pages for s in spans)
        missing = [f'{prefix}{i:03d}' for i in range(count) if f'{prefix}{i:03d}' not in text]
        assert not missing, f'缺少 {missing}'
        assert len(pages) >= 2, '没有续页'
        for p, spans in pages:
            assert re.search(r'\b[IVXLCDM]+\b', p.get_text(clip=fitz.Rect(0, 775, 596, 820))), '续页缺页码'
            assert p.get_text(clip=fitz.Rect(0, 50, 596, 85)).strip(), '续页缺页眉'
            ys = sorted(set(round(s['origin'][1], 2) for s in spans))
            assert all(abs((b-a)-20)<0.1 for a,b in zip(ys, ys[1:])), f'行距异常：{ys}'
            assert all(s['bbox'][2] <= (185 if p.number % 2 == 0 else 180)*72/25.4+1 for s in spans), '超出版心右边界'
    for kind in ('list-of-figures', 'list-of-tables', 'notation', 'abbreviations'):
        check(kind+' 跨页完整性、行距、页眉页码', lambda k=kind: long_index(k))

    def roman(n):
        result = ''
        for value, letters in ((1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')):
            while n >= value:
                result += letters
                n -= value
        return result
    def counters():
        source = (ROOT/'template/thesis.typ').read_text().replace('abstract: [', 'abstract: [#for i in range(110) { [长摘要连续编号测试。]; parbreak() }\n', 1)
        pdf = compile_pdf('long-front', source)
        nums = [p.get_text(clip=fitz.Rect(0,775,596,820)).strip() for p in pdf]
        nums = [n for n in nums if re.fullmatch('[IVXLCDM]+', n)]
        assert len(nums)>=16, f'长前置测试未展开：{nums}'
        assert nums == [roman(i+1) for i in range(len(nums))], f'罗马页码不连续：{nums}'
    check('实际模板长摘要罗马页码连续', counters)
    for bachelor in (False, True):
        name = '本科' if bachelor else '硕士'
        imp = '#import "@preview/modern-xdu-thesis:0.1.0": bachelor\n#let documentclass = bachelor.documentclass\n' if bachelor else IMPORT
        check(name+' 拒绝已移除 bib 参数', lambda imp=imp: compile_pdf('removed-bib', imp+'#let (doc, references) = documentclass()\n#show: doc\n#references(bib: none)', rejected=True))
        def body_case(imp=imp):
            shutil.copy2(ROOT/'dev/refs-demo.bib', work/'refs.bib')
            pdf = compile_pdf('body-bib', imp+'#let (doc, references) = documentclass()\n#show: doc\n#cite(<gb1>)\n#references(body: bibliography("refs.bib", style: "gb-7714-2015-numeric", title: none))')
            assert '广西' in ''.join(p.get_text() for p in pdf)
        check(name+' 包外 body 文献', body_case)

print(f'回归汇总：失败 {len(failures)} 项')
raise SystemExit(bool(failures))
