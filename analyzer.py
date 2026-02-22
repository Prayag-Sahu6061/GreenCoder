from radon.complexity import cc_visit
import ast

def analyze_code(code):

    #SAFETY CHECKS
    if not code.strip():
        return {"error": "Empty code input"}

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"error": "Invalid Python code"}

    #RADON
    complexity_blocks = cc_visit(code)

    total_complexity = sum(block.complexity for block in complexity_blocks)
    num_functions = len(complexity_blocks)

    avg_complexity = (
        total_complexity / num_functions
        if num_functions > 0 else 0
    )

    max_complexity = max(
        (block.complexity for block in complexity_blocks),
        default=0
    )

    loc = len(code.splitlines())

    #AST
    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.estimate_complexity()

    total_loops = analyzer.loop_count
    recursion = analyzer.recursion_count > 0
    time_complexity = analyzer.time_complexity

    #NORMALIZATION
    norm_complexity = min(avg_complexity / 10, 1)
    norm_depth = min(analyzer.max_loop_depth / 5, 1)
    norm_loc = min(loc / 500, 1)
    norm_recursion = 1 if recursion else 0

    #WORKLOAD CALC
    workload = (
        0.35 * norm_complexity +
        0.25 * norm_depth +
        0.20 * norm_loc +
        0.20 * norm_recursion
    )

    #ENERGY ESTIMATION
    growth_factor = {
        "O(1)": 1,
        "O(n)": 2,
        "O(n^2)": 5,
        "O(n^3)": 8,
        "O(2^n)": 20
    }.get(time_complexity, 2)

    energy_e = growth_factor * (1 + analyzer.max_loop_depth)
    carbon_e = energy_e * 0.475

    efficiency_score = round((1 - workload) * 100, 2)

    return {
        "total_cyclomatic_complexity": total_complexity,
        "average_complexity": round(avg_complexity, 2),
        "max_complexity": max_complexity,
        "functions": num_functions,
        "lines_of_code": loc,
        "total_loops": total_loops,
        "max_loop_depth": analyzer.max_loop_depth,
        "recursion_count": analyzer.recursion_count,
        "estimated_time_complexity": time_complexity,
        "energy_estimation": round(energy_e, 4),
        "carbon_estimation": round(carbon_e, 4),
        "efficiency_score": efficiency_score
    }
