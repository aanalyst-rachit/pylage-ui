from pylage.core.component import component
from pylage.core.tree import print_tree
from pylage.core.tree import collect_ids, count_components


def Heading(text):
    return component("Heading", text=text)


def Button(text, **props):
    return component("Button", text=text, **props)


def Column(*children):
    return component("Column", *children)


app = Column(
    Heading("Hello pylage"),
    "Plain text",
    Button("Click me", variant="primary"),
    None,
)

print("=== PYLAGE COMPONENT TREE ===")
print_tree(app)

print("\n=== COMPONENT IDS ===")
ids = collect_ids(app)

for item in ids:
    print(item)

print("\n=== COUNTS ===")
print("Components:", count_components(app))
print("Unique IDs:", len(set(ids)))
print("Children of root:", len(app.children))
