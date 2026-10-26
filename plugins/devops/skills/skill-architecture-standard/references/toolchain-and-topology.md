# Toolchain & Topology — รายละเอียด + เหตุผล

## เหตุผลของแต่ละมาตรฐาน
- **Next.js (web default):** FE+BE ในตัว, Claude เขียนเก่ง, deploy เป็น container ง่าย, ลดจำนวน stack ที่ทีมต้องรู้
- **PostgreSQL self-host ใน Docker (default ทุก env):** รันใน compose เหมือนกันทุก environment = parity เต็ม + ไม่มีค่า service · **RDS (managed) เฉพาะเมื่อทีม BI ร้องขอใน phase production** — โอกาสน้อยเพราะต้นทุนสูง (ถ้าใช้ BI ดูแล)
- **Microsoft Authentication (Microsoft Entra ID):** พนักงานมีบัญชี Microsoft 365 ขององค์กรอยู่แล้ว → login ครั้งเดียว (SSO), ได้ MFA / Conditional Access / ปิดบัญชีเมื่อพนักงานออกจากศูนย์กลางเดียว · auth เขียนเองพลาดง่าย + เสี่ยง (ดู OWASP A07) จึงห้าม hand-roll
  - **Next.js:** Auth.js (`next-auth`) provider `microsoft-entra-id` หรือ `@azure/msal-node` · ตรวจ session ฝั่ง server ทุก route ที่ป้องกัน
  - **FastAPI:** verify access token (JWT) ของ Entra ฝั่ง server — ตรวจ signature จาก JWKS, `iss` (tenant), `aud` (client ID ของ API), `exp`, และ scope/role ที่ต้องการ
  - **App registration:** ขอผ่าน BI · ตั้ง redirect URI แยก dev / UAT / prod · client secret หรือ certificate อยู่ใน env/secret manager เท่านั้น ห้ามเข้า git
  - **Single-tenant เป็น default** (เฉพาะบัญชีองค์กร) · ใช้ App roles / group ของ Entra แทนการเก็บ role เองเมื่อทำได้
- **Docker + compose:** dev = prod parity, BI promote image เดียวข้าม Hostinger→AWS ได้
- **GitHub + 3-tier:** main←uat←feature, PR-only, credential gate (skill-git-standard)

## Topology รายละเอียด
| Env | ที่ | ใคร deploy | how |
|---|---|---|---|
| dev | local | ทุกคน | `docker compose up --build` |
| UAT | Hostinger (VPS+Docker) | ทีมทั่วไป (self-serve) | push source → CI build → run container |
| prod | AWS (App Runner / Lightsail Containers) | **BI เท่านั้น** | CI build official image จาก main → Docker Hub private → deploy |

> เลือก App Runner = auto-scale+HTTPS · Lightsail Containers = ราคาคงที่ (กัน cost บาน hackathon)

## Guardrails (cost + security)
- **AWS รวมศูนย์ที่ BI** — ทีมทั่วไปไม่เปิด account/resource เอง · ตั้ง Budget + Alert
- **Docker Hub = private** (BI ดูแล) · credential ของ registry/cloud อยู่ใน CI secret เท่านั้น
- **`/security-check` ก่อน promote** — secret-scan + container-iac + OWASP ตามชนิดงาน
- **Docker parity บังคับ** — UAT กับ prod ต้องเป็น image เดียวกัน

## เมื่อจะเบี่ยงจากมาตรฐาน
1. ระบุเหตุผลใน "Proposed Approach" ของ project-proposal (skill-PM)
2. **ก่อนถึง phase ขึ้น production → PM เคาะได้เลย** (ไม่ต้องรอ BI) · ตอน promote ขึ้น prod → BI review อีกชั้นตาม guardrails
3. ถ้า approve → บันทึกเป็น decision ใน CLAUDE.md/requirements ของโปรเจกต์นั้น
