from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def make_diversity_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Happy Pop One",
            artist="Shared Artist",
            genre="pop",
            mood="happy",
            energy=0.80,
            tempo_bpm=120,
            valence=0.90,
            danceability=0.82,
            acousticness=0.18,
        ),
        Song(
            id=2,
            title="Happy Pop Two",
            artist="Shared Artist",
            genre="pop",
            mood="happy",
            energy=0.79,
            tempo_bpm=121,
            valence=0.89,
            danceability=0.81,
            acousticness=0.20,
        ),
        Song(
            id=3,
            title="Happy Pop Three",
            artist="Different Artist",
            genre="pop",
            mood="happy",
            energy=0.78,
            tempo_bpm=119,
            valence=0.88,
            danceability=0.80,
            acousticness=0.19,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_diversity_penalty_flags_repeated_artist_and_genre():
    rec = make_diversity_recommender()
    chosen_songs = [rec.songs[0]]

    penalty, reasons = rec._diversity_penalty(rec.songs[1], chosen_songs)

    assert penalty == 3.0
    assert "artist already in top results (-2.0)" in reasons
    assert "genre already in top results (-1.0)" in reasons


def test_recommend_prefers_unique_artist_when_scores_are_close():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_diversity_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert len({song.artist for song in results}) == 2
    assert any(song.artist == "Different Artist" for song in results)
