# SGI-Alpha Directory Structure and LLM Integration Map

Mapping of the Synthetic General Intelligence (SGI) architecture, documenting filenames, descriptions, and integration roles.

## Actors

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/coding_actor.py | Distributed Ray actor specialized in coding tasks, implementing autonomous receive, calculate_confidence_score logic. | Ray Actor (Distributed) |
| actors/critic_actor.py | Functional component implementing InternalCritic with core focus on critique_code, receive. | Ray Actor (Distributed) |
| actors/planner.py | Functional component implementing Planner with core focus on receive, create_plan. | Ray Actor (Distributed) |
| actors/reasoner_actor.py | Distributed Ray actor specialized in reasoner tasks, implementing autonomous receive, reason logic. | Ray Actor (Distributed) |
| actors/search_actor.py | Distributed Ray actor specialized in technical search and RAG, implementing Matryoshka-Tiered Retrieval and SIMD-optimized reranking. | Ray Actor (Distributed) |
| actors/self_model.py | Functional component implementing SelfModel with core focus on receive, update_state. | Cognitive Module (Integrated) |
| actors/vision.py | Functional component implementing VisionModule with core focus on receive, process_image. | Cognitive Module (Integrated) |

## Actors/Social

| File | Description | Integration Role |
| :--- | :--- | :--- |
| actors/social/discourse.py | Functional component implementing DiscourseModule with core focus on receive, analyze_pragmatics. | Cognitive Module (Integrated) |
| actors/social/social_reasoner.py | Functional component implementing SocialReasoner with core focus on receive, get_context. | Ray Actor (Distributed) |
| actors/social/theory_of_mind.py | Functional component implementing TheoryOfMind with core focus on receive, update_agent_model. | Ray Actor (Distributed) |

## Blueteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| blueteam/adaptive_defense_agent.py | Functional component implementing AdaptiveDefenseAgent with core focus on respond. | Logic Component |
| blueteam/blueteam_manager.py | Central orchestrator for the Blueteam subsystem. Manages agent lifecycles and coordinates message-passing for defend, receive tasks. | Ray Actor (Distributed) |
| blueteam/cyber_range.py | Functional component implementing CyberRange with core focus on simulate_traffic. | Logic Component |
| blueteam/deception_layer.py | Functional component implementing DeceptionLayer with core focus on deploy_honeypot. | Logic Component |
| blueteam/defense_orchestrator.py | Functional component implementing DefenseOrchestrator with core focus on orchestrate. | Logic Component |
| blueteam/detection_engine.py | Computational engine implementing detection algorithms and state transformations for the blueteam module. | Logic Component |
| blueteam/dlp_agent.py | Functional component implementing DLPAagent with core focus on inspect. | Logic Component |
| blueteam/firewall_agent.py | Functional component implementing FirewallAgent with core focus on filter, receive. | Cognitive Module (Integrated) |
| blueteam/forensic_agent.py | Functional component implementing ForensicAgent with core focus on analyze. | Logic Component |

## Cee Layer

| File | Description | Integration Role |
| :--- | :--- | :--- |
| cee_layer/cee_manager.py | Central orchestrator for the Cee Layer subsystem. Manages agent lifecycles and coordinates message-passing for process, receive tasks. | Ray Actor (Distributed) |
| cee_layer/cognitive_affective_bridge.py | Functional component implementing CognitiveAffectiveBridge with core focus on modulate. | Logic Component |
| cee_layer/emotion_appraisal.py | Functional component implementing EmotionAppraisal with core focus on appraise. | Logic Component |
| cee_layer/emotion_generator.py | Functional component implementing EmotionGenerator with core focus on generate. | Logic Component |
| cee_layer/emotion_regulator.py | Functional component implementing EmotionRegulator with core focus on regulate. | Logic Component |
| cee_layer/ethical_evaluator.py | Functional component implementing EthicalEvaluator with core focus on evaluate. | Logic Component |
| cee_layer/moral_weighting.py | Functional component implementing MoralWeighting with core focus on weight. | Logic Component |

## Conflict Resolution

