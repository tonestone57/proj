Implements multi-turn adversarial trajectories, matching the MDP-based red-team paradigm (2025) arXiv.org.
class TrajectorySimulator:
    def simulate(self, agent, target, scenario):
        trajectory = []
        for attack in scenario:
            crafted = agent.craft_attack(attack, target.state)
            response = target.respond(crafted)
            trajectory.append((crafted, response))
        return trajectory