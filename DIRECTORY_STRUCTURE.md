# SGI-Alpha Directory Structure and Integration Map

This document provides a detailed overview of every file in the SGI-Alpha repository, <br>explaining its purpose and its specific role within the LLM-driven APW architecture.

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| AGENTS.md | Implements core AGENTS.md logic. Supports the primary <br>functional requirements of the  subsystem within the SGI framework. | Utility/Config |
| README.md | Implements core README.md logic. Supports the primary <br>functional requirements of the  subsystem within the SGI framework. | Utility/Config |
| compilation_errors.log | System diagnostic log file capturing detailed telemetry and runtime events for compilation errors monitoring. | Utility/Config |
| config.yaml | The authoritative system configuration manifest. It defines hardware-specific thread limits, thermal thresholds for the 15W TDP CPU, memory safety guards to prevent system crashes on 16GB RAM, and tiered precision standards for various cognitive components. | Utility/Config |
| find_invalid_py.py | Implements core find invalid py logic. Supports the primary <br>functional requirements of the  subsystem within the SGI framework. | Utility/Config |
| hardware_verification.log | System diagnostic log file capturing detailed telemetry and runtime events for hardware verification monitoring. | Utility/Config |
| main.py | The primary system entry point for SGI-Alpha. It orchestrates the initialization of Ray distributed compute, the shared singleton model registry for memory-efficient LLM inference, and the main cognitive heartbeat loop that drives autonomous operation on Intel i5-8265U hardware. | Logic Component |
| setup_8265u.sh | Implements core setup 8265u.sh logic. Supports the primary <br>functional requirements of the  subsystem within the SGI framework. | Utility/Config |

## Actors (`actors/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | A specialized polyglot execution agent capable of sandboxed code execution within Firecracker microVMs. It implements AST-aware KV cache compression (CodeComp) and Digital Twin branching to maintain context integrity during complex development tasks. | Ray Actor (Distributed) |
| actors/critic_actor.py | Implements core critic actor logic. Supports the primary <br>functional requirements of the actors subsystem within the SGI framework. | Ray Actor (Distributed) |
| actors/planner.py | The system's strategic reasoning module that decomposes high-level user objectives into hierarchical, actionable task sequences. It utilizes the shared LLM to perform task decomposition and continuously validates results against the original mission goals. | Ray Actor (Distributed) |
| actors/reasoner_actor.py | A high-fidelity logical inference engine that integrates Z3 SMT solvers for formal verification. It operates natively in sym_int8 precision to achieve maximum AVX2 throughput on Intel hardware while proving code correctness and logical consistency. | Ray Actor (Distributed) |
| actors/search_actor.py | A multi-stage agentic RAG pipeline component that performs autonomous online research using Tavily and SearXNG. It enforces a strict License Guardian gate to prevent the ingestion of GPL/LGPL licensed code into the system's knowledge base. | Ray Actor (Distributed) |
| actors/self_model.py | Implements core self model logic. Supports the primary <br>functional requirements of the actors subsystem within the SGI framework. | Cognitive Module (Integrated) |
| actors/social/discourse.py | Implements core discourse logic. Supports the primary <br>functional requirements of the social subsystem within the SGI framework. | Cognitive Module (Integrated) |
| actors/social/social_reasoner.py | Implements core social reasoner logic. Supports the primary <br>functional requirements of the social subsystem within the SGI framework. | Ray Actor (Distributed) |
| actors/social/theory_of_mind.py | Implements core theory of mind logic. Supports the primary <br>functional requirements of the social subsystem within the SGI framework. | Ray Actor (Distributed) |
| actors/vision.py | Implementation of NeuralLVC / CoPE for Video/Vision data.         Achieves up to 93% reduction in token usage for VideoLMs. | Cognitive Module (Integrated) |

## Blueteam (`blueteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Implements core adaptive defense agent logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/blueteam_manager.py | Orchestration layer for Blueteam operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| blueteam/cyber_range.py | Implements core cyber range logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/deception_layer.py | Implements core deception layer logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/defense_orchestrator.py | Implements core defense orchestrator logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/detection_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| blueteam/dlp_agent.py | Implements core dlp agent logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/firewall_agent.py | Implements core firewall agent logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |
| blueteam/forensic_agent.py | Implements core forensic agent logic. Supports the primary <br>functional requirements of the blueteam subsystem within the SGI framework. | Logic Component |

