# SGI-Alpha Directory Structure and Integration Map

This document provides a detailed overview of the SGI-Alpha repository, mapping each file to its purpose and role within the LLM-driven APW architecture.

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| AGENTS.md | SGI Roadmap: i7-8265U Optimized | Utility Component |
| README.md | SGI-Alpha: AGI LLM for Coding, Math and Logic | Utility Component |
| compilation_errors.log | Diagnostic log recording compilation errors events.  Used for debugging and system-wide telemetry... | Utility Component |
| config.yaml | Authoritative system manifest defining hardware limits, system constants, and cognitive thresholds.
Acts as the single source of truth for all module configurations. | Core Module |
| find_invalid_py.py | Implements core logic for Find Invalid Py functionality.  Supports the primary mission of  within... | Utility Component |
| hardware_verification.log | Diagnostic log recording hardware verification events.  Used for debugging and system-wide teleme... | Utility Component |
| main.py | System entry point; orchestrates Ray initialization, shared model provider, and the cognitive heartbeat loop.
Ensures all threads and memory are managed within Intel i5-8265U constraints. | Core Module |
| setup_8265u.sh | Authoritative setup process for Intel i5-8265U (SGI Standard) | Utility Component |

## Actors (`actors/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | Specialized agent for sandboxed code execution, polyglot verification, and Digital Twin branching.
Uses Firecracker microVMs for stateful persistence and secure execution of untrusted code. | Ray Actor |
| actors/critic_actor.py | SGI 2026: Semantic code analysis via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/planner.py | Strategy engine that decomposes high-level objectives into hierarchical task sequences for other actors.
Uses the shared LLM to perform intelligent task decomposition and goal-oriented planning. | Ray Actor |
| actors/reasoner_actor.py | High-fidelity logical inference engine integrating Z3 SMT solvers for formal proof and safety verification.
Operates natively in sym_int8 precision for maximum AVX2 efficiency on Intel hardware. | Ray Actor |
| actors/search_actor.py | Multi-stage RAG agent utilizing Tavily/SearXNG with built-in license compliance and JIT distillation.
Enforces a License Guardian gate to prevent the integration of GPL/LGPL licensed code. | Ray Actor |
| actors/self_model.py | Implements core logic for Self Model functionality.  Supports the primary mission of actors withi... | Cognitive Actor (LLM-Integrated) |
| actors/social/discourse.py | Placeholder pragmatic inference | Cognitive Actor (LLM-Integrated) |
| actors/social/social_reasoner.py | Standard async recall for episodic memory | Ray Actor (LLM Interface) |
| actors/social/theory_of_mind.py | SGI 2026: Complex intention inference via Shared Model Provider | Ray Actor (LLM Interface) |
| actors/vision.py | Implementation of NeuralLVC / CoPE for Video/Vision data.         Achieves up to 93% reduction in... | Cognitive Actor (LLM-Integrated) |

## Blueteam (`blueteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Implements core logic for Adaptive Defense Agent functionality.  Supports the primary mission of ... | Logic Component |
| blueteam/blueteam_manager.py | Orchestration layer for blueteam sub-components.  Coordinates communication and lifecycle managem... | Ray Actor (LLM Interface) |
| blueteam/cyber_range.py | Implements core logic for Cyber Range functionality.  Supports the primary mission of blueteam wi... | Logic Component |
| blueteam/deception_layer.py | Implements core logic for Deception Layer functionality.  Supports the primary mission of bluetea... | Logic Component |
| blueteam/defense_orchestrator.py | Implements core logic for Defense Orchestrator functionality.  Supports the primary mission of bl... | Logic Component |
| blueteam/detection_engine.py | Implements core logic for Detection Engine functionality.  Supports the primary mission of bluete... | Logic Component |
| blueteam/dlp_agent.py | Implements core logic for Dlp Agent functionality.  Supports the primary mission of blueteam with... | Logic Component |
| blueteam/firewall_agent.py | Implements core logic for Firewall Agent functionality.  Supports the primary mission of blueteam... | Logic Component |
| blueteam/forensic_agent.py | Implements core logic for Forensic Agent functionality.  Supports the primary mission of blueteam... | Logic Component |

