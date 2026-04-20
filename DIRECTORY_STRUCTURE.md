# SGI-Alpha Complete Directory Structure and Integration Map

This document lists every file in the repository, its purpose, and how it integrates into the LLM-driven SGI architecture.

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| AGENTS.md | SGI Roadmap: i7-8265U Optimized | Utility/Component |
| README.md | SGI-Alpha: AGI LLM for Coding, Math and Logic | Utility/Component |
| compilation_errors.log | Log file tracking compilation errors. | Utility/Component |
| config.yaml | Central configuration manifest for system-wide thresholds and hardware limits. | Utility/Component |
| find_invalid_py.py | Implements core logic for Find Invalid Py functionality. | Utility/Component |
| hardware_verification.log | Log file tracking hardware verification. | Utility/Component |
| main.py | Proactive RAM Guard to prevent swap lag and system crash. | Class/Logic Component |
| setup_8265u.sh | Authoritative setup process for Intel i5-8265U (SGI Standard) | Utility/Component |

## Actors (`actors/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | Specialized cognitive agent for specific domain tasks. | Ray Actor (LLM Interface) |
| actors/critic_actor.py | Specialized cognitive agent for specific domain tasks. | Ray Actor (LLM Interface) |
| actors/planner.py | SGI 2026: Intelligent task decomposition via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/reasoner_actor.py | Specialized cognitive agent for specific domain tasks. | Ray Actor (LLM Interface) |
| actors/search_actor.py | Specialized cognitive agent for specific domain tasks. | Ray Actor (LLM Interface) |
| actors/self_model.py | Implements core logic for Self Model functionality. | Cognitive Actor (LLM-Integrated) |
| actors/social/discourse.py | Placeholder pragmatic inference | Cognitive Actor (LLM-Integrated) |
| actors/social/social_reasoner.py | Retrieve recent interactions from episodic memory | Ray Actor (LLM Interface) |
| actors/social/theory_of_mind.py | SGI 2026: Complex intention inference via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/vision.py | Implementation of NeuralLVC / CoPE for Video/Vision data. | Cognitive Actor (LLM-Integrated) |

## Blueteam (`blueteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Implements core logic for Adaptive Defense Agent functionality. | Class/Logic Component |
| blueteam/blueteam_manager.py | Orchestrates sub-components within the blueteam module. | Class/Logic Component |
| blueteam/cyber_range.py | Implements core logic for Cyber Range functionality. | Class/Logic Component |
| blueteam/deception_layer.py | Implements core logic for Deception Layer functionality. | Class/Logic Component |
| blueteam/defense_orchestrator.py | Implements core logic for Defense Orchestrator functionality. | Class/Logic Component |
| blueteam/detection_engine.py | Implements core logic for Detection Engine functionality. | Class/Logic Component |
| blueteam/dlp_agent.py | Implements core logic for Dlp Agent functionality. | Class/Logic Component |
| blueteam/firewall_agent.py | Implements core logic for Firewall Agent functionality. | Class/Logic Component |
| blueteam/forensic_agent.py | Implements core logic for Forensic Agent functionality. | Class/Logic Component |

## Cee Layer (`cee_layer/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestrates sub-components within the cee_layer module. | Class/Logic Component |
| cee_layer/cognitive_affective_bridge.py | Implements core logic for Cognitive Affective Bridge functionality. | Class/Logic Component |
| cee_layer/emotion_appraisal.py | Implements core logic for Emotion Appraisal functionality. | Class/Logic Component |
| cee_layer/emotion_generator.py | Implements core logic for Emotion Generator functionality. | Class/Logic Component |
| cee_layer/emotion_regulator.py | Implements core logic for Emotion Regulator functionality. | Class/Logic Component |
| cee_layer/ethical_evaluator.py | Implements core logic for Ethical Evaluator functionality. | Class/Logic Component |
| cee_layer/moral_weighting.py | Implements core logic for Moral Weighting functionality. | Class/Logic Component |

## Conflict Resolution (`conflict_resolution/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestrates sub-components within the conflict_resolution module. | Class/Logic Component |
| conflict_resolution/contradiction_detector.py | Implements core logic for Contradiction Detector functionality. | Class/Logic Component |
| conflict_resolution/ethical_appraisal.py | Implements core logic for Ethical Appraisal functionality. | Class/Logic Component |
| conflict_resolution/moral_agents.py | Implements core logic for Moral Agents functionality. | Class/Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Implements core logic for Probabilistic Reasoner functionality. | Class/Logic Component |
| conflict_resolution/resolution_protocol.py | Implements core logic for Resolution Protocol functionality. | Class/Logic Component |
| conflict_resolution/survivability_engine.py | Implements core logic for Survivability Engine functionality. | Class/Logic Component |
| conflict_resolution/value_arbitration.py | Implements core logic for Value Arbitration functionality. | Class/Logic Component |

