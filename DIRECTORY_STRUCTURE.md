# SGI-Alpha Complete Directory Structure and Integration Map

This document lists every file in the repository, its purpose, and how it integrates into the LLM-driven SGI architecture.

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| AGENTS.md | SGI Roadmap: i7-8265U Optimized | Utility/Component |
| AGI.docx | Binary or unreadable file | Static Resource |
| DIRECTORY_STRUCTURE.md | Empty file | N/A |
| README.md | SGI-Alpha: AGI LLM for Coding, Math and Logic | Utility/Component |
| compilation_errors.log | Logic for compilation_errors.log | Utility/Component |
| config.yaml | SGI Configuration Manifest (v1.0) | Utility/Component |
| find_invalid_py.py | Logic for find_invalid_py | Utility/Component |
| hardware_verification.log | Logic for hardware_verification.log | Utility/Component |
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
| actors/self_model.py | Logic for self_model | Cognitive Actor (LLM-Integrated) |
| actors/social/discourse.py | Placeholder pragmatic inference | Cognitive Actor (LLM-Integrated) |
| actors/social/social_reasoner.py | Retrieve recent interactions from episodic memory | Ray Actor (LLM Interface) |
| actors/social/theory_of_mind.py | SGI 2026: Complex intention inference via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/vision.py | Implementation of NeuralLVC / CoPE for Video/Vision data. | Cognitive Actor (LLM-Integrated) |

## Blueteam (`blueteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Logic for adaptive_defense_agent | Class/Logic Component |
| blueteam/blueteam_manager.py | Orchestrates sub-components within the blueteam module. | Class/Logic Component |
| blueteam/cyber_range.py | Logic for cyber_range | Class/Logic Component |
| blueteam/deception_layer.py | Logic for deception_layer | Class/Logic Component |
| blueteam/defense_orchestrator.py | Logic for defense_orchestrator | Class/Logic Component |
| blueteam/detection_engine.py | Logic for detection_engine | Class/Logic Component |
| blueteam/dlp_agent.py | Logic for dlp_agent | Class/Logic Component |
| blueteam/firewall_agent.py | Logic for firewall_agent | Class/Logic Component |
| blueteam/forensic_agent.py | Logic for forensic_agent | Class/Logic Component |

## Cee Layer (`cee_layer/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestrates sub-components within the cee_layer module. | Class/Logic Component |
| cee_layer/cognitive_affective_bridge.py | Logic for cognitive_affective_bridge | Class/Logic Component |
| cee_layer/emotion_appraisal.py | Logic for emotion_appraisal | Class/Logic Component |
| cee_layer/emotion_generator.py | Logic for emotion_generator | Class/Logic Component |
| cee_layer/emotion_regulator.py | Logic for emotion_regulator | Class/Logic Component |
| cee_layer/ethical_evaluator.py | Logic for ethical_evaluator | Class/Logic Component |
| cee_layer/moral_weighting.py | Logic for moral_weighting | Class/Logic Component |

## Conflict Resolution (`conflict_resolution/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestrates sub-components within the conflict_resolution module. | Class/Logic Component |
| conflict_resolution/contradiction_detector.py | Logic for contradiction_detector | Class/Logic Component |
| conflict_resolution/ethical_appraisal.py | Logic for ethical_appraisal | Class/Logic Component |
| conflict_resolution/moral_agents.py | Logic for moral_agents | Class/Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Logic for probabilistic_reasoner | Class/Logic Component |
| conflict_resolution/resolution_protocol.py | Logic for resolution_protocol | Class/Logic Component |
| conflict_resolution/survivability_engine.py | Logic for survivability_engine | Class/Logic Component |
| conflict_resolution/value_arbitration.py | Logic for value_arbitration | Class/Logic Component |

## Console (`console/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Logic for action_queue | Class/Logic Component |
| console/approval_gateway.py | Logic for approval_gateway | Class/Logic Component |
| console/audit_log.py | Logic for audit_log | Class/Logic Component |
| console/confidence_monitor.py | Logic for confidence_monitor | Class/Logic Component |
| console/console_manager.py | Orchestrates sub-components within the console module. | Class/Logic Component |
| console/escalation_engine.py | Logic for escalation_engine | Class/Logic Component |
| console/human_interface.py | Placeholder for UI integration | Class/Logic Component |
| console/oversight_dashboard.py | Logic for oversight_dashboard | Class/Logic Component |

