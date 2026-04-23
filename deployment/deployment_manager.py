from core.base import CognitiveModule
import ray
@ray.remote
class DeploymentManager(CognitiveModule):
    def __init__(self, env=None, registry=None, version_manager=None, policy_loader=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.env = env
        self.registry = registry
        self.version_manager = version_manager
        self.policy_loader = policy_loader

    def deploy(self, agent_id, agent, metadata, version):
        self.registry.register(agent_id, metadata)
        self.version_manager.record_version(agent_id, version)
        self.env.launch_agent(agent_id, agent)

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass

        """Standard SGI message receiver."""
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "deployment_request":
            result = self.deploy(message['data']['agent_id'], message['data']['agent'], message['data']['metadata'], message['data']['version'])
            self.send_result("deployment_result", result)