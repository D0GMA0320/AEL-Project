"""Run a code-protected demo with a temporary tunnel or an existing connector."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.local' / 'demo'
sys.path.insert(0, str(ROOT))
from demo_security import valid_public_origin

def configured_origin(public_url=None, quick=False):
    """A local setting selects the existing Windows connector; no token is read."""
    if quick:
        return None
    setting = STATE / 'named-origin.txt'
    value = public_url if public_url is not None else (
        setting.read_text(encoding='utf-8-sig').strip() if setting.exists() else None
    )
    if value is not None and not valid_public_origin(value):
        raise ValueError('Use a lowercase HTTPS address without a path, port or trailing slash in .local/demo/named-origin.txt.')
    return value

def wait_for_server(server, port):
    for _ in range(50):
        if server.poll() is not None:
            raise RuntimeError('The classroom server stopped; see .local/demo/server.log.')
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            pass
        time.sleep(0.1)
    raise RuntimeError('The classroom server did not become ready; see .local/demo/server.log.')

def install_tunnel():
    binary = STATE / 'cloudflared.exe'
    receipt = STATE / 'cloudflared-release.json'
    if binary.exists() and receipt.exists():
        record = json.loads(receipt.read_text())
        if hashlib.sha256(binary.read_bytes()).hexdigest() == record['sha256']:
            return binary
        raise RuntimeError('Tunnel binary checksum changed. Remove only .local/demo/cloudflared.exe and its receipt, then retry.')
    print('Downloading the official Cloudflare tunnel helper into .local/demo ...', flush=True)
    request = urllib.request.Request('https://api.github.com/repos/cloudflare/cloudflared/releases/latest', headers={'User-Agent':'AEL-Classroom'})
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)
    asset = next(a for a in release['assets'] if a['name'] == 'cloudflared-windows-amd64.exe')
    digest = asset.get('digest', '')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
        raise RuntimeError('The official release did not supply a SHA256 digest. Download was not started.')
    url = asset['browser_download_url']
    if not url.startswith('https://github.com/cloudflare/cloudflared/releases/download/'):
        raise RuntimeError('Unexpected download location')
    with urllib.request.urlopen(url, timeout=90) as response:
        contents = response.read(100_000_000)
    actual = hashlib.sha256(contents).hexdigest()
    if actual != digest.split(':')[1]:
        raise RuntimeError('Official tunnel download checksum mismatch')
    binary.write_bytes(contents)
    receipt.write_text(json.dumps({'version':release['tag_name'], 'url':url, 'sha256':actual},indent=2))
    return binary

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--install-only',action='store_true')
    parser.add_argument('--stop',action='store_true')
    parser.add_argument('--port',type=int,default=8767)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--public-url',help='Use an existing Cloudflare connector with this HTTPS origin.')
    mode.add_argument('--quick',action='store_true',help='Use a temporary tunnel instead of the saved named origin.')
    args=parser.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    stop_file=STATE/'stop'
    if args.stop:
        stop_file.write_text('stop')
        print('Stop requested. The demo will close; any separately installed Cloudflare service stays running.')
        return
    if args.install_only:
        install_tunnel()
        print('Official tunnel helper downloaded and checksum verified.')
        return
    public=configured_origin(args.public_url,args.quick)
    named=public is not None
    # Fail before changing runtime state if another demo already owns this port.
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',args.port))
    binary=None if named else install_tunnel()
    stop_file.unlink(missing_ok=True)
    origin=STATE/'origin.txt'
    origin.write_text(public or '',encoding='utf-8')
    code=secrets.token_urlsafe(9)
    env=os.environ.copy();env['AEL_DEMO_CODE']=code
    flags=getattr(subprocess,'CREATE_NO_WINDOW',0)
    processes=[]
    print('Starting classroom server using your existing Cloudflare connector ...' if named else 'Starting classroom server and temporary HTTPS tunnel ...',flush=True)
    try:
        if os.name=='nt':ctypes.windll.kernel32.SetThreadExecutionState(0x80000003)
        with (STATE/'server.log').open('w',encoding='utf-8') as server_log, (STATE/'tunnel.log').open('w',encoding='utf-8') as tunnel_log:
            server=subprocess.Popen([sys.executable,'-u',str(ROOT/'server.py'),'--port',str(args.port),'--demo-origin-file',str(origin)],cwd=ROOT,env=env,stdout=server_log,stderr=subprocess.STDOUT,creationflags=flags)
            processes.append(server)
            wait_for_server(server,args.port)
            if not named:
                # Empty config avoids accidentally using an unrelated tunnel configuration.
                config=STATE/'tunnel-config.yml';config.write_text('{}\n')
                tunnel=subprocess.Popen([str(binary),'tunnel','--config',str(config),'--no-autoupdate','--protocol','http2','--url',f'http://127.0.0.1:{args.port}'],cwd=ROOT,stdout=tunnel_log,stderr=subprocess.STDOUT,creationflags=flags)
                processes.append(tunnel)
                for _ in range(60):
                    if server.poll() is not None or tunnel.poll() is not None:raise RuntimeError('A demo process stopped; see .local/demo logs.')
                    text=(STATE/'tunnel.log').read_text(encoding='utf-8',errors='replace')
                    found=re.search(r'https://[a-z0-9-]+\.trycloudflare\.com',text)
                    if found:public=found.group();break
                    time.sleep(1)
                if not public:raise RuntimeError('No tunnel URL was returned within 60 seconds; see .local/demo/tunnel.log.')
            origin.write_text(public,encoding='utf-8')
            restart_note='The address stays the same; the classroom code changes after restart. Keep the Cloudflared Windows service running. Connector health is shown in your Cloudflare dashboard.' if named else 'The address and code change after restart.'
            instructions=f'URL: {public}\nClassroom code: {code}\nKeep this PC on and connected. Run stop-internet-demo.cmd to stop.\n{restart_note}\n'
            (STATE/'share.txt').write_text(instructions,encoding='utf-8')
            print(instructions,flush=True)
            while not stop_file.exists():
                if any(p.poll() is not None for p in processes):raise RuntimeError('A demo process stopped. Restart start-internet-demo.cmd and read the new classroom code.')
                time.sleep(1)
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:process.kill()
        if os.name=='nt':ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        print('Demo stopped. The app is offline; your separate Cloudflare service is unchanged.' if named else 'Demo stopped. The previous public URL is no longer served.',flush=True)

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:pass
    except Exception as error:
        print('Demo could not continue:',str(error),file=sys.stderr)
        sys.exit(1)
