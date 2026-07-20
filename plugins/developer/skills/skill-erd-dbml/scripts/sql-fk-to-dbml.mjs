#!/usr/bin/env node
// sql-fk-to-dbml.mjs — เติม DBML `Ref:` (relationships) + `TableGroup` (zone) จากไฟล์ SQL migration
// เหตุผล: `sql2dbml` (@dbml/cli) ทิ้ง FK แบบ `ALTER TABLE … ADD CONSTRAINT … FOREIGN KEY` → ตารางลอยไม่มีเส้น
// รองรับ: ชื่อ quoted/unquoted · มี/ไม่มี schema (ไม่มี = public) · single + composite FK · หลายไฟล์
// Usage:  node sql-fk-to-dbml.mjs <migration.sql ...>  >> docs/erd.dbml

import { readFileSync } from 'node:fs';

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node sql-fk-to-dbml.mjs <migration.sql ...>');
  process.exit(1);
}
const sql = files.map((f) => readFileSync(f, 'utf8')).join('\n');

const I = String.raw`"?([A-Za-z_][\w$]*)"?`; // identifier — quoted หรือไม่ก็ได้
const qualify = (schema, table) => (schema ? `"${schema}"."${table}"` : `"${table}"`);
const fmtCols = (raw) => {
  const cols = raw.split(',').map((c) => `"${c.trim().replace(/^"|"$/g, '')}"`);
  return cols.length === 1 ? cols[0] : `(${cols.join(', ')})`;
};

/* ── 1) FK → Ref (single + composite) ── */
const fkRe = new RegExp(
  String.raw`ALTER TABLE\s+(?:ONLY\s+)?(?:${I}\.)?${I}\s+ADD\s+CONSTRAINT\s+${I}\s+FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+(?:${I}\.)?${I}\s*\(([^)]+)\)`,
  'gi'
);
const refs = new Set();
let m;
while ((m = fkRe.exec(sql)) !== null) {
  const [, srcSchema, srcTable, , srcCols, refSchema, refTable, refCols] = m;
  // ">" = many-to-one (child.fk -> parent.pk) · FK ที่ติด UNIQUE (= 1:1) → แก้ ">" เป็น "-" ด้วยมือ
  refs.add(`Ref: ${qualify(srcSchema, srcTable)}.${fmtCols(srcCols)} > ${qualify(refSchema, refTable)}.${fmtCols(refCols)}`);
}

/* ── 2) CREATE TABLE → TableGroup ต่อ Postgres schema (zone) ── */
const tableRe = new RegExp(String.raw`CREATE TABLE(?:\s+IF NOT EXISTS)?\s+(?:${I}\.)?${I}`, 'gi');
const groups = new Map(); // schema -> [ชื่อ table ตามรูปแบบที่ sql2dbml จะใช้,...]
while ((m = tableRe.exec(sql)) !== null) {
  const schema = m[1] ?? 'public';
  if (!groups.has(schema)) groups.set(schema, []);
  // ตารางไม่มี schema ใน source → sql2dbml ตั้งชื่อไม่มี prefix — ต้องอ้างแบบเดียวกันไม่งั้น group หา table ไม่เจอ
  groups.get(schema).push(qualify(m[1], m[2]));
}

/* ── output ── */
if (refs.size === 0) {
  console.error('warning: ไม่พบ FOREIGN KEY แบบ ALTER TABLE — ถ้า FK เขียน inline ใน CREATE TABLE, sql2dbml จัดการให้แล้ว');
}
let out = '\n// ── Relationships (auto: migration FKs) ──\n';
out += [...refs].sort().join('\n') + '\n';

// จัดโซนเฉพาะเมื่อมีมากกว่า 1 schema (ทั้งหมดอยู่ public = ไม่ต้องแบ่ง)
const palette = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#a855f7', '#14b8a6', '#f97316'];
const schemas = [...groups.keys()].sort();
if (schemas.length > 1) {
  out += '\n// ── Table Groups / Zones (auto: per Postgres schema) ──\n';
  schemas.forEach((schema, i) => {
    out += `TableGroup "${schema}" [color: ${palette[i % palette.length]}] {\n`;
    for (const t of groups.get(schema).sort()) out += `  ${t}\n`;
    out += '}\n';
  });
}
process.stdout.write(out);
