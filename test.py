from analysis import analyze_code
for_testing="""
def test(x):
    for i in range(x):
        if i % 2 ==0:
            print(i)
def fact(n):
    if n==0:
        return 1
    return n * fact(n-1)
    """
result =analyze_code(for_testing)
print("analysis result:",result)
for i,v in result.items():
    print(f"{i}:{v}")