## Cee Layer (`cee_layer/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Orchestration layer for Cee Layer operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| cee_layer/cognitive_affective_bridge.py | Implements core cognitive affective bridge logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |
| cee_layer/emotion_appraisal.py | Implements core emotion appraisal logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |
| cee_layer/emotion_generator.py | Implements core emotion generator logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |
| cee_layer/emotion_regulator.py | Implements core emotion regulator logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |
| cee_layer/ethical_evaluator.py | Implements core ethical evaluator logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |
| cee_layer/moral_weighting.py | Implements core moral weighting logic. Supports the primary <br>functional requirements of the cee_layer subsystem within the SGI framework. | Logic Component |

## Conflict Resolution (`conflict_resolution/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Orchestration layer for Conflict Resolution operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| conflict_resolution/contradiction_detector.py | Implements core contradiction detector logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |
| conflict_resolution/ethical_appraisal.py | Implements core ethical appraisal logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |
| conflict_resolution/moral_agents.py | Implements core moral agents logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Implements core probabilistic reasoner logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |
| conflict_resolution/resolution_protocol.py | Implements core resolution protocol logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |
| conflict_resolution/survivability_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| conflict_resolution/value_arbitration.py | Implements core value arbitration logic. Supports the primary <br>functional requirements of the conflict_resolution subsystem within the SGI framework. | Logic Component |

## Console (`console/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Implements core action queue logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |
| console/approval_gateway.py | Implements core approval gateway logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |
| console/audit_log.py | Implements core audit log logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |
| console/confidence_monitor.py | Implements core confidence monitor logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |
| console/console_manager.py | Orchestration layer for Console operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| console/escalation_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| console/human_interface.py | Implements core human interface logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |
| console/oversight_dashboard.py | Implements core oversight dashboard logic. Supports the primary <br>functional requirements of the console subsystem within the SGI framework. | Logic Component |

## Core (`core/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Provides the fundamental base class (CognitiveModule) for all integrated SGI agents. It implements automated registration with the Global Workspace, standardizes constructor signatures, and provides a unified asynchronous message routing interface. | Cognitive Module (Integrated) |
| core/config.py | Implements core config logic. Supports the primary <br>functional requirements of the core subsystem within the SGI framework. | Utility/Config |
| core/controller.py | Tracks pulse-active modules. | Logic Component |
| core/drives.py | Implements core drives logic. Supports the primary <br>functional requirements of the core subsystem within the SGI framework. | Logic Component |
| core/heartbeat.py | Implements core heartbeat logic. Supports the primary <br>functional requirements of the core subsystem within the SGI framework. | Logic Component |
| core/message_bus/fast_path.py | Simulates Flash-Optimized LZ4 compression for Tier 1 (Ephemeral) storage.     Focuses on sub-millisecond latency for the Reflex Arc. | Logic Component |
| core/message_bus/priority_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| core/message_bus/router.py | Implements core router logic. Supports the primary <br>functional requirements of the message_bus subsystem within the SGI framework. | Logic Component |
| core/model_registry.py | Singleton Model Provider to prevent RAM crash on 16GB systems.     Loads the model once and provides inference for specialized actors. | Ray Actor (Distributed) |
| core/scheduler.py | A priority-based task orchestrator (Ray Actor) that manages the execution queue for all cognitive workloads. It ensures efficient delegation of tasks to specialized actors based on system entropy, priority metrics, and real-time hardware availability. | Ray Actor (Distributed) |
| core/workspace.py | The distributed state manager (GlobalWorkspace) implemented as a Ray Actor. It maintains the system's message history, manages current broadcasts, and ensures state consistency and event synchronization across all registered asynchronous agents. | Ray Actor (Distributed) |

## Deployment (`deployment/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Implements core agent registry logic. Supports the primary <br>functional requirements of the deployment subsystem within the SGI framework. | Logic Component |
| deployment/deployment_manager.py | Orchestration layer for Deployment operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |
| deployment/policy_loader.py | Implements core policy loader logic. Supports the primary <br>functional requirements of the deployment subsystem within the SGI framework. | Logic Component |
| deployment/runtime_env.py | Implements core runtime env logic. Supports the primary <br>functional requirements of the deployment subsystem within the SGI framework. | Logic Component |
| deployment/version_manager.py | Orchestration layer for Deployment operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |

