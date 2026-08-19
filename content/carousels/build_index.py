#!/usr/bin/env python3
"""Собирает INDEX.md — таблицу всех каруселей — из метаданных файлов папки.

Запуск:  python3 content/carousels/build_index.py
"""

import re
from pathlib import Path

FOLDER = Path(__file__).parent
COLUMNS = ["date", "title", "topic", "platform", "slides", "status"]
HEADERS = ["Дата", "Название", "Тема", "Площадка", "Слайдов", "Статус"]


def read_front_matter(path):
    """Возвращает словарь метаданных из блока между --- в начале файла."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None

    meta = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta


def escape(value):
    """Экранирует вертикальную черту, чтобы не ломать таблицу markdown."""
    return str(value).replace("|", "\\|")


def main():
    rows = []
    skipped = []

    for path in sorted(FOLDER.glob("*.md")):
        if path.name.startswith("_") or path.name in ("README.md", "INDEX.md"):
            continue
        meta = read_front_matter(path)
        if meta is None:
            skipped.append(path.name)
            continue
        rows.append((meta, path.name))

    rows.sort(key=lambda row: row[0].get("date", ""), reverse=True)

    lines = [
        "# Реестр каруселей",
        "",
        "<!-- Файл собирается автоматически: python3 content/carousels/build_index.py -->",
        "<!-- Правьте не его, а метаданные в самих каруселях. -->",
        "",
        f"Всего каруселей: **{len(rows)}**",
        "",
    ]

    if rows:
        lines.append("| " + " | ".join(HEADERS) + " | Файл |")
        lines.append("|" + "---|" * (len(HEADERS) + 1))
        for meta, name in rows:
            cells = [escape(meta.get(key, "—")) for key in COLUMNS]
            cells.append(f"[{escape(name)}]({name})")
            lines.append("| " + " | ".join(cells) + " |")
    else:
        lines.append("Пока пусто. Добавьте первый файл по шаблону `_TEMPLATE.md`.")

    if skipped:
        lines += ["", "## Без метаданных", ""]
        lines += [f"- `{name}` — нет блока `---` в начале файла" for name in skipped]

    lines.append("")
    (FOLDER / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"INDEX.md обновлён: {len(rows)} каруселей, пропущено {len(skipped)}")


if __name__ == "__main__":
    main()
