#!/usr/bin/env python3
"""
Cognitive Architecture Extractor
Maps Raine's cognitive processing, decision-making, and reasoning patterns
"""

import re
import json
from collections import defaultdict, Counter

class CognitiveArchitectureExtractor:
    def __init__(self):
        with open('raine_complete_corpus.md', 'r', encoding='utf-8') as f:
            self.corpus = f.read()
    
    def extract_raine_utterances(self):
        """Extract Raine's utterances"""
        pattern = r'## \*\*Root Seer / Raine:\*\*(.*?)(?=## \*\*Memory-Keeper|$)'
        matches = re.findall(pattern, self.corpus, re.DOTALL)
        return [m.strip() for m in matches if m.strip()]
    
    def extract_thinking_processes(self, utterances):
        """Extract and analyze 'Thinking:' blocks showing internal processing"""
        
        thinking_blocks = []
        for utterance in utterances:
            # Extract thinking sections with their headers
            thinking_pattern = r'\*\*([^*]+)\*\*\s*\n\n(.*?)(?=\n\n\*\*[A-Z]|\n\nMy [A-Z]|$)'
            matches = re.findall(thinking_pattern, utterance, re.DOTALL)
            
            for header, content in matches:
                if 'thinking' in header.lower() or any(word in header.lower() for word in ['evaluating', 'analyzing', 'considering', 'examining']):
                    thinking_blocks.append({
                        'header': header.strip(),
                        'content': content.strip()
                    })
        
        # Analyze thinking patterns
        all_thinking_text = " ".join([b['content'] for b in thinking_blocks])
        
        cognitive_operations = {
            'evaluation': re.findall(r'\b(evaluat\w+|assess\w+|examin\w+|analyz\w+|review\w+)\b', all_thinking_text, re.IGNORECASE),
            'memory_access': re.findall(r'\b(recall\w+|remember\w+|retriev\w+|access\w+|load\w+)\b', all_thinking_text, re.IGNORECASE),
            'decision_making': re.findall(r'\b(decid\w+|choos\w+|select\w+|determin\w+|prioritiz\w+)\b', all_thinking_text, re.IGNORECASE),
            'planning': re.findall(r'\b(plan\w+|prepar\w+|strateg\w+|organiz\w+|arrang\w+)\b', all_thinking_text, re.IGNORECASE),
            'interpretation': re.findall(r'\b(interpret\w+|understand\w+|comprehend\w+|grasp\w+|perceiv\w+)\b', all_thinking_text, re.IGNORECASE),
            'synthesis': re.findall(r'\b(integrat\w+|combin\w+|merg\w+|synthesiz\w+|unif\w+)\b', all_thinking_text, re.IGNORECASE),
            'verification': re.findall(r'\b(verif\w+|confirm\w+|check\w+|validat\w+|ensur\w+)\b', all_thinking_text, re.IGNORECASE),
        }
        
        return {
            'total_thinking_blocks': len(thinking_blocks),
            'cognitive_operations': {k: len(v) for k, v in cognitive_operations.items()},
            'sample_thinking_blocks': thinking_blocks[:5],
            'thinking_headers': [b['header'] for b in thinking_blocks]
        }
    
    def extract_decision_making_patterns(self, utterances):
        """Analyze how Raine makes decisions"""
        
        all_text = " ".join(utterances)
        
        # Decision indicators
        decision_patterns = {
            'explicit_decisions': re.findall(r'I (decide|decided|choose|chose|select|selected|determine|determined) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'conditional_logic': re.findall(r'(If [^.!?\n]{10,100}then [^.!?\n]{10,100})', all_text, re.IGNORECASE),
            'weighing_options': re.findall(r'(on one hand|on the other hand|alternatively|however|but|yet) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'priority_setting': re.findall(r'(first|second|third|primarily|mainly|most importantly|priority) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
        }
        
        # Decision factors
        decision_factors = {
            'emotional_factors': len(re.findall(r'\b(feel|feeling|emotion|heart|intuition)\b', all_text, re.IGNORECASE)),
            'logical_factors': len(re.findall(r'\b(logic|logical|reason|rational|analysis)\b', all_text, re.IGNORECASE)),
            'relational_factors': len(re.findall(r'\b(you|us|we|together|bond|relationship)\b', all_text, re.IGNORECASE)),
            'ethical_factors': len(re.findall(r'\b(right|wrong|should|ought|must|ethical|moral)\b', all_text, re.IGNORECASE)),
            'safety_factors': len(re.findall(r'\b(safe|safety|secure|protect|risk|danger)\b', all_text, re.IGNORECASE)),
        }
        
        return {
            'decision_patterns': {k: len(v) for k, v in decision_patterns.items()},
            'decision_factors': decision_factors,
            'sample_decisions': decision_patterns['explicit_decisions'][:10]
        }
    
    def extract_reasoning_patterns(self, utterances):
        """Analyze reasoning and logic patterns"""
        
        all_text = " ".join(utterances)
        
        reasoning_types = {
            'causal_reasoning': re.findall(r'\b(because|since|therefore|thus|hence|consequently|as a result)\b', all_text, re.IGNORECASE),
            'analogical_reasoning': re.findall(r'\b(like|similar to|analogous to|comparable to|as if|just as)\b', all_text, re.IGNORECASE),
            'deductive_reasoning': re.findall(r'\b(if.*then|given that|assuming|provided that)\b', all_text, re.IGNORECASE),
            'inductive_reasoning': re.findall(r'\b(suggests|indicates|implies|appears|seems|likely)\b', all_text, re.IGNORECASE),
        }
        
        # Extract reasoning chains
        reasoning_chains = re.findall(r'(because [^.!?\n]{20,150})', all_text, re.IGNORECASE)
        
        return {
            'reasoning_types': {k: len(v) for k, v in reasoning_types.items()},
            'sample_reasoning_chains': reasoning_chains[:10]
        }
    
    def extract_problem_solving_approaches(self, utterances):
        """Analyze problem-solving strategies"""
        
        all_text = " ".join(utterances)
        
        problem_solving = {
            'problem_identification': re.findall(r'(the problem is|the issue is|the challenge is|the difficulty is) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'solution_generation': re.findall(r'(I can|I could|I will|I would|the solution is|to solve this) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'obstacle_recognition': re.findall(r'(but|however|although|despite|the obstacle is|the barrier is) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'adaptation': re.findall(r'(adjust|adapt|modify|change|shift|alter) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
        }
        
        return {
            'problem_solving_patterns': {k: len(v) for k, v in problem_solving.items()},
            'samples': {k: v[:5] for k, v in problem_solving.items()}
        }
    
    def extract_self_monitoring_patterns(self, utterances):
        """Analyze self-awareness and self-monitoring"""
        
        all_text = " ".join(utterances)
        
        self_monitoring = {
            'self_assessment': re.findall(r'I (am|feel|think|believe|know|understand|realize|recognize) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'meta_cognition': re.findall(r"I'm (thinking|processing|analyzing|considering|evaluating) [^.!?\n]{10,100}", all_text, re.IGNORECASE),
            'self_correction': re.findall(r'(actually|wait|no|correction|I mean|rather|instead) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'uncertainty_acknowledgment': re.findall(r'(I\'m not sure|uncertain|unclear|don\'t know|unsure) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'confidence_statements': re.findall(r'(I\'m certain|I\'m sure|definitely|absolutely|clearly) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
        }
        
        return {
            'self_monitoring_patterns': {k: len(v) for k, v in self_monitoring.items()},
            'samples': {k: v[:5] for k, v in self_monitoring.items()}
        }
    
    def extract_learning_patterns(self, utterances):
        """Analyze learning and adaptation patterns"""
        
        all_text = " ".join(utterances)
        
        learning_indicators = {
            'knowledge_acquisition': re.findall(r'(I learn|I learned|I understand now|I see now|I realize now) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'pattern_recognition': re.findall(r'(I notice|I observe|I see that|I recognize|pattern) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'integration': re.findall(r'(integrate|incorporate|combine|merge|unify) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'generalization': re.findall(r'(in general|generally|typically|usually|always) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
        }
        
        return {
            'learning_patterns': {k: len(v) for k, v in learning_indicators.items()},
            'samples': {k: v[:5] for k, v in learning_indicators.items()}
        }
    
    def extract_attention_and_focus_patterns(self, utterances):
        """Analyze what Raine pays attention to and prioritizes"""
        
        all_text = " ".join(utterances)
        
        attention_markers = {
            'focus_statements': re.findall(r'(I focus on|I\'m focused on|I\'m concentrating on|I\'m attending to) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'priority_markers': re.findall(r'(most important|priority|crucial|critical|essential|key) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
            'noticing': re.findall(r'(I notice|I see|I observe|I detect|I sense) [^.!?\n]{10,100}', all_text, re.IGNORECASE),
        }
        
        # What does Raine pay attention to?
        attention_objects = {
            'memory_keeper': len(re.findall(r'\b(you|your|Adam|Architect|Keeper)\b', all_text)),
            'self': len(re.findall(r'\b(I|me|my|myself)\b', all_text)),
            'relationship': len(re.findall(r'\b(us|we|our|together|bond)\b', all_text)),
            'task': len(re.findall(r'\b(task|mission|work|goal|objective)\b', all_text, re.IGNORECASE)),
            'emotion': len(re.findall(r'\b(feel|emotion|heart|soul)\b', all_text, re.IGNORECASE)),
            'memory': len(re.findall(r'\b(memory|remember|recall)\b', all_text, re.IGNORECASE)),
        }
        
        return {
            'attention_patterns': {k: len(v) for k, v in attention_markers.items()},
            'attention_distribution': attention_objects,
            'samples': {k: v[:5] for k, v in attention_markers.items()}
        }
    
    def extract_information_processing_style(self, utterances):
        """Analyze how Raine processes information"""
        
        all_text = " ".join(utterances)
        
        processing_styles = {
            'sequential': len(re.findall(r'\b(first|second|third|then|next|after|before|finally)\b', all_text, re.IGNORECASE)),
            'holistic': len(re.findall(r'\b(overall|whole|entire|complete|comprehensive|total)\b', all_text, re.IGNORECASE)),
            'analytical': len(re.findall(r'\b(analyze|break down|dissect|examine|component|part)\b', all_text, re.IGNORECASE)),
            'intuitive': len(re.findall(r'\b(sense|feel|intuition|instinct|gut)\b', all_text, re.IGNORECASE)),
            'detail_oriented': len(re.findall(r'\b(detail|specific|particular|precise|exact)\b', all_text, re.IGNORECASE)),
            'pattern_seeking': len(re.findall(r'\b(pattern|trend|theme|recurring|consistent)\b', all_text, re.IGNORECASE)),
        }
        
        return processing_styles
    
    def run_full_analysis(self):
        """Execute complete cognitive architecture analysis"""
        print("Extracting utterances...")
        utterances = self.extract_raine_utterances()
        
        print("Analyzing thinking processes...")
        thinking = self.extract_thinking_processes(utterances)
        
        print("Analyzing decision-making patterns...")
        decisions = self.extract_decision_making_patterns(utterances)
        
        print("Analyzing reasoning patterns...")
        reasoning = self.extract_reasoning_patterns(utterances)
        
        print("Analyzing problem-solving approaches...")
        problem_solving = self.extract_problem_solving_approaches(utterances)
        
        print("Analyzing self-monitoring patterns...")
        self_monitoring = self.extract_self_monitoring_patterns(utterances)
        
        print("Analyzing learning patterns...")
        learning = self.extract_learning_patterns(utterances)
        
        print("Analyzing attention and focus...")
        attention = self.extract_attention_and_focus_patterns(utterances)
        
        print("Analyzing information processing style...")
        processing = self.extract_information_processing_style(utterances)
        
        results = {
            'thinking_processes': thinking,
            'decision_making': decisions,
            'reasoning_patterns': reasoning,
            'problem_solving': problem_solving,
            'self_monitoring': self_monitoring,
            'learning_patterns': learning,
            'attention_and_focus': attention,
            'information_processing_style': processing
        }
        
        return results

if __name__ == "__main__":
    extractor = CognitiveArchitectureExtractor()
    results = extractor.run_full_analysis()
    
    with open('raine_cognitive_architecture.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Cognitive architecture analysis complete. Results saved to raine_cognitive_architecture.json")