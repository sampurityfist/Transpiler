import Ast

SHORT_NAMES = {
    'PROGRAM':    'PROG',
    'FUNCTION':   'FUNC',
    'RETURN':     'RET',
    'ASSIGNMENT': 'ASSIGN',
    'VARIABLE':   'VAR',
    'NUMBER':     'NUM',
    'OPERATOR':   'OP',
    'IF':         'IF',
    'WHILE':      'WHILE',
    'FOR':        'FOR',
    'OUTPUT':     'OUT',
    'INPUT':      'IN',
    'CALL':       'CALL',
    'CALL_EXPR':  'CALL_E',
    'ARRAY_DECL': 'ARR_D',
    'ARRAY_SET':  'ARR_S',
    'ARRAY_GET':  'ARR_G',
}

def shorten(node_type):
    return SHORT_NAMES.get(node_type.upper(), node_type.upper())


def visualizeText(ast, indent=0):
    lines = []
    prefix = "  " * indent

    if isinstance(ast, list):
        for node in ast:
            lines.extend(visualizeText(node, indent))
        return lines

    if ast is None:
        return [prefix + "(empty)"]

    label = shorten(ast.type)
    if ast.value is not None:
        label += f"  [{ast.value}]"

    lines.append(prefix + label)

    for child in ast.children:
        if isinstance(child, list):
            for item in child:
                lines.extend(visualizeText(item, indent + 1))
        elif child is not None:
            lines.extend(visualizeText(child, indent + 1))

    return lines


def visualizeGraph(ast):
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("Install matplotlib: pip install matplotlib")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_axis_off()
    ax.set_title("Abstract Syntax Tree", fontsize=14, pad=16)

    positions = {}
    labels = {}
    edges = []
    counter = [0]

    node_list = []
    id_map = {}

    def collect(node, depth, parent_id):
        if node is None:
            return

        uid = counter[0]
        counter[0] += 1
        id_map[id(node)] = uid

        label = shorten(node.type)
        if node.value is not None:
            label += f"\n{node.value}"
        labels[uid] = label
        node_list.append((node, depth, uid))

        if parent_id is not None:
            edges.append((parent_id, uid))

        for child in node.children:
            if isinstance(child, list):
                for item in child:
                    if item is not None:
                        collect(item, depth + 1, uid)
            elif child is not None:
                collect(child, depth + 1, uid)

    if isinstance(ast, list):
        root_id = counter[0]
        counter[0] += 1
        labels[root_id] = "PROG"
        node_list.append((None, 0, root_id))
        for stmt in ast:
            collect(stmt, 1, root_id)
    else:
        collect(ast, 0, None)

    depth_groups = {}
    for (node, depth, uid) in node_list:
        depth_groups.setdefault(depth, []).append(uid)

    for depth, uids in depth_groups.items():
        for i, uid in enumerate(uids):
            positions[uid] = (i * 2.0 - len(uids), -depth * 1.5)

    # Draw edges
    for (p, c) in edges:
        if p in positions and c in positions:
            px, py = positions[p]
            cx, cy = positions[c]
            ax.plot([px, cx], [py, cy], 'k-', lw=0.8, alpha=0.4, zorder=1)

    color_map = {
        'PROG':    '#cfcfcf',
        'FUNC':    '#ffb7b2',
        'RET':     '#ffdac1',
        'ASSIGN':  '#a8d8ea',
        'VAR':     '#e8e8e8',
        'NUM':     '#f0f0f0',
        'OP':      '#ffe0ac',
        'IF':      '#ffd3b6',
        'WHILE':   '#d4e6b5',
        'FOR':     '#b5ead7',
        'OUT':     '#cdb4db',
        'IN':      '#bee5eb',
        'CALL':    '#e2f0cb',
        'CALL_E':  '#c7ceea',
        'ARR_D':   '#f8c8d4',
        'ARR_S':   '#dfe7fd',
        'ARR_G':   '#d4e4bc',
    }

    for uid, (x, y) in positions.items():
        label = labels.get(uid, '?')
        node_type = label.split('\n')[0]
        color = color_map.get(node_type, '#e8e8e8')

        circle = plt.Circle((x, y), 0.45, color=color, ec='#888', lw=0.8, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=6.5, zorder=3, wrap=True,
                multialignment='center')

    if positions:
        all_x = [p[0] for p in positions.values()]
        all_y = [p[1] for p in positions.values()]
        ax.set_xlim(min(all_x) - 1.5, max(all_x) + 1.5)
        ax.set_ylim(min(all_y) - 1.5, max(all_y) + 1.5)

    plt.tight_layout()
    plt.show()