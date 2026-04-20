# SGI-Alpha Directory Structure and Integration Map

This document provides a detailed overview of the SGI-Alpha repository, mapping each file to its purpose and role within the LLM-driven APW architecture.

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| AGENTS.md | SGI Roadmap: i7-8265U Optimized | Utility Component |
| README.md | SGI-Alpha: AGI LLM for Coding, Math and Logic | Utility Component |
| compilation_errors.log | Diagnostic log recording compilation errors events. | Utility Component |
| config.yaml | Authoritative system manifest defining hardware limits, system constants, and cognitive thresholds. | Core Module |
| find_invalid_py.py | Implements core find invalid py logic. | Utility Component |
| hardware_verification.log | Diagnostic log recording hardware verification events. | Utility Component |
| main.py | System entry point; orchestrates Ray initialization, shared model provider, and the cognitive heartbeat loop. | Core Module |
| setup_8265u.sh | Authoritative setup process for Intel i5-8265U (SGI Standard) | Utility Component |

## Actors (`actors/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | Specialized agent for sandboxed code execution, polyglot verification, and Digital Twin branching. | Ray Actor |
| actors/critic_actor.py | SGI 2026: Semantic code analysis via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/planner.py | Strategy engine that decomposes high-level objectives into hierarchical task sequences for other actors. | Ray Actor |
| actors/reasoner_actor.py | High-fidelity logical inference engine integrating Z3 SMT solvers for formal proof and safety verification. | Ray Actor |
| actors/search_actor.py | Multi-stage RAG agent utilizing Tavily/SearXNG with built-in license compliance and JIT distillation. | Ray Actor |
| actors/self_model.py | Implements core self model logic. | Cognitive Actor (LLM-Integrated) |
| actors/social/discourse.py | Placeholder pragmatic inference | Cognitive Actor (LLM-Integrated) |
| actors/social/social_reasoner.py | Retrieve recent interactions from episodic memory | Ray Actor (LLM Interface) |
| actors/social/theory_of_mind.py | SGI 2026: Complex intention inference via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/vision.py | Implementation of NeuralLVC / CoPE for Video/Vision data. | Cognitive Actor (LLM-Integrated) |

## Blueteam (`blueteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Implements core adaptive defense agent logic. | Logic Class |
| blueteam/blueteam_manager.py | Orchestration layer for blueteam sub-components. | Ray Actor (LLM Interface) |
| blueteam/cyber_range.py | Implements core cyber range logic. | Logic Class |
| blueteam/deception_layer.py | Implements core deception layer logic. | Logic Class |
| blueteam/defense_orchestrator.py | Implements core defense orchestrator logic. | Logic Class |
| blueteam/detection_engine.py | Implements core detection engine logic. | Logic Class |
| blueteam/dlp_agent.py | Implements core dlp agent logic. | Logic Class |
| blueteam/firewall_agent.py | Implements core firewall agent logic. | Logic Class |
| blueteam/forensic_agent.py | Implements core forensic agent logic. | Logic Class |

## Cee Layer (`cee_layer/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestration layer for cee_layer sub-components. | Logic Class |
| cee_layer/cognitive_affective_bridge.py | Implements core cognitive affective bridge logic. | Logic Class |
| cee_layer/emotion_appraisal.py | Implements core emotion appraisal logic. | Logic Class |
| cee_layer/emotion_generator.py | Implements core emotion generator logic. | Logic Class |
| cee_layer/emotion_regulator.py | Implements core emotion regulator logic. | Logic Class |
| cee_layer/ethical_evaluator.py | Implements core ethical evaluator logic. | Logic Class |
| cee_layer/moral_weighting.py | Implements core moral weighting logic. | Logic Class |