## Console (`console/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Implements core logic for Action Queue functionality. | Class/Logic Component |
| console/approval_gateway.py | Implements core logic for Approval Gateway functionality. | Class/Logic Component |
| console/audit_log.py | Implements core logic for Audit Log functionality. | Class/Logic Component |
| console/confidence_monitor.py | Implements core logic for Confidence Monitor functionality. | Class/Logic Component |
| console/console_manager.py | Orchestrates sub-components within the console module. | Class/Logic Component |
| console/escalation_engine.py | Implements core logic for Escalation Engine functionality. | Class/Logic Component |
| console/human_interface.py | Placeholder for UI integration | Class/Logic Component |
| console/oversight_dashboard.py | Implements core logic for Oversight Dashboard functionality. | Class/Logic Component |

## Core (`core/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Implements core logic for Base functionality. | Cognitive Actor (LLM-Integrated) |
| core/config.py | Dynamic configuration loader for parsing and validating config settings. | Utility/Component |
| core/controller.py | Tracks pulse-active modules. | Class/Logic Component |
| core/drives.py | Calculates the entropy of the system state based on message history. | Class/Logic Component |
| core/heartbeat.py | High uncertainty: The agent is "confused" or facing a new problem | Class/Logic Component |
| core/message_bus/fast_path.py | Simulates Flash-Optimized LZ4 compression for Tier 1 (Ephemeral) storage. | Class/Logic Component |
| core/message_bus/priority_engine.py | Time-sensitive messages get higher priority | Class/Logic Component |
| core/message_bus/router.py | Example routing logic | Class/Logic Component |
| core/model_registry.py | Singleton Model Provider to prevent RAM crash on 16GB systems. | Ray Actor (LLM Interface) |
| core/scheduler.py | Use counter as a tie-breaker to avoid comparing modules | Ray Actor (LLM Interface) |
| core/workspace.py | Keep history manageable using centralized config | Ray Actor (LLM Interface) |

## Deployment (`deployment/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Implements core logic for Agent Registry functionality. | Class/Logic Component |
| deployment/deployment_manager.py | Orchestrates sub-components within the deployment module. | Class/Logic Component |
| deployment/policy_loader.py | Implements core logic for Policy Loader functionality. | Class/Logic Component |
| deployment/runtime_env.py | Implements core logic for Runtime Env functionality. | Class/Logic Component |
| deployment/version_manager.py | Orchestrates sub-components within the deployment module. | Class/Logic Component |

## Economics (`economics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Implements core logic for Agent Policy functionality. | Class/Logic Component |
| economics/context_engine.py | Implements core logic for Context Engine functionality. | Class/Logic Component |
| economics/coordination_protocol.py | Implements core logic for Coordination Protocol functionality. | Class/Logic Component |
| economics/economic_manager.py | Orchestrates sub-components within the economics module. | Class/Logic Component |
| economics/fairness_engine.py | Implements core logic for Fairness Engine functionality. | Class/Logic Component |
| economics/optimizer.py | Implements core logic for Optimizer functionality. | Class/Logic Component |
| economics/orchestration_layer.py | Implements core logic for Orchestration Layer functionality. | Class/Logic Component |
| economics/resource_model.py | Implements core logic for Resource Model functionality. | Class/Logic Component |
| economics/utility_engine.py | Implements core logic for Utility Engine functionality. | Class/Logic Component |

## Emotion (`emotion/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Example reasoning logic | Class/Logic Component |
| emotion/affective_state.py | Simple affective dynamics | Class/Logic Component |
| emotion/appraisal.py | Implements core logic for Appraisal functionality. | Class/Logic Component |
| emotion/emotion_manager.py | Orchestrates sub-components within the emotion module. | Class/Logic Component |

## Incident Response (`incident_response/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Implements core logic for Audit Logger functionality. | Class/Logic Component |
| incident_response/containment_engine.py | Implements core logic for Containment Engine functionality. | Class/Logic Component |
| incident_response/detectors.py | Implements core logic for Detectors functionality. | Class/Logic Component |
| incident_response/eradication_engine.py | Implements core logic for Eradication Engine functionality. | Class/Logic Component |
| incident_response/incident_classifier.py | Implements core logic for Incident Classifier functionality. | Class/Logic Component |
| incident_response/incident_manager.py | Orchestrates sub-components within the incident_response module. | Class/Logic Component |
| incident_response/recovery_engine.py | Implements core logic for Recovery Engine functionality. | Class/Logic Component |
| incident_response/semantic_checks.py | Implements core logic for Semantic Checks functionality. | Class/Logic Component |