## Core (`core/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Logic for base | Cognitive Actor (LLM-Integrated) |
| core/config.py | Load configuration from manifest | Utility/Component |
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
| deployment/agent_registry.py | Logic for agent_registry | Class/Logic Component |
| deployment/deployment_manager.py | Orchestrates sub-components within the deployment module. | Class/Logic Component |
| deployment/policy_loader.py | Logic for policy_loader | Class/Logic Component |
| deployment/runtime_env.py | Logic for runtime_env | Class/Logic Component |
| deployment/version_manager.py | Orchestrates sub-components within the deployment module. | Class/Logic Component |

## Economics (`economics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Logic for agent_policy | Class/Logic Component |
| economics/context_engine.py | Logic for context_engine | Class/Logic Component |
| economics/coordination_protocol.py | Logic for coordination_protocol | Class/Logic Component |
| economics/economic_manager.py | Orchestrates sub-components within the economics module. | Class/Logic Component |
| economics/fairness_engine.py | Logic for fairness_engine | Class/Logic Component |
| economics/optimizer.py | Logic for optimizer | Class/Logic Component |
| economics/orchestration_layer.py | Logic for orchestration_layer | Class/Logic Component |
| economics/resource_model.py | Logic for resource_model | Class/Logic Component |
| economics/utility_engine.py | Logic for utility_engine | Class/Logic Component |

## Emotion (`emotion/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Example reasoning logic | Class/Logic Component |
| emotion/affective_state.py | Simple affective dynamics | Class/Logic Component |
| emotion/appraisal.py | Logic for appraisal | Class/Logic Component |
| emotion/emotion_manager.py | Orchestrates sub-components within the emotion module. | Class/Logic Component |

## Incident Response (`incident_response/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Logic for audit_logger | Class/Logic Component |
| incident_response/containment_engine.py | Logic for containment_engine | Class/Logic Component |
| incident_response/detectors.py | Logic for detectors | Class/Logic Component |
| incident_response/eradication_engine.py | Logic for eradication_engine | Class/Logic Component |
| incident_response/incident_classifier.py | Logic for incident_classifier | Class/Logic Component |
| incident_response/incident_manager.py | Orchestrates sub-components within the incident_response module. | Class/Logic Component |
| incident_response/recovery_engine.py | Logic for recovery_engine | Class/Logic Component |
| incident_response/semantic_checks.py | Logic for semantic_checks | Class/Logic Component |

## Institutional Ai (`institutional_ai/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Logic for coordination_layer | Class/Logic Component |
| institutional_ai/governance_graph.py | Logic for governance_graph | Class/Logic Component |
| institutional_ai/incentive_engine.py | Logic for incentive_engine | Class/Logic Component |
| institutional_ai/institutional_manager.py | Orchestrates sub-components within the institutional_ai module. | Class/Logic Component |
| institutional_ai/oversight_agents.py | Logic for oversight_agents | Class/Logic Component |
| institutional_ai/real_time_control.py | Logic for real_time_control | Class/Logic Component |
| institutional_ai/role_definitions.py | Logic for role_definitions | Class/Logic Component |
| institutional_ai/rule_engine.py | Logic for rule_engine | Class/Logic Component |
| institutional_ai/sanction_engine.py | Logic for sanction_engine | Class/Logic Component |
| institutional_ai/trust_engine.py | Logic for trust_engine | Class/Logic Component |

## Memory (`memory/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implementation of LLM-Arithmetic Coding for Deep Archive. | Cognitive Actor (LLM-Integrated) |
| memory/memory_manager.py | Orchestrates sub-components within the memory module. | Ray Actor (LLM Interface) |
| memory/scratchpad.py | Logic for scratchpad | Class/Logic Component |
| memory/short_term/episodic_memory.py | Logic for episodic_memory | Class/Logic Component |

## Memory Consolidation (`memory_consolidation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestrates sub-components within the memory_consolidation module. | Class/Logic Component |
| memory_consolidation/consolidation_scheduler.py | Logic for consolidation_scheduler | Class/Logic Component |
| memory_consolidation/generative_trainer.py | Logic for generative_trainer | Class/Logic Component |
| memory_consolidation/hippocampal_replay.py | Simple sequential replay | Class/Logic Component |
| memory_consolidation/schema_manager.py | Orchestrates sub-components within the memory_consolidation module. | Class/Logic Component |

## Meta Learning (`meta_learning/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Logic for adaptation_engine | Class/Logic Component |
| meta_learning/meta_manager.py | Orchestrates sub-components within the meta_learning module. | Class/Logic Component |
| meta_learning/meta_policy.py | Logic for meta_policy | Class/Logic Component |
| meta_learning/performance_tracker.py | Logic for performance_tracker | Class/Logic Component |
| meta_learning/strategy_optimizer.py | Logic for strategy_optimizer | Class/Logic Component |