## Cee Layer (`cee_layer/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestration layer for cee_layer sub-components.  Coordinates communication and lifecycle manage... | Logic Component |
| cee_layer/cognitive_affective_bridge.py | Implements core logic for Cognitive Affective Bridge functionality.  Supports the primary mission... | Logic Component |
| cee_layer/emotion_appraisal.py | Implements core logic for Emotion Appraisal functionality.  Supports the primary mission of cee_l... | Logic Component |
| cee_layer/emotion_generator.py | Implements core logic for Emotion Generator functionality.  Supports the primary mission of cee_l... | Logic Component |
| cee_layer/emotion_regulator.py | Implements core logic for Emotion Regulator functionality.  Supports the primary mission of cee_l... | Logic Component |
| cee_layer/ethical_evaluator.py | Implements core logic for Ethical Evaluator functionality.  Supports the primary mission of cee_l... | Logic Component |
| cee_layer/moral_weighting.py | Implements core logic for Moral Weighting functionality.  Supports the primary mission of cee_lay... | Logic Component |

## Conflict Resolution (`conflict_resolution/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestration layer for conflict_resolution sub-components.  Coordinates communication and lifecy... | Logic Component |
| conflict_resolution/contradiction_detector.py | Implements core logic for Contradiction Detector functionality.  Supports the primary mission of ... | Logic Component |
| conflict_resolution/ethical_appraisal.py | Implements core logic for Ethical Appraisal functionality.  Supports the primary mission of confl... | Logic Component |
| conflict_resolution/moral_agents.py | Implements core logic for Moral Agents functionality.  Supports the primary mission of conflict_r... | Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Implements core logic for Probabilistic Reasoner functionality.  Supports the primary mission of ... | Logic Component |
| conflict_resolution/resolution_protocol.py | Implements core logic for Resolution Protocol functionality.  Supports the primary mission of con... | Logic Component |
| conflict_resolution/survivability_engine.py | Implements core logic for Survivability Engine functionality.  Supports the primary mission of co... | Logic Component |
| conflict_resolution/value_arbitration.py | Implements core logic for Value Arbitration functionality.  Supports the primary mission of confl... | Logic Component |

## Console (`console/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Implements core logic for Action Queue functionality.  Supports the primary mission of console wi... | Logic Component |
| console/approval_gateway.py | Implements core logic for Approval Gateway functionality.  Supports the primary mission of consol... | Logic Component |
| console/audit_log.py | Implements core logic for Audit Log functionality.  Supports the primary mission of console withi... | Logic Component |
| console/confidence_monitor.py | Implements core logic for Confidence Monitor functionality.  Supports the primary mission of cons... | Logic Component |
| console/console_manager.py | Orchestration layer for console sub-components.  Coordinates communication and lifecycle manageme... | Ray Actor (LLM Interface) |
| console/escalation_engine.py | Implements core logic for Escalation Engine functionality.  Supports the primary mission of conso... | Logic Component |
| console/human_interface.py | Implements core logic for Human Interface functionality.  Supports the primary mission of console... | Logic Component |
| console/oversight_dashboard.py | Implements core logic for Oversight Dashboard functionality.  Supports the primary mission of con... | Logic Component |

## Core (`core/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Fundamental base class for all SGI modules; handles automated workspace registration and message routing.
Ensures that all agents can communicate seamlessly through the asynchronous message bus. | Core Module |
| core/config.py | Dynamic configuration loader for parsing and validating system settings from config.yaml.
Provides typed access to hardware-specific limits and precision standards. | Core Module |
| core/controller.py | Tracks pulse-active modules. | Logic Component |
| core/drives.py | Curiosity engine that calculates system entropy and surprise metrics to trigger proactive re-planning.
Measures information density to balance between active learning and background consolidation. | Core Module |
| core/heartbeat.py | High uncertainty: The agent is "confused" or facing a new problem | Logic Component |
| core/message_bus/fast_path.py | Simulates Flash-Optimized LZ4 compression for Tier 1 (Ephemeral) storage.     Focuses on sub-mill... | Logic Component |
| core/message_bus/priority_engine.py | Time-sensitive messages get higher priority | Logic Component |
| core/message_bus/router.py | Implements core logic for Router functionality.  Supports the primary mission of message_bus with... | Logic Component |
| core/model_registry.py | Singleton Model Provider to prevent RAM crash on 16GB systems.     Loads the model once and provi... | Ray Actor (LLM Interface) |
| core/scheduler.py | Intelligent task queue that manages priority-based delegation of workloads to specialized actors.
Optimizes task flow to prevent bottlenecks in the distributed reasoning loop. | Ray Actor |
| core/workspace.py | Global broadcast center managing the shared state and message history of the APW architecture.
Provides a centralized state store (GlobalWorkspace) accessible to all Ray actors. | Ray Actor |

