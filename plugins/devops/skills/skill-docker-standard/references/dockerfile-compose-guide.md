# Dockerfile + Compose Guide (no-secret patterns)

> เป้าหมาย: image เล็ก, ปลอดภัย, dev=prod parity, **ไม่มี secret ใน image**

## Dockerfile — best practices
- **Multi-stage build** — stage build แยกจาก stage runtime (ไม่ติด dev deps/secret มากับ runtime)
- **Non-root user** — `USER node` / สร้าง user เอง ไม่รันเป็น root
- **Pin base image** — `node:20-alpine` ไม่ใช่ `node:latest`
- **`.dockerignore`** ครอบ `.env`, `*.pem`, `secrets*`, `.git`, `node_modules`
- ❌ ห้าม `ENV SECRET=...`, `COPY .env .`, hardcode key

ตัวอย่างโครง (Node/Next.js):
```dockerfile
# ---- build stage ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---- runtime stage ----
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/.next ./.next
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

## docker-compose.yml — สำหรับ dev local
- รวม service ที่ต้องใช้ (app + db) ให้ dev = prod
- **secret ผ่าน `env_file`** (ไฟล์ `.env` ที่ gitignored) ไม่เขียนค่าใน compose

```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env          # .env อยู่ใน .gitignore + .dockerignore
    depends_on: [db]
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pw   # หรือ env_file
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes: { pgdata: {} }
```

## วิธีจัดการ secret ให้ถูก
| ขั้นตอน | secret มาจากไหน |
|---|---|
| dev local | `env_file: .env` (gitignored) |
| build (ถ้าจำเป็นจริง ๆ) | BuildKit `--secret` mount (ไม่ค้างใน layer) |
| runtime prod | orchestrator/CI inject env (AWS Secrets Manager / runtime `-e`) |

> ✅ ทดสอบ: `docker history <image>` ต้องไม่เห็น secret · รัน `/skill-cybersecurity-container-iac` ก่อน promote
