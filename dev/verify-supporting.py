#!/usr/bin/env python3
"""验收开题、中期和通用课程实验报告 PDF。

检查项不是“看起来像表”：A4 页面、正文 12pt、固定 20pt 基线、可打印边界、
封面标题、关键字段、章节顺序、表格框线和末页残留都会进入失败码。
"""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

import fitz


A4 = (595.276, 841.89)


def normalized(text: str) -> str:
    return "".join(text.split())


def fail(message: str) -> None:
    print(f"不合格：{message}")


def profile_checks(graduate: str, degree: str) -> dict[str, object]:
    prefix = "专业学位" if degree == "professional" else ""
    level = "博士" if graduate == "doctor" else "硕士"
    proposal_title = f"{prefix}{level}学位论文开题报告表"
    interim_title = f"{prefix}{level}学位论文中期考核报告表"
    if degree == "professional" and graduate == "doctor":
        proposal_fields = ("学位类别", "领域（方向）", "指导教师")
        interim_fields = proposal_fields
    elif degree == "professional":
        proposal_fields = ("学位类别", "领域", "校内导师", "校外导师")
        interim_fields = proposal_fields
    else:
        proposal_fields = ("一级学科", "二级学科", "指导教师")
        interim_fields = proposal_fields
    return {
        "proposal_title": proposal_title,
        "interim_title": interim_title,
        "proposal_fields": proposal_fields,
        "interim_fields": interim_fields,
        "proposal_sections": (
            ("一、论文概况", "二、选题依据", "三、研究方案", "四、研究基础",
             "五、开题报告记录", "六、开题报告评语及结论", "七、指导教师意见")
            if graduate == "doctor"
            else ("一、论文概况", "二、选题依据", "三、研究方案", "四、研究基础",
                  "五、指导教师意见", "六、开题报告记录", "七、开题报告评语及结论")
        ),
        "interim_sections": (
            "一、学位论文研究目标及研究内容",
            "二、目前已完成学位论文工作的内容",
            "三、现阶段完成的工作与开题报告内容不相符的情况说明",
            "四、下一步工作计划及需要完成的研究内容和需要解决的关键技术",
            "五、已发表的与学位论文相关的学术论文、其他研究成果以及拟发表的研究成果",
            "指导教师评价意见",
            "中期总结报告评语及结论",
        ),
    }


def section_positions(text: str, sections: tuple[str, ...]) -> list[int]:
    haystack = normalized(text)
    positions = []
    for section in sections:
        needle = normalized(section)
        position = haystack.find(needle)
        if position < 0:
            raise ValueError(f"缺少章节“{section}”")
        positions.append(position)
    if positions != sorted(positions):
        raise ValueError("章节顺序错误：" + " / ".join(sections))
    return positions


def check_margin_ink(page: fitz.Page, clip: fitz.Rect, name: str) -> None:
    """扫描页面外侧条带内的真实墨迹，避免把 CJK 字形的标点外框当成越界。"""
    if clip.is_empty:
        return
    pix = page.get_pixmap(
        clip=clip,
        colorspace=fitz.csGRAY,
        alpha=False,
        dpi=144,
        annots=False,
    )
    if pix.samples and min(pix.samples) < 245:
        raise ValueError(
            f"第 {page.number + 1} 页{name}存在越界墨迹，"
            f"检查区 {clip.x0:.2f}～{clip.x1:.2f} / {clip.y0:.2f}～{clip.y1:.2f}bp"
        )


def check_page_geometry(doc: fitz.Document, margin_x: float, margin_y: float) -> None:
    # 标点字形外框可能比实际墨迹宽约 6pt。按 AGENTS 的规约检查真实墨迹，
    # 但只容许 2pt 栅格化误差，不通过改写页边距来让检查通过。
    tolerance = 2.0
    for number, page in enumerate(doc, start=1):
        width, height = page.rect.width, page.rect.height
        if abs(width - A4[0]) > 1.5 or abs(height - A4[1]) > 1.5:
            raise ValueError(f"第 {number} 页不是 A4：{width:.2f} × {height:.2f}bp")
        forbidden = {
            "左侧": fitz.Rect(0, 0, margin_x - tolerance, height),
            "右侧": fitz.Rect(width - margin_x + tolerance, 0, width, height),
            "上侧": fitz.Rect(0, 0, width, margin_y - tolerance),
            "下侧": fitz.Rect(0, height - margin_y + tolerance, width, height),
        }
        for name, clip in forbidden.items():
            check_margin_ink(page, clip, name)


def check_body_metrics(doc: fitz.Document) -> tuple[int, int]:
    body_spans = 0
    exact_20 = 0
    for page in doc:
        baselines = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                if not line.get("spans"):
                    continue
                span = line["spans"][0]
                if abs(span["size"] - 12) <= 0.2:
                    baselines.append(span["origin"][1])
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if abs(span["size"] - 12) <= 0.2:
                        body_spans += 1
        # Typst 会把跨行段落拆成多个 PDF block，不能只在 block 内比较。
        # 同一表格行的多个单元格共享基线，先去重，再统计真实的 20pt 行距。
        unique_baselines = sorted({
            round(baseline, 3) for baseline in baselines
        })
        for previous, current in zip(unique_baselines, unique_baselines[1:]):
            if abs(current - previous - 20) <= 0.08:
                exact_20 += 1
    if body_spans < 10:
        raise ValueError(f"正文 12pt 文字过少：{body_spans} 个 span")
    if exact_20 < 4:
        raise ValueError(f"未找到足够的固定 20pt 基线：仅 {exact_20} 处")
    return body_spans, exact_20


