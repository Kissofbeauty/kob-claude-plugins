# CI/CD & Promote to Production (BI เท่านั้น)

> ทำหลัง **management approve** · official image **build จาก `main`** ไม่ใช่จาก local ของ user

## หลักการ
- **Source of truth = `main`** (ผ่าน PR + review + security gate ตาม skill-git-standard)
- **CI build image จาก main** → reproducible, ตรวจสอบได้, ไม่เชื่อ artifact จากเครื่องใคร
- **Registry = Docker Hub (private repo)** ที่ทีม BI ดูแล
- credential ของ registry/cloud อยู่ใน **CI secret** เท่านั้น — ไม่อยู่ใน image/โค้ด

## CI/CD flow (เมื่อ main เปลี่ยน)
```
push/merge → main
   ↓
CI (GitHub Actions):
  1. test + lint
  2. security gate: secret-scan + container-iac scan  ← ต้องผ่าน
  3. docker build (multi-stage) จาก source บน main
  4. docker login (CI secret) → push Docker Hub PRIVATE
     tag: <commit-sha> + prod
  5. deploy prod (AWS) — pull image แล้ว run
```

## ตัวอย่างโครง GitHub Actions (BI ตั้งใน repo prod)
```yaml
on:
  push:
    branches: [main]
jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - name: Security gate (ต้องผ่านก่อน build)
        run: ./scripts/security-gate.sh        # secret-scan + container-iac
      - name: Build image
        run: docker build -t $REPO:${{ github.sha }} -t $REPO:prod .
      - name: Login + push (private)
        run: |
          echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u "${{ secrets.DOCKERHUB_USER }}" --password-stdin
          docker push $REPO:${{ github.sha }}
          docker push $REPO:prod
      - name: Deploy prod (AWS)
        run: ./scripts/deploy-prod.sh ${{ github.sha }}   # pull + run image เดิม
```
> `secrets.DOCKERHUB_*` = CI secret (private repo) · ไม่อยู่ใน image
> `$REPO` = `<biorg>/<app>` บน Docker Hub **private**

## Promote checklist (BI)
- [ ] source บน `main` ผ่าน review + security gate
- [ ] image build จาก main (ไม่ใช่ local) + ไม่มี secret (`docker history` สะอาด)
- [ ] push ขึ้น **private** repo เท่านั้น
- [ ] tag ด้วย commit-sha (rollback ได้) + `prod`
- [ ] deploy ใช้ image เดิมกับที่ทดสอบ (parity)
