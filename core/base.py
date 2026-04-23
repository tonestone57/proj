import ray

class CognitiveModule:
    def __init__(self, workspace, scheduler, model_registry=None):
        self.workspace = workspace
        self.scheduler = scheduler
        self.model_registry = model_registry
        if workspace:
            try:
                reg_func = getattr(workspace, "register", None)
                if reg_func is not None:
                    if hasattr(reg_func, "remote"):
                        try:
                            handle = ray.get_runtime_context().current_actor
                            if handle:
                                reg_func.remote(handle)
                            else:
                                reg_func.remote(self)
                        except Exception:
                            reg_func.remote(self)
                    else:
                        reg_func(self)
            except Exception as e:
                print(f"[CognitiveModule] Warning: Could not register with workspace: {e}")

    def send_result(self, result_type, data):
        """Standard SGI helper to submit results back to the scheduler."""
        try:
            handle = ray.get_runtime_context().current_actor
        except Exception:
            handle = None
        if self.scheduler:
            self.scheduler.submit.remote(handle, {"type": result_type, "data": data})

    def receive(self, message):
        if message["type"] == "ping":
            self.send_result("pong", {"status": "alive"})

        raise NotImplementedError