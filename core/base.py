import ray

class CognitiveModule:
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        if workspace:
            try:
                # Use getattr to safely check for the register method on a Ray ActorHandle or local object
                reg_func = getattr(workspace, "register", None)
                if reg_func is not None:
                    # Ray ActorMethods have a .remote attribute
                    if hasattr(reg_func, "remote"):
                        try:
                            # Pass the handle, not 'self', to avoid copying the object instance
                            handle = ray.get_runtime_context().current_actor
                            if handle:
                                reg_func.remote(handle)
                            else:
                                reg_func.remote(self)
                        except Exception:
                            reg_func.remote(self)
                    else:
                        # Local synchronous call
                        reg_func(self)
            except Exception as e:
                print(f"[CognitiveModule] Warning: Could not register with workspace: {e}")

    def receive(self, message):
        raise NotImplementedError