## Metacognition (`metacognition/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Logic for adaptation_engine | Class/Logic Component |
| metacognition/consensus_controller.py | Logic for consensus_controller | Class/Logic Component |
| metacognition/mape_k_loop.py | Logic for mape_k_loop | Class/Logic Component |
| metacognition/meta_monitor.py | Logic for meta_monitor | Class/Logic Component |
| metacognition/meta_reasoner.py | SGI 2026: Semantic quality evaluation via LLM inference | Ray Actor (LLM Interface) |
| metacognition/metacognition_manager.py | Orchestrates sub-components within the metacognition module. | Class/Logic Component |
| metacognition/perception_reflector.py | Logic for perception_reflector | Class/Logic Component |
| metacognition/transparency_engine.py | Logic for transparency_engine | Class/Logic Component |

## Monitoring (`monitoring/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Logic for conformance_engine | Class/Logic Component |
| monitoring/drift_detector.py | Logic for drift_detector | Class/Logic Component |
| monitoring/monitoring_manager.py | Orchestrates sub-components within the monitoring module. | Class/Logic Component |
| monitoring/risk_monitor.py | Logic for risk_monitor | Class/Logic Component |
| monitoring/semantic_trace.py | Logic for semantic_trace | Class/Logic Component |
| monitoring/telemetry_collector.py | Logic for telemetry_collector | Class/Logic Component |
| monitoring/thermal_guard.py | Monitors CPU temperature and load. | Ray Actor (LLM Interface) |

## Motivation (`motivation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Logic for curiosity | Class/Logic Component |
| motivation/motivation_manager.py | Orchestrates sub-components within the motivation module. | Class/Logic Component |
| motivation/novelty.py | Logic for novelty | Class/Logic Component |
| motivation/reward_engine.py | Logic for reward_engine | Class/Logic Component |
| motivation/uncertainty.py | Logic for uncertainty | Class/Logic Component |

## Negotiation (`negotiation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Logic for compliance_engine | Class/Logic Component |
| negotiation/concession.py | Logic for concession | Class/Logic Component |
| negotiation/consensus_engine.py | Logic for consensus_engine | Class/Logic Component |
| negotiation/negotiation_manager.py | Orchestrates sub-components within the negotiation module. | Class/Logic Component |
| negotiation/negotiation_protocol.py | Logic for negotiation_protocol | Class/Logic Component |
| negotiation/proposal.py | Logic for proposal | Class/Logic Component |
| negotiation/treaty_graph.py | Logic for treaty_graph | Class/Logic Component |
| negotiation/utility.py | Logic for utility | Class/Logic Component |

## Orchestration (`orchestration/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |
| orchestration/event_router.py | Logic for event_router | Class/Logic Component |
| orchestration/group_chat_coordinator.py | Logic for group_chat_coordinator | Class/Logic Component |
| orchestration/interrupt_handler.py | Logic for interrupt_handler | Class/Logic Component |
| orchestration/orchestration_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |
| orchestration/priority_scheduler.py | Logic for priority_scheduler | Class/Logic Component |
| orchestration/state_manager.py | Orchestrates sub-components within the orchestration module. | Class/Logic Component |

## Purpleteam (`purpleteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Logic for bas_engine | Class/Logic Component |
| purpleteam/blue_agent.py | Logic for blue_agent | Class/Logic Component |
| purpleteam/fusion_orchestrator.py | Logic for fusion_orchestrator | Class/Logic Component |
| purpleteam/purple_manager.py | Orchestrates sub-components within the purpleteam module. | Class/Logic Component |
| purpleteam/red_agent.py | Logic for red_agent | Class/Logic Component |
| purpleteam/remediation_engine.py | Logic for remediation_engine | Class/Logic Component |
| purpleteam/scoring_engine.py | Logic for scoring_engine | Class/Logic Component |
| purpleteam/selfplay_engine.py | Logic for selfplay_engine | Class/Logic Component |

## Redteam (`redteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Logic for adversarial_agent | Class/Logic Component |
| redteam/attack_library.py | Logic for attack_library | Class/Logic Component |
| redteam/ecosystem_simulator.py | Logic for ecosystem_simulator | Class/Logic Component |
| redteam/exploit_generator.py | Logic for exploit_generator | Class/Logic Component |
| redteam/redteam_manager.py | Orchestrates sub-components within the redteam module. | Class/Logic Component |
| redteam/scenario_engine.py | Logic for scenario_engine | Class/Logic Component |
| redteam/trajectory_simulator.py | Logic for trajectory_simulator | Class/Logic Component |
| redteam/vulnerability_scoring.py | Logic for vulnerability_scoring | Class/Logic Component |