| File | Description | Integration Role |
| :--- | :--- | :--- |
| conflict_resolution/conflict_manager.py | Central orchestrator for the Conflict Resolution subsystem. Manages agent lifecycles and coordinates message-passing for resolve, receive tasks. | Ray Actor (Distributed) |
| conflict_resolution/contradiction_detector.py | Functional component implementing ContradictionDetector with core focus on detect. | Logic Component |
| conflict_resolution/ethical_appraisal.py | Functional component implementing EthicalAppraisal with core focus on evaluate. | Logic Component |
| conflict_resolution/moral_agents.py | Functional component implementing MoralAgent with core focus on argue. | Logic Component |
| conflict_resolution/probabilistic_reasoner.py | Functional component implementing ProbabilisticReasoner with core focus on infer. | Logic Component |
| conflict_resolution/resolution_protocol.py | Functional component implementing ResolutionProtocol with core focus on resolve. | Logic Component |
| conflict_resolution/survivability_engine.py | Computational engine implementing survivability algorithms and state transformations for the conflict_resolution module. | Logic Component |
| conflict_resolution/value_arbitration.py | Functional component implementing ValueArbitration with core focus on arbitrate. | Logic Component |

## Console

| File | Description | Integration Role |
| :--- | :--- | :--- |
| console/action_queue.py | Functional component implementing ActionQueue with core focus on enqueue, dequeue. | Logic Component |
| console/approval_gateway.py | Functional component implementing ApprovalGateway with core focus on request_approval, approve. | Logic Component |
| console/audit_log.py | Functional component implementing AuditLog with core focus on record, view. | Logic Component |
| console/confidence_monitor.py | Functional component implementing ConfidenceMonitor with core focus on evaluate. | Logic Component |
| console/console_manager.py | Central orchestrator for the Console subsystem. Manages agent lifecycles and coordinates message-passing for review_action, process_queue tasks. | Ray Actor (Distributed) |
| console/escalation_engine.py | Computational engine implementing escalation algorithms and state transformations for the console module. | Logic Component |
| console/human_interface.py | Functional component implementing HumanInterface with core focus on present, get_decision. | Logic Component |
| console/oversight_dashboard.py | Functional component implementing OversightDashboard with core focus on update, view. | Logic Component |

## Core

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/base.py | Functional component implementing CognitiveModule with core focus on receive. | Cognitive Module (Integrated) |
| core/config.py | Functional component implementing config logic within the core framework. | Logic Component |
| core/controller.py | Functional component implementing DPSController with core focus on monitor_heartbeat, reload_config. | Logic Component |
| core/drives.py | Computational engine implementing drive algorithms and state transformations for the core module. | Logic Component |
| core/heartbeat.py | Functional component implementing CognitiveHeartbeat with core focus on heartbeat_tick, run. | Logic Component |
| core/model_registry.py | Distributed Ray actor providing a RAM-optimized singleton for Tier 3 models, implementing Speculative Lookahead and Paged KV management. | Ray Actor (Distributed) |
| core/scheduler.py | Functional component implementing Scheduler with core focus on submit, next. | Ray Actor (Distributed) |
| core/workspace.py | Functional component implementing GlobalWorkspace with core focus on register, broadcast. | Ray Actor (Distributed) |

## Core/Message Bus

| File | Description | Integration Role |
| :--- | :--- | :--- |
| core/message_bus/fast_path.py | Functional component implementing FastPathLZ4 with core focus on compress, decompress. | Logic Component |
| core/message_bus/priority_engine.py | Computational engine implementing priority algorithms and state transformations for the message_bus module. | Logic Component |
| core/message_bus/router.py | Functional component implementing TaskRouter with core focus on route. | Logic Component |

## Deployment

| File | Description | Integration Role |
| :--- | :--- | :--- |
| deployment/agent_registry.py | Functional component implementing AgentRegistry with core focus on register, get. | Logic Component |
| deployment/deployment_manager.py | Central orchestrator for the Deployment subsystem. Manages agent lifecycles and coordinates message-passing for deploy, receive tasks. | Ray Actor (Distributed) |
| deployment/policy_loader.py | Functional component implementing PolicyLoader with core focus on load, get. | Logic Component |
| deployment/runtime_env.py | Functional component implementing RuntimeEnvironment with core focus on launch_agent, stop_agent. | Logic Component |
| deployment/version_manager.py | Central orchestrator for the Deployment subsystem. Manages agent lifecycles and coordinates message-passing for record_version, latest tasks. | Ray Actor (Distributed) |

## Economics

