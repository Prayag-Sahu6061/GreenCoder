
from radon.complexity import cc_visit
import re
def analyze_code(code:str):
    complexity_blocks = cc_visit(code)
    total_complexity=sum(block.complexity for block in complexity_blocks)
    num_functions = len(complexity_blocks)
    loc=len(code.splitlines())

    for_loops=len(re.findall(r'\bfor\b',code))
    while_loops=len(re.findall(r'\bwhile\b',code)) 
    total_loops = for_loops + while_loops
    recursion=False 
    for block in complexity_blocks:
        pattern=rf"\b{block.name}\s*\("
        matches=re.findall(pattern,code) 
        if len(matches)>1:
            recursion=True
            break
        workload=(total_complexity*1.5)+(total_loops*2)+(loc*0.05) 
        energy_e=workload*0.01
        carbon_e=energy_e*0.475
        complexity_penalty=total_complexity *2
        loop_penalty=total_loops *4
        recursion_penalty=5 if recursion else 0
        loc_penalty=loc *0.1
        raw_score=100-(complexity_penalty+loop_penalty+recursion_penalty+loc_penalty)
        efficiency_score=max(0,min(100,round(raw_score,2)))
        return {
            "complexity":total_complexity,
            "functions":num_functions,
            "lines of codes":loc,
            "loops detected":total_loops,
            "recursion detected":recursion,
            "energy estimation":round(energy_e,4),
            "carbon estimation":round(carbon_e,4),
            "efficiency score":efficiency_score
        }
    