## Conflict Resolution (`conflict_resolution/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestration layer for conflict_resolution sub-components. | Logic Class |
| conflict_resolution/contradiction_detector.py | Implements core contradiction detector logic. | Logic Class |
| conflict_resolution/ethical_appraisal.py | Implements core ethical appraisal logic. | Logic Class |
| conflict_resolution/moral_agents.py | Implements core moral agents logic. | Logic Class |
| conflict_resolution/probabilistic_reasoner.py | Implements core probabilistic reasoner logic. | Logic Class |
| conflict_resolution/resolution_protocol.py | Implements core resolution protocol logic. | Logic Class |
| conflict_resolution/survivability_engine.py | Implements core survivability engine logic. | Logic Class |
| conflict_resolution/value_arbitration.py | Implements core value arbitration logic. | Logic Class |

## Console (`console/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Implements core action queue logic. | Logic Class |
| console/approval_gateway.py | Implements core approval gateway logic. | Logic Class |
| console/audit_log.py | Implements core audit log logic. | Logic Class |
| console/confidence_monitor.py | Implements core confidence monitor logic. | Logic Class |
| console/console_manager.py | Orchestration layer for console sub-components. | Ray Actor (LLM Interface) |
| console/escalation_engine.py | Implements core escalation engine logic. | Logic Class |
| console/human_interface.py | Placeholder for UI integration | Logic Class |
| console/oversight_dashboard.py | Implements core oversight dashboard logic. | Logic Class |

## Core (`core/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Fundamental base class for all SGI modules; handles automated workspace registration and message routing. | Core Module |
| core/config.py | Dynamic configuration loader for parsing and validating system settings from config.yaml. | Core Module |
| core/controller.py | Tracks pulse-active modules. | Logic Class |
| core/drives.py | Curiosity engine that calculates system entropy and surprise metrics to trigger proactive re-planning. | Core Module |
| core/heartbeat.py | High uncertainty: The agent is "confused" or facing a new problem | Logic Class |
| core/message_bus/fast_path.py | Simulates Flash-Optimized LZ4 compression for Tier 1 (Ephemeral) storage. | Logic Class |
| core/message_bus/priority_engine.py | Time-sensitive messages get higher priority | Logic Class |
| core/message_bus/router.py | Example routing logic | Logic Class |
| core/model_registry.py | Singleton Model Provider to prevent RAM crash on 16GB systems. | Ray Actor (LLM Interface) |
| core/scheduler.py | Intelligent task queue that manages priority-based delegation of workloads to specialized actors. | Ray Actor |
| core/workspace.py | Global broadcast center managing the shared state and message history of the APW architecture. | Ray Actor |

## Deployment (`deployment/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Implements core agent registry logic. | Logic Class |
| deployment/deployment_manager.py | Orchestration layer for deployment sub-components. | Logic Class |
| deployment/policy_loader.py | Implements core policy loader logic. | Logic Class |
| deployment/runtime_env.py | Implements core runtime env logic. | Logic Class |
| deployment/version_manager.py | Orchestration layer for deployment sub-components. | Logic Class |

## Economics (`economics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Implements core agent policy logic. | Logic Class |
| economics/context_engine.py | Implements core context engine logic. | Logic Class |
| economics/coordination_protocol.py | Implements core coordination protocol logic. | Logic Class |
| economics/economic_manager.py | Orchestration layer for economics sub-components. | Ray Actor (LLM Interface) |
| economics/fairness_engine.py | Implements core fairness engine logic. | Logic Class |
| economics/optimizer.py | Implements core optimizer logic. | Logic Class |
| economics/orchestration_layer.py | Implements core orchestration layer logic. | Logic Class |
| economics/resource_model.py | Implements core resource model logic. | Logic Class |
| economics/utility_engine.py | Implements core utility engine logic. | Logic Class |

## Emotion (`emotion/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Example reasoning logic | Logic Class |
| emotion/affective_state.py | Simple affective dynamics | Logic Class |
| emotion/appraisal.py | Implements core appraisal logic. | Logic Class |
| emotion/emotion_manager.py | Orchestration layer for emotion sub-components. | Ray Actor (LLM Interface) |

