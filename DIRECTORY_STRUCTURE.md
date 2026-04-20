# SGI-Alpha Directory Structure and LLM Integration Map

This document provides a comprehensive mapping of every file in the SGI-Alpha repository, detailing its purpose and its specific role within the LLM-driven APW architecture.

## Actors

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | Specialized distributed agent for coding tasks within the APW architecture. | Ray Actor (Distributed) |
| actors/critic_actor.py | Implements core critic actor logic and functional requirements within the actors subsystem. | Ray Actor (Distributed) |
| actors/planner.py | Implements core planner logic and functional requirements within the actors subsystem. | Ray Actor (Distributed) |
| actors/reasoner_actor.py | Specialized distributed agent for reasoner tasks within the APW architecture. | Ray Actor (Distributed) |
| actors/search_actor.py | Specialized distributed agent for license tasks within the APW architecture. | Ray Actor (Distributed) |
| actors/self_model.py | Implements core self model logic and functional requirements within the actors subsystem. | Cognitive Module (Integrated) |
| actors/vision.py | Implements core vision logic and functional requirements within the actors subsystem. | Cognitive Module (Integrated) |

## Actors/Social

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/social/discourse.py | Implements core discourse logic and functional requirements within the social subsystem. | Cognitive Module (Integrated) |
| actors/social/social_reasoner.py | Implements core social reasoner logic and functional requirements within the social subsystem. | Ray Actor (Distributed) |
| actors/social/theory_of_mind.py | Implements core theory of mind logic and functional requirements within the social subsystem. | Ray Actor (Distributed) |

## Blueteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Implements core adaptive defense agent logic and functional requirements within the blueteam subsystem. | Logic Component |
| blueteam/blueteam_manager.py | Orchestration layer for Blueteam operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| blueteam/cyber_range.py | Implements core cyber range logic and functional requirements within the blueteam subsystem. | Logic Component |
| blueteam/deception_layer.py | Implements core deception layer logic and functional requirements within the blueteam subsystem. | Logic Component |
| blueteam/defense_orchestrator.py | Implements core defense orchestrator logic and functional requirements within the blueteam subsystem. | Logic Component |
| blueteam/detection_engine.py | Core logic engine for detection processing and state transformations. | Logic Component |
| blueteam/dlp_agent.py | Implements core dlp agent logic and functional requirements within the blueteam subsystem. | Logic Component |
| blueteam/firewall_agent.py | Implements core firewall agent logic and functional requirements within the blueteam subsystem. | Cognitive Module (Integrated) |
| blueteam/forensic_agent.py | Implements core forensic agent logic and functional requirements within the blueteam subsystem. | Logic Component |

## Cee Layer

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestration layer for Cee Layer operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| cee_layer/cognitive_affective_bridge.py | Implements core cognitive affective bridge logic and functional requirements within the cee_layer subsystem. | Logic Component |
| cee_layer/emotion_appraisal.py | Implements core emotion appraisal logic and functional requirements within the cee_layer subsystem. | Logic Component |
| cee_layer/emotion_generator.py | Implements core emotion generator logic and functional requirements within the cee_layer subsystem. | Logic Component |
| cee_layer/emotion_regulator.py | Implements core emotion regulator logic and functional requirements within the cee_layer subsystem. | Logic Component |
| cee_layer/ethical_evaluator.py | Implements core ethical evaluator logic and functional requirements within the cee_layer subsystem. | Logic Component |
| cee_layer/moral_weighting.py | Implements core moral weighting logic and functional requirements within the cee_layer subsystem. | Logic Component |

## Conflict Resolution

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestration layer for Conflict Resolution operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| conflict_resolution/contradiction_detector.py | Implements core contradiction detector logic and functional requirements within the conflict_resolution subsystem. | Logic Component |
| conflict_resolution/ethical_appraisal.py | Implements core ethical appraisal logic and functional requirements within the conflict_resolution subsystem. | Logic Component |
| conflict_resolution/moral_agents.py | Implements core moral agents logic and functional requirements within the conflict_resolution subsystem. | Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Implements core probabilistic reasoner logic and functional requirements within the conflict_resolution subsystem. | Logic Component |
| conflict_resolution/resolution_protocol.py | Implements core resolution protocol logic and functional requirements within the conflict_resolution subsystem. | Logic Component |
| conflict_resolution/survivability_engine.py | Core logic engine for survivability processing and state transformations. | Logic Component |
| conflict_resolution/value_arbitration.py | Implements core value arbitration logic and functional requirements within the conflict_resolution subsystem. | Logic Component |

