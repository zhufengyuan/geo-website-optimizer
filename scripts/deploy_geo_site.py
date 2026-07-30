#!/usr/bin/env python3
"""
GEO Website Deployment Script — Dual-server synchronized deployment via SSH/SFTP.

Features:
- Upload modified files to remote server via SFTP
- Execute build sequence (clear .next → build → PM2 delete+start → verify)
- Support dual-server deployment with different configs
- Verification checklist after deployment

Usage:
    # Single server
    python deploy_geo_site.py --host 106.52.23.83 --port 22 --user root \
        --password 'PASS' --project /srv/proj2 \
        --node-bin /root/.nvm/versions/node/v18.20.8/bin/node \
        --app-port 3000 --pm2-name yunding-geo-site \
        --files src/app/page.tsx src/app/faq/page.tsx

    # Dual server (using config file)
    python deploy_geo_site.py --config deploy_config.json --files src/app/page.tsx
"""

import argparse
import io
import json
import os
import paramiko
import sys
import time


def connect_ssh(host, port, username, password, timeout=15):
    """Connect to SSH server."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username,
                password=password, timeout=timeout)
    return ssh


def read_remote(sftp, path):
    """Read remote file, return str."""
    with sftp.open(path, 'r') as f:
        data = f.read()
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data


def write_remote(sftp, path, content):
    """Write content to remote file."""
    with sftp.open(path, 'w') as f:
        if isinstance(content, str):
            f.write(content.encode('utf-8'))
        else:
            f.write(content)


def upload_file(sftp, local_path, remote_path):
    """Upload a local file to remote server."""
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    write_remote(sftp, remote_path, content)


def upload_content(sftp, content, remote_path):
    """Upload string content to remote server (no local file needed)."""
    sftp.putfo(io.BytesIO(content.encode('utf-8')), remote_path)


def exec_command(ssh, command, timeout=300):
    """Execute SSH command, return (exit_code, stdout, stderr)."""
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return exit_code, out, err


def build_and_deploy(ssh, config):
    """Execute build sequence on server."""
    project = config['project']
    node_bin = config['node_bin']
    app_port = config['app_port']
    pm2_name = config['pm2_name']
    
    print(f"\n--- Building on {config['host']} ---")
    
    # 1. Clear .next cache
    print("  [1/5] Clearing .next cache...")
    code, out, err = exec_command(ssh, f'rm -rf {project}/.next')
    if code != 0:
        print(f"  Warning: rm -rf .next returned {code}: {err}")
    
    # 2. Build
    print("  [2/5] Building Next.js...")
    build_cmd = f'cd {project} && {node_bin} node_modules/.bin/next build 2>&1'
    code, out, err = exec_command(ssh, build_cmd, timeout=600)
    if code != 0:
        print(f"  ❌ Build FAILED (exit {code})")
        print(f"  stdout: {out[-2000:]}")
        print(f"  stderr: {err[-2000:]}")
        return False
    
    # Check BUILD_ID exists
    code, out, err = exec_command(ssh, f'test -f {project}/.next/BUILD_ID && echo OK')
    if 'OK' not in out:
        print(f"  ❌ BUILD_ID missing after build!")
        return False
    
    print("  ✅ Build successful")
    
    # 3. Delete PM2 process
    print(f"  [3/5] Deleting PM2 process '{pm2_name}'...")
    exec_command(ssh, f'pm2 delete {pm2_name} 2>/dev/null')
    
    # 4. Fresh start
    print(f"  [4/5] Starting PM2 process '{pm2_name}'...")
    code, out, err = exec_command(ssh, f'cd {project} && pm2 start ecosystem.config.js 2>&1')
    if code != 0:
        print(f"  ❌ PM2 start failed: {err}")
        return False
    
    # Save PM2 list
    exec_command(ssh, 'pm2 save 2>/dev/null')
    
    # 5. Wait and verify
    print(f"  [5/5] Waiting for warmup...")
    time.sleep(5)
    
    code, out, err = exec_command(ssh, f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{app_port}/')
    if out.strip() == '200':
        print(f"  ✅ Homepage HTTP 200")
    else:
        print(f"  ❌ Homepage HTTP {out.strip()}")
        return False
    
    return True


def verify_deployment(ssh, config, routes=None):
    """Run verification checks on deployed site."""
    app_port = config['app_port']
    base = f'http://localhost:{app_port}'
    
    if routes is None:
        routes = ['/', '/faq', '/about', '/cases', '/contact', '/geo-service',
                  '/insights', '/tech-docs', '/llms.txt', '/llms-full.txt',
                  '/robots.txt', '/sitemap.xml']
    
    print(f"\n--- Verifying {config['host']} ---")
    all_ok = True
    
    for route in routes:
        code, out, err = exec_command(ssh, f'curl -s -o /dev/null -w "%{{http_code}}" {base}{route}')
        status = out.strip()
        ok = status == '200'
        if not ok:
            all_ok = False
        print(f"  {'✅' if ok else '❌'} {route}: {status}")
    
    # Additional checks
    code, out, err = exec_command(ssh, f'curl -s {base}/robots.txt | grep -c "User-agent"')
    print(f"  robots.txt UA rules: {out.strip()}")
    
    code, out, err = exec_command(ssh, f'curl -s {base}/sitemap.xml | grep -c "<loc>"')
    print(f"  sitemap URLs: {out.strip()}")
    
    code, out, err = exec_command(ssh, f'curl -s {base}/faq | grep -c "question"')
    print(f"  FAQ entries: {out.strip()}")
    
    code, out, err = exec_command(ssh, f'curl -s {base}/ | grep -c "BreadcrumbList"')
    print(f"  Homepage BreadcrumbList: {out.strip()}")
    
    code, out, err = exec_command(ssh, f'curl -s {base}/ | grep -c "Organization"')
    print(f"  Homepage Organization Schema: {out.strip()}")
    
    return all_ok


def deploy_to_server(config, files_to_upload=None, content_to_upload=None):
    """Deploy to a single server.
    
    Args:
        config: dict with host, port, user, password, project, node_bin, app_port, pm2_name
        files_to_upload: list of (local_path, remote_path) tuples
        content_to_upload: list of (content_str, remote_path) tuples
    """
    print(f"\n{'='*60}")
    print(f"  Deploying to {config['host']}:{config['port']}")
    print(f"{'='*60}")
    
    # Connect
    print("Connecting via SSH...")
    ssh = connect_ssh(config['host'], config['port'], config['user'], config['password'])
    sftp = ssh.open_sftp()
    print("✅ SSH connected")
    
    # Upload files
    if files_to_upload:
        print(f"\nUploading {len(files_to_upload)} files...")
        for local_path, remote_path in files_to_upload:
            full_remote = f"{config['project']}/{remote_path}"
            print(f"  → {remote_path}")
            upload_file(sftp, local_path, full_remote)
    
    if content_to_upload:
        print(f"\nUploading {len(content_to_upload)} generated files...")
        for content, remote_path in content_to_upload:
            full_remote = f"{config['project']}/{remote_path}"
            print(f"  → {remote_path}")
            upload_content(sftp, content, full_remote)
    
    sftp.close()
    
    # Build and deploy
    success = build_and_deploy(ssh, config)
    if not success:
        print(f"\n❌ Deployment FAILED on {config['host']}")
        ssh.close()
        return False
    
    # Verify
    all_ok = verify_deployment(ssh, config)
    
    ssh.close()
    return all_ok


def main():
    parser = argparse.ArgumentParser(description='GEO Website Deployment Tool')
    parser.add_argument('--host', help='Server hostname/IP')
    parser.add_argument('--port', type=int, default=22, help='SSH port (default: 22)')
    parser.add_argument('--user', default='root', help='SSH username')
    parser.add_argument('--password', help='SSH password')
    parser.add_argument('--project', default='/srv/proj2', help='Project path on server')
    parser.add_argument('--node-bin', default='/usr/bin/node', help='Node binary path')
    parser.add_argument('--app-port', type=int, default=3000, help='Application port')
    parser.add_argument('--pm2-name', default='yunding-geo-site', help='PM2 process name')
    parser.add_argument('--config', help='JSON config file for dual-server deployment')
    parser.add_argument('--files', nargs='*', help='Local files to upload (as remote_path)')
    parser.add_argument('--verify-only', action='store_true', help='Only verify, no deploy')
    
    args = parser.parse_args()
    
    if args.config:
        with open(args.config, 'r') as f:
            configs = json.load(f)
        if not isinstance(configs, list):
            configs = [configs]
    else:
        if not args.host or not args.password:
            print("Error: --host and --password required (or use --config)")
            sys.exit(1)
        configs = [{
            'host': args.host,
            'port': args.port,
            'user': args.user,
            'password': args.password,
            'project': args.project,
            'node_bin': args.node_bin,
            'app_port': args.app_port,
            'pm2_name': args.pm2_name,
        }]
    
    # Prepare files to upload
    files_to_upload = None
    if args.files:
        files_to_upload = []
        for f in args.files:
            # Assume local path same as remote relative path
            if os.path.exists(f):
                files_to_upload.append((f, f))
            else:
                print(f"Warning: file not found: {f}")
    
    # Deploy to each server
    results = []
    for config in configs:
        if args.verify_only:
            ssh = connect_ssh(config['host'], config['port'], config['user'], config['password'])
            ok = verify_deployment(ssh, config)
            ssh.close()
            results.append((config['host'], ok))
        else:
            ok = deploy_to_server(config, files_to_upload=files_to_upload)
            results.append((config['host'], ok))
    
    # Summary
    print(f"\n{'='*60}")
    print("  DEPLOYMENT SUMMARY")
    print(f"{'='*60}")
    for host, ok in results:
        print(f"  {'✅' if ok else '❌'} {host}")
    
    all_success = all(ok for _, ok in results)
    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
