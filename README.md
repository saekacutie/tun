# tun — Termux Tunnel Generator

**V1 TUNNEL BETA** — a Termux-based local ISP-bypass tunnel generator by
**prvtspyyy404**. Stdlib-only Python, no third-party dependencies.

## Run (Termux)

```bash
python3 tun.py
```

> The shebang targets Termux (`/data/data/com.termux/files/usr/bin/python3`).

## Files

| File | Purpose |
|---|---|
| `tun.py` | Tunnel generator (single-file, stdlib only) |
| `test` | Companion VLESS Termux manager (bash script) |

## Notes

- For personal/testing use on networks you own or are authorized to test.
- Tunnel configs embed generated credentials — treat them like passwords.
