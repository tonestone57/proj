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
                    if "manager" in file or "actor" in file or "module" in file:
                        if not has_cognitive_module:
                            discrepancies.append(f"{path}: Missing CognitiveModule inheritance")
                        if not has_receive:
                            discrepancies.append(f"{path}: Missing receive method")
                        if not has_ray_remote and "manager" in file:
                             discrepancies.append(f"{path}: Missing @ray.remote (optional but recommended for managers)")

                except Exception as e:
                    discrepancies.append(f"{path}: Error parsing: {e}")
    return discrepancies

def main():
    dirs_to_audit = [
        "actors", "blueteam", "cee_layer", "conflict_resolution", "deployment",
        "economics", "emotion", "incident_response", "institutional_ai",
        "memory", "memory_consolidation", "meta_learning", "metacognition",
        "monitoring", "motivation", "negotiation", "orchestration", "purpleteam",
        "redteam", "safety_ethics", "simulation", "training", "world_model"
    ]

    all_discrepancies = []
    for d in dirs_to_audit:
        if os.path.exists(d):
            all_discrepancies.extend(audit_directory(d))

    if all_discrepancies:
        print("SGI LLM Audit Found Discrepancies:")
        for d in all_discrepancies:
            print(f" - {d}")
    else:
        print("✅ SGI LLM Audit Passed: All modules follow standard patterns.")

if __name__ == "__main__":
    main()