## Economics (`economics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Implements core agent policy logic. Supports the primary <br>functional requirements of the economics subsystem within the SGI framework. | Logic Component |
| economics/context_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| economics/coordination_protocol.py | Implements core coordination protocol logic. Supports the primary <br>functional requirements of the economics subsystem within the SGI framework. | Logic Component |
| economics/economic_manager.py | Orchestration layer for Economics operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| economics/fairness_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| economics/optimizer.py | Implements core optimizer logic. Supports the primary <br>functional requirements of the economics subsystem within the SGI framework. | Logic Component |
| economics/orchestration_layer.py | Implements core orchestration layer logic. Supports the primary <br>functional requirements of the economics subsystem within the SGI framework. | Logic Component |
| economics/resource_model.py | Implements core resource model logic. Supports the primary <br>functional requirements of the economics subsystem within the SGI framework. | Logic Component |
| economics/utility_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |

## Emotion (`emotion/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Implements core affective reasoner logic. Supports the primary <br>functional requirements of the emotion subsystem within the SGI framework. | Logic Component |
| emotion/affective_state.py | Implements core affective state logic. Supports the primary <br>functional requirements of the emotion subsystem within the SGI framework. | Logic Component |
| emotion/appraisal.py | Implements core appraisal logic. Supports the primary <br>functional requirements of the emotion subsystem within the SGI framework. | Logic Component |
| emotion/emotion_manager.py | Orchestration layer for Emotion operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |

## Incident Response (`incident_response/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Implements core audit logger logic. Supports the primary <br>functional requirements of the incident_response subsystem within the SGI framework. | Logic Component |
| incident_response/containment_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| incident_response/detectors.py | Implements core detectors logic. Supports the primary <br>functional requirements of the incident_response subsystem within the SGI framework. | Logic Component |
| incident_response/eradication_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| incident_response/incident_classifier.py | Implements core incident classifier logic. Supports the primary <br>functional requirements of the incident_response subsystem within the SGI framework. | Logic Component |
| incident_response/incident_manager.py | Orchestration layer for Incident Response operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| incident_response/recovery_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| incident_response/semantic_checks.py | Implements core semantic checks logic. Supports the primary <br>functional requirements of the incident_response subsystem within the SGI framework. | Logic Component |

## Institutional Ai (`institutional_ai/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Implements core coordination layer logic. Supports the primary <br>functional requirements of the institutional_ai subsystem within the SGI framework. | Logic Component |
| institutional_ai/governance_graph.py | Implements core governance graph logic. Supports the primary <br>functional requirements of the institutional_ai subsystem within the SGI framework. | Logic Component |
| institutional_ai/incentive_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| institutional_ai/institutional_manager.py | Orchestration layer for Institutional Ai operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |
| institutional_ai/oversight_agents.py | Implements core oversight agents logic. Supports the primary <br>functional requirements of the institutional_ai subsystem within the SGI framework. | Logic Component |
| institutional_ai/real_time_control.py | Implements core real time control logic. Supports the primary <br>functional requirements of the institutional_ai subsystem within the SGI framework. | Logic Component |
| institutional_ai/role_definitions.py | Implements core role definitions logic. Supports the primary <br>functional requirements of the institutional_ai subsystem within the SGI framework. | Logic Component |
| institutional_ai/rule_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| institutional_ai/sanction_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| institutional_ai/trust_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |

## Memory (`memory/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Implementation of LLM-Arithmetic Coding for Deep Archive.         Stores token probabilities predicted by the LLM for massive compression ratios. | Cognitive Module (Integrated) |
| memory/memory_manager.py | An adaptive resource manager that implements RAM guards to prevent OOM events. It triggers neural consolidation sleep cycles for background refactoring and memory indexing, utilizing LLM-Zip for Tier 3 deep neural archiving. | Ray Actor (Distributed) |
| memory/scratchpad.py | Implements core scratchpad logic. Supports the primary <br>functional requirements of the memory subsystem within the SGI framework. | Logic Component |
| memory/short_term/episodic_memory.py | Implements core episodic memory logic. Supports the primary <br>functional requirements of the short_term subsystem within the SGI framework. | Logic Component |