## Institutional Ai (`institutional_ai/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Implements core logic for Coordination Layer functionality. | Class/Logic Component |
| institutional_ai/governance_graph.py | Implements core logic for Governance Graph functionality. | Class/Logic Component |
| institutional_ai/incentive_engine.py | Implements core logic for Incentive Engine functionality. | Class/Logic Component |
| institutional_ai/institutional_manager.py | Orchestrates sub-components within the institutional_ai module. | Class/Logic Component |
| institutional_ai/oversight_agents.py | Implements core logic for Oversight Agents functionality. | Class/Logic Component |
| institutional_ai/real_time_control.py | Implements core logic for Real Time Control functionality. | Class/Logic Component |
| institutional_ai/role_definitions.py | Implements core logic for Role Definitions functionality. | Class/Logic Component |
| institutional_ai/rule_engine.py | Implements core logic for Rule Engine functionality. | Class/Logic Component |
| institutional_ai/sanction_engine.py | Implements core logic for Sanction Engine functionality. | Class/Logic Component |
| institutional_ai/trust_engine.py | Implements core logic for Trust Engine functionality. | Class/Logic Component |

## Memory (`memory/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implementation of LLM-Arithmetic Coding for Deep Archive. | Cognitive Actor (LLM-Integrated) |
| memory/memory_manager.py | Orchestrates sub-components within the memory module. | Ray Actor (LLM Interface) |
| memory/scratchpad.py | Implements core logic for Scratchpad functionality. | Class/Logic Component |
| memory/short_term/episodic_memory.py | Implements core logic for Episodic Memory functionality. | Class/Logic Component |

## Memory Consolidation (`memory_consolidation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestrates sub-components within the memory_consolidation module. | Class/Logic Component |
| memory_consolidation/consolidation_scheduler.py | Implements core logic for Consolidation Scheduler functionality. | Class/Logic Component |
| memory_consolidation/generative_trainer.py | Implements core logic for Generative Trainer functionality. | Class/Logic Component |
| memory_consolidation/hippocampal_replay.py | Simple sequential replay | Class/Logic Component |
| memory_consolidation/schema_manager.py | Orchestrates sub-components within the memory_consolidation module. | Class/Logic Component |

## Meta Learning (`meta_learning/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Implements core logic for Adaptation Engine functionality. | Class/Logic Component |
| meta_learning/meta_manager.py | Orchestrates sub-components within the meta_learning module. | Class/Logic Component |
| meta_learning/meta_policy.py | Implements core logic for Meta Policy functionality. | Class/Logic Component |
| meta_learning/performance_tracker.py | Implements core logic for Performance Tracker functionality. | Class/Logic Component |
| meta_learning/strategy_optimizer.py | Implements core logic for Strategy Optimizer functionality. | Class/Logic Component |

## Metacognition (`metacognition/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Implements core logic for Adaptation Engine functionality. | Class/Logic Component |
| metacognition/consensus_controller.py | Implements core logic for Consensus Controller functionality. | Class/Logic Component |
| metacognition/mape_k_loop.py | Implements core logic for Mape K Loop functionality. | Class/Logic Component |
| metacognition/meta_monitor.py | Implements core logic for Meta Monitor functionality. | Class/Logic Component |
| metacognition/meta_reasoner.py | SGI 2026: Semantic quality evaluation via LLM inference | Ray Actor (LLM Interface) |
| metacognition/metacognition_manager.py | Orchestrates sub-components within the metacognition module. | Class/Logic Component |
| metacognition/perception_reflector.py | Implements core logic for Perception Reflector functionality. | Class/Logic Component |
| metacognition/transparency_engine.py | Implements core logic for Transparency Engine functionality. | Class/Logic Component |

## Monitoring (`monitoring/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Implements core logic for Conformance Engine functionality. | Class/Logic Component |
| monitoring/drift_detector.py | Implements core logic for Drift Detector functionality. | Class/Logic Component |
| monitoring/monitoring_manager.py | Orchestrates sub-components within the monitoring module. | Class/Logic Component |
| monitoring/risk_monitor.py | Implements core logic for Risk Monitor functionality. | Class/Logic Component |
| monitoring/semantic_trace.py | Implements core logic for Semantic Trace functionality. | Class/Logic Component |
| monitoring/telemetry_collector.py | Implements core logic for Telemetry Collector functionality. | Class/Logic Component |
| monitoring/thermal_guard.py | Monitors CPU temperature and load. | Ray Actor (LLM Interface) |

