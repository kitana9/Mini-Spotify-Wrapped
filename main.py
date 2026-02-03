from songs import Song, PopSong, RockSong, ClassicalSong
from user import User
from streaming_system import StreamingSystem

def main():
    print("=" * 70)
    print("      მუსიკალური სტრიმინგის სისტემის დემონსტრაცია")
    print("=" * 70)
    print()

    system = StreamingSystem("GeorgianMusic Streaming")
    print(f"✓ სისტემა '{system.platform_name}' შეიქმნა!\n")

    """დავამატოთ სიმღერები"""
    print("📀 სიმღერების დამატება...")
    print("-" * 40)

    pop1 = PopSong("Billie Jean", "Michael Jackson", 294, True)
    pop2 = PopSong("Blinding Lights", "The Weeknd", 200, True)
    pop3 = PopSong("Shake It Off", "Taylor Swift", 219, False)

    rock1 = RockSong("Bohemian Rhapsody", "Queen", 354, 9, True)
    rock2 = RockSong("Stairway to Heaven", "Led Zeppelin", 482, 8, True)
    rock3 = RockSong("Hotel California", "Eagles", 390, 7, True)

    classical1 = ClassicalSong("Moonlight Sonata", "Ludwig van Beethoven",
                               330, "Ludwig van Beethoven", "Romantic", ["Piano"])
    classical2 = ClassicalSong("Four Seasons: Spring", "Antonio Vivaldi",
                               200, "Antonio Vivaldi", "Baroque", ["Violin", "Orchestra"])
    classical3 = ClassicalSong("Symphony No. 5", "Ludwig van Beethoven",
                               435, "Ludwig van Beethoven", "Classical", ["Orchestra"])
    classical4 = ClassicalSong("Clair de Lune", "Claude Debussy",
                               300, "Claude Debussy", "Impressionist", ["Piano"])

    """დავამატოთ სისტემაშიც"""
    for song in [pop1, pop2, pop3, rock1, rock2, rock3,
                 classical1, classical2, classical3, classical4]:
        system.add_song(song)
        print(f"  ✓ დაემატა: {song} (ID: {song.song_id})")

    print(f"\nჯამური სიმღერები სისტემაში: {len(system.songs)}\n")

    """დავამატოთ მომხმარებლები"""
    print("👤 მომხმარებლების რეგისტრაცია...")
    print("-" * 40)

    user1 = User("giorgi_music", "giorgi@gmail.com", False)
    user2 = User("mari_beats", "mari@gmail.com", True, 9.99)
    user3 = User("nino_rocks", "nino@gmail.com", True, 9.99)
    user4 = User("luka_classical", "luka@gmail.com", False)
    user5 = User("ana_pop", "ana@gmail.com", True, 9.99)

    for user in [user1, user2, user3, user4, user5]:
        system.add_user(user)
        print(f"  ✓ {user}")

    print(f"\nჯამური მომხმარებლები: {len(system.users)}\n")

    """დავიწყოთ მოსმენა"""
    print("🎧 მოსმენების სიმულაცია...")
    print("-" * 40)

    """გიორგის მოსმენები"""
    user1.listen_to_song(rock1, "2025-01-10")
    user1.listen_to_song(rock1, "2025-01-11")
    user1.listen_to_song(rock2, "2025-01-11")
    user1.listen_to_song(rock3, "2025-01-12")

    """მარის მოსმენები"""
    user2.listen_to_song(pop1, "2025-01-10")
    user2.listen_to_song(pop1, "2025-01-11")
    user2.listen_to_song(pop2, "2025-01-11")
    user2.listen_to_song(pop3, "2025-01-12")

    """ნინოს მოსმენები"""
    user3.listen_to_song(rock1, "2025-01-10")
    user3.listen_to_song(rock1, "2025-01-11")
    user3.listen_to_song(rock2, "2025-01-12")

    """ლუკას მოსმენები"""
    user4.listen_to_song(classical1, "2025-01-10")
    user4.listen_to_song(classical2, "2025-01-11")
    user4.listen_to_song(classical1, "2025-01-12")
    user4.listen_to_song(classical3, "2025-01-13")

    """ანას მოსმენები"""
    user5.listen_to_song(pop1, "2025-01-10")
    user5.listen_to_song(pop2, "2025-01-11")
    user5.listen_to_song(pop1, "2025-01-12")

    print("  ✓ მოსმენები დასრულდა!\n")

    """რეიტინგები"""
    print("⭐ რეიტინგების დამატება...")
    print("-" * 40)

    user1.rate_song(rock1, 5.0)
    user1.rate_song(rock2, 4.8)
    user1.rate_song(rock3, 4.5)

    user2.rate_song(pop1, 4.9)
    user2.rate_song(pop2, 4.7)
    user2.rate_song(pop3, 4.3)

    user3.rate_song(rock1, 4.8)
    user3.rate_song(rock2, 4.9)

    user4.rate_song(classical1, 4.7)
    user4.rate_song(classical2, 4.6)
    user4.rate_song(classical3, 4.8)

    user5.rate_song(pop1, 4.8)
    user5.rate_song(pop2, 4.6)

    print("  ✓ რეიტინგები დაემატა!\n")

    """ფლეილისტების შექმნა"""
    print("📋 პლეილისტების შექმნა...")
    print("-" * 40)

    user1.create_playlist("My Rock Collection")
    user1.add_to_playlist("My Rock Collection", rock1)
    user1.add_to_playlist("My Rock Collection", rock2)
    user1.add_to_playlist("My Rock Collection", rock3)

    user2.create_playlist("Pop Favorites")
    user2.add_to_playlist("Pop Favorites", pop1)
    user2.add_to_playlist("Pop Favorites", pop2)

    user4.create_playlist("Classical Evening")
    user4.add_to_playlist("Classical Evening", classical1)
    user4.add_to_playlist("Classical Evening", classical2)
    user4.add_to_playlist("Classical Evening", classical4)

    print()

    """სტატისტიკის დაბეჭდვა"""
    print("📊 სისტემის სტატისტიკა:")
    print("=" * 70)

    print(f"\n💰 ყოველთვიური შემოსავალი: {system.get_total_premium_revenue():.2f} ლარი")
    print(f"🎤 ყველაზე პოპულარული არტისტი: {system.get_most_popular_artist()}")

    print("\n🏆 TOP 5 სიმღერი (რეიტინგით):")
    for i, song in enumerate(system.get_top_rated_songs(5), 1):
        print(f"  {i}. {song} - ⭐ {song.get_average_rating():.1f}/5.0")

    print("\n🔥 TOP 5 სიმღერი (მოსმენებით):")
    for i, song in enumerate(system.get_most_played_songs(5), 1):
        print(f"  {i}. {song} - 🎵 {song.play_count:,} მოსმენა")

    print("\n👥 მომხმარებლების საყვარელი არტისტები:")
    for user in [user1, user2, user3, user4, user5]:
        fav = user.get_favorite_artist(system.songs)
        hours = user.get_total_listening_time(system.songs) / 3600
        print(f"  • {user.username}: {fav} | ჯამური: {hours:.1f} საათი")

    """ანგარიშის დაბეჭდვა"""
    print("\n" + "=" * 70)
    print("📄 დეტალური ანგარიშის გენერაცია...")
    print("-" * 40)

    system.generate_report("streaming_report.txt")

    print("\n✅ პროგრამა წარმატებით დასრულდა!")
    print("=" * 70)

if __name__ == "__main__":
    main()

