from toas_bot import ToasBot

from time import sleep

if __name__ == "__main__":
    booking_type = "Sauna"  # "pesuvuorot", "saunavuorot", "kerhohuoneet"
    booking_time = "20:30 2023-12-15"  # Format: "HH:MM YYYY-MM-DD" !!! Automatically rounded to the last 30 min interval!!!
    bot = ToasBot()
    # Test club room changes
    print("\nTESTING CLUB ROOM CHANGES")
    bot.open_club_room_reservation_page()
    print(f"Type: {bot.current_booking_type}")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("C-D")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")

    # Test sauna changes
    print("\nTESTING SAUNA CHANGES")
    bot.open_sauna_reservation_page()
    print(f"Type: {bot.current_booking_type}")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("C-D")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")

    # Test laundy changes
    print("\nTESTING LAUNDRY CHANGES")
    bot.open_laundry_reservation_page()
    print(f"Type: {bot.current_booking_type}")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("C-D")
    print(f"Staircase: {bot.current_staircase}")
    bot.select_staricase("A-B")
    print(f"Staircase: {bot.current_staircase}")