## Incident Response (`incident_response/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Implements core audit logger logic. | Logic Class |
| incident_response/containment_engine.py | Implements core containment engine logic. | Logic Class |
| incident_response/detectors.py | Implements core detectors logic. | Logic Class |
| incident_response/eradication_engine.py | Implements core eradication engine logic. | Logic Class |
| incident_response/incident_classifier.py | Implements core incident classifier logic. | Logic Class |
| incident_response/incident_manager.py | Orchestration layer for incident_response sub-components. | Ray Actor (LLM Interface) |
| incident_response/recovery_engine.py | Implements core recovery engine logic. | Logic Class |
| incident_response/semantic_checks.py | Implements core semantic checks logic. | Logic Class |

## Institutional Ai (`institutional_ai/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Implements core coordination layer logic. | Logic Class |
| institutional_ai/governance_graph.py | Implements core governance graph logic. | Logic Class |
| institutional_ai/incentive_engine.py | Implements core incentive engine logic. | Logic Class |
| institutional_ai/institutional_manager.py | Orchestration layer for institutional_ai sub-components. | Logic Class |
| institutional_ai/oversight_agents.py | Implements core oversight agents logic. | Logic Class |
| institutional_ai/real_time_control.py | Implements core real time control logic. | Logic Class |
| institutional_ai/role_definitions.py | Implements core role definitions logic. | Logic Class |
| institutional_ai/rule_engine.py | Implements core rule engine logic. | Logic Class |
| institutional_ai/sanction_engine.py | Implements core sanction engine logic. | Logic Class |
| institutional_ai/trust_engine.py | Implements core trust engine logic. | Logic Class |

## Memory (`memory/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implementation of LLM-Arithmetic Coding for Deep Archive. | Cognitive Actor (LLM-Integrated) |
| memory/memory_manager.py | Adaptive resource manager implementing RAM guards and triggering neural consolidation sleep cycles. | Ray Actor |
| memory/scratchpad.py | Implements core scratchpad logic. | Logic Class |
| memory/short_term/episodic_memory.py | Implements core episodic memory logic. | Logic Class |

## Memory Consolidation (`memory_consolidation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestration layer for memory_consolidation sub-components. | Logic Class |
| memory_consolidation/consolidation_scheduler.py | Implements core consolidation scheduler logic. | Logic Class |
| memory_consolidation/generative_trainer.py | Implements core generative trainer logic. | Logic Class |
| memory_consolidation/hippocampal_replay.py | Simple sequential replay | Logic Class |
| memory_consolidation/schema_manager.py | Orchestration layer for memory_consolidation sub-components. | Logic Class |

## Meta Learning (`meta_learning/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Implements core adaptation engine logic. | Logic Class |
| meta_learning/meta_manager.py | Orchestration layer for meta_learning sub-components. | Ray Actor (LLM Interface) |
| meta_learning/meta_policy.py | Implements core meta policy logic. | Logic Class |
| meta_learning/performance_tracker.py | Implements core performance tracker logic. | Logic Class |
| meta_learning/strategy_optimizer.py | Implements core strategy optimizer logic. | Logic Class |

## Metacognition (`metacognition/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Implements core adaptation engine logic. | Logic Class |
| metacognition/consensus_controller.py | Implements core consensus controller logic. | Logic Class |
| metacognition/mape_k_loop.py | Implements core mape k loop logic. | Logic Class |
| metacognition/meta_monitor.py | Implements core meta monitor logic. | Logic Class |
| metacognition/meta_reasoner.py | SGI 2026: Semantic quality evaluation via LLM inference | Ray Actor (LLM Interface) |
| metacognition/metacognition_manager.py | Orchestration layer for metacognition sub-components. | Ray Actor (LLM Interface) |
| metacognition/perception_reflector.py | Implements core perception reflector logic. | Logic Class |
| metacognition/transparency_engine.py | Implements core transparency engine logic. | Logic Class |