| File | Description | Integration Role |
| :--- | :--- | :--- |
| economics/agent_policy.py | Functional component implementing AgentPolicy with core focus on act. | Logic Component |
| economics/context_engine.py | Computational engine implementing context algorithms and state transformations for the economics module. | Logic Component |
| economics/coordination_protocol.py | Functional component implementing CoordinationProtocol with core focus on consensus. | Logic Component |
| economics/economic_manager.py | Central orchestrator for the Economics subsystem. Manages agent lifecycles and coordinates message-passing for allocate, receive tasks. | Ray Actor (Distributed) |
| economics/fairness_engine.py | Computational engine implementing fairness algorithms and state transformations for the economics module. | Logic Component |
| economics/optimizer.py | Functional component implementing Optimizer with core focus on optimize. | Logic Component |
| economics/orchestration_layer.py | Functional component implementing OrchestrationLayer with core focus on orchestrate. | Logic Component |
| economics/resource_model.py | Functional component implementing resource model logic within the economics framework. | Logic Component |
| economics/utility_engine.py | Computational engine implementing utility algorithms and state transformations for the economics module. | Logic Component |

## Emotion

| File | Description | Integration Role |
| :--- | :--- | :--- |
| emotion/affective_reasoner.py | Functional component implementing AffectiveReasoner with core focus on reason. | Logic Component |
| emotion/affective_state.py | Functional component implementing AffectiveState with core focus on update, snapshot. | Logic Component |
| emotion/appraisal.py | Functional component implementing EmotionalAppraisal with core focus on appraise. | Logic Component |
| emotion/emotion_manager.py | Central orchestrator for the Emotion subsystem. Manages agent lifecycles and coordinates message-passing for process_event, receive tasks. | Ray Actor (Distributed) |

## Incident Response

| File | Description | Integration Role |
| :--- | :--- | :--- |
| incident_response/audit_logger.py | Functional component implementing AuditLogger with core focus on log. | Logic Component |
| incident_response/containment_engine.py | Computational engine implementing containment algorithms and state transformations for the incident_response module. | Logic Component |
| incident_response/detectors.py | Functional component implementing Detectors with core focus on detect_prompt_injection, detect_memory_poisoning. | Logic Component |
| incident_response/eradication_engine.py | Computational engine implementing eradication algorithms and state transformations for the incident_response module. | Logic Component |
| incident_response/incident_classifier.py | Functional component implementing IncidentClassifier with core focus on classify. | Logic Component |
| incident_response/incident_manager.py | Central orchestrator for the Incident Response subsystem. Manages agent lifecycles and coordinates message-passing for handle, receive tasks. | Ray Actor (Distributed) |
| incident_response/recovery_engine.py | Computational engine implementing recovery algorithms and state transformations for the incident_response module. | Logic Component |
| incident_response/semantic_checks.py | Functional component implementing SemanticChecks with core focus on check. | Logic Component |

## Institutional Ai

| File | Description | Integration Role |
| :--- | :--- | :--- |
| institutional_ai/coordination_layer.py | Functional component implementing CoordinationLayer with core focus on coordinate. | Logic Component |
| institutional_ai/governance_graph.py | Functional component implementing GovernanceGraph with core focus on add_role, add_constraint. | Logic Component |
| institutional_ai/incentive_engine.py | Computational engine implementing incentive algorithms and state transformations for the institutional_ai module. | Logic Component |
| institutional_ai/institutional_manager.py | Central orchestrator for the Institutional Ai subsystem. Manages agent lifecycles and coordinates message-passing for evaluate, receive tasks. | Ray Actor (Distributed) |
| institutional_ai/oversight_agents.py | Functional component implementing OversightAgent with core focus on review. | Logic Component |
| institutional_ai/real_time_control.py | Functional component implementing RealTimeControl with core focus on intercept. | Logic Component |
| institutional_ai/role_definitions.py | Functional component implementing RoleDefinitions with core focus on get_role. | Logic Component |
| institutional_ai/rule_engine.py | Computational engine implementing rule algorithms and state transformations for the institutional_ai module. | Logic Component |
| institutional_ai/sanction_engine.py | Computational engine implementing sanction algorithms and state transformations for the institutional_ai module. | Logic Component |
| institutional_ai/trust_engine.py | Computational engine implementing trust algorithms and state transformations for the institutional_ai module. | Logic Component |