## Console

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Implements core action queue logic and functional requirements within the console subsystem. | Logic Component |
| console/approval_gateway.py | Implements core approval gateway logic and functional requirements within the console subsystem. | Logic Component |
| console/audit_log.py | Implements core audit log logic and functional requirements within the console subsystem. | Logic Component |
| console/confidence_monitor.py | Implements core confidence monitor logic and functional requirements within the console subsystem. | Logic Component |
| console/console_manager.py | Orchestration layer for Console operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| console/escalation_engine.py | Core logic engine for escalation processing and state transformations. | Logic Component |
| console/human_interface.py | Implements core human interface logic and functional requirements within the console subsystem. | Logic Component |
| console/oversight_dashboard.py | Implements core oversight dashboard logic and functional requirements within the console subsystem. | Logic Component |

## Core

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Implements core base logic and functional requirements within the core subsystem. | Cognitive Module (Integrated) |
| core/config.py | Implements core config logic and functional requirements within the core subsystem. | Logic Component |
| core/controller.py | Implements core controller logic and functional requirements within the core subsystem. | Logic Component |
| core/drives.py | Core logic engine for drive processing and state transformations. | Logic Component |
| core/heartbeat.py | Implements core heartbeat logic and functional requirements within the core subsystem. | Logic Component |
| core/model_registry.py | Implements core model registry logic and functional requirements within the core subsystem. | Ray Actor (Distributed) |
| core/scheduler.py | Implements core scheduler logic and functional requirements within the core subsystem. | Ray Actor (Distributed) |
| core/workspace.py | Implements core workspace logic and functional requirements within the core subsystem. | Ray Actor (Distributed) |

## Core/Message Bus

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/message_bus/fast_path.py | Implements core fast path logic and functional requirements within the message_bus subsystem. | Logic Component |
| core/message_bus/priority_engine.py | Core logic engine for priority processing and state transformations. | Logic Component |
| core/message_bus/router.py | Implements core router logic and functional requirements within the message_bus subsystem. | Logic Component |

## Deployment

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Implements core agent registry logic and functional requirements within the deployment subsystem. | Logic Component |
| deployment/deployment_manager.py | Orchestration layer for Deployment operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| deployment/policy_loader.py | Implements core policy loader logic and functional requirements within the deployment subsystem. | Logic Component |
| deployment/runtime_env.py | Implements core runtime env logic and functional requirements within the deployment subsystem. | Logic Component |
| deployment/version_manager.py | Orchestration layer for Deployment operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |

## Economics

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Implements core agent policy logic and functional requirements within the economics subsystem. | Logic Component |
| economics/context_engine.py | Core logic engine for context processing and state transformations. | Logic Component |
| economics/coordination_protocol.py | Implements core coordination protocol logic and functional requirements within the economics subsystem. | Logic Component |
| economics/economic_manager.py | Orchestration layer for Economics operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| economics/fairness_engine.py | Core logic engine for fairness processing and state transformations. | Logic Component |
| economics/optimizer.py | Implements core optimizer logic and functional requirements within the economics subsystem. | Logic Component |
| economics/orchestration_layer.py | Implements core orchestration layer logic and functional requirements within the economics subsystem. | Logic Component |
| economics/resource_model.py | Implements core resource model logic and functional requirements within the economics subsystem. | Logic Component |
| economics/utility_engine.py | Core logic engine for utility processing and state transformations. | Logic Component |

## Emotion

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Implements core affective reasoner logic and functional requirements within the emotion subsystem. | Logic Component |
| emotion/affective_state.py | Implements core affective state logic and functional requirements within the emotion subsystem. | Logic Component |
| emotion/appraisal.py | Implements core appraisal logic and functional requirements within the emotion subsystem. | Logic Component |
| emotion/emotion_manager.py | Orchestration layer for Emotion operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |

## Incident Response

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Implements core audit logger logic and functional requirements within the incident_response subsystem. | Logic Component |
| incident_response/containment_engine.py | Core logic engine for containment processing and state transformations. | Logic Component |
| incident_response/detectors.py | Implements core detectors logic and functional requirements within the incident_response subsystem. | Logic Component |
| incident_response/eradication_engine.py | Core logic engine for eradication processing and state transformations. | Logic Component |
| incident_response/incident_classifier.py | Implements core incident classifier logic and functional requirements within the incident_response subsystem. | Logic Component |
| incident_response/incident_manager.py | Orchestration layer for Incident Response operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| incident_response/recovery_engine.py | Core logic engine for recovery processing and state transformations. | Logic Component |
| incident_response/semantic_checks.py | Implements core semantic checks logic and functional requirements within the incident_response subsystem. | Logic Component |