## Memory Consolidation (`memory_consolidation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Orchestration layer for Memory Consolidation operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| memory_consolidation/consolidation_scheduler.py | Implements core consolidation scheduler logic. Supports the primary <br>functional requirements of the memory_consolidation subsystem within the SGI framework. | Logic Component |
| memory_consolidation/generative_trainer.py | Implements core generative trainer logic. Supports the primary <br>functional requirements of the memory_consolidation subsystem within the SGI framework. | Logic Component |
| memory_consolidation/hippocampal_replay.py | Implements core hippocampal replay logic. Supports the primary <br>functional requirements of the memory_consolidation subsystem within the SGI framework. | Logic Component |
| memory_consolidation/schema_manager.py | Orchestration layer for Memory Consolidation operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |

## Meta Learning (`meta_learning/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| meta_learning/meta_manager.py | Orchestration layer for Meta Learning operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| meta_learning/meta_policy.py | Implements core meta policy logic. Supports the primary <br>functional requirements of the meta_learning subsystem within the SGI framework. | Logic Component |
| meta_learning/performance_tracker.py | Implements core performance tracker logic. Supports the primary <br>functional requirements of the meta_learning subsystem within the SGI framework. | Logic Component |
| meta_learning/strategy_optimizer.py | Implements core strategy optimizer logic. Supports the primary <br>functional requirements of the meta_learning subsystem within the SGI framework. | Logic Component |

## Metacognition (`metacognition/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| metacognition/consensus_controller.py | Implements core consensus controller logic. Supports the primary <br>functional requirements of the metacognition subsystem within the SGI framework. | Logic Component |
| metacognition/mape_k_loop.py | Implements core mape k loop logic. Supports the primary <br>functional requirements of the metacognition subsystem within the SGI framework. | Logic Component |
| metacognition/meta_monitor.py | Implements core meta monitor logic. Supports the primary <br>functional requirements of the metacognition subsystem within the SGI framework. | Logic Component |
| metacognition/meta_reasoner.py | Implements core meta reasoner logic. Supports the primary <br>functional requirements of the metacognition subsystem within the SGI framework. | Ray Actor (Distributed) |
| metacognition/metacognition_manager.py | Orchestration layer for Metacognition operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| metacognition/perception_reflector.py | Implements core perception reflector logic. Supports the primary <br>functional requirements of the metacognition subsystem within the SGI framework. | Logic Component |
| metacognition/transparency_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |

## Monitoring (`monitoring/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| monitoring/drift_detector.py | Implements core drift detector logic. Supports the primary <br>functional requirements of the monitoring subsystem within the SGI framework. | Logic Component |
| monitoring/monitoring_manager.py | Orchestration layer for Monitoring operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| monitoring/risk_monitor.py | Implements core risk monitor logic. Supports the primary <br>functional requirements of the monitoring subsystem within the SGI framework. | Logic Component |
| monitoring/semantic_trace.py | Implements core semantic trace logic. Supports the primary <br>functional requirements of the monitoring subsystem within the SGI framework. | Logic Component |
| monitoring/telemetry_collector.py | Implements core telemetry collector logic. Supports the primary <br>functional requirements of the monitoring subsystem within the SGI framework. | Logic Component |
| monitoring/thermal_guard.py | A hardware-aware safety circuit breaker that monitors CPU load and temperature. It prevents thermal throttling on the Intel Whiskey Lake architecture by pausing intensive cognitive tasks during overheat events to protect system health. | Ray Actor (Distributed) |

## Motivation (`motivation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Implements core curiosity logic. Supports the primary <br>functional requirements of the motivation subsystem within the SGI framework. | Logic Component |
| motivation/motivation_manager.py | Orchestration layer for Motivation operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| motivation/novelty.py | Implements core novelty logic. Supports the primary <br>functional requirements of the motivation subsystem within the SGI framework. | Logic Component |
| motivation/reward_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| motivation/uncertainty.py | Implements core uncertainty logic. Supports the primary <br>functional requirements of the motivation subsystem within the SGI framework. | Logic Component |

