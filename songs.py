class Song:
    _song_counter = 0

    def __init__(self, title:str, artist:str, duration:int):
        Song._song_counter += 1
        self.song_id = f"S{Song._song_counter:03d}"
        self.title = title
        self.artist = artist
        self.duration = duration
        self.play_count = 0
        self.total_rating = 0.0
        self.rating_count = 0

    def play(self) -> None:
        self.play_count += 1 # სიმღერის დაკვრა

    def add_rating(self, rating:float) -> None:
        """რეიტინგის ვალიდაცია"""
        try:
            if not(1.0 <= rating <= 5.0):
                raise ValueError("რეიტინგი უნდა იყოს 1.0-დან 5.0-ის ჩათვლით.")
            self.total_rating += rating
            self.rating_count += 1
        except ValueError as e:
            print(f"მოხდა შეცდომა: {e}")
        except TypeError:
            print(f"შეცდომა: რეიტინგი უნდა იყოს რიცხვი")

    def get_average_rating(self) -> float:
        if self.rating_count == 0:
            return 0.0
        return self.total_rating / self.rating_count

    def get_duration_formatted(self) -> str:
        """წამებსა და წუთებში გადაყვანა"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    def get_info(self) -> str:
        avg_rating = self.get_average_rating()
        return (f"ID: {self.song_id} | {self.title} - {self.artist}\n"
                f"ხანგრძლივობა: {self.get_duration_formatted()}\n"
                f"რეიტინგი: {avg_rating:.1f} ({self.rating_count} შეფასება)\n"
                f"მოსმენების რაოდენობა: {self.play_count}"
                )

    def __str__(self) -> str:
        return f"{self.title} - {self.artist}"

class PopSong(Song):
    _pop_counter = 0
    def __init__(self, title:str, artist:str, duration: int, is_chart_topper: bool):
        super().__init__(title, artist, duration)
        PopSong._pop_counter += 1
        self.song_id = f"P{PopSong._pop_counter:03d}"
        self.is_chart_topper = is_chart_topper

    def calculate_popularity(self) -> float:
        return self.play_count * 1.5 + (50 if self.is_chart_topper else 0)

    def get_charted_status(self) -> str:
        return "Chart Topper" if self.is_chart_topper else "Popular Track"

class RockSong(Song):
    _rock_counter = 0
    def __init__(self, title:str, artist:str, duration:int, intensity_level:int, has_guitar_solo: bool):
        super().__init__(title, artist, duration)
        RockSong._rock_counter += 1
        self.song_id = f"R{RockSong._rock_counter:03d}"
        self.intensity_level = intensity_level
        self.has_guitar_solo = has_guitar_solo

    def calculate_energy_score(self) -> float:
        return self.intensity_level * 10 +(25 if self.has_guitar_solo else 0)

    def get_intensity_description(self) -> str:
        solo = "Yes" if self.has_guitar_solo else "No"
        return f"High Intensity ({self.intensity_level}/10 | Guitar Solo: {solo})"

class ClassicalSong(Song):
    _classical_counter = 0
    def __init__(self, title:str, artist:str, duration:int, composer:str, era:str, instruments: list):
        super().__init__(title, artist, duration)
        ClassicalSong._classical_counter +=1
        self.song_id = f"C{ClassicalSong._classical_counter:03d}"
        self.composer = composer
        self.era = era
        self.instruments = instruments

    def calculate_complexity_score(self) -> float:
        return (self.duration/ 60) * 5 +len(self.instruments) * 10

    def get_classical_info(self) -> str:
        used_instruments = ",".join(self.instruments)
        return f"Composer: {self.composer} | Era: {self.era} | Instruments: {used_instruments}"