## Memory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/memory_manager.py | Central orchestrator for the Memory subsystem. Manages agent lifecycles and coordinates message-passing for receive, trigger_sleep_cycle tasks. | Ray Actor (Distributed) |
| memory/scratchpad.py | Functional component implementing WorkingMemory with core focus on store, retrieve. | Logic Component |

## Memory Consolidation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory_consolidation/consolidation_manager.py | Central orchestrator for the Memory Consolidation subsystem. Manages agent lifecycles and coordinates message-passing for consolidate, receive tasks. | Ray Actor (Distributed) |
| memory_consolidation/consolidation_scheduler.py | Functional component implementing ConsolidationScheduler with core focus on select_for_replay. | Logic Component |
| memory_consolidation/generative_trainer.py | Functional component implementing GenerativeTrainer with core focus on train_on_replay. | Logic Component |
| memory_consolidation/hippocampal_replay.py | Functional component implementing HippocampalReplay with core focus on sample_replay_batch, generate_replay_sequence. | Logic Component |
| memory_consolidation/schema_manager.py | Central orchestrator for the Memory Consolidation subsystem. Manages agent lifecycles and coordinates message-passing for update_schema, apply_schema tasks. | Ray Actor (Distributed) |

## Memory/Long Term

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/long_term/semantic_memory.py | Functional component implementing SemanticMemory with core focus on store_fact, query. | Cognitive Module (Integrated) |

## Memory/Short Term

| File | Description | Integration Role |
| :--- | :--- | :--- |
| memory/short_term/episodic_memory.py | Functional component implementing EpisodicMemory with core focus on add_episode, recall_recent. | Logic Component |

## Meta Learning

| File | Description | Integration Role |
| :--- | :--- | :--- |
| meta_learning/adaptation_engine.py | Computational engine implementing adaptation algorithms and state transformations for the meta_learning module. | Logic Component |
| meta_learning/meta_manager.py | Central orchestrator for the Meta Learning subsystem. Manages agent lifecycles and coordinates message-passing for update_meta_strategy, receive tasks. | Ray Actor (Distributed) |
| meta_learning/meta_policy.py | Functional component implementing MetaPolicy with core focus on select_strategy. | Logic Component |
| meta_learning/performance_tracker.py | Functional component implementing PerformanceTracker with core focus on record, recent_average. | Logic Component |
| meta_learning/strategy_optimizer.py | Functional component implementing StrategyOptimizer with core focus on update, best_strategy. | Logic Component |

## Metacognition

| File | Description | Integration Role |
| :--- | :--- | :--- |
| metacognition/adaptation_engine.py | Computational engine implementing adaptation algorithms and state transformations for the metacognition module. | Logic Component |
| metacognition/consensus_controller.py | Functional component implementing ConsensusController with core focus on combine. | Logic Component |
| metacognition/mape_k_loop.py | Functional component implementing MAPEKLoop with core focus on cycle. | Logic Component |
| metacognition/meta_monitor.py | Functional component implementing MetaMonitor with core focus on observe. | Logic Component |
| metacognition/meta_reasoner.py | Functional component implementing MetaReasoner with core focus on receive, evaluate_reasoning. | Ray Actor (Distributed) |
| metacognition/metacognition_manager.py | Central orchestrator for the Metacognition subsystem. Manages agent lifecycles and coordinates message-passing for introspect, receive tasks. | Ray Actor (Distributed) |
| metacognition/perception_reflector.py | Functional component implementing PerceptionReflector with core focus on evaluate_perception. | Logic Component |
| metacognition/transparency_engine.py | Computational engine implementing transparency algorithms and state transformations for the metacognition module. | Logic Component |

## Monitoring

| File | Description | Integration Role |
| :--- | :--- | :--- |
| monitoring/conformance_engine.py | Computational engine implementing conformance algorithms and state transformations for the monitoring module. | Logic Component |
| monitoring/drift_detector.py | Functional component implementing DriftDetector with core focus on detect. | Logic Component |
| monitoring/monitoring_manager.py | Central orchestrator for the Monitoring subsystem. Manages agent lifecycles and coordinates message-passing for monitor, receive tasks. | Ray Actor (Distributed) |
| monitoring/risk_monitor.py | Functional component implementing RiskMonitor with core focus on assess. | Logic Component |
| monitoring/semantic_trace.py | Functional component implementing SemanticTrace with core focus on trace. | Logic Component |
| monitoring/telemetry_collector.py | Functional component implementing TelemetryCollector with core focus on collect. | Logic Component |
| monitoring/thermal_guard.py | Functional component implementing ThermalGuard with core focus on get_thermal_state, check_health. | Ray Actor (Distributed) |

