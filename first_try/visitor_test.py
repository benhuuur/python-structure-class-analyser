import ast

class MyVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f'Function definition: {node.name}')
        self.generic_visit(node)

    def visit_Assign(self, node):
        print('Assignment:')
        for target in node.targets:
            if isinstance(target, ast.Name):
                print(f'  {target.id} = ...')
        self.generic_visit(node)

    def visit_Num(self, node):
        print(f'Number constant: {node.n}')
        self.generic_visit(node)

# Exemplo de código para análise
code = """
def add(a, b):
    result = a + b
    return result
"""

# Analisar o código fonte em um AST
tree = ast.parse(code)

# Criar uma instância do visitor e visitar o AST
visitor = MyVisitor()
visitor.visit(tree)