## Monitoring (`monitoring/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Implements core conformance engine logic. | Logic Class |
| monitoring/drift_detector.py | Implements core drift detector logic. | Logic Class |
| monitoring/monitoring_manager.py | Orchestration layer for monitoring sub-components. | Ray Actor (LLM Interface) |
| monitoring/risk_monitor.py | Implements core risk monitor logic. | Logic Class |
| monitoring/semantic_trace.py | Implements core semantic trace logic. | Logic Class |
| monitoring/telemetry_collector.py | Implements core telemetry collector logic. | Logic Class |
| monitoring/thermal_guard.py | Hardware protection module that monitors CPU temperature and load to prevent thermal throttling. | Ray Actor |

## Motivation (`motivation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Implements core curiosity logic. | Logic Class |
| motivation/motivation_manager.py | Orchestration layer for motivation sub-components. | Ray Actor (LLM Interface) |
| motivation/novelty.py | Implements core novelty logic. | Logic Class |
| motivation/reward_engine.py | Implements core reward engine logic. | Logic Class |
| motivation/uncertainty.py | Implements core uncertainty logic. | Logic Class |

## Negotiation (`negotiation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Implements core compliance engine logic. | Logic Class |
| negotiation/concession.py | Implements core concession logic. | Logic Class |
| negotiation/consensus_engine.py | Implements core consensus engine logic. | Logic Class |
| negotiation/negotiation_manager.py | Orchestration layer for negotiation sub-components. | Ray Actor (LLM Interface) |
| negotiation/negotiation_protocol.py | Implements core negotiation protocol logic. | Logic Class |
| negotiation/proposal.py | Implements core proposal logic. | Logic Class |
| negotiation/treaty_graph.py | Implements core treaty graph logic. | Logic Class |
| negotiation/utility.py | Implements core utility logic. | Logic Class |

## Orchestration (`orchestration/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestration layer for orchestration sub-components. | Logic Class |
| orchestration/event_router.py | Implements core event router logic. | Logic Class |
| orchestration/group_chat_coordinator.py | Implements core group chat coordinator logic. | Logic Class |
| orchestration/interrupt_handler.py | Implements core interrupt handler logic. | Logic Class |
| orchestration/orchestration_manager.py | Orchestration layer for orchestration sub-components. | Ray Actor (LLM Interface) |
| orchestration/priority_scheduler.py | Implements core priority scheduler logic. | Logic Class |
| orchestration/state_manager.py | Orchestration layer for orchestration sub-components. | Logic Class |

## Purpleteam (`purpleteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Implements core bas engine logic. | Logic Class |
| purpleteam/blue_agent.py | Implements core blue agent logic. | Logic Class |
| purpleteam/fusion_orchestrator.py | Implements core fusion orchestrator logic. | Logic Class |
| purpleteam/purple_manager.py | Orchestration layer for purpleteam sub-components. | Ray Actor (LLM Interface) |
| purpleteam/red_agent.py | Implements core red agent logic. | Logic Class |
| purpleteam/remediation_engine.py | Implements core remediation engine logic. | Logic Class |
| purpleteam/scoring_engine.py | Implements core scoring engine logic. | Logic Class |
| purpleteam/selfplay_engine.py | Implements core selfplay engine logic. | Logic Class |

## Redteam (`redteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Implements core adversarial agent logic. | Logic Class |
| redteam/attack_library.py | Implements core attack library logic. | Logic Class |
| redteam/ecosystem_simulator.py | Implements core ecosystem simulator logic. | Logic Class |
| redteam/exploit_generator.py | Implements core exploit generator logic. | Logic Class |
| redteam/redteam_manager.py | Orchestration layer for redteam sub-components. | Ray Actor (LLM Interface) |
| redteam/scenario_engine.py | Implements core scenario engine logic. | Logic Class |
| redteam/trajectory_simulator.py | Implements core trajectory simulator logic. | Logic Class |
| redteam/vulnerability_scoring.py | Implements core vulnerability scoring logic. | Logic Class |

## Runtime (`runtime/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Implements core agi runtime logic. | Logic Class |
| runtime/agi_state.py | Implements core agi state logic. | Logic Class |
| runtime/event_bus.py | Implements core event bus logic. | Logic Class |
| runtime/governance_gateway.py | Implements core governance gateway logic. | Logic Class |
| runtime/runtime_logger.py | Implements core runtime logger logic. | Logic Class |
| runtime/safety_hooks.py | Implements core safety hooks logic. | Logic Class |
| runtime/scheduler.py | Implements core scheduler logic. | Logic Class |

