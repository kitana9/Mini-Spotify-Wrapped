from datetime import datetime
from songs import Song
class User:
    _user_counter = 0
    def __init__(self, username:str, email:str, is_premium: bool, monthly_fee:float = 0.0):
        User._user_counter +=1
        self.user_id = f"U{User._user_counter:03d}"
        self.username = username
        self.email = email
        self.is_premium = is_premium
        self.monthly_fee = monthly_fee
        self.listening_history = []
        self.playlists = {}

    def upgrade_to_premium(self, monthly_fee: float) -> None:
        self.is_premium = True
        self.monthly_fee = monthly_fee
        print(f"{self.username}-მა იყიდა პრემიუმი, თვიური გადასახადი: {self.monthly_fee} GEL")

    def listen_to_song(self, song: Song, date:str):
        time = datetime.now().strftime("%H:%M:%S")
        self.listening_history.append((song.song_id, time))
        song.play()

    def rate_song(self, song: Song, rating:float) -> None:
        song.add_rating(rating)

    def create_playlist(self, playlist_name:str) -> None:
        try:
            if playlist_name in self.playlists:
                print(f"ფლეილისტი {playlist_name} უკვე არსებობს")
                return False
            self.playlists[playlist_name] = []
            return True
        except ValueError as e:
            print(f"დაფიქისრდა შეცდომა: {e}")

    def add_to_playlist(self, playlist_name: str, song: Song) -> bool:
        """ფლეილისტიში დამატება"""
        try:
            if playlist_name not in self.playlists:
                print(f"ფლეილისტი '{playlist_name}' არ არსებობს!")
                return False
            self.playlists[playlist_name].append(song.song_id)
            return True
        except (KeyError, ValueError) as e:
            print(f"შეცდომა: {e}")

    def get_playlist_duration(self, playlist_name:str, songs_dict:dict)-> int:
        if playlist_name not in self.playlists:
            return 0
        total = 0
        for song_id in self.playlists[playlist_name]:
            if song_id in songs_dict:
                total +=songs_dict[song_id].duration
        return total

    def get_listening_history(self) ->str:
        try:
            if not self.listening_history:
                return "ისტორია ცარიელია"
            result = f"\n{self.username}-ის მოსმენების ისტორია:\n"
            result += "=" * 60 + "\n"
            for item in self.listening_history:
                try:
                    if isinstance(item, tuple) and len(item) >= 3:
                        song_id, timestamp, date = item
                        result += f"{date} {timestamp} - Song ID: {song_id}\n"
                    elif isinstance(item, (tuple, list)) and len(item) >= 1:
                        song_id = item[0]
                        result += f"Song ID: {song_id}\n"
                except (ValueError, IndexError):
                    continue

            return result
        except Exception as e:
            print(f"შეცდომა get_listening_history-ში: {e}")
            return "შეცდომა ისტორიის ჩატვირთვისას"

    def get_total_listening_time(self, songs_dict: dict) -> int:
        try:
            total = 0
            for item in self.listening_history:
                try:
                    if isinstance(item, tuple) and len(item) >= 3:
                        song_id = item[0]
                    elif isinstance(item, (tuple, list)) and len(item) >= 1:
                        song_id = item[0]
                    else:
                        continue

                    if song_id in songs_dict:
                        total += songs_dict[song_id].duration
                except (ValueError, IndexError, TypeError):
                    continue
            return total
        except Exception as e:
            print(f"შეცდომა get_total_listening_time-ში: {e}")
            return 0

    def get_favorite_artist(self, songs_dict: dict) -> str:
        try:
            if not self.listening_history:
                return "არ არის ისტორია"
            artist_counts = {}
            for item in self.listening_history:
                try:
                    if isinstance(item, tuple) and len(item) >= 3:
                        song_id = item[0]
                    elif isinstance(item, (tuple, list)) and len(item) >= 1:
                        song_id = item[0]
                    else:
                        continue
                    if song_id in songs_dict:
                        artist = songs_dict[song_id].artist
                        artist_counts[artist] = artist_counts.get(artist, 0) + 1
                except (ValueError, IndexError, KeyError, AttributeError):
                    continue

            if not artist_counts:
                return "არ არის ისტორია"
            return max(artist_counts, key=artist_counts.get)
        except Exception as e:
            print(f"შეცდომა get_favorite_artist-ში: {e}")
            return "შეცდომა"

    def __str__(self) -> str:
        status = "Premium" if self.is_premium else "Free"
        return f"User: {self.username} (ID: {self.user_id} - {status}"
