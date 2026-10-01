"""Everything that prints the menu or the receipt."""
import datetime
from menu import STORE_NAME

WIDTH = 40


def display_menu(lookup):
    print("=" * WIDTH)
    print(STORE_NAME.center(WIDTH))
    print("=" * WIDTH)
    for number in lookup:
        name, price = lookup[number]
        print(f"{number:>2}. {name:<20} PHP {price:>6.2f}")
    print("=" * WIDTH)


def print_receipt(orders, subtotal, discount, discount_label, total):
    print("\n" + "=" * WIDTH)
    print(STORE_NAME.center(WIDTH))
    print(datetime.datetime.now().strftime("%b %d, %Y %I:%M %p").center(WIDTH))
    print("-" * WIDTH)
    for item, qty, price in orders:
        print(f"{item:<16}{qty:>3} x {price:>6.2f} = {qty*price:>7.2f}")
    print("-" * WIDTH)
    print(f"{'SUBTOTAL':<25}{subtotal:>15.2f}")
    if discount_label:
        print(f"{discount_label:<25}{-discount:>15.2f}")
    print(f"{'TOTAL':<25}{total:>15.2f}")
    print("=" * WIDTH)
    print("Thank you, come again!".center(WIDTH))
    print("=" * WIDTH + "\n")