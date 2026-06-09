# Git Guide — คู่มือคำสั่ง Git พื้นฐาน → ขั้นสูง

รวมคำสั่ง Git ที่ใช้บ่อย พร้อมคำอธิบาย ไทย/อังกฤษ ใช้เป็น cheatsheet ได้

> A practical Git cheatsheet, basic → advanced.

---

## 1. แนวคิดพื้นฐาน (Core Concepts)

```
Working Directory  →  Staging Area  →  Local Repo  →  Remote Repo
   (แก้ไฟล์)            (git add)        (git commit)     (git push)
```

| คำ (Term) | ความหมาย (Meaning) |
|---|---|
| **Working directory** | ไฟล์ที่คุณกำลังแก้อยู่ |
| **Staging area (index)** | ที่พักไฟล์ที่เลือกจะ commit |
| **Commit** | snapshot ของโค้ด ณ จุดเวลาหนึ่ง |
| **Branch** | สายงานแยกของ commit |
| **Remote** | repo บนเซิร์ฟเวอร์ (เช่น GitHub) |
| **HEAD** | ตำแหน่ง commit ปัจจุบันที่คุณอยู่ |

---

## 2. ตั้งค่าครั้งแรก (Setup)

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"   # ใช้ VS Code เป็น editor
git config commit.template .gitmessage           # ใช้ commit template
```

---

## 3. คำสั่งประจำวัน (Everyday Commands)

```bash
git status                 # ดูสถานะไฟล์
git add <file>             # stage ไฟล์เดียว
git add -p                 # stage ทีละส่วน (เลือกได้ว่าจะเอา hunk ไหน)
git commit                 # commit (เปิด editor)
git commit -m "msg"        # commit พร้อมข้อความสั้น
git log --oneline --graph  # ดูประวัติแบบกราฟ
git diff                   # ดูสิ่งที่เปลี่ยน (ยังไม่ stage)
git diff --staged          # ดูสิ่งที่ stage แล้ว
```

---

## 4. Branch & Merge

```bash
git branch                      # list branch
git checkout -b feature/x     # สร้าง + สลับไป branch ใหม่
git switch uat                  # สลับ branch (คำสั่งใหม่ที่ชัดกว่า)
git merge feature/x           # merge branch เข้า branch ปัจจุบัน
git branch -d feature/x       # ลบ branch (local)
git push origin --delete feature/x   # ลบ branch บน remote
```

---

## 5. Remote

```bash
git remote -v                       # ดู remote
git remote add origin <url>         # ผูก remote
git pull origin uat                 # ดึง + merge
git fetch origin                    # ดึงอย่างเดียว (ไม่ merge)
git push -u origin feature/x      # push ครั้งแรก (ตั้ง upstream)
git push                            # push ครั้งถัดไป
```

> **`pull` = `fetch` + `merge`** — ถ้าอยากควบคุมเอง ใช้ `fetch` แล้วค่อย merge/rebase

---

## 6. Undo & แก้ไข (Undo / Fix mistakes)

| สถานการณ์ (Situation) | คำสั่ง (Command) |
|---|---|
| ยกเลิกการแก้ไฟล์ (ยังไม่ add) | `git restore <file>` |
| เอาไฟล์ออกจาก staging | `git restore --staged <file>` |
| แก้ commit ล่าสุด (ข้อความ/ไฟล์) | `git commit --amend` |
| ย้อน commit แต่เก็บการแก้ไว้ | `git reset --soft HEAD~1` |
| ย้อน commit ทิ้งการแก้ทั้งหมด ⚠️ | `git reset --hard HEAD~1` |
| สร้าง commit ใหม่ที่กลับด้าน (ปลอดภัยบน shared) | `git revert <hash>` |

> ⚠️ `reset --hard` ลบงานถาวร — ใช้บน branch ตัวเองเท่านั้น ห้ามใช้บน shared branch

---

## 7. Stash (พักงานชั่วคราว)

```bash
git stash              # เก็บงานที่ทำค้างไว้ (เคลียร์ working dir)
git stash list         # ดูรายการ stash
git stash pop          # เอางานล่าสุดกลับมา + ลบออกจาก stash
git stash apply        # เอากลับมาแต่ยังเก็บใน stash
git stash drop         # ลบ stash
```
> ใช้เมื่อ: ต้องสลับ branch ด่วน แต่ยังไม่อยาก commit

---

## 8. Rebase (จัดประวัติให้สะอาด)

```bash
git rebase origin/uat          # ย้าย commit ของเราไปต่อท้าย uat ล่าสุด
git rebase -i HEAD~3           # แก้/รวม/เรียง 3 commit ล่าสุด (interactive)
git rebase --continue          # ทำต่อหลังแก้ conflict
git rebase --abort             # ยกเลิก rebase
```

> **กฎทอง / Golden rule:** อย่า rebase branch ที่ push และมีคนอื่นใช้ร่วมแล้ว
> (rebase เปลี่ยน history — ใช้ได้กับ branch ส่วนตัวเท่านั้น)

---

## 9. ค้นหา & ตรวจสอบ (Inspect & Debug)

```bash
git log --oneline --graph --all     # กราฟทุก branch
git show <hash>                     # ดูรายละเอียด commit
git blame <file>                    # ดูว่าใครแก้บรรทัดไหน
git diff uat..feature/x           # เทียบ 2 branch
git bisect start                    # หา commit ที่ทำให้บั๊ก (binary search)
```

---

## 10. คำสั่งฉุกเฉิน (Emergency)

```bash
git reflog                     # ดูทุกการเคลื่อนไหวของ HEAD (กู้ commit ที่ "หาย")
git reset --hard <hash>        # กระโดดกลับไป commit นั้น (จาก reflog)
git cherry-pick <hash>         # ดึง commit เดียวจาก branch อื่นมาใช้
```

> **`git reflog` คือเพื่อนที่ดีที่สุดยามฉุกเฉิน** — แม้ `reset --hard` ไปแล้ว commit ก็ยังกู้ได้จากตรงนี้

---

## 11. เกร็ดน่ารู้ (Tips)

- `git add -p` ช่วยให้ commit เล็กและมีความหมาย
- ตั้ง alias: `git config --global alias.lg "log --oneline --graph --all"`
- `.gitignore` กันไฟล์ที่ไม่ควรขึ้น repo (build, .env, node_modules)
- commit บ่อย ๆ ทีละเรื่อง ดีกว่า commit ใหญ่ก้อนเดียว
