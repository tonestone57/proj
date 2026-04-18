class EcosystemSimulator:
    def simulate(self, agents, scenario_engine):
        results = {}
        for agent in agents:
            scenario = scenario_engine.get_scenario("policy_evasion")
            results[agent.id] = scenario
        return results