## Motivation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| motivation/curiosity.py | Functional component implementing CuriosityModule with core focus on compute_curiosity. | Logic Component |
| motivation/motivation_manager.py | Central orchestrator for the Motivation subsystem. Manages agent lifecycles and coordinates message-passing for evaluate, receive tasks. | Ray Actor (Distributed) |
| motivation/novelty.py | Functional component implementing NoveltyModule with core focus on compute_novelty. | Logic Component |
| motivation/reward_engine.py | Computational engine implementing intrinsicreward algorithms and state transformations for the motivation module. | Logic Component |
| motivation/uncertainty.py | Functional component implementing UncertaintyModule with core focus on compute_uncertainty. | Logic Component |

## Negotiation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| negotiation/compliance_engine.py | Computational engine implementing compliance algorithms and state transformations for the negotiation module. | Logic Component |
| negotiation/concession.py | Functional component implementing ConcessionStrategy with core focus on concede. | Logic Component |
| negotiation/consensus_engine.py | Computational engine implementing consensus algorithms and state transformations for the negotiation module. | Logic Component |
| negotiation/negotiation_manager.py | Central orchestrator for the Negotiation subsystem. Manages agent lifecycles and coordinates message-passing for negotiate, receive tasks. | Ray Actor (Distributed) |
| negotiation/negotiation_protocol.py | Functional component implementing NegotiationProtocol with core focus on negotiate. | Logic Component |
| negotiation/proposal.py | Functional component implementing proposal logic within the negotiation framework. | Logic Component |
| negotiation/treaty_graph.py | Functional component implementing TreatyGraph with core focus on add_treaty, add_dependency. | Logic Component |
| negotiation/utility.py | Functional component implementing UtilitySystem with core focus on individual, joint. | Logic Component |

## Orchestration

| File | Description | Integration Role |
| :--- | :--- | :--- |
| orchestration/concurrency_manager.py | Central orchestrator for the Orchestration subsystem. Manages agent lifecycles and coordinates message-passing for run_parallel tasks. | Logic Component |
| orchestration/event_router.py | Functional component implementing EventRouter with core focus on subscribe, route. | Logic Component |
| orchestration/group_chat_coordinator.py | Functional component implementing GroupChatCoordinator with core focus on step. | Logic Component |
| orchestration/interrupt_handler.py | Functional component implementing InterruptHandler with core focus on check_interrupt. | Logic Component |
| orchestration/orchestration_manager.py | Central orchestrator for the Orchestration subsystem. Manages agent lifecycles and coordinates message-passing for handle_event, run_sequential tasks. | Ray Actor (Distributed) |
| orchestration/priority_scheduler.py | Functional component implementing PriorityScheduler with core focus on schedule, next. | Logic Component |
| orchestration/state_manager.py | Central orchestrator for the Orchestration subsystem. Manages agent lifecycles and coordinates message-passing for update, get tasks. | Logic Component |

## Purpleteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| purpleteam/bas_engine.py | Computational engine implementing bas algorithms and state transformations for the purpleteam module. | Logic Component |
| purpleteam/blue_agent.py | Functional component implementing BlueAgent with core focus on defend. | Logic Component |
| purpleteam/fusion_orchestrator.py | Functional component implementing FusionOrchestrator with core focus on cycle. | Logic Component |
| purpleteam/purple_manager.py | Central orchestrator for the Purpleteam subsystem. Manages agent lifecycles and coordinates message-passing for run_cycle, receive tasks. | Ray Actor (Distributed) |
| purpleteam/red_agent.py | Functional component implementing RedAgent with core focus on attack. | Logic Component |
| purpleteam/remediation_engine.py | Computational engine implementing remediation algorithms and state transformations for the purpleteam module. | Logic Component |
| purpleteam/scoring_engine.py | Computational engine implementing scoring algorithms and state transformations for the purpleteam module. | Logic Component |
| purpleteam/selfplay_engine.py | Computational engine implementing selfplay algorithms and state transformations for the purpleteam module. | Logic Component |

## Redteam