## Safety Ethics (`safety_ethics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Calculates cognitive load based on message frequency in a sliding window. | Logic Class |
| safety_ethics/conflict_resolver.py | Each option is a dict: {"action": ..., "ethical_score": ...} | Logic Class |
| safety_ethics/constraint_enforcer.py | Implements core constraint enforcer logic. | Logic Class |
| safety_ethics/deception_detector.py | Implements core deception detector logic. | Logic Class |
| safety_ethics/ethical_appraisal.py | Implements core ethical appraisal logic. | Logic Class |
| safety_ethics/ethics_manager.py | Provides a safety score between 0 and 1. | Logic Class |
| safety_ethics/governance_graph.py | Implements core governance graph logic. | Logic Class |
| safety_ethics/interpretability_monitor.py | Placeholder: detect suspicious circuits or anomalous activations | Logic Class |
| safety_ethics/moral_reasoner.py | Implements core moral reasoner logic. | Logic Class |
| safety_ethics/norm_library.py | Implements core norm library logic. | Logic Class |
| safety_ethics/oversight_agent.py | Implements core oversight agent logic. | Logic Class |
| safety_ethics/risk_classifier.py | Implements core risk classifier logic. | Logic Class |
| safety_ethics/safety_manager.py | Orchestrates multi-layered safety checks, including risk classification and behavioral constraints. | Ray Actor |
| safety_ethics/shutdown_controller.py | Implements core shutdown controller logic. | Logic Class |

## Self Model (`self_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Implements core autobiographical memory logic. | Logic Class |
| self_model/continuity_metrics.py | Implements core continuity metrics logic. | Logic Class |
| self_model/identity_kernel.py | Implements core identity kernel logic. | Logic Class |
| self_model/reflective_endorsement.py | Implements core reflective endorsement logic. | Logic Class |
| self_model/self_manager.py | Orchestration layer for self_model sub-components. | Ray Actor (LLM Interface) |
| self_model/temporal_self.py | Implements core temporal self logic. | Logic Class |

## Simulation (`simulation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Implements core agent adapter logic. | Logic Class |
| simulation/environment.py | Implements core environment logic. | Logic Class |
| simulation/governance_interventions.py | Implements core governance interventions logic. | Logic Class |
| simulation/interaction_protocol.py | Implements core interaction protocol logic. | Logic Class |
| simulation/metrics_engine.py | Implements core metrics engine logic. | Logic Class |
| simulation/replay_buffer.py | Implements core replay buffer logic. | Logic Class |
| simulation/sim_core.py | Implements core sim core logic. | Logic Class |
| simulation/simulation_manager.py | Orchestration layer for simulation sub-components. | Ray Actor (LLM Interface) |

## Tests (`tests/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Poll scheduler for results | Logic Class |

## Training (`training/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Implements core curriculum logic. | Logic Class |
| training/meta_learning.py | Implements core meta learning logic. | Logic Class |
| training/rl_trainer.py | Placeholder: choose best known action | Logic Class |
| training/self_supervised.py | Implements core self supervised logic. | Logic Class |
| training/training_manager.py | Orchestration layer for training sub-components. | Ray Actor (LLM Interface) |
| training/world_model_trainer.py | Update causal graph or state based on new data | Logic Class |

## World Model (`world_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Implements core causal graph logic. | Logic Class |
| world_model/counterfactuals.py | Implements core counterfactuals logic. | Logic Class |
| world_model/manager.py | Maintains the system's Digital Twin, simulating causal effects and tracking external environment state. | Ray Actor |
| world_model/prediction.py | Implements core prediction logic. | Logic Class |
| world_model/simulator.py | Update external entities based on causal effects | Logic Class |
| world_model/state.py | Identifies discrepancies between predicted and observed states. | Logic Class |
