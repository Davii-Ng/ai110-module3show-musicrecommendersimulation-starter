"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


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
        print(f"=== {profile_name} ===")
        print(f"prefs: {user_prefs}\n")
        for song, score, reasons in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            reason_text = ", ".join(reasons) if isinstance(reasons, list) else str(reasons)
            print(f"Because: {reason_text}")
            print()


if __name__ == "__main__":
    main()
