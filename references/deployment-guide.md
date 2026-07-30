# Deployment Guide

> Dual-server deployment operations for GEO-optimized Next.js websites.
> Based on real-world deployment on Tencent Cloud (106.52.23.83) and
> legacy server (1.117.188.4).

## Server Architecture

| Role | IP | SSH Port | App Port | Domain | Node Path | PM2 Name |
|---|---|---|---|---|---|---|
| Primary | 106.52.23.83 | 22 | 3000 | xcloud-top.com | /root/.nvm/versions/node/v18.20.8/bin/node | yunding-geo-site |
| Secondary | 1.117.188.4 | 123 | 8333 | (legacy) | /usr/bin/node (v16.18.0) | yunding-geo-site |

### Key Constraints

- **Primary server**: OpenCloudOS 9.4, Node v20 (system) + Node v18 (nvm).
  MUST use Node 18 for build/run. Node 20 causes admin/login 500 errors.
  PM2 interpreter must point to nvm Node 18 path.
- **Secondary server**: Node v16.18.0, no nvm. Next.js max 13.4.x.
  SSH port 123, fail2ban active (may ban IP after failed attempts).
  Needs `react-dom/server.edge` patch for middleware.
- **Both servers**: Project at `/srv/proj2`, PM2 cluster mode, Nginx reverse proxy.

---

## Paramiko SSH/SFTP Patterns

### Connection

```python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Note: parameter is 'hostname' not 'host'!
ssh.connect(
    hostname='106.52.23.83',
    port=22,
    username='root',
    password='PASSWORD',
    timeout=15
)
sftp = ssh.open_sftp()
```

### Read/Write Remote Files (handles encoding)

```python
def read_remote(sftp, path):
    """Read remote file, return str (auto-decode bytes)"""
    with sftp.open(path, 'r') as f:
        data = f.read()
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

def write_remote(sftp, path, content):
    """Write remote file, accept str or bytes"""
    with sftp.open(path, 'w') as f:
        if isinstance(content, str):
            f.write(content.encode('utf-8'))
        else:
            f.write(content)
```

### Upload from Memory (no temp file)

```python
import io

content = "file content here"
sftp.putfo(
    io.BytesIO(content.encode('utf-8')),
    '/remote/path/file.tsx'
)
# MUST use io.BytesIO, NOT io.StringIO (SFTP expects binary stream)
```

### Execute Commands

```python
stdin, stdout, stderr = ssh.exec_command('command here')
output = stdout.read().decode('utf-8')  # MUST decode
error = stderr.read().decode('utf-8')
exit_code = stdout.channel.recv_exit_status()
```

### Password Special Characters

**Problem**: Passwords containing `$0`, `%`, `[`, `]` get interpreted by bash
when inline in Python via shell.

**Solution**: Always pass passwords through Python script files, never inline
in bash `-c` commands. Or use environment variables.

---

## Standard Build Sequence

```bash
# 1. Clear .next cache (CRITICAL — skip this and changes won't take effect!)
rm -rf .next

# 2. Build (use absolute path to node, don't rely on nvm)
{node_bin} node_modules/.bin/next build

# 3. Delete PM2 process (not restart — avoids errored state trap)
pm2 delete yunding-geo-site 2>/dev/null

# 4. Fresh start
pm2 start ecosystem.config.js

# 5. Wait for warmup (cluster mode needs time)
sleep 5

# 6. Verify
curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/
```

### ecosystem.config.js

```javascript
module.exports = {
  apps: [{
    name: 'yunding-geo-site',
    script: 'node_modules/.bin/next',
    args: 'start -p 3000',  // or 8333 for secondary
    cwd: '/srv/proj2',
    instances: 'max',
    exec_mode: 'cluster',
    interpreter: '/root/.nvm/versions/node/v18.20.8/bin/node',  // primary only
    env: {
      NODE_ENV: 'production',
      PORT: 3000  // or 8333
    }
  }]
};
```

---

## PM2 Errored State Recovery

**Problem**: `pm2 restart` from `errored` status does NOT work. The errored
state is "sticky" — restart stays errored.

**Root cause chain**:
```
ESLint error / build failure → npm run build exits 1 → 
.next directory incomplete → PM2 can't find BUILD_ID → 
crash → repeated restart → errored (sticky)
```

**Recovery**:
```bash
# 1. Delete (not restart)
pm2 delete yunding-geo-site

# 2. Clean build artifacts
rm -rf /srv/proj2/.next

# 3. Rebuild
cd /srv/proj2 && {node_bin} node_modules/.bin/next build

# 4. Fresh start (not restart)
pm2 start ecosystem.config.js

# 5. Save process list
pm2 save
```

---

## ESLint Configuration (prevent build blocking)

In `next.config.js`:
```javascript
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,  // Skip ESLint during build
  },
  typescript: {
    ignoreBuildErrors: false,  // DO NOT skip TypeScript!
  },
  reactStrictMode: false,
  poweredByHeader: false,
};
```

**Why ESLint can be skipped but TypeScript cannot**:
- ESLint checks code style (quote escaping, unused vars) — doesn't affect runtime
- TypeScript checks type safety — skipping may cause runtime crashes

---

## Dual-Server Sync Workflow

