from typing import Dict, List, Tuple


def availability_overlap(vec_target: str, vec_other: str) -> float:
    """
    Compute the overlap score: fraction of the target's available
    slots that the other user is also available for.

    Returns a float in [0.0, 1.0]. If the target has no available slots, returns 0.0.
    """
    if len(vec_target) != 168 or len(vec_other) != 168:
        raise ValueError("Both availability vectors must be length 168.")

    target_indices = [i for i, c in enumerate(vec_target) if c == "1"]
    if not target_indices:
        return 0.0

    overlap = sum(1 for i in target_indices if vec_other[i] == "1")
    return overlap / len(target_indices)


def _ordered_skill_score(target_learn: List[str], teacher_teach: List[str]) -> float:
    """
    Compute an ordered skill alignment score between target's learn-list and
    a teacher's teach-list. Both lists are treated as ordered (index 0 = highest priority).

    Algorithm:
      - For each skill that appears in both lists, compute two position weights:
            weight_target = (len(target_learn) - index_in_target) / len(target_learn)
            weight_teacher = (len(teacher_teach) - index_in_teacher) / len(teacher_teach)
      - For that skill, skill_score = weight_target * weight_teacher.
      - The final skill alignment score is the maximum skill_score across all shared skills.

    This produces a score in (0.0, 1.0] where 1.0 is achieved when both lists have the
    same skill at index 0. If there are no shared skills, returns 0.0.
    """
    if not target_learn or not teacher_teach:
        return 0.0

    # Build quick index maps for O(1) lookup
    target_index = {skill: idx for idx, skill in enumerate(target_learn)}
    teacher_index = {skill: idx for idx, skill in enumerate(teacher_teach)}

    shared = set(target_index.keys()) & set(teacher_index.keys())
    if not shared:
        return 0.0

    len_t = len(target_learn)
    len_r = len(teacher_teach)

    best = 0.0
    for skill in shared:
        wt_target = (len_t - target_index[skill]) / len_t
        wt_teacher = (len_r - teacher_index[skill]) / len_r
        score_skill = wt_target * wt_teacher
        if score_skill > best:
            best = score_skill

    return best

##CALL THIS FUNCTION IN FLASK!!!!!
def availability_match_ordered(
    availabilities: Dict[str, str],
    # skills: Dict[str, Dict[str, List[str]]],
    teach_skills: Dict[str, List[str]],
    learn_skills: Dict[str, List[str]],
    target: str,
) -> List[Tuple[str, float]]:
    """
    Match using the availability overlap metric combined with an ordered skill alignment score, 
    but only include candidates who can engage in a reciprocal skill swap with the target.
        - Candidate teaches at least one skill from target's learn list.
        - Candidate wants to learn at least one skill from target's teach list.

    Notes:
    - The target's "learn" list is treated as ordered (earlier = higher priority).
    - Each candidate's "teach" list is also treated as ordered (earlier = higher priority).
    - Compute skill_alignment = _ordered_skill_score(target_learn, teacher_teach).
      If skill_alignment == 0.0 the candidate is skipped.
    - Final score for candidate = availability_overlap(target, candidate) * skill_alignment.

    Returns a list of (username, score) sorted by descending score.
    """
    if target not in availabilities:
        raise ValueError(f"Target '{target}' not found in availabilities.")
    if target not in teach_skills:
        raise ValueError(f"Target '{target}' not found in teach_skills data.")
    if target not in learn_skills:
        raise ValueError(f"Target '{target}' not found in learn_skills data.")

    target_learn = learn_skills[target]
    target_teach = teach_skills[target]
    if not target_learn or not target_teach:
        return []

    target_vec = availabilities[target]

    results: List[Tuple[str, float]] = []
    for user, vec in availabilities.items():
        if user == target:
            continue
        if user not in teach_skills:
            continue
        if user not in learn_skills:
            continue

        candidate_teach = teach_skills[user]
        candidate_learn = learn_skills[user]

        # Strict reciprocity check
        if not (set(candidate_teach) & set(target_learn)):
            continue
        if not (set(candidate_learn) & set(target_teach)):
            continue

        skill_align = _ordered_skill_score(target_learn, candidate_teach)
        if skill_align == 0.0:
            continue

        score_avail = availability_overlap(target_vec, vec)
        combined = score_avail * skill_align
        results.append((user, combined))

    results.sort(key=lambda x: (-x[1], x[0]))
    return results


if __name__ == "__main__":
    # Example usage demonstrating both functions
    availabilities = {
        "alice": "1" * 84 + "0" * 84,
        "bob": "0" * 42 + "1" * 42 + "0" * 84,
        "carol": "0" * 168,
        "dave": "1" * 168,
    }

    # Note: lists are ORDERED; index 0 = highest priority
    '''skills = {
        "alice": {"teach": ["python"], "learn": ["math", "design", "music"]},
        "bob": {"teach": ["math", "music"], "learn": ["python"]},
        "carol": {"teach": ["history"], "learn": ["math"]},
        "dave": {"teach": ["design", "math"], "learn": ["python", "math"]},
    }'''

    # Note: lists are ORDERED; index 0 = highest priority
    teach_skills = {
        "alice": ["python"],
        "bob": ["math", "music"],
        "carol": ["history"],
        "dave": ["design", "math"],
    }

    # Note: lists are ORDERED; index 0 = highest priority
    learn_skills = {
        "alice": ["math", "design", "music"],
        "bob": ["python"],
        "carol": ["math"],
        "dave": ["python", "math"],
    }

    target = "alice"

    print("\nOrdered reciprocal skill match:")
    for user, score in availability_match_ordered(availabilities, teach_skills, learn_skills, target):
        print(f"{user}: {score:.4f}")
