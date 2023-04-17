from typing import List


class CandidateService:

    @classmethod
    def get_candidates(cls) -> List[str]:
        return [line.strip() for line in open('data/candidates.txt').readlines()]