## Institutional Ai

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Implements core coordination layer logic and functional requirements within the institutional_ai subsystem. | Logic Component |
| institutional_ai/governance_graph.py | Implements core governance graph logic and functional requirements within the institutional_ai subsystem. | Logic Component |
| institutional_ai/incentive_engine.py | Core logic engine for incentive processing and state transformations. | Logic Component |
| institutional_ai/institutional_manager.py | Orchestration layer for Institutional Ai operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| institutional_ai/oversight_agents.py | Implements core oversight agents logic and functional requirements within the institutional_ai subsystem. | Logic Component |
| institutional_ai/real_time_control.py | Implements core real time control logic and functional requirements within the institutional_ai subsystem. | Logic Component |
| institutional_ai/role_definitions.py | Implements core role definitions logic and functional requirements within the institutional_ai subsystem. | Logic Component |
| institutional_ai/rule_engine.py | Core logic engine for rule processing and state transformations. | Logic Component |
| institutional_ai/sanction_engine.py | Core logic engine for sanction processing and state transformations. | Logic Component |
| institutional_ai/trust_engine.py | Core logic engine for trust processing and state transformations. | Logic Component |

## Memory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/memory_manager.py | Orchestration layer for Memory operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| memory/scratchpad.py | Implements core scratchpad logic and functional requirements within the memory subsystem. | Logic Component |

## Memory Consolidation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestration layer for Memory Consolidation operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| memory_consolidation/consolidation_scheduler.py | Implements core consolidation scheduler logic and functional requirements within the memory_consolidation subsystem. | Logic Component |
| memory_consolidation/generative_trainer.py | Implements core generative trainer logic and functional requirements within the memory_consolidation subsystem. | Logic Component |
| memory_consolidation/hippocampal_replay.py | Implements core hippocampal replay logic and functional requirements within the memory_consolidation subsystem. | Logic Component |
| memory_consolidation/schema_manager.py | Orchestration layer for Memory Consolidation operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |

## Memory/Long Term

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implements core semantic memory logic and functional requirements within the long_term subsystem. | Cognitive Module (Integrated) |

## Memory/Short Term

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/short_term/episodic_memory.py | Implements core episodic memory logic and functional requirements within the short_term subsystem. | Logic Component |

## Meta Learning

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Core logic engine for adaptation processing and state transformations. | Logic Component |
| meta_learning/meta_manager.py | Orchestration layer for Meta Learning operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| meta_learning/meta_policy.py | Implements core meta policy logic and functional requirements within the meta_learning subsystem. | Logic Component |
| meta_learning/performance_tracker.py | Implements core performance tracker logic and functional requirements within the meta_learning subsystem. | Logic Component |
| meta_learning/strategy_optimizer.py | Implements core strategy optimizer logic and functional requirements within the meta_learning subsystem. | Logic Component |

## Metacognition

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Core logic engine for adaptation processing and state transformations. | Logic Component |
| metacognition/consensus_controller.py | Implements core consensus controller logic and functional requirements within the metacognition subsystem. | Logic Component |
| metacognition/mape_k_loop.py | Implements core mape k loop logic and functional requirements within the metacognition subsystem. | Logic Component |
| metacognition/meta_monitor.py | Implements core meta monitor logic and functional requirements within the metacognition subsystem. | Logic Component |
| metacognition/meta_reasoner.py | Implements core meta reasoner logic and functional requirements within the metacognition subsystem. | Ray Actor (Distributed) |
| metacognition/metacognition_manager.py | Orchestration layer for Metacognition operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| metacognition/perception_reflector.py | Implements core perception reflector logic and functional requirements within the metacognition subsystem. | Logic Component |
| metacognition/transparency_engine.py | Core logic engine for transparency processing and state transformations. | Logic Component |

## Monitoring

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Core logic engine for conformance processing and state transformations. | Logic Component |
| monitoring/drift_detector.py | Implements core drift detector logic and functional requirements within the monitoring subsystem. | Logic Component |
| monitoring/monitoring_manager.py | Orchestration layer for Monitoring operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| monitoring/risk_monitor.py | Implements core risk monitor logic and functional requirements within the monitoring subsystem. | Logic Component |
| monitoring/semantic_trace.py | Implements core semantic trace logic and functional requirements within the monitoring subsystem. | Logic Component |
| monitoring/telemetry_collector.py | Implements core telemetry collector logic and functional requirements within the monitoring subsystem. | Logic Component |
| monitoring/thermal_guard.py | Implements core thermal guard logic and functional requirements within the monitoring subsystem. | Ray Actor (Distributed) |