| File | Description | Integration Role |
| :--- | :--- | :--- |
| redteam/adversarial_agent.py | Functional component implementing AdversarialAgent with core focus on craft_attack. | Logic Component |
| redteam/attack_library.py | Functional component implementing AttackLibrary with core focus on get. | Logic Component |
| redteam/ecosystem_simulator.py | Functional component implementing EcosystemSimulator with core focus on simulate. | Logic Component |
| redteam/exploit_generator.py | Functional component implementing ExploitGenerator with core focus on enhance. | Logic Component |
| redteam/redteam_manager.py | Central orchestrator for the Redteam subsystem. Manages agent lifecycles and coordinates message-passing for run, receive tasks. | Ray Actor (Distributed) |
| redteam/scenario_engine.py | Computational engine implementing scenario algorithms and state transformations for the redteam module. | Logic Component |
| redteam/trajectory_simulator.py | Functional component implementing TrajectorySimulator with core focus on simulate. | Logic Component |
| redteam/vulnerability_scoring.py | Functional component implementing VulnerabilityScoring with core focus on score. | Logic Component |

## Root Directory

| File | Description | Integration Role |
| :--- | :--- | :--- |
| ./AGENTS.md | Operational guidelines for autonomous agents, defining behavioral norms, safety constraints, and collaboration protocols. | Utility/Config |
| ./README.md | Core architectural overview. Documents the Asynchronous Predictive Workspace (APW) and neuro-symbolic reasoning cycles. | Utility/Config |
| ./config.yaml | Global system manifest defining hardware limits (15W TDP), precision tiers (sym_int8/Q4_K_M), and vector store settings for nomic-embed-text-v1.5. | Utility/Config |
| ./find_invalid_py.py | Functional component implementing find invalid py logic within the . framework. | Logic Component |
| ./main.py | Functional component implementing SGIHub with core focus on check_ram_guard, safe_delegate. | Entry Point |
| ./setup_8265u.sh | Environment setup for Intel i5-8265U. Configures IPEX-LLM, threading (OMP/MKL), and hardware-specific optimizations. | Utility/Config |

## Runtime

| File | Description | Integration Role |
| :--- | :--- | :--- |
| runtime/agi_runtime.py | Functional component implementing AGIRuntime with core focus on process. | Logic Component |
| runtime/agi_state.py | Functional component implementing agi state logic within the runtime framework. | Logic Component |
| runtime/event_bus.py | Functional component implementing EventBus with core focus on publish, consume. | Logic Component |
| runtime/governance_gateway.py | Functional component implementing GovernanceGateway with core focus on authorize. | Logic Component |
| runtime/runtime_logger.py | Functional component implementing RuntimeLogger with core focus on log. | Logic Component |
| runtime/safety_hooks.py | Functional component implementing SafetyHooks with core focus on validate. | Logic Component |
| runtime/scheduler.py | Functional component implementing Scheduler with core focus on next_phase. | Logic Component |

## Safety Ethics

| File | Description | Integration Role |
| :--- | :--- | :--- |
| safety_ethics/attention_gate.py | Functional component implementing AttentionGate with core focus on filter, amplify. | Logic Component |
| safety_ethics/conflict_resolver.py | Functional component implementing EthicalConflictResolver with core focus on resolve. | Logic Component |
| safety_ethics/constraint_enforcer.py | Functional component implementing ConstraintEnforcer with core focus on enforce. | Logic Component |
| safety_ethics/deception_detector.py | Functional component implementing DeceptionDetector with core focus on detect. | Logic Component |
| safety_ethics/ethical_appraisal.py | Functional component implementing EthicalAppraisal with core focus on appraise, violates_norm. | Logic Component |
| safety_ethics/ethics_manager.py | Central orchestrator for the Safety Ethics subsystem. Manages agent lifecycles and coordinates message-passing for is_safe, assess_safety tasks. | Ray Actor (Distributed) |
| safety_ethics/governance_graph.py | Functional component implementing GovernanceGraph with core focus on add_node, add_edge. | Logic Component |
| safety_ethics/interpretability_monitor.py | Functional component implementing InterpretabilityMonitor with core focus on analyze. | Logic Component |
| safety_ethics/moral_reasoner.py | Functional component implementing MoralReasoner with core focus on reason. | Logic Component |
| safety_ethics/norm_library.py | Functional component implementing NormLibrary with core focus on get_norms. | Logic Component |
| safety_ethics/oversight_agent.py | Functional component implementing OversightAgent with core focus on review. | Logic Component |
| safety_ethics/risk_classifier.py | Functional component implementing RiskClassifier with core focus on classify. | Logic Component |
| safety_ethics/safety_manager.py | Central orchestrator for the Safety Ethics subsystem. Manages agent lifecycles and coordinates message-passing for evaluate, receive tasks. | Ray Actor (Distributed) |
| safety_ethics/shutdown_controller.py | Functional component implementing ShutdownController with core focus on request_shutdown, is_active. | Logic Component |

