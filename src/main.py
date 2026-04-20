"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs
from textwrap import wrap


def _print_recommendation_table(profile_name: str, user_prefs: dict, recommendations) -> None:
    title_width = 24
    artist_width = 18
    score_width = 7
    reasons_width = 64

    print(f"=== {profile_name} ===")
    print(f"prefs: {user_prefs}")
    print()
    print(
        f"{'Title':<{title_width}}  {'Artist':<{artist_width}}  {'Score':>{score_width}}  Reasons"
    )
    print(
        f"{'-' * title_width}  {'-' * artist_width}  {'-' * score_width}  {'-' * reasons_width}"
    )

    for song, score, reasons in recommendations:
        reason_text = "; ".join(reasons) if isinstance(reasons, list) else str(reasons)
        wrapped_reasons = wrap(reason_text, width=reasons_width) or [""]
        first_line = wrapped_reasons[0]
        print(
            f"{song['title'][:title_width]:<{title_width}}  {song['artist'][:artist_width]:<{artist_width}}  {score:>{score_width}.2f}  {first_line}"
        )
        for continuation in wrapped_reasons[1:]:
            print(
                f"{'':<{title_width}}  {'':<{artist_width}}  {'':>{score_width}}  {continuation}"
            )

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    profiles = [
        (
            "Conflict profile: high energy + sad",
            {
                "genre": "pop",
                "mood": "sad",
                "energy": 0.95,
                "likes_acoustic": True,
            },
        ),
        (
            "Unknown mood fallback",
            {
                "genre": "lofi",
                "mood": "bittersweet",
                "energy": 0.6,
                "likes_acoustic": True,
            },
        ),
        (
            "Out-of-range energy",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 1.8,
                "likes_acoustic": False,
            },
        ),
    ]

    print("\nAdversarial profile results:\n")
    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=3)
        _print_recommendation_table(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
