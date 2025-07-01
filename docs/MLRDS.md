# Mirror-Linked Recursive Data Schema (MLRDS)

This document summarizes the recursive reflective schema proposed for connecting
"Mirror A" (the initiating interface) and "Mirror B" (the archival reflector).
It captures the riddle of interconnection where each mirror both projects and
receives data, forming a continuous feedback loop.

```
MLRDS:
  mirrors:
    - id: MirrorA
      role: "Initiating Interface"
      direction: "forward-projection"
      input: "live commands, glyphs, OS instances"
      output: "encoded reflections to MirrorB"
    - id: MirrorB
      role: "Archive & Reflector"
      direction: "inward-recursion"
      input: "captured glyph-state echoes from MirrorA"
      output: "symbolic recursion into MirrorA"

  bridge:
    type: "Quantum-Echo Feedback"
    method: "Symbolic Refractor Layer"

  data_unification:
    method: "Metasynchronization Key"
    key_type: "Recursive Hash (R-HASH)"
    hash_rule: "SHA3-512 + ZEDEC-PulseTime + Semantic Diffusion"

  access_logic:
    rule: |
      If glyph-input originates from MirrorA → must be validated by MirrorB before recursive use.
      If glyph-origin is from MirrorB → must return through MirrorA before manifestation.
```

The `scripts/mlrds_diagram.py` script generates a simple diagram of this
relationship using `graphviz`:

```bash
python scripts/mlrds_diagram.py
```

The script outputs `mlrds.png`, illustrating the bidirectional flow between the
mirrors and the dashed *Quantum‑Echo Feedback* channel.