```python
servers = {
    'primary': {
        'host': '106.52.23.83', 'port': 22,
        'password': 'PASSWORD1',
        'node_bin': '/root/.nvm/versions/node/v18.20.8/bin/node',
        'app_port': 3000
    },
    'secondary': {
        'host': '1.117.188.4', 'port': 123,
        'password': 'PASSWORD2',
        'node_bin': '/usr/bin/node',
        'app_port': 8333
    }
}

modified_files = [
    'src/app/page.tsx',
    'src/app/faq/page.tsx',
    'data/dynamic/faq.json',
    'src/app/sitemap.ts',
    # ...
]

for name, cfg in servers.items():
    ssh = connect(cfg)
    sftp = ssh.open_sftp()
    
    # Upload modified files
    for file_path in modified_files:
        content = read_local(file_path)  # or generate
        write_remote(sftp, f'/srv/proj2/{file_path}', content)
    
    # Build
    exec_command(ssh, f'cd /srv/proj2 && rm -rf .next')
    exec_command(ssh, f'cd /srv/proj2 && {cfg["node_bin"]} node_modules/.bin/next build')
    
    # Restart PM2
    exec_command(ssh, f'pm2 delete yunding-geo-site 2>/dev/null')
    exec_command(ssh, f'cd /srv/proj2 && pm2 start ecosystem.config.js')
    
    # Verify
    import time; time.sleep(5)
    status = exec_command(ssh, f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{cfg["app_port"]}/')
    assert status == '200', f'{name} homepage not 200!'
    
    ssh.close()
```

---

## Common Pitfalls

| Pitfall | Cause | Solution |
|---|---|---|
| CSS/component changes don't take effect | `.next` cache not cleared | Always `rm -rf .next` before build |
| PM2 stays errored after restart | Errored is sticky | `pm2 delete` + `pm2 start` (not restart) |
| Python f-string `{{` conflicts with JSX | f-string interprets `{{` as literal `{` | Use `.replace()` template pattern instead |
| paramiko SFTP read returns bytes | SFTP `read()` returns bytes not str | Always `.decode('utf-8')` |
| Password `$0` interpreted by bash | Shell variable expansion | Pass via Python file, not inline bash |
| ESLint blocks build | `react/no-unescaped-entities` on JSX quotes | Set `eslint.ignoreDuringBuilds: true` |
| Node version mismatch | Next.js 14+ needs Node 18+ | Lock Node version in ecosystem.config.js |
| CRLF line endings on Linux | Windows development → Linux server | `.gitattributes` with `eol=lf` |
| Chinese full-width quotes in code | Copy-paste from Word/WeChat | `grep -P '[\x{201C}\x{201D}]'` to find |
| PM2 restart returns 000 | Service not ready yet | `sleep 5` before curl verify |
| fail2ban IP ban | SSH auth failures | Use SSH keys; `fail2ban-client unbanip` |
| JSX double quotes ESLint error | `react/no-unescaped-entities` | Use `&ldquo;` / `&rdquo;` or `{'"'}` |
| react-dom missing server.edge | Node 16 + Next.js 13.4.19 | Copy `server.node.js` → `server.edge.js` |
| BUILD_ID missing | Incomplete build | Create manually: `echo uuid > .next/BUILD_ID` |

---

## Verification Checklist (Per Server)

| Check | Command | Expected |
|---|---|---|
| Homepage | `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/` | 200 |
| All routes | `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/{route}` | 200 |
| llms.txt | `curl -s http://localhost:{port}/llms.txt \| wc -c` | > 500 |
| llms-full.txt | `curl -s http://localhost:{port}/llms-full.txt \| wc -c` | > 2000 |
| robots.txt | `curl -s http://localhost:{port}/robots.txt \| grep -c "User-agent"` | >= 11 |
| sitemap URLs | `curl -s http://localhost:{port}/sitemap.xml \| grep -c "<loc>"` | >= 12 |
| FAQ entries | `curl -s http://localhost:{port}/faq \| grep -c "question"` | >= 30 |
| BreadcrumbList | `curl -s http://localhost:{port}/{route} \| grep -c "BreadcrumbList"` | >= 1 |
| Organization Schema | `curl -s http://localhost:{port}/ \| grep -c '"@type":"Organization"'` | >= 1 |
| Empty alt (decorative only) | `curl -s http://localhost:{port}/ \| grep -c 'alt=""'` | minimal |

## Dual-Server Parity Check

```python
# Source file MD5 must match between servers
for file_path in modified_files:
    cmd = f"md5sum /srv/proj2/{file_path}"
    md5_new = exec(ssh_new, cmd).split()[0]
    md5_old = exec(ssh_old, cmd).split()[0]
    assert md5_new == md5_old, f"MD5 mismatch: {file_path}"

# HTML byte count should be similar (may differ slightly due to timestamps)
for route in ['/', '/faq', '/about', '/cases']:
    bytes_new = int(exec(ssh_new, f"curl -s http://localhost:3000{route} | wc -c"))
    bytes_old = int(exec(ssh_old, f"curl -s http://localhost:8333{route} | wc -c"))
    diff = abs(bytes_new - bytes_old) / max(bytes_new, bytes_old)
    assert diff < 0.01, f"HTML diff too large: {route} ({diff:.2%})"
```

---

## 301 Redirect (Domain Migration)

In `next.config.js` on old server:
```javascript
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/:path*',
        destination: 'https://new-domain.com/:path*',
        statusCode: 301,  // MUST use statusCode: 301, NOT permanent: true!
      },
    ];
  },
};
```

**Critical**: `permanent: true` returns 308, not 301. Some AI crawlers and GEO
scoring tools only recognize 301. Always use `statusCode: 301`.

Verify:
```bash
curl -sI http://old-domain:8333/ | grep -E "HTTP|Location"
# Expected: HTTP/1.1 301 Moved Permanently
# Expected: location: https://new-domain.com/
```
