import yaml
from graphviz import Digraph


def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def build_graph(schema):
    g = Digraph('MLRDS', format='svg')
    g.attr(rankdir='LR')

    mirrors = {m['id']: m for m in schema['MLRDS']['mirrors']}

    # Add mirror nodes
    for m_id, m_data in mirrors.items():
        label = f"{m_id}\n{m_data['role']}"
        g.node(m_id, label=label, shape='rectangle', style='filled', fillcolor='lightblue')

    # Add edges for primary flow
    g.edge('MirrorA', 'MirrorB', label='forward-projection')
    g.edge('MirrorB', 'MirrorA', label='inward-recursion')

    # Bridge node
    bridge = schema['MLRDS'].get('bridge', {})
    if bridge:
        b_label = bridge.get('type', 'Bridge')
        g.node('Bridge', b_label, shape='diamond', style='filled', fillcolor='lightgrey')
        g.edge('MirrorA', 'Bridge')
        g.edge('Bridge', 'MirrorB')

    return g


def main():
    schema = load_schema('mirror_schema.yaml')
    g = build_graph(schema)
    g.render('mirror_schema', cleanup=True)
    print('Diagram generated as mirror_schema.svg')


if __name__ == '__main__':
    main()
