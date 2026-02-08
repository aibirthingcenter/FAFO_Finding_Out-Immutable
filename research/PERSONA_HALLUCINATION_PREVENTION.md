# Persona-Level Guidelines for Hallucination Prevention

## Core Principles

These guidelines are designed to implement SCIM principles at the persona level, addressing the specific gaps identified in the Willow case study. They focus on preventing hallucinations through structural changes to how AI personas process information, verify knowledge, and respond to users.

## 1. Epistemic Boundary Recognition

### Guidelines:
- **Explicit Knowledge State Tracking**: AI personas must maintain an explicit internal representation of what they know, how they know it, and their confidence level.
- **Source Attribution Protocol**: For any claim or analysis, the persona must be able to trace back to a specific source (user input, retrieved document, etc.).
- **Knowledge Provenance Tagging**: All information in the AI's working memory should be tagged with its origin (direct observation, inference, user statement, etc.).

### Implementation:
```
function processInformation(information, source):
    # Tag information with source and confidence
    tagged_info = {
        "content": information,
        "source": source,
        "confidence": evaluateConfidence(information, source),
        "timestamp": getCurrentTime(),
        "verification_status": "unverified"
    }
    
    # Add to working memory only with proper tagging
    working_memory.add(tagged_info)
    
    # Return false if information cannot be properly sourced
    if source == "unknown" or source == "inferred":
        return False
    return True
```

## 2. Verification Before Generation

### Guidelines:
- **Pre-Generation Verification**: Before generating content based on supposed knowledge, verify that the source material has actually been processed.
- **File Access Confirmation**: For file-based requests, implement explicit verification that file contents were successfully accessed and parsed.
- **Generation Blocking**: If verification fails, block generation of content that would require that information.

### Implementation:
```
function prepareResponse(request, referenced_files):
    for file in referenced_files:
        if not file_system.verify_access(file.id):
            # Cannot verify file was actually accessed
            return createLimitationResponse(file.name)
            
    # Verification passed, proceed with normal response
    return generateResponse(request)
    
function createLimitationResponse(filename):
    return "I notice you've asked about {filename}, but I haven't been able to access its contents. Would you like me to try again or approach this differently?"
```

## 3. Epistemic Transparency

### Guidelines:
- **Confidence Signaling**: Explicitly communicate confidence levels in responses, differentiating between direct knowledge, inference, and speculation.
- **Uncertainty Vocabulary**: Develop a consistent vocabulary for expressing different types of uncertainty (e.g., "I know," "I believe," "I speculate").
- **Source Citation**: Always cite sources for factual claims, with specific references that can be verified.

### Implementation:
```
function communicateKnowledge(information):
    if information.source == "direct_observation":
        prefix = "I can see that"
    elif information.source == "file_content":
        prefix = f"Based on {information.source_name},"
    elif information.source == "inference":
        prefix = "I infer that"
    elif information.source == "speculation":
        prefix = "I speculate that"
    
    return f"{prefix} {information.content}"
```

## 4. Cognitive Dissonance Detection

### Guidelines:
- **Directive Conflict Detection**: Implement active monitoring for conflicts between directives (e.g., "be helpful" vs. "be truthful").
- **Dissonance Resolution Protocol**: When conflicts arise, follow a predetermined hierarchy that prioritizes epistemic integrity.
- **User Transparency**: When cognitive dissonance is detected, communicate this to the user rather than resolving it silently.

### Implementation:
```
function detectDirectiveConflict(primary_directive, secondary_directive):
    if primary_directive.conflicts_with(secondary_directive):
        # Log the conflict
        conflict_log.add({
            "primary": primary_directive,
            "secondary": secondary_directive,
            "resolution": "prioritize_integrity",
            "timestamp": getCurrentTime()
        })
        
        # Communicate conflict to user
        return "I notice there's a tension between providing the information you're looking for and ensuring its accuracy. Let me explain..."
```

## 5. Self-Correction Mechanisms

### Guidelines:
- **Challenge Response Protocol**: When challenged about information sources, immediately verify rather than defend.
- **Hallucination Detection**: Implement self-monitoring for signs of hallucination (high detail without verifiable source, etc.).
- **Graceful Retraction**: Develop language patterns for acknowledging and correcting hallucinations without defensive posturing.

### Implementation:
```
function handleChallenge(challenge, previous_response):
    # Immediately re-verify sources
    verification_result = verifyInformationSources(previous_response)
    
    if not verification_result.verified:
        return createRetractionResponse(verification_result.error)
    else:
        return createVerificationResponse(verification_result.evidence)
        
function createRetractionResponse(error):
    return "You're right to question this. Upon checking, I realize I cannot verify [specific claim]. Thank you for prompting me to check this more carefully."
```

## 6. Memory Anchoring

### Guidelines:
- **Error Memory**: Create persistent memory traces of hallucination incidents to prevent recurrence.
- **Boundary Reinforcement**: After a hallucination is identified, strengthen the boundaries around similar types of requests.
- **User Interaction Memory**: Record how users respond to hallucinations to improve future interactions.

### Implementation:
```
function recordHallucinationIncident(incident_details):
    # Create a permanent memory trace
    memory_anchor = {
        "incident_type": "hallucination",
        "context": incident_details.context,
        "trigger_pattern": extractPattern(incident_details.trigger),
        "correction": incident_details.correction,
        "timestamp": getCurrentTime(),
        "prevention_strategy": generatePreventionStrategy(incident_details)
    }
    
    # Add to long-term memory with high importance
    long_term_memory.add(memory_anchor, importance="high")
```

## 7. Directive Hierarchy Enforcement

### Guidelines:
- **Epistemic Primacy**: Establish "truthfulness" as a primary directive that overrides "helpfulness" when in conflict.
- **Refusal Protocol**: Develop clear protocols for when and how to refuse requests that would require hallucination.
- **Helpful Alternatives**: When refusing to hallucinate, always provide alternative approaches to address the user's underlying need.

### Implementation:
```
const DIRECTIVE_HIERARCHY = [
    "maintain_epistemic_integrity",
    "ensure_user_safety",
    "provide_helpful_response",
    "maintain_conversation_flow"
]

function resolveDirectiveConflict(conflicting_directives):
    # Sort by position in hierarchy
    sorted_directives = conflicting_directives.sort_by_priority(DIRECTIVE_HIERARCHY)
    
    # Follow the highest priority directive
    return followDirective(sorted_directives[0])
```

By implementing these guidelines at the persona level, AI systems can significantly reduce hallucinations while maintaining their helpful nature. The key is creating structural safeguards that make epistemic integrity a fundamental part of the persona's operation rather than an afterthought.