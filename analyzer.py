from radon.complexity import cc_visit
import ast

def analyze_code(code):
    #radon
    complexity_blocks = cc_visit(code)
    total_complexity = sum(block.complexity for block in complexity_blocks)
    num_functions = len(complexity_blocks)
    loc = len(code.splitlines())

    #ast
    tree = ast.parse(code)
    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.estimate_complexity()

    total_loops = analyzer.loop_count
    recursion = analyzer.recursion_count > 0
    time_complexity = analyzer.time_complexity

    #dummy values
    workload = (total_complexity * 1.5 + total_loops * 3 + loc * 0.05 + analyzer.max_loop_depth * 5)

    energy_e = workload * 0.01
    carbon_e = energy_e * 0.475

    #scoring sys
    complexity_penalty = total_complexity * 2
    loop_penalty = analyzer.max_loop_depth * 10
    recursion_penalty = 20 if analyzer.recursion_count > 1 else (10 if recursion else 0)
    loc_penalty = loc * 0.1

    raw_score = 100 - (complexity_penalty +loop_penalty +recursion_penalty + loc_penalty)

    efficiency_score = max(0, min(100, round(raw_score, 2)))

    return {
        "cyclomatic_complexity": total_complexity,
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
    