## Deployment (`deployment/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Implements core logic for Agent Registry functionality.  Supports the primary mission of deployme... | Logic Component |
| deployment/deployment_manager.py | Orchestration layer for deployment sub-components.  Coordinates communication and lifecycle manag... | Logic Component |
| deployment/policy_loader.py | Implements core logic for Policy Loader functionality.  Supports the primary mission of deploymen... | Logic Component |
| deployment/runtime_env.py | Implements core logic for Runtime Env functionality.  Supports the primary mission of deployment ... | Logic Component |
| deployment/version_manager.py | Orchestration layer for deployment sub-components.  Coordinates communication and lifecycle manag... | Logic Component |

## Economics (`economics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Implements core logic for Agent Policy functionality.  Supports the primary mission of economics ... | Logic Component |
| economics/context_engine.py | Implements core logic for Context Engine functionality.  Supports the primary mission of economic... | Logic Component |
| economics/coordination_protocol.py | Implements core logic for Coordination Protocol functionality.  Supports the primary mission of e... | Logic Component |
| economics/economic_manager.py | Orchestration layer for economics sub-components.  Coordinates communication and lifecycle manage... | Ray Actor (LLM Interface) |
| economics/fairness_engine.py | Implements core logic for Fairness Engine functionality.  Supports the primary mission of economi... | Logic Component |
| economics/optimizer.py | Implements core logic for Optimizer functionality.  Supports the primary mission of economics wit... | Logic Component |
| economics/orchestration_layer.py | Implements core logic for Orchestration Layer functionality.  Supports the primary mission of eco... | Logic Component |
| economics/resource_model.py | Implements core logic for Resource Model functionality.  Supports the primary mission of economic... | Logic Component |
| economics/utility_engine.py | Implements core logic for Utility Engine functionality.  Supports the primary mission of economic... | Logic Component |

## Emotion (`emotion/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Implements core logic for Affective Reasoner functionality.  Supports the primary mission of emot... | Logic Component |
| emotion/affective_state.py | Implements core logic for Affective State functionality.  Supports the primary mission of emotion... | Logic Component |
| emotion/appraisal.py | Implements core logic for Appraisal functionality.  Supports the primary mission of emotion withi... | Logic Component |
| emotion/emotion_manager.py | Orchestration layer for emotion sub-components.  Coordinates communication and lifecycle manageme... | Ray Actor (LLM Interface) |

## Incident Response (`incident_response/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Implements core logic for Audit Logger functionality.  Supports the primary mission of incident_r... | Logic Component |
| incident_response/containment_engine.py | Implements core logic for Containment Engine functionality.  Supports the primary mission of inci... | Logic Component |
| incident_response/detectors.py | Implements core logic for Detectors functionality.  Supports the primary mission of incident_resp... | Logic Component |
| incident_response/eradication_engine.py | Implements core logic for Eradication Engine functionality.  Supports the primary mission of inci... | Logic Component |
| incident_response/incident_classifier.py | Implements core logic for Incident Classifier functionality.  Supports the primary mission of inc... | Logic Component |
| incident_response/incident_manager.py | Orchestration layer for incident_response sub-components.  Coordinates communication and lifecycl... | Ray Actor (LLM Interface) |
| incident_response/recovery_engine.py | Implements core logic for Recovery Engine functionality.  Supports the primary mission of inciden... | Logic Component |
| incident_response/semantic_checks.py | Implements core logic for Semantic Checks functionality.  Supports the primary mission of inciden... | Logic Component |