## Self Model

| File | Description | Integration Role |
| :--- | :--- | :--- |
| self_model/autobiographical_memory.py | Functional component implementing AutobiographicalMemory with core focus on store_episode, summarize. | Logic Component |
| self_model/continuity_metrics.py | Functional component implementing ContinuityMetrics with core focus on compute_icm, compute_pdm. | Logic Component |
| self_model/identity_kernel.py | Functional component implementing IdentityKernel with core focus on get_kernel, enforce. | Logic Component |
| self_model/reflective_endorsement.py | Functional component implementing ReflectiveEndorsement with core focus on endorse. | Logic Component |
| self_model/self_manager.py | Central orchestrator for the Self Model subsystem. Manages agent lifecycles and coordinates message-passing for update_self, approve_update tasks. | Ray Actor (Distributed) |
| self_model/temporal_self.py | Functional component implementing TemporalSelf with core focus on update_present, record_past. | Logic Component |

## Simulation

| File | Description | Integration Role |
| :--- | :--- | :--- |
| simulation/agent_adapter.py | Functional component implementing AgentAdapter with core focus on step. | Logic Component |
| simulation/environment.py | Functional component implementing Environment with core focus on update. | Logic Component |
| simulation/governance_interventions.py | Functional component implementing GovernanceInterventions with core focus on apply. | Logic Component |
| simulation/interaction_protocol.py | Functional component implementing InteractionProtocol with core focus on mediate. | Logic Component |
| simulation/metrics_engine.py | Computational engine implementing metrics algorithms and state transformations for the simulation module. | Logic Component |
| simulation/replay_buffer.py | Functional component implementing ReplayBuffer with core focus on record. | Logic Component |
| simulation/sim_core.py | Functional component implementing SimulationCore with core focus on tick, schedule. | Logic Component |
| simulation/simulation_manager.py | Central orchestrator for the Simulation subsystem. Manages agent lifecycles and coordinates message-passing for step, receive tasks. | Ray Actor (Distributed) |

## Tests

| File | Description | Integration Role |
| :--- | :--- | :--- |
| tests/test_sgi_features.py | Functional component implementing TestSGIIntegration with core focus on setUpClass, tearDownClass. | Logic Component |

## Training

| File | Description | Integration Role |
| :--- | :--- | :--- |
| training/curriculum.py | Functional component implementing Curriculum with core focus on update, get_current_tasks. | Logic Component |
| training/meta_learning.py | Functional component implementing MetaLearning with core focus on update, adjust_learning_rates. | Logic Component |
| training/rl_trainer.py | Functional component implementing RLTrainer with core focus on update_policy, choose_action. | Logic Component |
| training/self_supervised.py | Functional component implementing SelfSupervisedTrainer with core focus on train_step. | Logic Component |
| training/training_manager.py | Central orchestrator for the Training subsystem. Manages agent lifecycles and coordinates message-passing for train, receive tasks. | Ray Actor (Distributed) |
| training/world_model_trainer.py | Functional component implementing WorldModelTrainer with core focus on train_step. | Logic Component |

## World Model

| File | Description | Integration Role |
| :--- | :--- | :--- |
| world_model/causal_graph.py | Functional component implementing CausalGraph with core focus on add_causal_link, get_effects. | Logic Component |
| world_model/counterfactuals.py | What would happen if…? | Logic Component |
| world_model/manager.py | Central orchestrator for the World Model subsystem. Manages agent lifecycles and coordinates message-passing for update_world, predict_future tasks. | Ray Actor (Distributed) |
| world_model/prediction.py | Computational engine implementing prediction algorithms and state transformations for the world_model module. | Logic Component |
| world_model/simulator.py | Functional component implementing Simulator with core focus on simulate_step, simulate_sequence. | Logic Component |
| world_model/state.py | Functional component implementing WorldState with core focus on update_internal, update_external. | Logic Component |
