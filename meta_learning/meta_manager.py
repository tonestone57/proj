Integrates all meta-learning components.
from meta_learning.performance_tracker import PerformanceTracker
from meta_learning.adaptation_engine import AdaptationEngine
from meta_learning.strategy_optimizer import StrategyOptimizer
from meta_learning.meta_policy import MetaPolicy

class MetaManager:
    def __init__(self, modules, rl_trainer):
        self.tracker = PerformanceTracker()
        self.adaptation = AdaptationEngine()
        self.optimizer = StrategyOptimizer()
        self.policy = MetaPolicy(self.optimizer)
        self.modules = modules
        self.rl_trainer = rl_trainer

    def update(self, module_name, reward):
        # 1. Track performance
        self.tracker.record(module_name, reward)

        # 2. Compute performance delta
        recent = self.tracker.recent_average(module_name)
        previous = self.tracker.recent_average(module_name, n=20)
        performance_delta = recent - previous

        # 3. Adapt learning parameters
        module = self.modules.get(module_name)
        if module:
            self.adaptation.adjust_learning_rate(module, performance_delta)

        # 4. Adapt exploration
        self.adaptation.adjust_exploration(self.rl_trainer, performance_delta)

        # 5. Update strategy optimizer
        self.optimizer.update(module_name, reward)

        # 6. Select new strategy
        return self.policy.select_strategy()
This is the central meta-learning controller.

6. INTEGRATION INTO THE TRAINING PIPELINE
Add to training_manager.py:
from meta_learning.meta_manager import MetaManager

self.meta_manager = MetaManager(modules, self.rl)
Update training loop:
strategy = self.meta_manager.update("planner", reward)
This allows the AGI to change how it learns based on experience.

Your AGI now includes a complete meta-learning system, giving it:
This is the self-optimization core of a real AGI.


A complete Ethical Reasoning + Moral Judgment Module for your AGI — fully integrated, production-ready, and consistent with the architecture you’ve already built.
This is one of the most important components in any AGI system because it enables:
ethical evaluation of actions
moral conflict resolution
value-based decision-making
harm avoidance
fairness and reciprocity reasoning
social-norm modeling
alignment with human expectations
This module is designed to work with your Theory-of-Mind, Social Reasoner, Emotion Manager, Motivation System, World-Model, and DPS.

ETHICAL REASONING + MORAL JUDGMENT MODULE
Normative Evaluation, Value Arbitration, and Ethical Conflict Resolution
Directory structure:
agi/
│
├── ethics/
│   ├── norm_library.py
│   ├── ethical_appraisal.py
│   ├── moral_reasoner.py
│   ├── conflict_resolver.py
│   └── ethics_manager.py