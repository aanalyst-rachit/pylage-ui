from pylage.core.state import State


print("=== PYLAGE STATE TEST ===")

count = State(0)

print("Initial:", count.value)


def listener(old, new):
    print(f"Changed: {old} -> {new}")


unsubscribe = count.subscribe(listener)

count.set(1)
count.set(2)
count.set(2)

print("Current:", count.value)

unsubscribe()

count.set(3)

print("After unsubscribe:", count.value)
