
val = ["string", "10", "0.5", 19, 0.5]
for v in val:
    try:
        if not v.is_integer():
            print("float", float(v))
        
    except AttributeError:
        try:
            if v.isnumeric():
                print("int_str", int(v))
            else:
                try:
                    v = float(v)
                    print("float_str", float(v))
                except ValueError:
                    print("str", str(v))
        except AttributeError:
            print("int", v )
