#!/usr/bin/env python3
"""ตัวตรวจ manifest อัตโนมัติของ kob-claude-plugins (kissofbeauty marketplace)

ตรวจให้ครบก่อนรวมเข้า main เพื่อกัน JSON พัง / skill ผิดมาตรฐาน:
  - .claude-plugin/marketplace.json valid + มี key name, owner, plugins(array)
  - ทุก entry ใน plugins[] มี name, source, description และ path ใน source มีจริง
  - plugins/*/.claude-plugin/plugin.json valid + มี key name, description
  - plugins/*/skills/*/SKILL.md มี frontmatter (คั่นด้วย ---) ที่มี
    name (ตรงชื่อโฟลเดอร์) และ description (ไม่ว่าง)

ใช้ stdlib ล้วน ไม่ import lib นอก (parse frontmatter เองแบบง่าย)
exit 0 = ผ่าน, exit 1 = มี error
"""

import json
import sys
from pathlib import Path

# บังคับ stdout/stderr เป็น UTF-8 เพื่อให้พิมพ์ภาษาไทยได้บน Windows console (cp1252)
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

# repo root = parent ของ scripts/ (ตำแหน่งสคริปต์อยู่ที่ scripts/validate.py)
REPO_ROOT = Path(__file__).resolve().parent.parent

# เก็บ error/warning ที่เจอ
errors: list[str] = []


def err(msg: str) -> None:
    """บันทึก error (ทำให้ exit code = 1)"""
    errors.append(msg)


def rel(path: Path) -> str:
    """แสดง path แบบ relative กับ repo root เพื่ออ่านง่าย"""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path):
    """อ่านไฟล์ JSON; คืน (data, error_message) — ถ้าพัง data เป็น None"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return None, f"อ่านไฟล์ไม่ได้: {e}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, f"JSON ไม่ valid ที่บรรทัด {e.lineno} คอลัมน์ {e.colno}: {e.msg}"


def parse_frontmatter(path: Path):
    """parse YAML frontmatter แบบง่าย (ไม่ import yaml)

    อ่านบรรทัดระหว่าง --- คู่แรก แล้วแยก key: value
    คืน (dict, error_message). ถ้าไม่มี frontmatter -> ({}, error)
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        return {}, f"อ่านไฟล์ไม่ได้: {e}"

    # หา --- เปิด (ต้องเป็นบรรทัดแรกที่ไม่ว่าง)
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx >= len(lines) or lines[idx].strip() != "---":
        return {}, "ไม่พบ frontmatter (ต้องขึ้นต้นด้วย ---)"

    start = idx + 1
    end = None
    for i in range(start, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, "frontmatter ไม่ปิด (ขาด --- ปิดท้าย)"

    data: dict[str, str] = {}
    for i in range(start, end):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # ตัด quote คู่/เดี่ยวที่ครอบ value (ถ้ามี)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            data[key] = value
    return data, None


def check_marketplace() -> None:
    """ตรวจ .claude-plugin/marketplace.json"""
    path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    if not path.exists():
        err(f"ไม่พบไฟล์ {rel(path)}")
        return

    data, e = load_json(path)
    if e:
        err(f"{rel(path)}: {e}")
        return
    if not isinstance(data, dict):
        err(f"{rel(path)}: root ต้องเป็น object")
        return

    for key in ("name", "owner", "plugins"):
        if key not in data:
            err(f"{rel(path)}: ขาด key '{key}'")

    plugins = data.get("plugins")
    if plugins is not None and not isinstance(plugins, list):
        err(f"{rel(path)}: 'plugins' ต้องเป็น array")
        return

    if isinstance(plugins, list):
        for i, entry in enumerate(plugins):
            label = f"{rel(path)}: plugins[{i}]"
            if not isinstance(entry, dict):
                err(f"{label} ต้องเป็น object")
                continue
            for key in ("name", "source", "description"):
                if key not in entry or str(entry.get(key, "")).strip() == "":
                    err(f"{label} ขาด/ว่าง key '{key}'")
            source = entry.get("source")
            if isinstance(source, str) and source.strip():
                src_path = (REPO_ROOT / source).resolve()
                if not src_path.exists():
                    err(f"{label} source '{source}' ไม่มีอยู่จริง")


def check_plugins() -> None:
    """ตรวจ plugins/*/.claude-plugin/plugin.json ทุกตัว"""
    plugin_jsons = sorted((REPO_ROOT / "plugins").glob("*/.claude-plugin/plugin.json"))
    if not plugin_jsons:
        err("ไม่พบ plugin.json ใต้ plugins/*/.claude-plugin/")
        return

    for path in plugin_jsons:
        data, e = load_json(path)
        if e:
            err(f"{rel(path)}: {e}")
            continue
        if not isinstance(data, dict):
            err(f"{rel(path)}: root ต้องเป็น object")
            continue
        for key in ("name", "description"):
            if key not in data or str(data.get(key, "")).strip() == "":
                err(f"{rel(path)}: ขาด/ว่าง key '{key}'")


def check_skills() -> None:
    """ตรวจ plugins/*/skills/*/SKILL.md ทุกตัว"""
    skill_files = sorted((REPO_ROOT / "plugins").glob("*/skills/*/SKILL.md"))
    for path in skill_files:
        skill_dir = path.parent.name  # ชื่อโฟลเดอร์ skill
        fm, e = parse_frontmatter(path)
        if e:
            err(f"{rel(path)}: {e}")
            continue

        name = fm.get("name", "").strip()
        if not name:
            err(f"{rel(path)}: frontmatter ขาด 'name'")
        elif name != skill_dir:
            err(f"{rel(path)}: 'name' ({name}) ไม่ตรงชื่อโฟลเดอร์ ({skill_dir})")

        if not fm.get("description", "").strip():
            err(f"{rel(path)}: frontmatter ขาด/ว่าง 'description'")

    return len(skill_files)


def main() -> int:
    print(f"ตรวจ manifest จาก repo root: {REPO_ROOT}\n")

    check_marketplace()
    check_plugins()
    skill_count = check_skills()

    plugin_count = len(sorted((REPO_ROOT / "plugins").glob("*/.claude-plugin/plugin.json")))

    print(f"  plugin.json ที่ตรวจ : {plugin_count}")
    print(f"  SKILL.md ที่ตรวจ    : {skill_count}\n")

    if errors:
        print(f"พบปัญหา {len(errors)} รายการ:")
        for i, msg in enumerate(errors, 1):
            print(f"  {i}. {msg}")
        print("\nผลลัพธ์: FAIL — แก้ให้ครบก่อนเปิด PR")
        return 1

    print("ผลลัพธ์: PASS — manifest ผ่านมาตรฐานทั้งหมด")
    return 0


if __name__ == "__main__":
    sys.exit(main())
