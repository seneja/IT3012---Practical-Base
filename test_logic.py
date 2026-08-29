from logic_engine import KnowledgeBase

def test_forward_chaining():
    kb = KnowledgeBase()
    
    # Add Domain Rules
    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')
    
    # Test Case 1: Safe Engagement
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.forward_chain()
    assert 'SafeToEngage' in kb.facts, "Test 1 Failed: Should deduce SafeToEngage"
    assert 'Retreat' not in kb.facts, "Test 1 Failed: Should NOT deduce Retreat"
    
    # Test Case 2: Unsafe Engagement (Bloodseeker Missing)
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')
    kb.forward_chain()
    assert 'Retreat' in kb.facts, "Test 2 Failed: Should deduce Retreat to override search"
    
    print("All Logic Engine Test Cases Passed!")


def test_astar_integration():
    from agent import SearchAgent
    agent = SearchAgent()
    
    # Test Case 3: A* avoids tile with food + toxic trap when Bloodseeker is missing
    percept_missing = {
        'grid_size': (3, 3),
        'walls': [],
        'all_food': [(1, 1), (2, 1)],
        'toxic_traps': [(1, 1)],
        'opponents': [] # Bloodseeker is missing
    }
    
    path_missing = agent.astar_search(
        start_pos=(0, 1),
        goal_pos=(2, 1),
        walls=[],
        grid_size=(3, 3),
        heuristic_type='manhattan',
        percept=percept_missing
    )
    
    assert path_missing is not None, "A* should find a path around the trap"
    assert len(path_missing) == 4, f"A* should avoid (1, 1), expected path length 4, got {len(path_missing)}: {path_missing}"
    
    # Test Case 4: A* does NOT avoid tile when Bloodseeker is present
    percept_present = {
        'grid_size': (3, 3),
        'walls': [],
        'all_food': [(1, 1), (2, 1)],
        'toxic_traps': [(1, 1)],
        'opponents': [[0, 2]] # Bloodseeker is NOT missing
    }
    
    path_present = agent.astar_search(
        start_pos=(0, 1),
        goal_pos=(2, 1),
        walls=[],
        grid_size=(3, 3),
        heuristic_type='manhattan',
        percept=percept_present
    )
    
    assert path_present is not None
    assert len(path_present) == 2, f"A* should go straight through (1, 1) when Bloodseeker is present, expected path length 2, got {len(path_present)}: {path_present}"
    
    print("A* Logic Integration Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()
    test_astar_integration()