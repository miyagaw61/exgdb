def fn(*args, addrs=None):
    print("args:", repr(args))
    print("addrs:", repr(addrs))

fn((0, 1, 2))
fn((0, 1, 2), ["A", "B", "C"])
fn(["A", "B", "C"])
