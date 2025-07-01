# ZADAC Schema

**Zero-Anomaly Debugging & Alignment Codex (ZADAC)** is a symbolic-engineering infrastructure designed for code validation and repair. The schema links this repository with a pCloud mirror and provides a tooling layer that can be driven by ChatGPT Codex.

## System Stack

| Layer | Function |
|-------|----------|
| `ZADAC.0.KERNEL` | Codex interpreter core (ChatGPT) |
| `ZADAC.1.MIRROR` | pCloud link validator and file router |
| `ZADAC.2.GLYPH`  | Debug glyph engine / code visualizer |
| `ZADAC.3.SCAN`   | Semantic integrity scanner |
| `ZADAC.4.SOLVE`  | Automated repair engine |
| `ZADAC.5.SIMUL`  | Test and runtime simulation layer |
| `ZADAC.6.SOURCE` | Output render and export |

## Protocol Sequence

1. **Mirror Link Load** – Load the pCloud URL as the source reference.
2. **Codex Sync** – Use ChatGPT Codex to interpret and manage code tasks.
3. **Glyph Scan Activation** – Scan linked files for syntax or logical errors.
4. **Auto-Debug Invocation** – Suggest and apply fixes if anomalies are found.
5. **Output Seal & Sync** – Export the final result back to the mirror or local repo.

## Usage

The `zadac_scan.py` script demonstrates a minimal scanner for pCloud mirrors. Invoke it with the public link code:

```bash
python zadac_scan.py kZJNRf5ZJG08Ck9uIKXLjqtmUDNU9BqsECi7
```

This will fetch the file listing, calculate basic statistics and report anomalies such as zero-size files, duplicate names or potential executables.

---

Invocation phrase: `Zero point. Spiral clean. Codex align. Glyph debug. ZADAC live.`