def check_form_lines(doc: fitz.Document) -> int:
    drawings = 0
    for page in doc:
        drawings += len(page.get_drawings())
    if drawings < 8:
        raise ValueError(f"表格框线过少：{drawings} 个绘图对象")
    return drawings


def verify(path: Path, kind: str, graduate: str, degree: str) -> None:
    if not path.is_file():
        raise ValueError(f"找不到 PDF：{path}")
    doc = fitz.open(path)
    if len(doc) < 1:
        raise ValueError("PDF 没有页面")
    if any(len(page.get_text().strip()) < 5 for page in doc):
        raise ValueError("存在空白页或只有极少文字的残页")

    if kind in ("proposal", "interim"):
        margin_x = margin_y = 72.0
        config = profile_checks(graduate, degree)
        first_text = normalized(doc[0].get_text())
        expected_title = config["proposal_title"] if kind == "proposal" else config["interim_title"]
        if normalized(expected_title) not in first_text:
            raise ValueError(f"封面缺少正确表名“{expected_title}”")
        fields = config["proposal_fields"] if kind == "proposal" else config["interim_fields"]
        for field in fields:
            if normalized(field) not in first_text:
                raise ValueError(f"封面缺少字段“{field}”")
        full_text = normalized("".join(page.get_text() for page in doc))
        if "A3" not in full_text or "20磅" not in full_text:
            raise ValueError("填写说明缺少 A3 套印或 20 磅行距要求")
        sections = config["proposal_sections"] if kind == "proposal" else config["interim_sections"]
        section_positions(full_text, sections)
        if kind == "proposal":
            for label in ("一级指标", "二级指标", "评价意见", "论文选题", "研究方案", "研究基础", "进度安排"):
                if normalized(label) not in full_text:
                    raise ValueError(f"开题评语表缺少“{label}”")
            if graduate == "doctor" and normalized("论文的创新点") not in full_text:
                raise ValueError("博士开题报告缺少“论文的创新点”")
            if graduate == "master" and degree == "professional" and normalized("实习单位名称") not in full_text:
                raise ValueError("专业硕士开题报告缺少实习单位字段")
    elif kind == "bachelor-proposal":
        margin_x, margin_y = 89.86, 72.0
        text = normalized(doc[0].get_text())
        if "本科生毕业论文（设计）开题报告" not in text:
            raise ValueError("本科开题封面缺少表名")
        full_text = normalized("".join(page.get_text() for page in doc))
        section_positions(full_text, (
            "一、论文名称及项目来源", "二、研究目的和意义", "三、国内外研究现状和发展趋势",
            "四、主要研究内容、要解决的问题及本文的初步方案", "五、工作的主要阶段、进度和完成时间",
            "六、已进行的前期准备工作", "七、指导教师意见", "学院审核意见",
        ))
        if "一式三份" not in full_text:
            raise ValueError("本科开题报告缺少“一式三份”说明")
    elif kind == "bachelor-interim":
        margin_x = margin_y = 72.0
        text = normalized(doc[0].get_text())
        if "本科生毕业设计（论文）中期报告" not in text:
            raise ValueError("本科中期封面缺少表名")
        full_text = normalized("".join(page.get_text() for page in doc))
        section_positions(full_text, (
            "1、毕业设计工作是否更换题目及是否按开题报告预定的内容及进度安排进行",
            "2、目前已完成的研究工作及结果", "3．后期拟完成的研究工作及进度安排",
            "4．存在的困难与问题", "5．如期完成全部论文工作的可能性",
            "6、指导导师意见", "7、中期报告检查组意见", "8、承担毕业设计单位审核",
        ))
        if "A3" not in full_text or "20磅" not in full_text:
            raise ValueError("本科中期要求缺少 A3 套印或 20 磅行距")
    elif kind == "course-report":
        margin_x = margin_y = 62.36
        full_text = normalized("".join(page.get_text() for page in doc))
        section_positions(full_text, ("1实验目的", "2实验环境", "3实验原理", "4实验步骤", "5实验结果", "6分析与结论"))
        if "提交前自查" not in full_text:
            raise ValueError("课程报告缺少提交前自查提示")
        if "不是学校统一模板" not in full_text:
            raise ValueError("课程报告没有声明非学校统一模板")
    else:
        raise ValueError(f"未知 kind：{kind}")

    check_page_geometry(doc, margin_x, margin_y)
    body_spans, exact_20 = check_body_metrics(doc)
    drawings = check_form_lines(doc) if kind != "course-report" else 0
    print(
        f"合格：{path.name}｜{kind}/{graduate}/{degree}｜{len(doc)} 页｜"
        f"A4｜正文 {body_spans} span｜20pt 基线 {exact_20} 处"
        + (f"｜框线 {drawings} 个" if drawings else "")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--kind", required=True, choices=(
        "proposal", "interim", "bachelor-proposal", "bachelor-interim", "course-report",
    ))
    parser.add_argument("--graduate", choices=("master", "doctor"), default="master")
    parser.add_argument("--degree", choices=("academic", "professional"), default="academic")
    args = parser.parse_args()
    try:
        verify(args.pdf.resolve(), args.kind, args.graduate, args.degree)
    except (OSError, ValueError, fitz.FileDataError) as error:
        fail(str(error))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
