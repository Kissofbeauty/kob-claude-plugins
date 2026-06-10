# OWASP Top 10:2025 — Quick Reference

> ตัวอย่างโค้ดด้านล่างเป็น **Python/JS** เพื่อความกระชับ — **pattern ใช้ได้ทุกภาษา** ให้เทียบเคียง equivalent ในภาษาเป้าหมาย (เช่น weak hash, string-concat SQL, unsafe deserialize, fail-open มีในทุกภาษา)

## A01:2025 — Broken Access Control (was #1 in 2021)
**CWEs:** 34 mapped | **Prevalence:** 94% of tested apps

Patterns to detect:
- Direct object references ที่ไม่ตรวจสอบ ownership: `GET /file?id=123`
- Missing `@login_required` / `@permission_required`
- CORS: `Access-Control-Allow-Origin: *` ใน API ที่มี auth
- Force browsing: `/admin`, `/debug`, `/actuator` endpoints
- JWT claims ที่ไม่ validate server-side
- SSRF: ดึง URL จาก user input โดยไม่ validate

## A02:2025 — Security Misconfiguration (was #5 in 2021)
**CWEs:** 20 mapped

Patterns to detect:
- `DEBUG = True` ใน Django/Flask production config
- Default passwords (`admin:admin`, `root:root`)
- Unnecessary HTTP methods (PUT, DELETE บน endpoints ที่ไม่ต้องการ)
- Missing security headers: `X-Frame-Options`, `Content-Security-Policy`, `HSTS`
- `.env` files ไม่อยู่ใน `.gitignore`
- Stack traces ใน HTTP responses

## A03:2025 — Software Supply Chain Failures (NEW — was A06 Vulnerable Components)
**CWEs:** 20 mapped

Patterns to detect:
- Unpinned dependencies: `requests>=2.0` (ควรใช้ `==` หรือ range ที่แคบ)
- Known CVE packages (ตรวจ version ใน pyproject.toml/package.json)
- Build scripts ที่ download แล้ว pipe to shell: `curl | bash`
- Missing integrity checks บน downloaded artifacts

Common Python CVE packages to check:
- `cryptography < 41.0.0` — หลาย CVE
- `pillow < 10.0.0` — arbitrary code execution
- `pyyaml < 6.0` — arbitrary code execution
- `requests < 2.28.0` — multiple issues

## A04:2025 — Cryptographic Failures (was #2)
**CWEs:** 29 mapped

Patterns to detect:
```python
# ❌ Weak hashing
import hashlib
hashlib.md5(password.encode()).hexdigest()
hashlib.sha1(data).hexdigest()

# ❌ Weak encryption
from Crypto.Cipher import DES  # block size 64-bit
AES.new(key, AES.MODE_ECB)     # ECB mode ไม่ปลอดภัย

# ❌ Insecure random
import random
token = random.randint(1000, 9999)  # predictable

# ❌ Hardcoded key
SECRET_KEY = "mysecretkey123"

# ✅ Correct
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())

import secrets
token = secrets.token_urlsafe(32)
```

## A05:2025 — Injection (was #3)
**CWEs:** 33 mapped (includes XSS)

### SQL Injection patterns:
```python
# ❌
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute("SELECT * FROM users WHERE id = " + user_id)

# ✅
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### Command Injection patterns:
```python
# ❌
os.system(f"ping {host}")
subprocess.call(f"ls {path}", shell=True)

# ✅
subprocess.run(["ping", host], shell=False)
```

### Path Traversal patterns:
```python
# ❌
with open(f"/uploads/{filename}") as f: ...

# ✅
safe_path = Path("/uploads") / Path(filename).name
if not safe_path.resolve().is_relative_to(Path("/uploads")):
    raise ValueError("Invalid path")
```

## A06:2025 — Insecure Design (was #4)
**CWEs:** 40 mapped

Patterns to detect:
- ไม่มี rate limiting บน: login, password reset, OTP
- ไม่มี account lockout หลัง failed attempts
- Business logic: negative quantities, price = 0
- Missing CSRF protection บน state-changing forms

## A07:2025 — Authentication Failures (was #7)
**CWEs:** 36 mapped

Patterns to detect:
```python
# ❌ Weak password hashing
import hashlib
password_hash = hashlib.sha256(password.encode()).hexdigest()

# ❌ JWT alg:none vulnerability
jwt.decode(token, options={"verify_signature": False})

# ❌ Hardcoded credentials
if username == "admin" and password == "admin123":

# ✅
import bcrypt
bcrypt.checkpw(password.encode(), stored_hash)
```

## A08:2025 — Software/Data Integrity Failures (same as 2021)
**CWEs:** 10 mapped

Patterns to detect:
```python
# ❌ Unsafe deserialization
import pickle
data = pickle.loads(user_input)  # RCE possible

# ❌ Unsafe YAML
import yaml
yaml.load(user_data)  # use yaml.safe_load() instead

# ❌ Unsafe eval
eval(user_expression)
exec(user_code)
```

## A09:2025 — Security Logging & Alerting Failures (was #9)
**CWEs:** 4 mapped

Patterns to detect:
- ไม่มี logging บน auth events
- Log ข้อมูล sensitive: password, token, credit card
- ไม่มี audit trail บน admin actions

```python
# ❌ Logging sensitive data
logger.info(f"Login: user={username}, password={password}")

# ✅
logger.info(f"Login attempt: user={username}, success={result}")
logger.warning(f"Failed login: user={username}, ip={ip}, attempt={count}")
```

## A10:2025 — Mishandling of Exceptional Conditions (NEW)
**CWEs:** 24 mapped

Patterns to detect:
```python
# ❌ Fail open — อนุญาตเมื่อ error
try:
    result = check_permission(user)
except:
    result = True  # dangerous!

# ❌ Swallowing errors
try:
    validate_input(data)
except Exception:
    pass  # attacker can bypass validation

# ❌ Exposing internal state
except Exception as e:
    return {"error": str(e), "traceback": traceback.format_exc()}

# ✅ Fail closed
try:
    result = check_permission(user)
except Exception:
    logger.error("Permission check failed", exc_info=True)
    return False  # deny on error
```
