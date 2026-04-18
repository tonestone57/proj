class DeploymentManager:
    def __init__(self, env, registry, version_manager, policy_loader):
        self.env = env
        self.registry = registry
        self.version_manager = version_manager
        self.policy_loader = policy_loader

    def deploy(self, agent_id, agent, metadata, version):
        self.registry.register(agent_id, metadata)
        self.version_manager.record_version(agent_id, version)
        self.env.launch_agent(agent_id, agent)
