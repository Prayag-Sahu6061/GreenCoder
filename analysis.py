import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.loop_count = 0
        self.max_loop_depth = 0
        self.current_loop_depth = 0
        self.recursion_count = 0
        self.function_stack = []
        self.time_complexity = "O(1)"

    # -------- LOOP DETECTION --------
    def visit_For(self, node):
        self.loop_count += 1
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node):
        self.loop_count += 1
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    # -------- FUNCTION TRACKING --------
    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    # -------- RECURSION DETECTION --------
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.function_stack:
                self.recursion_count += 1
        self.generic_visit(node)

    # -------- TIME COMPLEXITY ESTIMATION --------
    def estimate_complexity(self):
        if self.max_loop_depth == 0:
            self.time_complexity = "O(1)"
        elif self.max_loop_depth == 1:
            self.time_complexity = "O(n)"
        elif self.max_loop_depth == 2:
            self.time_complexity = "O(n^2)"
        elif self.max_loop_depth >= 3:
            self.time_complexity = "O(n^3)"