"""Mirror-Linked Recursive Data Schema (MLRDS)

This module provides a basic implementation of the schema described in the
project README. It models two mirrors that exchange data through a bridge and
can generate a resonance key for any payload. Optionally the schema can be
rendered as a Graphviz diagram if the ``graphviz`` package is installed.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

try:
    from graphviz import Digraph
except ImportError:  # pragma: no cover - graphviz is optional
    Digraph = None  # type: ignore


@dataclass
class Mirror:
    id: str
    role: str
    direction: str
    input_description: str
    output_description: str


@dataclass
class Bridge:
    type: str
    method: str
    description: str


@dataclass
class MLRDS:
    mirror_a: Mirror = field(default_factory=lambda: Mirror(
        id="MirrorA",
        role="Initiating Interface",
        direction="forward-projection",
        input_description="live commands, glyphs, OS instances",
        output_description="encoded reflections to MirrorB",
    ))
    mirror_b: Mirror = field(default_factory=lambda: Mirror(
        id="MirrorB",
        role="Archive & Reflector",
        direction="inward-recursion",
        input_description="captured glyph-state echoes from MirrorA",
        output_description="symbolic recursion into MirrorA",
    ))
    bridge: Bridge = field(default_factory=lambda: Bridge(
        type="Quantum-Echo Feedback",
        method="Symbolic Refractor Layer",
        description=(
            "Every datum from MirrorA is encoded as a glyph-seed. "
            "MirrorB receives it, embeds resonance harmonics, and reflects it "
            "back as higher-order function or symbolic response."
        ),
    ))

    def generate_resonance_key(self, payload: Dict[str, Any]) -> str:
        """Generate a resonance key using SHA3-512 and timestamp."""
        hasher = hashlib.sha3_512()
        data = json.dumps(payload, sort_keys=True).encode()
        hasher.update(data)
        hasher.update(str(time.time()).encode())
        return hasher.hexdigest()

    def encode_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Attach a resonance key and mirror metadata to the payload."""
        key = self.generate_resonance_key(payload)
        return {
            "glyph_id": key[:12],
            "mirror_origin": self.mirror_a.id,
            "mirror_target": self.mirror_b.id,
            "resonance_key": key,
            "payload": payload,
        }

    def to_graphviz(self) -> Optional[str]:
        """Return a Graphviz representation of the schema if possible."""
        if Digraph is None:
            return None
        dot = Digraph(comment="Mirror Linked Recursive Data Schema")
        dot.node(self.mirror_a.id, self.mirror_a.role)
        dot.node(self.mirror_b.id, self.mirror_b.role)
        dot.edge(self.mirror_a.id, self.mirror_b.id, label="forward-projection")
        dot.edge(self.mirror_b.id, self.mirror_a.id, label="inward-recursion")
        return dot.source


def demo() -> None:
    """Demonstrate encoding a payload and optionally print diagram."""
    schema = MLRDS()
    sample_payload = {"symbol": "\ud83c\df00", "intent": "Reflect/Upgrade"}
    encoded = schema.encode_payload(sample_payload)
    print("Encoded Payload:\n", json.dumps(encoded, indent=2))
    diagram = schema.to_graphviz()
    if diagram:
        print("\nGraphviz Diagram:\n", diagram)


if __name__ == "__main__":
    demo()

