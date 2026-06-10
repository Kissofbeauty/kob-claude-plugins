# Container & IaC Security Checklist

checklist ละเอียดสำหรับ Dockerfile / Kubernetes / Terraform — แต่ละข้อมี ❌ bad → ✅ good
ตัวอย่าง secret ทั้งหมดเป็นค่า dummy (`allowlist secret` ต่อท้ายเพื่อกัน pre-commit สแกน)

---

## 1. Dockerfile / Compose

### 1.1 รัน as root
ไม่มี `USER` → process รันด้วย uid 0 ภายใน container = เสี่ยง escape เป็น root บน host

```dockerfile
# ❌ bad — ไม่มี USER, รันด้วย root
FROM node:20
COPY . /app
CMD ["node", "server.js"]
```
```dockerfile
# ✅ good — สร้าง non-root user แล้วสลับไปใช้
FROM node:20
RUN useradd --create-home --uid 10001 appuser
COPY --chown=appuser . /app
USER appuser
CMD ["node", "server.js"]
```

### 1.2 ใช้ `:latest` / ไม่ pin digest
`:latest` ทำให้ build ไม่ reproducible และดึง image ที่อาจถูกแก้ไขภายหลัง

```dockerfile
# ❌ bad
FROM python:latest
```
```dockerfile
# ✅ good — pin tag + digest
FROM python:3.12.4-slim@sha256:2b3e6f1d6e... 
```

### 1.3 Secret ใน ENV / ARG
ค่าที่ใส่ใน `ENV`/`ARG` ถูกฝังใน image layer และอ่านได้ด้วย `docker history`

```dockerfile
# ❌ bad
ENV API_TOKEN=tok_live_demo1234567890   # allowlist secret
ARG DB_PASSWORD=SuperSecretP@ss         # allowlist secret
```
```dockerfile
# ✅ good — ใช้ BuildKit secret mount หรือ runtime env (ไม่ฝังใน layer)
RUN --mount=type=secret,id=api_token \
    API_TOKEN="$(cat /run/secrets/api_token)" ./build.sh
```

### 1.4 ADD แทน COPY
`ADD` auto-extract tar และดึง URL ได้ → พฤติกรรมไม่คาดคิด / MITM ใช้ `COPY` เสมอเว้นแต่จำเป็น

```dockerfile
# ❌ bad
ADD https://example.com/app.tar.gz /app/
```
```dockerfile
# ✅ good
COPY app.tar.gz /app/
RUN tar -xzf /app/app.tar.gz -C /app
```

### 1.5 ติดตั้งของไม่จำเป็น / ไม่ลบ cache
attack surface โต + image ใหญ่

```dockerfile
# ❌ bad
RUN apt-get update && apt-get install -y curl vim build-essential
```
```dockerfile
# ✅ good — ติดเท่าที่ต้อง, no-recommends, ลบ cache ใน layer เดียว
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*
```

### 1.6 Compose: privileged / host mode / docker socket
```yaml
# ❌ bad
services:
  app:
    privileged: true
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```
```yaml
# ✅ good — drop privilege, no host network, ไม่ mount docker socket
services:
  app:
    privileged: false
    cap_drop: ["ALL"]
    read_only: true
```

---

## 2. Kubernetes

### 2.1 privileged container
```yaml
# ❌ bad
securityContext:
  privileged: true
```
```yaml
# ✅ good
securityContext:
  privileged: false
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

### 2.2 hostPath / hostNetwork / hostPID / hostIPC
ทะลุ isolation ของ node

```yaml
# ❌ bad
spec:
  hostNetwork: true
  hostPID: true
  volumes:
    - name: host
      hostPath: { path: / }
```
```yaml
# ✅ good — ไม่ใช้ host namespace, ใช้ volume แบบ scoped
spec:
  hostNetwork: false
  hostPID: false
  volumes:
    - name: data
      emptyDir: {}
```

### 2.3 ไม่ตั้ง resource limits/requests
เสี่ยง resource exhaustion / DoS

```yaml
# ❌ bad — ไม่มี resources
containers:
  - name: app
    image: app:1.2.3
```
```yaml
# ✅ good
containers:
  - name: app
    image: app:1.2.3
    resources:
      requests: { cpu: "100m", memory: "128Mi" }
      limits:   { cpu: "500m", memory: "512Mi" }
```

### 2.4 runAsNonRoot / readOnlyRootFilesystem
```yaml
# ❌ bad — รันเป็น root, FS เขียนได้
containers:
  - name: app
    image: app:1.2.3
```
```yaml
# ✅ good
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  readOnlyRootFilesystem: true
```

### 2.5 capabilities เกินจำเป็น
```yaml
# ❌ bad
securityContext:
  capabilities:
    add: ["SYS_ADMIN", "NET_ADMIN"]
```
```yaml
# ✅ good — drop ALL แล้ว add เฉพาะที่จำเป็น
securityContext:
  capabilities:
    drop: ["ALL"]
    add: ["NET_BIND_SERVICE"]
```

### 2.6 Secret เป็น plaintext
```yaml
# ❌ bad — secret โผล่ใน manifest / env value
env:
  - name: DB_PASSWORD
    value: "SuperSecretP@ss"   # allowlist secret
```
```yaml
# ✅ good — อ้างจาก Secret object (หรือ external secret manager)
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: password
```

---

## 3. Terraform / IaC

### 3.1 Storage public (S3)
```hcl
# ❌ bad
resource "aws_s3_bucket" "data" {
  bucket = "kob-data"
  acl    = "public-read"
}
```
```hcl
# ✅ good — private + block public access
resource "aws_s3_bucket" "data" {
  bucket = "kob-data"
}
resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### 3.2 Security group เปิด 0.0.0.0/0 บน port อ่อนไหว
```hcl
# ❌ bad — SSH เปิดทั้งโลก
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}
```
```hcl
# ✅ good — จำกัด CIDR เฉพาะ office/VPN
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.20.0.0/24"]
}
```

### 3.3 Unencrypted storage
```hcl
# ❌ bad
resource "aws_ebs_volume" "vol" {
  availability_zone = "ap-southeast-1a"
  size              = 50
}
```
```hcl
# ✅ good — encryption at rest + KMS
resource "aws_ebs_volume" "vol" {
  availability_zone = "ap-southeast-1a"
  size              = 50
  encrypted         = true
  kms_key_id        = aws_kms_key.ebs.arn
}
```

### 3.4 IAM policy กว้างเกิน
```hcl
# ❌ bad — wildcard ทุก action ทุก resource
statement {
  effect    = "Allow"
  actions   = ["*"]
  resources = ["*"]
}
```
```hcl
# ✅ good — least privilege
statement {
  effect    = "Allow"
  actions   = ["s3:GetObject", "s3:PutObject"]
  resources = ["arn:aws:s3:::kob-data/*"]
}
```

### 3.5 Hardcoded secret ใน .tf / .tfvars
```hcl
# ❌ bad
variable "db_password" {
  default = "SuperSecretP@ss"   # allowlist secret
}
```
```hcl
# ✅ good — ไม่มี default, inject ผ่าน env/secret manager
variable "db_password" {
  type      = string
  sensitive = true
}
# TF_VAR_db_password ตั้งผ่าน CI secret / Vault
```

### 3.6 Logging / versioning ปิด
```hcl
# ✅ good — เปิด versioning + access log บน bucket สำคัญ
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration { status = "Enabled" }
}
```
