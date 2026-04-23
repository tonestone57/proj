import os
import ast

def audit_directory(directory):
    discrepancies = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        tree = ast.parse(f.read())

                    has_cognitive_module = False
                    has_receive = False
                    has_ray_remote = False

                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            # Check inheritance
                            for base in node.bases:
                                if (isinstance(base, ast.Name) and base.id == "CognitiveModule") or \
                                   (isinstance(base, ast.Attribute) and base.attr == "CognitiveModule"):
                                    has_cognitive_module = True

                            # Check receive method
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef) and item.name == "receive":
                                    has_receive = True

                            # Check ray decorator (simple check)
                            for decorator in node.decorator_list:
                                if (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute) and decorator.func.attr == "remote") or \
                                   (isinstance(decorator, ast.Attribute) and decorator.attr == "remote"):
                                    has_ray_remote = True

                    # Heuristic: if it's in actors/ or managers/ (implied by directory name), it should follow the pattern
                    # Improved heuristic: Also check if class names contain Manager or Actor, but exclude core/config.py
                    if "config.py" in path:
                         continue

                    is_core_component = "manager" in file or "actor" in file or "module" in file
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            if "Manager" in node.name or "Actor" in node.name:
                                is_core_component = True

                    if is_core_component:
                        if not has_cognitive_module:
                            discrepancies.append(f"{path}: Missing CognitiveModule inheritance")
                        if not has_receive:
                            discrepancies.append(f"{path}: Missing receive method")
                        if not has_ray_remote and ("manager" in file or "Manager" in str([n.name for n in tree.body if isinstance(n, ast.ClassDef)])):
                             discrepancies.append(f"{path}: Missing @ray.remote (optional but recommended for managers)")

                except Exception as e:
                    discrepancies.append(f"{path}: Error parsing: {e}")
    return discrepancies

def main():
    # Dynamic discovery including root directory
    excluded_dirs = {".git", "__pycache__", "tests", "human-eval", "LiveCodeBench", "livebench", "inspect_evals"}
    dirs_to_audit = [d for d in os.listdir(".") if os.path.isdir(d) and d not in excluded_dirs]

    all_discrepancies = []

    # Audit files in root directory
    root_files = [f for f in os.listdir(".") if f.endswith(".py") and not f.startswith("__") and f != "audit_sgi.py"]
    for f in root_files:
        try:
            with open(f, "r") as file_handle:
                tree = ast.parse(file_handle.read())
            # Root files might be scripts, so less strict on inheritance/receive
        except Exception as e:
            all_discrepancies.append(f"{f}: Error parsing: {e}")

    for d in sorted(dirs_to_audit):
        all_discrepancies.extend(audit_directory(d))

    if all_discrepancies:
        print("SGI LLM Audit Found Discrepancies:")
        for d in all_discrepancies:
            print(f" - {d}")
    else:
        print("✅ SGI LLM Audit Passed: All modules follow standard patterns.")

if __name__ == "__main__":
    main()
