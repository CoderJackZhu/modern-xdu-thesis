#!/usr/bin/env python3
"""只用 curl 读取官方 HTML 页面；不下载附件，不更改规格。"""
import concurrent.futures
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin,urlparse

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DOCS=['格式规格.md','官方要求摘录.md','配套材料导航.md','博士规格.md']
class Page(HTMLParser):
    def __init__(self):super().__init__();self.text=[];self.links=[];self.link=None;self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style'):self.skip+=1
        if tag=='a':self.link={'href':a.get('href',''),'text':a.get('title','')}
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag=='a' and self.link:self.links.append(self.link);self.link=None
    def handle_data(self,text):
        if not self.skip:self.text.append(text.strip())
        if self.link:self.link['text']+=text.strip()

def fetch(url):
    last=None
    for attempt in range(1,4):
        p=subprocess.run(['curl','-L','--max-time','25','--connect-timeout','10','-sS','--fail',url],capture_output=True,timeout=30)
        if p.returncode==0:
            raw=p.stdout
            try:s=raw.decode('utf-8')
            except UnicodeDecodeError:s=raw.decode('gb18030',errors='replace')
            parser=Page();parser.feed(s);text='\n'.join(t for t in parser.text if t)
            relevant=[dict(text=l['text'],url=urljoin(url,l['href'])) for l in parser.links if re.search('论文|学位|模板|表格|撰写|毕业设计|开题|中期',l['text'])]
            dates=[text[max(0,m.start()-90):m.end()+180] for m in re.finditer(r'20\d{2}\s*[年./-]\s*\d{1,2}(?:\s*[月./-]\s*\d{1,2})?',text)]
            (HERE/'out'/('official-'+re.sub('[^a-zA-Z0-9]+','-',url)+'.txt')).write_text(text)
            return dict(url=url,status='成功',attempts=attempt,dates=dates,links=relevant,title=text[:220])
        last=p.stderr.decode(errors='replace')
    return dict(url=url,status='跳过：连续3次网络失败',error=last)

def main():
    source=[]
    for name in DOCS:
        s=(ROOT/'docs'/name).read_text()
        for url in re.findall(r'https?://[^\s<>）)\]]+',s):
            if urlparse(url).hostname and urlparse(url).hostname.endswith('xidian.edu.cn'):
                source.append(dict(file='docs/'+name,url=url,recorded_dates=sorted(set(re.findall(r'20\d{2}[.年/-]\d{1,2}',s)))))
    urls=sorted(set(x['url'] for x in source)|{'https://gr.xidian.edu.cn/xwsy/zlxz.htm','https://jwc.xidian.edu.cn','https://jwc.xidian.edu.cn/info/1022/12943.htm'})
    # 严格不请求附件直链。
    urls=[u for u in urls if not re.search(r'\.(zip|rar|docx?|pdf)(?:$|\?)|download.jsp',u,re.I)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:pages=list(ex.map(fetch,urls))
    # 总目录中与论文撰写/毕业设计相关的当前通知（限12条），不跟踪附件。
    more=[]
    for page in pages:
        if page['url'].endswith('zlxz.htm') or page['url'].rstrip('/')=='https://jwc.xidian.edu.cn':
            for link in page.get('links',[]):
                if re.search('撰写|模板|毕业设计|毕业论文|论文格式',link['text']) and re.search(r'/info/\d+/\d+\.htm',link['url']) and link['url'] not in urls:more.append(link['url'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:pages+=list(ex.map(fetch,sorted(set(more))[:12]))
    result=dict(checked_at='2026-11-02 Asia/Shanghai',sources=source,pages=pages,limitations='只比较公开HTML上的发布日期与附件名版本；未下载附件、未核验附件正文，不代表所有学院通知均已排除。')
    (HERE/'official-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    for p in pages:print(p['url'],p['status'],p.get('dates',[])[:3],flush=True)
if __name__=='__main__':main()