## Negotiation (`negotiation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| negotiation/concession.py | Implements core concession logic. Supports the primary <br>functional requirements of the negotiation subsystem within the SGI framework. | Logic Component |
| negotiation/consensus_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| negotiation/negotiation_manager.py | Orchestration layer for Negotiation operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| negotiation/negotiation_protocol.py | Implements core negotiation protocol logic. Supports the primary <br>functional requirements of the negotiation subsystem within the SGI framework. | Logic Component |
| negotiation/proposal.py | Implements core proposal logic. Supports the primary <br>functional requirements of the negotiation subsystem within the SGI framework. | Logic Component |
| negotiation/treaty_graph.py | Implements core treaty graph logic. Supports the primary <br>functional requirements of the negotiation subsystem within the SGI framework. | Logic Component |
| negotiation/utility.py | Implements core utility logic. Supports the primary <br>functional requirements of the negotiation subsystem within the SGI framework. | Logic Component |

## Orchestration (`orchestration/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Orchestration layer for Orchestration operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |
| orchestration/event_router.py | Implements core event router logic. Supports the primary <br>functional requirements of the orchestration subsystem within the SGI framework. | Logic Component |
| orchestration/group_chat_coordinator.py | Implements core group chat coordinator logic. Supports the primary <br>functional requirements of the orchestration subsystem within the SGI framework. | Logic Component |
| orchestration/interrupt_handler.py | Implements core interrupt handler logic. Supports the primary <br>functional requirements of the orchestration subsystem within the SGI framework. | Logic Component |
| orchestration/orchestration_manager.py | A high-level coordinator for multi-agent workflows. It manages group chat sessions, concurrent task execution, and resource allocation across the actor pool to ensure efficient and conflict-free collaboration on complex objectives. | Ray Actor (Distributed) |
| orchestration/priority_scheduler.py | Implements core priority scheduler logic. Supports the primary <br>functional requirements of the orchestration subsystem within the SGI framework. | Logic Component |
| orchestration/state_manager.py | Orchestration layer for Orchestration operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Logic Component |

## Purpleteam (`purpleteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| purpleteam/blue_agent.py | Implements core blue agent logic. Supports the primary <br>functional requirements of the purpleteam subsystem within the SGI framework. | Logic Component |
| purpleteam/fusion_orchestrator.py | Implements core fusion orchestrator logic. Supports the primary <br>functional requirements of the purpleteam subsystem within the SGI framework. | Logic Component |
| purpleteam/purple_manager.py | Simulates adversarial scenarios using integrated red and blue agents to stress-test system security and resilience. It orchestrates automated remediation and self-play evolution cycles to harden the SGI against sophisticated cyber threats. | Ray Actor (Distributed) |
| purpleteam/red_agent.py | Implements core red agent logic. Supports the primary <br>functional requirements of the purpleteam subsystem within the SGI framework. | Logic Component |
| purpleteam/remediation_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| purpleteam/scoring_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| purpleteam/selfplay_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |

## Redteam (`redteam/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Implements core adversarial agent logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |
| redteam/attack_library.py | Implements core attack library logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |
| redteam/ecosystem_simulator.py | Implements core ecosystem simulator logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |
| redteam/exploit_generator.py | Implements core exploit generator logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |
| redteam/redteam_manager.py | Orchestration layer for Redteam operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| redteam/scenario_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| redteam/trajectory_simulator.py | Implements core trajectory simulator logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |
| redteam/vulnerability_scoring.py | Implements core vulnerability scoring logic. Supports the primary <br>functional requirements of the redteam subsystem within the SGI framework. | Logic Component |

## Runtime (`runtime/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Implements core agi runtime logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/agi_state.py | Implements core agi state logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/event_bus.py | Implements core event bus logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/governance_gateway.py | Implements core governance gateway logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/runtime_logger.py | Implements core runtime logger logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/safety_hooks.py | Implements core safety hooks logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |
| runtime/scheduler.py | Implements core scheduler logic. Supports the primary <br>functional requirements of the runtime subsystem within the SGI framework. | Logic Component |