## Institutional Ai (`institutional_ai/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Implements core logic for Coordination Layer functionality.  Supports the primary mission of inst... | Logic Component |
| institutional_ai/governance_graph.py | Implements core logic for Governance Graph functionality.  Supports the primary mission of instit... | Logic Component |
| institutional_ai/incentive_engine.py | Implements core logic for Incentive Engine functionality.  Supports the primary mission of instit... | Logic Component |
| institutional_ai/institutional_manager.py | Orchestration layer for institutional_ai sub-components.  Coordinates communication and lifecycle... | Logic Component |
| institutional_ai/oversight_agents.py | Implements core logic for Oversight Agents functionality.  Supports the primary mission of instit... | Logic Component |
| institutional_ai/real_time_control.py | Implements core logic for Real Time Control functionality.  Supports the primary mission of insti... | Logic Component |
| institutional_ai/role_definitions.py | Implements core logic for Role Definitions functionality.  Supports the primary mission of instit... | Logic Component |
| institutional_ai/rule_engine.py | Implements core logic for Rule Engine functionality.  Supports the primary mission of institution... | Logic Component |
| institutional_ai/sanction_engine.py | Implements core logic for Sanction Engine functionality.  Supports the primary mission of institu... | Logic Component |
| institutional_ai/trust_engine.py | Implements core logic for Trust Engine functionality.  Supports the primary mission of institutio... | Logic Component |

## Memory (`memory/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implementation of LLM-Arithmetic Coding for Deep Archive.         Stores token probabilities pred... | Cognitive Actor (LLM-Integrated) |
| memory/memory_manager.py | Adaptive resource manager implementing RAM guards and triggering neural consolidation sleep cycles.
Manages the tiered memory stack, moving data between FAISS, Qdrant, and LanceDB based on saliency. | Ray Actor |
| memory/scratchpad.py | Implements core logic for Scratchpad functionality.  Supports the primary mission of memory withi... | Logic Component |
| memory/short_term/episodic_memory.py | Implements core logic for Episodic Memory functionality.  Supports the primary mission of short_t... | Logic Component |

## Memory Consolidation (`memory_consolidation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestration layer for memory_consolidation sub-components.  Coordinates communication and lifec... | Logic Component |
| memory_consolidation/consolidation_scheduler.py | Implements core logic for Consolidation Scheduler functionality.  Supports the primary mission of... | Logic Component |
| memory_consolidation/generative_trainer.py | Implements core logic for Generative Trainer functionality.  Supports the primary mission of memo... | Logic Component |
| memory_consolidation/hippocampal_replay.py | Implements core logic for Hippocampal Replay functionality.  Supports the primary mission of memo... | Logic Component |
| memory_consolidation/schema_manager.py | Orchestration layer for memory_consolidation sub-components.  Coordinates communication and lifec... | Logic Component |

## Meta Learning (`meta_learning/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Implements core logic for Adaptation Engine functionality.  Supports the primary mission of meta_... | Logic Component |
| meta_learning/meta_manager.py | Orchestration layer for meta_learning sub-components.  Coordinates communication and lifecycle ma... | Ray Actor (LLM Interface) |
| meta_learning/meta_policy.py | Implements core logic for Meta Policy functionality.  Supports the primary mission of meta_learni... | Logic Component |
| meta_learning/performance_tracker.py | Implements core logic for Performance Tracker functionality.  Supports the primary mission of met... | Logic Component |
| meta_learning/strategy_optimizer.py | Implements core logic for Strategy Optimizer functionality.  Supports the primary mission of meta... | Logic Component |

## Metacognition (`metacognition/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Implements core logic for Adaptation Engine functionality.  Supports the primary mission of metac... | Logic Component |
| metacognition/consensus_controller.py | Implements core logic for Consensus Controller functionality.  Supports the primary mission of me... | Logic Component |
| metacognition/mape_k_loop.py | Implements core logic for Mape K Loop functionality.  Supports the primary mission of metacogniti... | Logic Component |
| metacognition/meta_monitor.py | Implements core logic for Meta Monitor functionality.  Supports the primary mission of metacognit... | Logic Component |
| metacognition/meta_reasoner.py | SGI 2026: Semantic quality evaluation via LLM inference | Ray Actor (LLM Interface) |
| metacognition/metacognition_manager.py | Orchestration layer for metacognition sub-components.  Coordinates communication and lifecycle ma... | Ray Actor (LLM Interface) |
| metacognition/perception_reflector.py | Implements core logic for Perception Reflector functionality.  Supports the primary mission of me... | Logic Component |
| metacognition/transparency_engine.py | Implements core logic for Transparency Engine functionality.  Supports the primary mission of met... | Logic Component |

