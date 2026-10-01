import datetime
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MenuItem:
    number: int
    name: str
    price: float
    category: str


class Menu:
    """Holds menu items grouped by category and numbers them for lookup."""

    def __init__(self, data: dict):
        self._items: dict[int, MenuItem] = {}
        number = 1
        for category, items in data.items():
            for name, price in items.items():
                self._items[number] = MenuItem(number, name, price, category)
                number += 1

    def __contains__(self, number: int) -> bool:
        return number in self._items

    def __iter__(self):
        return iter(self._items.values())

    def get(self, number: int) -> MenuItem:
        return self._items[number]


@dataclass
class OrderLine:
    item: MenuItem
    quantity: int

    @property
    def amount(self) -> float:
        return self.item.price * self.quantity


@dataclass
class Discount:
    label: Optional[str]
    amount: float


class DiscountPolicy:
    """Decides which discount applies to an order."""

    def __init__(self, senior_rate=0.20, bulk_rate=0.05, bulk_qty=5):
        self.senior_rate = senior_rate
        self.bulk_rate = bulk_rate
        self.bulk_qty = bulk_qty

    def evaluate(self, order: "Order") -> Discount:
        if order.is_senior:
            return Discount(
                f"Senior/PWD Discount ({self.senior_rate:.0%})",
                order.subtotal * self.senior_rate,
            )
        if order.total_quantity >= self.bulk_qty:
            return Discount(
                f"Discount ({self.bulk_rate:.0%})",
                order.subtotal * self.bulk_rate,
            )
        return Discount(None, 0.0)


@dataclass
class Order:
    discount_policy: DiscountPolicy
    lines: list[OrderLine] = field(default_factory=list)
    is_senior: bool = False
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def add(self, item: MenuItem, quantity: int) -> None:
        self.lines.append(OrderLine(item, quantity))

    @property
    def subtotal(self) -> float:
        return sum(line.amount for line in self.lines)

    @property
    def total_quantity(self) -> int:
        return sum(line.quantity for line in self.lines)

    @property
    def discount(self) -> Discount:
        return self.discount_policy.evaluate(self)

    @property
    def total(self) -> float:
        return self.subtotal - self.discount.amount


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------
class Printer:
    """Renders the menu and receipts to the console."""

    def __init__(self, store_name: str, width: int = 40):
        self.store_name = store_name
        self.width = width

    def show_menu(self, menu: Menu) -> None:
        w = self.width
        print("=" * w)
        print(self.store_name.center(w))
        print("=" * w)
        for item in menu:
            print(f"{item.number:>2}. {item.name:<20} PHP {item.price:>6.2f}")
        print("=" * w)

    def show_receipt(self, order: Order) -> None:
        w = self.width
        discount = order.discount
        print("\n" + "=" * w)
        print(self.store_name.center(w))
        print(order.created_at.strftime("%b %d, %Y %I:%M %p").center(w))
        print("-" * w)
        for line in order.lines:
            print(
                f"{line.item.name:<16}{line.quantity:>3} x "
                f"{line.item.price:>6.2f} = {line.amount:>7.2f}"
            )
        print("-" * w)
        print(f"{'SUBTOTAL':<25}{order.subtotal:>15.2f}")
        if discount.label:
            print(f"{discount.label:<25}{-discount.amount:>15.2f}")
        print(f"{'TOTAL':<25}{order.total:>15.2f}")
        print("=" * w)
        print("Thank you, come again!".center(w))
        print("=" * w + "\n")


class ConsoleInput:
    """Validated user input helpers."""

    @staticmethod
    def yes_no(prompt: str) -> bool:
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print(" Invalid choice! Please enter 'y' or 'n'.")

    @staticmethod
    def item_number(menu: Menu) -> int:
        while True:
            raw = input("Item number: ").strip()
            if raw.isdigit() and int(raw) in menu:
                return int(raw)
            print("  Invalid item number.")

    @staticmethod
    def quantity() -> int:
        while True:
            raw = input("Quantity: ").strip()
            if raw.isdigit() and int(raw) > 0:
                return int(raw)
            print("  Invalid quantity.")


class Restaurant:
    def __init__(self, name: str, menu: Menu, printer: Printer,
                 discount_policy: DiscountPolicy):
        self.name = name
        self.menu = menu
        self.printer = printer
        self.discount_policy = discount_policy

    def _take_order(self) -> Order:
        order = Order(self.discount_policy)
        while True:
            item = self.menu.get(ConsoleInput.item_number(self.menu))
            order.add(item, ConsoleInput.quantity())
            if not ConsoleInput.yes_no("Order another item? (y/n): "):
                break
        order.is_senior = ConsoleInput.yes_no("Senior Citizen/PWD? (y/n): ")
        return order

    def run(self) -> None:
        while True:
            self.printer.show_menu(self.menu)

            if not ConsoleInput.yes_no("Order now? (y/n): "):
                break

            order = self._take_order()
            self.printer.show_receipt(order)

            if not ConsoleInput.yes_no("Would you like to order again? (y/n): "):
                break
        print("Goodbye!")