class Product:
    """
    Product model used in app (basic).
    """
    def __init__(self, name: str, price: float, description: str = "", image_url: str = ""):
        self.name = name
        self.price = float(price)
        self.description = description
        self.image_url = image_url

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Product has no attribute '{key}'")

    def to_dict(self):
        return {"name": self.name, "price": self.price, "description": self.description, "image_url": self.image_url}

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"