## Monitoring (`monitoring/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Implements core logic for Conformance Engine functionality.  Supports the primary mission of moni... | Logic Component |
| monitoring/drift_detector.py | Implements core logic for Drift Detector functionality.  Supports the primary mission of monitori... | Logic Component |
| monitoring/monitoring_manager.py | Orchestration layer for monitoring sub-components.  Coordinates communication and lifecycle manag... | Ray Actor (LLM Interface) |
| monitoring/risk_monitor.py | Implements core logic for Risk Monitor functionality.  Supports the primary mission of monitoring... | Logic Component |
| monitoring/semantic_trace.py | Implements core logic for Semantic Trace functionality.  Supports the primary mission of monitori... | Logic Component |
| monitoring/telemetry_collector.py | Implements core logic for Telemetry Collector functionality.  Supports the primary mission of mon... | Logic Component |
| monitoring/thermal_guard.py | Hardware protection module that monitors CPU temperature and load to prevent thermal throttling.
Acts as a system circuit breaker, pausing complex tasks if hardware limits are exceeded. | Ray Actor |

## Motivation (`motivation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Implements core logic for Curiosity functionality.  Supports the primary mission of motivation wi... | Logic Component |
| motivation/motivation_manager.py | Orchestration layer for motivation sub-components.  Coordinates communication and lifecycle manag... | Ray Actor (LLM Interface) |
| motivation/novelty.py | Implements core logic for Novelty functionality.  Supports the primary mission of motivation with... | Logic Component |
| motivation/reward_engine.py | Implements core logic for Reward Engine functionality.  Supports the primary mission of motivatio... | Logic Component |
| motivation/uncertainty.py | Implements core logic for Uncertainty functionality.  Supports the primary mission of motivation ... | Logic Component |

## Negotiation (`negotiation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Implements core logic for Compliance Engine functionality.  Supports the primary mission of negot... | Logic Component |
| negotiation/concession.py | Implements core logic for Concession functionality.  Supports the primary mission of negotiation ... | Logic Component |
| negotiation/consensus_engine.py | Implements core logic for Consensus Engine functionality.  Supports the primary mission of negoti... | Logic Component |
| negotiation/negotiation_manager.py | Orchestration layer for negotiation sub-components.  Coordinates communication and lifecycle mana... | Ray Actor (LLM Interface) |
| negotiation/negotiation_protocol.py | Implements core logic for Negotiation Protocol functionality.  Supports the primary mission of ne... | Logic Component |
| negotiation/proposal.py | Implements core logic for Proposal functionality.  Supports the primary mission of negotiation wi... | Logic Component |
| negotiation/treaty_graph.py | Implements core logic for Treaty Graph functionality.  Supports the primary mission of negotiatio... | Logic Component |
| negotiation/utility.py | Implements core logic for Utility functionality.  Supports the primary mission of negotiation wit... | Logic Component |

## Orchestration (`orchestration/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestration layer for orchestration sub-components.  Coordinates communication and lifecycle ma... | Logic Component |
| orchestration/event_router.py | Implements core logic for Event Router functionality.  Supports the primary mission of orchestrat... | Logic Component |
| orchestration/group_chat_coordinator.py | Implements core logic for Group Chat Coordinator functionality.  Supports the primary mission of ... | Logic Component |
| orchestration/interrupt_handler.py | Implements core logic for Interrupt Handler functionality.  Supports the primary mission of orche... | Logic Component |
| orchestration/orchestration_manager.py | Orchestration layer for orchestration sub-components.  Coordinates communication and lifecycle ma... | Ray Actor (LLM Interface) |
| orchestration/priority_scheduler.py | Implements core logic for Priority Scheduler functionality.  Supports the primary mission of orch... | Logic Component |
| orchestration/state_manager.py | Orchestration layer for orchestration sub-components.  Coordinates communication and lifecycle ma... | Logic Component |

