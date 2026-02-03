from datetime import datetime
from songs import Song, PopSong, RockSong, ClassicalSong
from user import User

class StreamingSystem:
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.songs = {}
        self.users = {}

    def add_song(self, song: Song) -> None:
        self.songs[song.song_id] = song

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def find_song(self, song_id:str):
        if song_id not in self.songs:
            raise KeyError(f"სიმღერა {song_id} არ მოიძებნა")
        return self.songs.get(song_id)

    def find_user(self, user_id:str):
        if user_id not in self.users:
            raise KeyError(f"მომხმარებელი ID-ით {user_id} არ მოიძებნა")
        return self.users.get(user_id)

    def get_songs_by_genre(self, genre:str) -> list:
        genres = {
            "PopSong": PopSong,
            "RockSong": RockSong,
            "ClassicalSong": ClassicalSong,
        }
        if genre not in genres:
            return []

        genre_type = genres[genre]
        return [song for song in self.songs.values() if isinstance(song, genre_type)]

    def get_top_rated_songs(self, limit: int=10) -> list:
        songs = []
        for song in self.songs.values():
            if song.rating_count >0:
                songs.append(song)

        songs.sort(key=lambda song: song.get_average_rating(), reverse=True)
        return songs[:limit]

    def get_most_played_songs(self, limit: int=10) -> list:
        songs = []
        for song in self.songs.values():
            songs.append(song)

        songs.sort(key=lambda song: song.play_count, reverse=True)
        return songs[:limit]

    def get_total_premium_revenue(self) -> float:
        total_premium_revenue = 0
        for user in self.users.values():
            if user.is_premium:
                total_premium_revenue += user.monthly_fee
        return total_premium_revenue

    def get_most_popular_artist(self) -> str:
        try:
            artist_counts = {}
            for user in self.users.values():
                for item in user.listening_history:
                    if len(item) >= 3:
                        song_id, _, _, = item
                    elif len(item) >= 1:
                        song_id = item[0]
                    else:
                        continue

                    if song_id in self.songs:
                        artist = self.songs[song_id].artist
                        artist_counts[artist] = artist_counts.get(artist, 0) + 1

            if not artist_counts:
                return "მონაცემები არ არის ხელმისაწვდომი"

            most_popular = max(artist_counts, key=artist_counts.get)
            return (f"{most_popular} ({artist_counts[most_popular]} მოსმენა)")
        except Exception as e:
            print(f"შეცდომა: {e}")

    def generate_report(self, filename:str) -> None:
        """ფინალური ანგარიშის დაბეჭდვა"""
        try:
            with open(filename, "w", encoding = "utf-8") as f:
                f.write("="*65 +"\n")
                f.write(f"    {self.platform_name} - ანგარიში\n")
                f.write("="*65 +"\n")
                f.write(f"თარიღი: {datetime.now().strftime('%Y-%m-%d')}\n\n")

                """სიმღერების სტატისტიკა"""
                pop_songs = self.get_songs_by_genre("PopSong")
                rock_songs = self.get_songs_by_genre("RockSong")
                classic_songs = self.get_songs_by_genre("ClassicalSong")

                f.write("სიმღერების სტატისტიკა:\n")
                f.write("-"*24 +"\n")
                f.write(f"ჯამური სიმღერები: {len(self.songs)}\n")
                f.write(f"  -პოპ: {len(pop_songs)}\n")
                f.write(f"  -როკ: {len(rock_songs)}\n")
                f.write(f"  -კლასიკური: {len(classic_songs)}\n")

                """მომხმარებლების სტატისტიკა"""
                premium_users = [user for user in self.users.values() if user.is_premium]
                free_users = [user for user in self.users.values() if not user.is_premium]

                f.write("მომხმარებლების სტატისტიკა:\n")
                f.write("-"*27 +"\n")
                f.write(f"რეგისტრირებული მომხმარებლები: {len(self.users)}\n")
                f.write(f"  -პრემიუმ აბონენტები: {len(premium_users)}\n")
                f.write(f"  -უფასო მომხმარებლები: {len(free_users)}\n")

                """ფინანსური ანგარიში"""
                revenue = self.get_total_premium_revenue()
                f.write("ფინანსური ანგარიში:\n")
                f.write("-"*19+"'\n")
                f.write(f"ყოველთვიური შემოსავალი პრემიუმებიდან: {revenue:.2f} ლარი\n")
                f.write(f"ყველაზე პოპულარული არტისტი: {self.get_most_popular_artist()}\n\n")

                """TOP 10 სიმღერა რეიტინგით"""
                f.write("TOP 10 სიმღერა (რეიტინგით):\n")
                f.write("-"*29+"\n")
                top_rated = self.get_top_rated_songs(10)
                for idx, song in enumerate(top_rated, 1):
                    avg = song.get_average_rating()
                    f.write(f"{idx}. {song.title} - {song.artist} ⭐ {avg:.1f}/5.0" 
                            f"({song.rating_count} რეიტინგი)\n")
                f.write("\n")

                """TOP 10 სიმღერა მოსმენებით"""
                f.write("TOP 10 სიმღერა (მოსმენებით):\n")
                f.write("-"*30+"\n")
                most_played = self.get_most_played_songs(10)
                for idx, song in enumerate(most_played, 1):
                    f.write(f"{idx}. {song.title} - {song.artist} 🎵 {song.play_count:,} მოსმენა\n")
                f.write("\n")

                """TOP 5 მომხმარებელი"""
                f.write("TOP 5 მომხმარებელი (მოსმენილი დრო):\n")
                f.write("-"*36+"\n")
                users_with_time = []
                for user in self.users.values():
                    total_seconds = user.get_total_listening_time(self.songs)
                    hours = total_seconds // 3600
                    users_with_time.append((user, hours))

                users_with_time.sort(key=lambda x: x[1], reverse=True)
                for i, (user, hours) in enumerate(users_with_time[:5], 1):
                    status = "Premium" if user.is_premium else "Free"
                    f.write(f"{i}. {user.username} - {hours:.1f} საათი ({status})\n")
                f.write("\n")

                """სტატისტიკა ჟანრების მიხედვით"""
                f.write("დეტალური სტატისტიკა ჟანრების მიხედვით:\n")
                f.write("-"*41+"\n")

                self._write_pop_section(f, pop_songs)
                self._write_rock_section(f, rock_songs)
                self._write_classical_section(f, classic_songs)

                f.write("="*65 +"\n")
                f.write("           ანგარიშის დასასრული\n")
                f.write("="*65 +"\n")
            print(f"ანგარიში წარმატებით შეიქმნა: {filename}")
        except PermissionError as e:
            print(f"შეცდომა, თქვენ არ გაქვთ წვდომა ამ ფაილზე, {e}")
        except Exception as e:
            print(f" შეცდომა, {e}")

    def _write_pop_section(self, f, pop_songs):
        """Pop სექცია"""
        f.write("🎵 POP ᲛᲣᲡᲘᲙᲐ (PopSong):\n")
        f.write(f"   ჯამური სიმღერები: {len(pop_songs)}\n\n")
        f.write("   სიმღერების სია:\n")

        for song in pop_songs:
            chart_maker = "⭐" if song.is_chart_topper else ""
            f.write(f"   • {song.song_id} - {song.title} - {song.artist} "
                    f"({song.get_duration_formatted()}) {chart_maker} {song.get_charted_status()}\n")
            f.write(f"     მოსმენები: {song.play_count:,} | რეიტინგი: "
                    f"{song.get_average_rating():.1f}/5.0\n")

        total_plays = sum(s.play_count for s in pop_songs)
        avg_rating = sum(s.get_average_rating() for s in pop_songs) / len(pop_songs) if pop_songs else 0
        chart_toppers = sum(1 for s in pop_songs if s.is_chart_topper)

        f.write(f"\n   ჯამური მოსმენები: {total_plays:,}\n")
        f.write(f"   საშუალო რეიტინგი: {avg_rating:.1f}/5.0\n")
        f.write(f"   Chart Toppers: {chart_toppers}\n\n")

    def _write_rock_section(self, f, rock_songs):
        """როკ სექცია"""
        f.write("🎸 როკ ᲛᲣᲡᲘᲙᲐ (RockSong):\n")
        f.write(f"   ჯამური სიმღერები: {len(rock_songs)}\n\n")
        f.write("   სიმღერების სია:\n")

        for song in rock_songs:
            solo = "✓" if song.has_guitar_solo else "✗"
            f.write(f"   • {song.song_id} - {song.title} - {song.artist} "
                    f"({song.get_duration_formatted()}) 🔥 Intensity: {song.intensity_level}/10 | Solo: {solo}\n")
            f.write(f"     მოსმენები: {song.play_count:,} | რეიტინგი: "
                    f"{song.get_average_rating():.1f}/5.0\n")

        total_plays = sum(s.play_count for s in rock_songs)
        avg_rating = sum(s.get_average_rating() for s in rock_songs) / len(rock_songs) if rock_songs else 0
        avg_intensity = sum(s.intensity_level for s in rock_songs) / len(rock_songs) if rock_songs else 0
        guitar_solos = sum(1 for s in rock_songs if s.has_guitar_solo)

        f.write(f"\n   ჯამური მოსმენები: {total_plays:,}\n")
        f.write(f"   საშუალო რეიტინგი: {avg_rating:.1f}/5.0\n")
        f.write(f"   საშუალო ინტენსივობა: {avg_intensity:.1f}/10\n")
        f.write(f"   Guitar Solos: {guitar_solos}\n\n")

    def _write_classical_section(self, f, classical_songs):
        """კლასიკური სექცია"""
        f.write("🎻 ᲙᲚᲐᲡᲘᲙᲣᲠᲘ ᲛᲣᲡᲘᲙᲐ (ClassicalSong):\n")
        f.write(f"   ჯამური სიმღერები: {len(classical_songs)}\n\n")
        f.write("   სიმღერების სია:\n")

        for song in classical_songs:
            instruments_str = ", ".join(song.instruments)
            f.write(f"   • {song.song_id} - {song.title} - {song.artist} "
                    f"({song.get_duration_formatted()})\n")
            f.write(f"     Era: {song.era} | Instruments: {instruments_str}\n")
            f.write(f"     მოსმენები: {song.play_count:,} | რეიტინგი: "
                    f"{song.get_average_rating():.1f}/5.0\n")

        total_plays = sum(s.play_count for s in classical_songs)
        avg_rating = sum(s.get_average_rating() for s in classical_songs) / len(
            classical_songs) if classical_songs else 0

        """ეპოქების მიხედვით"""
        era_counts = {}
        for song in classical_songs:
            era_counts[song.era] = era_counts.get(song.era, 0) + 1

        f.write(f"\n   ჯამური მოსმენები: {total_plays:,}\n")
        f.write(f"   საშუალო რეიტინგი: {avg_rating:.1f}/5.0\n")
        f.write("   ეპოქების განაწილება:\n")
        for era, count in era_counts.items():
            f.write(f"     - {era}: {count} სიმღერა\n")
        f.write("\n")