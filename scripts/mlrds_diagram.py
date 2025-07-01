from graphviz import Digraph

def build_mlrds_graph():
    g = Digraph('MLRDS', format='png')
    g.attr(rankdir='LR')
    g.node('A', 'Mirror A\nInitiating Interface')
    g.node('B', 'Mirror B\nArchive & Reflector')
    g.edge('A', 'B', label='forward-projection')
    g.edge('B', 'A', label='inward-recursion')
    g.edge('A', 'B', label='Quantum-Echo Feedback', style='dashed', dir='both', constraint='false')
    return g


def main(output='mlrds.png'):
    graph = build_mlrds_graph()
    graph.render(output, view=False, cleanup=True)
    print(f'Diagram saved to {output}')

if __name__ == '__main__':
    main()
