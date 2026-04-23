from ml_personality_pipeline.derived_traits import derive_personality_scores, describe_scores


def test_derived_personality_scores_are_bounded():
    base_traits = {
        "openness": 0.72,
        "conscientiousness": 0.81,
        "extraversion": 0.65,
        "agreeableness": 0.78,
        "neuroticism": 0.20,
    }

    derived = derive_personality_scores(base_traits)
    assert derived, "Derived score dictionary must not be empty"
    assert all(0.0 <= value <= 1.0 for value in derived.values())


def test_introvert_extrovert_are_complementary():
    base_traits = {
        "openness": 0.5,
        "conscientiousness": 0.5,
        "extraversion": 0.31,
        "agreeableness": 0.5,
        "neuroticism": 0.5,
    }

    derived = derive_personality_scores(base_traits)
    assert abs((derived["introvert_score"] + derived["extrovert_score"]) - 1.0) < 1e-8


def test_score_descriptions_use_three_levels():
    descriptions = describe_scores({"a": 0.2, "b": 0.5, "c": 0.8})
    assert descriptions == {"a": "low", "b": "moderate", "c": "high"}
