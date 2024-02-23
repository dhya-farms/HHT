from app.customers.models import Customer, Address, Wishlist, WishlistItem, Review, CartItem
from app.utils.controllers import Controller


class CustomerController(Controller):
    def __init__(self):
        super().__init__(model=Customer)


class AddressController(Controller):
    def __init__(self):
        super().__init__(model=Address)


class WishlistController(Controller):
    def __init__(self):
        super().__init__(model=Wishlist)


class WishlistItemController(Controller):
    def __init__(self):
        super().__init__(model=WishlistItem)


class ReviewController(Controller):
    def __init__(self):
        super().__init__(model=Review)


class CartItemController(Controller):
    def __init__(self):
        super().__init__(model=CartItem)
