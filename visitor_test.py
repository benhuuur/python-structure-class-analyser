import ast
from pprint import pprint

class AwaitVisitor(ast.NodeVisitor):
    def visit_Await(self, node):
        print('Node type: Await\nFields: ', node._fields)
        self.generic_visit(node)

    def visit_Call(self,node):
        print('Node type: Call\nFields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self,node):
        print('Node type: Name\nFields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)


visitor = AwaitVisitor()
tree = ast.parse("""
async def someFunc():
  await other_func()
""")
pprint(ast.dump(tree))
visitor.visit(tree)