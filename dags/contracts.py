import decimal
import hashlib

import pydantic


class Price(pydantic.BaseModel):
    price: decimal.Decimal
    date: str | None = None

    def __str__(self) -> str:
        return f"{self.price} {self.date}"

    def data_hash(self) -> str:
        hasher = hashlib.sha256()
        hasher.update(str(self.price).encode("utf-8"))
        hasher.update(self.date.encode("utf-8") if self.date is not None else b"")
        return hasher.hexdigest()


class PriceList(pydantic.RootModel):
    root: list[Price]

    @property
    def data_hash(self) -> str:
        hasher = hashlib.sha256()
        for price in self.root:
            hasher.update(price.data_hash().encode("utf-8"))
        return hasher.hexdigest()


class Holding(pydantic.BaseModel):
    name: str
    percentage: decimal.Decimal | None = None
    position: int | None = None

    def __str__(self) -> str:
        return self.name

    @property
    def data_hash(self) -> str:
        hasher = hashlib.sha256()
        hasher.update(self.name.encode("utf-8"))
        hasher.update(
            str(self.percentage).encode("utf-8") if self.percentage is not None else b"",
        )
        hasher.update(
            str(self.position).encode("utf-8") if self.position is not None else b"",
        )
        return hasher.hexdigest()


class HoldingList(pydantic.RootModel):
    root: list[Holding]

    @property
    def data_hash(self) -> str:
        hasher = hashlib.sha256()
        for holding in self.root:
            hasher.update(holding.data_hash.encode("utf-8"))
        return hasher.hexdigest()
