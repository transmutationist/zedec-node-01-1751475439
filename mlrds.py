import hashlib
import time
from dataclasses import dataclass, field


def r_hash(data: str) -> str:
    """Compute a recursive hash using SHA3-512 and a time pulse."""
    pulse = str(int(time.time() * 1000))
    hasher = hashlib.sha3_512()
    hasher.update((data + pulse).encode("utf-8"))
    return hasher.hexdigest()


@dataclass
class Mirror:
    """Representation of a mirror node."""

    identifier: str
    role: str
    direction: str
    storage: list[str] = field(default_factory=list)

    def emit(self, payload: str) -> tuple[str, str]:
        key = r_hash(payload)
        self.storage.append(payload)
        return payload, key

    def reflect(self, payload: str) -> str:
        """Return a transformed version of the payload."""
        reflected = f"reflected:{payload}"
        self.storage.append(reflected)
        return reflected


class MLRDS:
    """Mirror Linked Recursive Data Schema simulation."""

    def __init__(self):
        self.mirror_a = Mirror(
            identifier="MirrorA",
            role="Initiating Interface",
            direction="forward-projection",
        )
        self.mirror_b = Mirror(
            identifier="MirrorB",
            role="Archive & Reflector",
            direction="inward-recursion",
        )

    def send(self, data: str) -> dict:
        original, key = self.mirror_a.emit(data)
        reflected = self.mirror_b.reflect(original)
        reflected_key = r_hash(reflected)
        return {
            "glyph_id": key,
            "mirror_origin": self.mirror_a.identifier,
            "mirror_target": self.mirror_b.identifier,
            "resonance_key": reflected_key,
            "payload": reflected,
        }


if __name__ == "__main__":
    schema = MLRDS()
    result = schema.send("hello")
    print(result)