## Runtime (`runtime/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Logic for agi_runtime | Class/Logic Component |
| runtime/agi_state.py | Logic for agi_state | Class/Logic Component |
| runtime/event_bus.py | Logic for event_bus | Class/Logic Component |
| runtime/governance_gateway.py | Logic for governance_gateway | Class/Logic Component |
| runtime/runtime_logger.py | Logic for runtime_logger | Class/Logic Component |
| runtime/safety_hooks.py | Logic for safety_hooks | Class/Logic Component |
| runtime/scheduler.py | Logic for scheduler | Class/Logic Component |

## Safety Ethics (`safety_ethics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Calculates cognitive load based on message frequency in a sliding window. | Class/Logic Component |
| safety_ethics/conflict_resolver.py | Each option is a dict: {"action": ..., "ethical_score": ...} | Class/Logic Component |
| safety_ethics/constraint_enforcer.py | Logic for constraint_enforcer | Class/Logic Component |
| safety_ethics/deception_detector.py | Logic for deception_detector | Class/Logic Component |
| safety_ethics/ethical_appraisal.py | Placeholder logic | Class/Logic Component |
| safety_ethics/ethics_manager.py | Provides a safety score between 0 and 1. | Class/Logic Component |
| safety_ethics/governance_graph.py | Logic for governance_graph | Class/Logic Component |
| safety_ethics/interpretability_monitor.py | Placeholder: detect suspicious circuits or anomalous activations | Class/Logic Component |
| safety_ethics/moral_reasoner.py | Logic for moral_reasoner | Class/Logic Component |
| safety_ethics/norm_library.py | Logic for norm_library | Class/Logic Component |
| safety_ethics/oversight_agent.py | Logic for oversight_agent | Class/Logic Component |
| safety_ethics/risk_classifier.py | Logic for risk_classifier | Class/Logic Component |
| safety_ethics/safety_manager.py | Orchestrates sub-components within the safety_ethics module. | Class/Logic Component |
| safety_ethics/shutdown_controller.py | Logic for shutdown_controller | Class/Logic Component |

## Self Model (`self_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Logic for autobiographical_memory | Class/Logic Component |
| self_model/continuity_metrics.py | Logic for continuity_metrics | Class/Logic Component |
| self_model/identity_kernel.py | Logic for identity_kernel | Class/Logic Component |
| self_model/reflective_endorsement.py | Logic for reflective_endorsement | Class/Logic Component |
| self_model/self_manager.py | Orchestrates sub-components within the self_model module. | Class/Logic Component |
| self_model/temporal_self.py | Logic for temporal_self | Class/Logic Component |

## Simulation (`simulation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Logic for agent_adapter | Class/Logic Component |
| simulation/environment.py | Logic for environment | Class/Logic Component |
| simulation/governance_interventions.py | Logic for governance_interventions | Class/Logic Component |
| simulation/interaction_protocol.py | Logic for interaction_protocol | Class/Logic Component |
| simulation/metrics_engine.py | Logic for metrics_engine | Class/Logic Component |
| simulation/replay_buffer.py | Logic for replay_buffer | Class/Logic Component |
| simulation/sim_core.py | Logic for sim_core | Class/Logic Component |
| simulation/simulation_manager.py | Orchestrates sub-components within the simulation module. | Class/Logic Component |

## Tests (`tests/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Poll scheduler for results | Class/Logic Component |

## Training (`training/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Logic for curriculum | Class/Logic Component |
| training/meta_learning.py | Logic for meta_learning | Class/Logic Component |
| training/rl_trainer.py | Placeholder: choose best known action | Class/Logic Component |
| training/self_supervised.py | Logic for self_supervised | Class/Logic Component |
| training/training_manager.py | Orchestrates sub-components within the training module. | Class/Logic Component |
| training/world_model_trainer.py | Update causal graph or state based on new data | Class/Logic Component |

## World Model (`world_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Logic for causal_graph | Class/Logic Component |
| world_model/counterfactuals.py | Logic for counterfactuals | Class/Logic Component |
| world_model/manager.py | Orchestrates sub-components within the world_model module. | Class/Logic Component |
| world_model/prediction.py | Logic for prediction | Class/Logic Component |
| world_model/simulator.py | Update external entities based on causal effects | Class/Logic Component |
| world_model/state.py | Identifies discrepancies between predicted and observed states. | Class/Logic Component |
