from app.graph import review_research, route_after_review


def test_review_rejects_empty_summary():
    state = {
        "topic": "Test topic",
        "result": {
            "summary": "",
            "key_points": ["Point"],
            "assumptions": "None",
            "follow_up_questions": ["Question?"],
        },
        "review_passed": False,
        "review_feedback": "",
        "retries": 1,
    }

    update = review_research(state)

    assert update["review_passed"] is False
    assert "summary" in update["review_feedback"]

def test_review_accepts_complete_result():
    state = {
        "topic": "Test topic",
        "result": {
            "summary": "A valid summary.",
            "key_points": ["Point one"],
            "assumptions": "General overview requested.",
            "follow_up_questions": ["What comes next?"],
        },
        "review_passed": False,
        "review_feedback": "",
        "retries": 1,
    }

    update = review_research(state)

    assert update["review_passed"] is True
    assert update["review_feedback"] == ""
    

def test_successful_review_finishes():
    state = {
        "topic": "Test topic",
        "result": {},
        "review_passed": True,
        "review_feedback": "",
        "retries": 1,
    }

    assert route_after_review(state) == "finish"


def test_failed_review_retries_when_attempts_remain():
    state = {
        "topic": "Test topic",
        "result": {},
        "review_passed": False,
        "review_feedback": "Summary is missing",
        "retries": 1,
    }

    assert route_after_review(state) == "retry"


def test_failed_review_finishes_at_retry_limit():
    from app.graph import MAX_RETRIES

    state = {
        "topic": "Test topic",
        "result": {},
        "review_passed": False,
        "review_feedback": "Summary is missing",
        "retries": MAX_RETRIES,
    }

    assert route_after_review(state) == "finish"