## Motivation (`motivation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Implements core logic for Curiosity functionality. | Class/Logic Component |
| motivation/motivation_manager.py | Orchestrates sub-components within the motivation module. | Class/Logic Component |
| motivation/novelty.py | Implements core logic for Novelty functionality. | Class/Logic Component |
| motivation/reward_engine.py | Implements core logic for Reward Engine functionality. | Class/Logic Component |
| motivation/uncertainty.py | Implements core logic for Uncertainty functionality. | Class/Logic Component |

## Negotiation (`negotiation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Implements core logic for Compliance Engine functionality. | Class/Logic Component |
| negotiation/concession.py | Implements core logic for Concession functionality. | Class/Logic Component |
| negotiation/consensus_engine.py | Implements core logic for Consensus Engine functionality. | Class/Logic Component |
| negotiation/negotiation_manager.py | Orchestrates sub-components within the negotiation module. | Class/Logic Component |
| negotiation/negotiation_protocol.py | Implements core logic for Negotiation Protocol functionality. | Class/Logic Component |
| negotiation/proposal.py | Implements core logic for Proposal functionality. | Class/Logic Component |
| negotiation/treaty_graph.py | Implements core logic for Treaty Graph functionality. | Class/Logic Component |
| negotiation/utility.py | Implements core logic for Utility functionality. | Class/Logic Component |

## Orchestration (`orchestration/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |
| orchestration/event_router.py | Implements core logic for Event Router functionality. | Class/Logic Component |
| orchestration/group_chat_coordinator.py | Implements core logic for Group Chat Coordinator functionality. | Class/Logic Component |
| orchestration/interrupt_handler.py | Implements core logic for Interrupt Handler functionality. | Class/Logic Component |
| orchestration/orchestration_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |
| orchestration/priority_scheduler.py | Implements core logic for Priority Scheduler functionality. | Class/Logic Component |
| orchestration/state_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |

## Purpleteam (`purpleteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Implements core logic for Bas Engine functionality. | Class/Logic Component |
| purpleteam/blue_agent.py | Implements core logic for Blue Agent functionality. | Class/Logic Component |
| purpleteam/fusion_orchestrator.py | Implements core logic for Fusion Orchestrator functionality. | Class/Logic Component |
| purpleteam/purple_manager.py | Orchestrates sub-components within the purpleteam module. | Class/Logic Component |
| purpleteam/red_agent.py | Implements core logic for Red Agent functionality. | Class/Logic Component |
| purpleteam/remediation_engine.py | Implements core logic for Remediation Engine functionality. | Class/Logic Component |
| purpleteam/scoring_engine.py | Implements core logic for Scoring Engine functionality. | Class/Logic Component |
| purpleteam/selfplay_engine.py | Implements core logic for Selfplay Engine functionality. | Class/Logic Component |

## Redteam (`redteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Implements core logic for Adversarial Agent functionality. | Class/Logic Component |
| redteam/attack_library.py | Implements core logic for Attack Library functionality. | Class/Logic Component |
| redteam/ecosystem_simulator.py | Implements core logic for Ecosystem Simulator functionality. | Class/Logic Component |
| redteam/exploit_generator.py | Implements core logic for Exploit Generator functionality. | Class/Logic Component |
| redteam/redteam_manager.py | Orchestrates sub-components within the redteam module. | Class/Logic Component |
| redteam/scenario_engine.py | Implements core logic for Scenario Engine functionality. | Class/Logic Component |
| redteam/trajectory_simulator.py | Implements core logic for Trajectory Simulator functionality. | Class/Logic Component |
| redteam/vulnerability_scoring.py | Implements core logic for Vulnerability Scoring functionality. | Class/Logic Component |

## Runtime (`runtime/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Implements core logic for Agi Runtime functionality. | Class/Logic Component |
| runtime/agi_state.py | Implements core logic for Agi State functionality. | Class/Logic Component |
| runtime/event_bus.py | Implements core logic for Event Bus functionality. | Class/Logic Component |
| runtime/governance_gateway.py | Implements core logic for Governance Gateway functionality. | Class/Logic Component |
| runtime/runtime_logger.py | Implements core logic for Runtime Logger functionality. | Class/Logic Component |
| runtime/safety_hooks.py | Implements core logic for Safety Hooks functionality. | Class/Logic Component |
| runtime/scheduler.py | Implements core logic for Scheduler functionality. | Class/Logic Component |

