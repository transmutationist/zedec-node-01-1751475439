import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.mlrds_diagram import build_mlrds_graph

def test_graph_contains_nodes():
    g = build_mlrds_graph()
    src = g.source
    assert 'Mirror A' in src
    assert 'Mirror B' in src