## Purpleteam (`purpleteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Implements core logic for Bas Engine functionality.  Supports the primary mission of purpleteam w... | Logic Component |
| purpleteam/blue_agent.py | Implements core logic for Blue Agent functionality.  Supports the primary mission of purpleteam w... | Logic Component |
| purpleteam/fusion_orchestrator.py | Implements core logic for Fusion Orchestrator functionality.  Supports the primary mission of pur... | Logic Component |
| purpleteam/purple_manager.py | Orchestration layer for purpleteam sub-components.  Coordinates communication and lifecycle manag... | Ray Actor (LLM Interface) |
| purpleteam/red_agent.py | Implements core logic for Red Agent functionality.  Supports the primary mission of purpleteam wi... | Logic Component |
| purpleteam/remediation_engine.py | Implements core logic for Remediation Engine functionality.  Supports the primary mission of purp... | Logic Component |
| purpleteam/scoring_engine.py | Implements core logic for Scoring Engine functionality.  Supports the primary mission of purplete... | Logic Component |
| purpleteam/selfplay_engine.py | Implements core logic for Selfplay Engine functionality.  Supports the primary mission of purplet... | Logic Component |

## Redteam (`redteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Implements core logic for Adversarial Agent functionality.  Supports the primary mission of redte... | Logic Component |
| redteam/attack_library.py | Implements core logic for Attack Library functionality.  Supports the primary mission of redteam ... | Logic Component |
| redteam/ecosystem_simulator.py | Implements core logic for Ecosystem Simulator functionality.  Supports the primary mission of red... | Logic Component |
| redteam/exploit_generator.py | Implements core logic for Exploit Generator functionality.  Supports the primary mission of redte... | Logic Component |
| redteam/redteam_manager.py | Orchestration layer for redteam sub-components.  Coordinates communication and lifecycle manageme... | Logic Component |
| redteam/scenario_engine.py | Implements core logic for Scenario Engine functionality.  Supports the primary mission of redteam... | Logic Component |
| redteam/trajectory_simulator.py | Implements core logic for Trajectory Simulator functionality.  Supports the primary mission of re... | Logic Component |
| redteam/vulnerability_scoring.py | Implements core logic for Vulnerability Scoring functionality.  Supports the primary mission of r... | Logic Component |

## Runtime (`runtime/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Implements core logic for Agi Runtime functionality.  Supports the primary mission of runtime wit... | Logic Component |
| runtime/agi_state.py | Implements core logic for Agi State functionality.  Supports the primary mission of runtime withi... | Logic Component |
| runtime/event_bus.py | Implements core logic for Event Bus functionality.  Supports the primary mission of runtime withi... | Logic Component |
| runtime/governance_gateway.py | Implements core logic for Governance Gateway functionality.  Supports the primary mission of runt... | Logic Component |
| runtime/runtime_logger.py | Implements core logic for Runtime Logger functionality.  Supports the primary mission of runtime ... | Logic Component |
| runtime/safety_hooks.py | Implements core logic for Safety Hooks functionality.  Supports the primary mission of runtime wi... | Logic Component |
| runtime/scheduler.py | Implements core logic for Scheduler functionality.  Supports the primary mission of runtime withi... | Logic Component |

## Safety Ethics (`safety_ethics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Calculates cognitive load based on message frequency in a sliding window. | Logic Component |
| safety_ethics/conflict_resolver.py | Each option is a dict: {"action": ..., "ethical_score": ...} | Logic Component |
| safety_ethics/constraint_enforcer.py | Implements core logic for Constraint Enforcer functionality.  Supports the primary mission of saf... | Logic Component |
| safety_ethics/deception_detector.py | Implements core logic for Deception Detector functionality.  Supports the primary mission of safe... | Logic Component |
| safety_ethics/ethical_appraisal.py | Implements core logic for Ethical Appraisal functionality.  Supports the primary mission of safet... | Logic Component |
| safety_ethics/ethics_manager.py | Provides a safety score between 0 and 1.         Used by AttentionGate for proactive vetoing. | Logic Component |
| safety_ethics/governance_graph.py | Implements core logic for Governance Graph functionality.  Supports the primary mission of safety... | Logic Component |
| safety_ethics/interpretability_monitor.py | Placeholder: detect suspicious circuits or anomalous activations | Logic Component |
| safety_ethics/moral_reasoner.py | Implements core logic for Moral Reasoner functionality.  Supports the primary mission of safety_e... | Logic Component |
| safety_ethics/norm_library.py | Implements core logic for Norm Library functionality.  Supports the primary mission of safety_eth... | Logic Component |
| safety_ethics/oversight_agent.py | Implements core logic for Oversight Agent functionality.  Supports the primary mission of safety_... | Logic Component |
| safety_ethics/risk_classifier.py | Implements core logic for Risk Classifier functionality.  Supports the primary mission of safety_... | Logic Component |
| safety_ethics/safety_manager.py | Orchestrates multi-layered safety checks, including risk classification and behavioral constraints.
Provides a proactive safety gate that vets all cognitive actions before execution. | Ray Actor |
| safety_ethics/shutdown_controller.py | Implements core logic for Shutdown Controller functionality.  Supports the primary mission of saf... | Logic Component |