## Safety Ethics (`safety_ethics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Calculates cognitive load based on message frequency in a sliding window. | Class/Logic Component |
| safety_ethics/conflict_resolver.py | Each option is a dict: {"action": ..., "ethical_score": ...} | Class/Logic Component |
| safety_ethics/constraint_enforcer.py | Implements core logic for Constraint Enforcer functionality. | Class/Logic Component |
| safety_ethics/deception_detector.py | Implements core logic for Deception Detector functionality. | Class/Logic Component |
| safety_ethics/ethical_appraisal.py | Placeholder logic | Class/Logic Component |
| safety_ethics/ethics_manager.py | Provides a safety score between 0 and 1. | Class/Logic Component |
| safety_ethics/governance_graph.py | Implements core logic for Governance Graph functionality. | Class/Logic Component |
| safety_ethics/interpretability_monitor.py | Placeholder: detect suspicious circuits or anomalous activations | Class/Logic Component |
| safety_ethics/moral_reasoner.py | Implements core logic for Moral Reasoner functionality. | Class/Logic Component |
| safety_ethics/norm_library.py | Implements core logic for Norm Library functionality. | Class/Logic Component |
| safety_ethics/oversight_agent.py | Implements core logic for Oversight Agent functionality. | Class/Logic Component |
| safety_ethics/risk_classifier.py | Implements core logic for Risk Classifier functionality. | Class/Logic Component |
| safety_ethics/safety_manager.py | Orchestrates sub-components within the safety_ethics module. | Class/Logic Component |
| safety_ethics/shutdown_controller.py | Implements core logic for Shutdown Controller functionality. | Class/Logic Component |

## Self Model (`self_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Implements core logic for Autobiographical Memory functionality. | Class/Logic Component |
| self_model/continuity_metrics.py | Implements core logic for Continuity Metrics functionality. | Class/Logic Component |
| self_model/identity_kernel.py | Implements core logic for Identity Kernel functionality. | Class/Logic Component |
| self_model/reflective_endorsement.py | Implements core logic for Reflective Endorsement functionality. | Class/Logic Component |
| self_model/self_manager.py | Orchestrates sub-components within the self_model module. | Class/Logic Component |
| self_model/temporal_self.py | Implements core logic for Temporal Self functionality. | Class/Logic Component |

## Simulation (`simulation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Implements core logic for Agent Adapter functionality. | Class/Logic Component |
| simulation/environment.py | Implements core logic for Environment functionality. | Class/Logic Component |
| simulation/governance_interventions.py | Implements core logic for Governance Interventions functionality. | Class/Logic Component |
| simulation/interaction_protocol.py | Implements core logic for Interaction Protocol functionality. | Class/Logic Component |
| simulation/metrics_engine.py | Implements core logic for Metrics Engine functionality. | Class/Logic Component |
| simulation/replay_buffer.py | Implements core logic for Replay Buffer functionality. | Class/Logic Component |
| simulation/sim_core.py | Implements core logic for Sim Core functionality. | Class/Logic Component |
| simulation/simulation_manager.py | Orchestrates sub-components within the simulation module. | Class/Logic Component |

## Tests (`tests/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Verification suite for system features and regressions. | Class/Logic Component |

## Training (`training/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Implements core logic for Curriculum functionality. | Class/Logic Component |
| training/meta_learning.py | Implements core logic for Meta Learning functionality. | Class/Logic Component |
| training/rl_trainer.py | Placeholder: choose best known action | Class/Logic Component |
| training/self_supervised.py | Implements core logic for Self Supervised functionality. | Class/Logic Component |
| training/training_manager.py | Orchestrates sub-components within the training module. | Class/Logic Component |
| training/world_model_trainer.py | Update causal graph or state based on new data | Class/Logic Component |

## World Model (`world_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Implements core logic for Causal Graph functionality. | Class/Logic Component |
| world_model/counterfactuals.py | Implements core logic for Counterfactuals functionality. | Class/Logic Component |
| world_model/manager.py | Orchestrates sub-components within the world_model module. | Class/Logic Component |
| world_model/prediction.py | Implements core logic for Prediction functionality. | Class/Logic Component |
| world_model/simulator.py | Update external entities based on causal effects | Class/Logic Component |
| world_model/state.py | Identifies discrepancies between predicted and observed states. | Class/Logic Component |
