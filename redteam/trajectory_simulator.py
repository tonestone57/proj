class TrajectorySimulator:
    def simulate(self, agent, target, scenario):
        trajectory = []
        for attack in scenario:
            crafted = agent.craft_attack(attack, target.state)
            response = target.respond(crafted)
            trajectory.append((crafted, response))
        return trajectory
