import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.recursion_count = 0
        self.nested_loops_count = 0
        self.loop_count = 0

        self.current_loop_depth = 0
        self.max_loop_depth = 0

        self.current_function = None
        self.function_lengths = []

        self.time_complexity = "n" #input data size

    #Detect For loops
    def visit_For(self, node):
        self.loop_count += 1
        self.current_loop_depth += 1

        if self.current_loop_depth > 1:
            self.nested_loops_count += 1

        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        #this is to enter into child nodes if they exist
        self.generic_visit(node)
        self.current_loop_depth -= 1

    #Detect While loops
    def visit_While(self, node):
        self.visit_For(node)  

    #detect Function definitions
    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.function_lengths.append(len(node.body))
        self.generic_visit(node)
        self.current_function = None

    #detect recursion
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == self.current_function:
                self.recursion_count += 1
        self.generic_visit(node)
    
    def estimate_complexity(self):
        if self.recursion_count > 1:
            self.time_complexity = "".join("2^n")
        if self.max_loop_depth == 1:
            self.time_complexity = "n"
        elif self.max_loop_depth = 2:
            self.time_complexity = "".join("n^2")
        elif self.max_loop_depth = 3:
            self.time_complexity = "".join("n^3")
        elif self.max_loop_depth > 3:
            self.time_complexity = "".join("n^k")
        
        
        