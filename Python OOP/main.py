from restaurant import Restaurant, Menu, Printer, DiscountPolicy

MENU_DATA = {
    "Burgers": {"Cheeseburger": 89.00, "Beef Burger": 129.00, "Chicken Burger": 99.00},
    "Sides": {"French Fries": 49.00, "Onion Rings": 55.00},
    "Drinks": {"Soft Drink": 39.00, "Iced Tea": 45.00, "Bottled Water": 25.00},
}


def main():
    name = "EDRIAN FOOD RESTAURANT"
    Restaurant(
        name=name,
        menu=Menu(MENU_DATA),
        printer=Printer(name, width=40),
        discount_policy=DiscountPolicy(senior_rate=0.20, bulk_rate=0.05, bulk_qty=5),
    ).run()


if __name__ == "__main__":
    main()