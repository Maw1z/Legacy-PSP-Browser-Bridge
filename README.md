# Legacy PSP Browser Bridge
### Bridging a 2004 PSP to the Modern Web Through an Intentional TLS Downgrade Proxy

A lightweight HTTP-to-HTTPS compatibility proxy that allows a Sony PSP to access modern HTTPS websites it cannot reach directly due to its outdated SSL/TLS stack. Built as a personal security research project to demonstrate TLS downgrade mechanics and cleartext credential exposure.

---

## What This Is

The PSP supports SSL 3.0 and TLS 1.0 with cipher suites (RC4, 3DES) that are prohibited by modern servers. It cannot complete a TLS handshake with any site requiring TLS 1.2 or higher, which is essentially every major website today.

This proxy sits between the PSP and the internet:

```
PSP  ──  HTTP  ──►  Proxy  ──  HTTPS  ──►  Website
```

The PSP sends plain HTTP to the proxy. The proxy establishes a modern TLS 1.3 connection upstream, retrieves the content, adapts the HTML for NetFront, and returns it over HTTP. The security consequence is intentional and documented: the PSP-to-proxy segment is unencrypted, and credentials submitted through the proxy travel in plaintext.

---

## Files

| File | Description |
|---|---|
| `proxy.py` | Main proxy with HTML transformation via the legacy adapter |
| `proxy_without_adapter.py` | Bare downgrade proxy, no HTML transformation |
| `legacy_adapter.py` | Strips modern HTML/CSS/JS elements and rewrites HTTPS URLs to HTTP |
| `index.html` | Test login page deployed to GitHub Pages for credential capture demo |
| `requirements.txt` | Python dependencies |

---

## Setup

```bash
pip install -r requirements.txt
python3 proxy.py
```

Proxy listens on `0.0.0.0:8888`.

On the PSP: **Network Settings → Infrastructure → your network → Proxy Server → your machine's local IP, port 8888**

---

## What Works

Sites that are mostly static HTML render acceptably on the PSP through the proxy:

- CNN Lite, NPR Text, CBC Lite
- Hacker News, Lobsters, Skimfeed
- Wikipedia Mobile
- RFC Editor
- GNU FTP
- Human Rights Watch
- WUKY Text

JavaScript-heavy sites do not render. NetFront predates HTML5, CSS3, and modern JS frameworks entirely.

---

## Security Note

This project demonstrates that the proxy topology is architecturally identical to an SSL stripping attack. The difference is intent: the PSP is a legacy client that cannot use modern HTTPS regardless, and the proxy is trusted and configured deliberately. The credential capture demonstration uses a controlled test page. Do not route authenticated sessions through this proxy.

---

## Full Writeup

[Dead Protocol Walking (PDF)](Dead%20Protocol%20Walking.docx) — covers PSP TLS history, NetFront limitations, proxy architecture, test results, Wireshark analysis, and security implications.