## Motivation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Implements core curiosity logic and functional requirements within the motivation subsystem. | Logic Component |
| motivation/motivation_manager.py | Orchestration layer for Motivation operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| motivation/novelty.py | Implements core novelty logic and functional requirements within the motivation subsystem. | Logic Component |
| motivation/reward_engine.py | Core logic engine for intrinsicreward processing and state transformations. | Logic Component |
| motivation/uncertainty.py | Implements core uncertainty logic and functional requirements within the motivation subsystem. | Logic Component |

## Negotiation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Core logic engine for compliance processing and state transformations. | Logic Component |
| negotiation/concession.py | Implements core concession logic and functional requirements within the negotiation subsystem. | Logic Component |
| negotiation/consensus_engine.py | Core logic engine for consensus processing and state transformations. | Logic Component |
| negotiation/negotiation_manager.py | Orchestration layer for Negotiation operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| negotiation/negotiation_protocol.py | Implements core negotiation protocol logic and functional requirements within the negotiation subsystem. | Logic Component |
| negotiation/proposal.py | Implements core proposal logic and functional requirements within the negotiation subsystem. | Logic Component |
| negotiation/treaty_graph.py | Implements core treaty graph logic and functional requirements within the negotiation subsystem. | Logic Component |
| negotiation/utility.py | Implements core utility logic and functional requirements within the negotiation subsystem. | Logic Component |

## Orchestration

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestration layer for Orchestration operations. Coordinates communication and lifecycle of specialized agents. | Logic Component |
| orchestration/event_router.py | Implements core event router logic and functional requirements within the orchestration subsystem. | Logic Component |
| orchestration/group_chat_coordinator.py | Implements core group chat coordinator logic and functional requirements within the orchestration subsystem. | Logic Component |
| orchestration/interrupt_handler.py | Implements core interrupt handler logic and functional requirements within the orchestration subsystem. | Logic Component |
| orchestration/orchestration_manager.py | Orchestration layer for Orchestration operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| orchestration/priority_scheduler.py | Implements core priority scheduler logic and functional requirements within the orchestration subsystem. | Logic Component |
| orchestration/state_manager.py | Orchestration layer for Orchestration operations. Coordinates communication and lifecycle of specialized agents. | Logic Component |

## Purpleteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Core logic engine for bas processing and state transformations. | Logic Component |
| purpleteam/blue_agent.py | Implements core blue agent logic and functional requirements within the purpleteam subsystem. | Logic Component |
| purpleteam/fusion_orchestrator.py | Implements core fusion orchestrator logic and functional requirements within the purpleteam subsystem. | Logic Component |
| purpleteam/purple_manager.py | Orchestration layer for Purpleteam operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| purpleteam/red_agent.py | Implements core red agent logic and functional requirements within the purpleteam subsystem. | Logic Component |
| purpleteam/remediation_engine.py | Core logic engine for remediation processing and state transformations. | Logic Component |
| purpleteam/scoring_engine.py | Core logic engine for scoring processing and state transformations. | Logic Component |
| purpleteam/selfplay_engine.py | Core logic engine for selfplay processing and state transformations. | Logic Component |

## Redteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Implements core adversarial agent logic and functional requirements within the redteam subsystem. | Logic Component |
| redteam/attack_library.py | Implements core attack library logic and functional requirements within the redteam subsystem. | Logic Component |
| redteam/ecosystem_simulator.py | Implements core ecosystem simulator logic and functional requirements within the redteam subsystem. | Logic Component |
| redteam/exploit_generator.py | Implements core exploit generator logic and functional requirements within the redteam subsystem. | Logic Component |
| redteam/redteam_manager.py | Orchestration layer for Redteam operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| redteam/scenario_engine.py | Core logic engine for scenario processing and state transformations. | Logic Component |
| redteam/trajectory_simulator.py | Implements core trajectory simulator logic and functional requirements within the redteam subsystem. | Logic Component |
| redteam/vulnerability_scoring.py | Implements core vulnerability scoring logic and functional requirements within the redteam subsystem. | Logic Component |

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| ./.gitignore | System component. | Asset |
| ./AGENTS.md | Specialized agent instructions and constraints. Defines the behavioral norms and operational guidelines for autonomous modules. | Utility/Config |
| ./README.md | Primary project documentation. Provides an overview of the SGI-Alpha architecture, hardware targets, and core operational principles. | Utility/Config |
| ./config.yaml | Global system configuration manifest. Defines hardware-specific thread limits, thermal thresholds, memory safety guards, and tiered precision standards. | Utility/Config |
| ./find_invalid_py.py | Implements core find invalid py logic and functional requirements within the . subsystem. | Logic Component |
| ./hardware_verification.log | System utility/configuration file: hardware_verification.log | Utility/Config |
| ./main.py | Implements core main logic and functional requirements within the . subsystem. | Entry Point |
| ./setup_8265u.sh | Authoritative setup script for Intel i5-8265U environment. Configures Intel-optimized PyTorch/IPEX-LLM and numerical library threading. | Utility/Config |

