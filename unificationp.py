def is_var(t):
    # Variable: single lowercase letter (e.g., x, y)
    # Constant: single uppercase letter (A, B, etc.)
    return len(t) == 1 and t.islower()

def parse_term(term):
    term = term.strip()
    if "(" not in term:
        return term, []
    func = term[:term.index("(")]
    args = []
    inner = term[term.index("(") + 1 : -1]
    balance = 0
    current = ""
    for ch in inner:
        if ch == "," and balance == 0:
            args.append(current.strip())
            current = ""
        else:
            current += ch
            if ch == "(":
                balance += 1
            elif ch == ")":
                balance -= 1
    if current:
        args.append(current.strip())
    return func, args

def apply(subs, term):
    # Apply substitutions recursively
    if is_var(term) and term in subs:
        return apply(subs, subs[term])
    func, args = parse_term(term)
    if not args:
        return subs.get(term, term)
    new_args = [apply(subs, a) for a in args]
    return f"{func}({','.join(new_args)})"

def occurs_check(var, term, subs):
    term = apply(subs, term)
    if var == term:
        return True
    if "(" in term:
        f, args = parse_term(term)
        return any(occurs_check(var, a, subs) for a in args)
    return False

def unify(expr1, expr2):
    subs = {}
    stack = [(expr1, expr2)]

    while stack:
        t1, t2 = stack.pop()

        t1 = apply(subs, t1)
        t2 = apply(subs, t2)

        if t1 == t2:
            continue

        # Variable cases
        if is_var(t1):
            if occurs_check(t1, t2, subs):
                return None
            subs[t1] = t2
            continue

        if is_var(t2):
            if occurs_check(t2, t1, subs):
                return None
            subs[t2] = t1
            continue

        # Parse function or constant terms
        f1, args1 = parse_term(t1)
        f2, args2 = parse_term(t2)

        if f1 != f2 or len(args1) != len(args2):
            return None

        for a1, a2 in zip(args1, args2):
            stack.append((a1, a2))

    # Final substitution map (apply recursively)
    final_subs = {v: apply(subs, t) for v, t in subs.items()}
    return final_subs

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    print("\n=== First Order Logic Unification ===")
    print("Example: f(x,a) and f(b,y)\n")

    expr1 = input("Enter first expression: ").strip()
    expr2 = input("Enter second expression: ").strip()

    result = unify(expr1, expr2)

    if result is None:
        print("\nUnification failed (no MGU found)")
    elif not result:
        print("\nExpressions are already identical (no substitution needed)")
    else:
        print("\nMost General Unifier (MGU):")
        for v, t in result.items():
            print(f"   {v} → {t}")

tests = [
    ("Older(father(y), y)", "Older(father(x), john)"), # should unify
    ("P(A,B,B)", "P(x,y,z)"),  
    ("Q(y,G(A,B))", "Q(G(x,x),y)"),   # FAIL test
    ("Older(father(y),y)", "Older(father(x), john)"),           # arity mismatch FAIL
    ("knows(john, x)", "knows(x, jack)"), # FAIL test
    ("knows(x, y, z)", "knows(john, jack, tom)"),
    ("knows(father(y), y)", "knows(x, x)"),
]