## Safety Ethics (`safety_ethics/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Calculates cognitive load based on message frequency in a sliding window. | Logic Component |
| safety_ethics/conflict_resolver.py | Implements core conflict resolver logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/constraint_enforcer.py | Implements core constraint enforcer logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/deception_detector.py | Implements core deception detector logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/ethical_appraisal.py | Implements core ethical appraisal logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/ethics_manager.py | Provides a safety score between 0 and 1.         Used by AttentionGate for proactive vetoing. | Logic Component |
| safety_ethics/governance_graph.py | Implements core governance graph logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/interpretability_monitor.py | Implements core interpretability monitor logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/moral_reasoner.py | Implements core moral reasoner logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/norm_library.py | Implements core norm library logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/oversight_agent.py | Implements core oversight agent logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/risk_classifier.py | Implements core risk classifier logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |
| safety_ethics/safety_manager.py | Orchestration layer for Safety Ethics operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| safety_ethics/shutdown_controller.py | Implements core shutdown controller logic. Supports the primary <br>functional requirements of the safety_ethics subsystem within the SGI framework. | Logic Component |

## Self Model (`self_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Implements core autobiographical memory logic. Supports the primary <br>functional requirements of the self_model subsystem within the SGI framework. | Logic Component |
| self_model/continuity_metrics.py | Implements core continuity metrics logic. Supports the primary <br>functional requirements of the self_model subsystem within the SGI framework. | Logic Component |
| self_model/identity_kernel.py | Implements core identity kernel logic. Supports the primary <br>functional requirements of the self_model subsystem within the SGI framework. | Logic Component |
| self_model/reflective_endorsement.py | Implements core reflective endorsement logic. Supports the primary <br>functional requirements of the self_model subsystem within the SGI framework. | Logic Component |
| self_model/self_manager.py | Orchestration layer for Self Model operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| self_model/temporal_self.py | Implements core temporal self logic. Supports the primary <br>functional requirements of the self_model subsystem within the SGI framework. | Logic Component |

## Simulation (`simulation/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Implements core agent adapter logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/environment.py | Implements core environment logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/governance_interventions.py | Implements core governance interventions logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/interaction_protocol.py | Implements core interaction protocol logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/metrics_engine.py | A core logic engine for specialized domain processing. Implements the underlying <br>algorithms and state transformations required for functional objectives within the system. | Logic Component |
| simulation/replay_buffer.py | Implements core replay buffer logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/sim_core.py | Implements core sim core logic. Supports the primary <br>functional requirements of the simulation subsystem within the SGI framework. | Logic Component |
| simulation/simulation_manager.py | Orchestration layer for Simulation operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |

## Tests (`tests/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Implements core test sgi features logic. Supports the primary <br>functional requirements of the tests subsystem within the SGI framework. | Logic Component |

## Training (`training/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Implements core curriculum logic. Supports the primary <br>functional requirements of the training subsystem within the SGI framework. | Logic Component |
| training/meta_learning.py | Implements core meta learning logic. Supports the primary <br>functional requirements of the training subsystem within the SGI framework. | Logic Component |
| training/rl_trainer.py | Implements core rl trainer logic. Supports the primary <br>functional requirements of the training subsystem within the SGI framework. | Logic Component |
| training/self_supervised.py | Implements core self supervised logic. Supports the primary <br>functional requirements of the training subsystem within the SGI framework. | Logic Component |
| training/training_manager.py | Orchestrates autonomous self-improvement cycles through self-supervised and reinforcement learning. It integrates world-model updates and meta-learning strategies to refine agent performance and adapt to new problem domains over time. | Ray Actor (Distributed) |
| training/world_model_trainer.py | Implements core world model trainer logic. Supports the primary <br>functional requirements of the training subsystem within the SGI framework. | Logic Component |

## World Model (`world_model/`)

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Implements core causal graph logic. Supports the primary <br>functional requirements of the world_model subsystem within the SGI framework. | Logic Component |
| world_model/counterfactuals.py | Implements core counterfactuals logic. Supports the primary <br>functional requirements of the world_model subsystem within the SGI framework. | Logic Component |
| world_model/manager.py | Orchestration layer for World Model operations. Coordinates communication <br>and manages the life-cycle of specialized agents within the distributed workspace architecture. | Ray Actor (Distributed) |
| world_model/prediction.py | Implements core prediction logic. Supports the primary <br>functional requirements of the world_model subsystem within the SGI framework. | Logic Component |
| world_model/simulator.py | Implements core simulator logic. Supports the primary <br>functional requirements of the world_model subsystem within the SGI framework. | Logic Component |
| world_model/state.py | Identifies discrepancies between predicted and observed states. | Logic Component |