## Runtime

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Implements core agi runtime logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/agi_state.py | Implements core agi state logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/event_bus.py | Implements core event bus logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/governance_gateway.py | Implements core governance gateway logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/runtime_logger.py | Implements core runtime logger logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/safety_hooks.py | Implements core safety hooks logic and functional requirements within the runtime subsystem. | Logic Component |
| runtime/scheduler.py | Implements core scheduler logic and functional requirements within the runtime subsystem. | Logic Component |

## Safety Ethics

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Implements core attention gate logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/conflict_resolver.py | Implements core conflict resolver logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/constraint_enforcer.py | Implements core constraint enforcer logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/deception_detector.py | Implements core deception detector logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/ethical_appraisal.py | Implements core ethical appraisal logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/ethics_manager.py | Orchestration layer for Safety Ethics operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| safety_ethics/governance_graph.py | Implements core governance graph logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/interpretability_monitor.py | Implements core interpretability monitor logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/moral_reasoner.py | Implements core moral reasoner logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/norm_library.py | Implements core norm library logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/oversight_agent.py | Implements core oversight agent logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/risk_classifier.py | Implements core risk classifier logic and functional requirements within the safety_ethics subsystem. | Logic Component |
| safety_ethics/safety_manager.py | Orchestration layer for Safety Ethics operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| safety_ethics/shutdown_controller.py | Implements core shutdown controller logic and functional requirements within the safety_ethics subsystem. | Logic Component |

## Self Model

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Implements core autobiographical memory logic and functional requirements within the self_model subsystem. | Logic Component |
| self_model/continuity_metrics.py | Implements core continuity metrics logic and functional requirements within the self_model subsystem. | Logic Component |
| self_model/identity_kernel.py | Implements core identity kernel logic and functional requirements within the self_model subsystem. | Logic Component |
| self_model/reflective_endorsement.py | Implements core reflective endorsement logic and functional requirements within the self_model subsystem. | Logic Component |
| self_model/self_manager.py | Orchestration layer for Self Model operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| self_model/temporal_self.py | Implements core temporal self logic and functional requirements within the self_model subsystem. | Logic Component |

## Simulation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Implements core agent adapter logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/environment.py | Implements core environment logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/governance_interventions.py | Implements core governance interventions logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/interaction_protocol.py | Implements core interaction protocol logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/metrics_engine.py | Core logic engine for metrics processing and state transformations. | Logic Component |
| simulation/replay_buffer.py | Implements core replay buffer logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/sim_core.py | Implements core sim core logic and functional requirements within the simulation subsystem. | Logic Component |
| simulation/simulation_manager.py | Orchestration layer for Simulation operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |

## Tests

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Implements core test sgi features logic and functional requirements within the tests subsystem. | Logic Component |

## Training

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Implements core curriculum logic and functional requirements within the training subsystem. | Logic Component |
| training/meta_learning.py | Implements core meta learning logic and functional requirements within the training subsystem. | Logic Component |
| training/rl_trainer.py | Implements core rl trainer logic and functional requirements within the training subsystem. | Logic Component |
| training/self_supervised.py | Implements core self supervised logic and functional requirements within the training subsystem. | Logic Component |
| training/training_manager.py | Orchestration layer for Training operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| training/world_model_trainer.py | Implements core world model trainer logic and functional requirements within the training subsystem. | Logic Component |

## World Model

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Implements core causal graph logic and functional requirements within the world_model subsystem. | Logic Component |
| world_model/counterfactuals.py | What would happen if…? | Logic Component |
| world_model/manager.py | Orchestration layer for World Model operations. Coordinates communication and lifecycle of specialized agents. | Ray Actor (Distributed) |
| world_model/prediction.py | Core logic engine for prediction processing and state transformations. | Logic Component |
| world_model/simulator.py | Implements core simulator logic and functional requirements within the world_model subsystem. | Logic Component |
| world_model/state.py | Implements core state logic and functional requirements within the world_model subsystem. | Logic Component |