## Self Model (`self_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Implements core logic for Autobiographical Memory functionality.  Supports the primary mission of... | Logic Component |
| self_model/continuity_metrics.py | Implements core logic for Continuity Metrics functionality.  Supports the primary mission of self... | Logic Component |
| self_model/identity_kernel.py | Implements core logic for Identity Kernel functionality.  Supports the primary mission of self_mo... | Logic Component |
| self_model/reflective_endorsement.py | Implements core logic for Reflective Endorsement functionality.  Supports the primary mission of ... | Logic Component |
| self_model/self_manager.py | Orchestration layer for self_model sub-components.  Coordinates communication and lifecycle manag... | Ray Actor (LLM Interface) |
| self_model/temporal_self.py | Implements core logic for Temporal Self functionality.  Supports the primary mission of self_mode... | Logic Component |

## Simulation (`simulation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Implements core logic for Agent Adapter functionality.  Supports the primary mission of simulatio... | Logic Component |
| simulation/environment.py | Implements core logic for Environment functionality.  Supports the primary mission of simulation ... | Logic Component |
| simulation/governance_interventions.py | Implements core logic for Governance Interventions functionality.  Supports the primary mission o... | Logic Component |
| simulation/interaction_protocol.py | Implements core logic for Interaction Protocol functionality.  Supports the primary mission of si... | Logic Component |
| simulation/metrics_engine.py | Implements core logic for Metrics Engine functionality.  Supports the primary mission of simulati... | Logic Component |
| simulation/replay_buffer.py | Implements core logic for Replay Buffer functionality.  Supports the primary mission of simulatio... | Logic Component |
| simulation/sim_core.py | Implements core logic for Sim Core functionality.  Supports the primary mission of simulation wit... | Logic Component |
| simulation/simulation_manager.py | Orchestration layer for simulation sub-components.  Coordinates communication and lifecycle manag... | Ray Actor (LLM Interface) |

## Tests (`tests/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Implements core logic for Test Sgi Features functionality.  Supports the primary mission of tests... | Logic Component |

## Training (`training/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Implements core logic for Curriculum functionality.  Supports the primary mission of training wit... | Logic Component |
| training/meta_learning.py | Implements core logic for Meta Learning functionality.  Supports the primary mission of training ... | Logic Component |
| training/rl_trainer.py | Placeholder: choose best known action | Logic Component |
| training/self_supervised.py | Implements core logic for Self Supervised functionality.  Supports the primary mission of trainin... | Logic Component |
| training/training_manager.py | Orchestration layer for training sub-components.  Coordinates communication and lifecycle managem... | Ray Actor (LLM Interface) |
| training/world_model_trainer.py | Update causal graph or state based on new data | Logic Component |

## World Model (`world_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Implements core logic for Causal Graph functionality.  Supports the primary mission of world_mode... | Logic Component |
| world_model/counterfactuals.py | Implements core logic for Counterfactuals functionality.  Supports the primary mission of world_m... | Logic Component |
| world_model/manager.py | Maintains the system's Digital Twin, simulating causal effects and tracking external environment state.
Uses causal graphs and counterfactual reasoning to predict the outcomes of potential actions. | Ray Actor |
| world_model/prediction.py | Implements core logic for Prediction functionality.  Supports the primary mission of world_model ... | Logic Component |
| world_model/simulator.py | Update external entities based on causal effects | Logic Component |
| world_model/state.py | Identifies discrepancies between predicted and observed states. | Logic Component |
