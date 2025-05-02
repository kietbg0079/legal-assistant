from datetime import datetime, date
from typing import Literal
import pydantic
from pydantic import field_serializer
from dataclasses import field

@pydantic.dataclasses.dataclass(frozen=True)
class UserInfoSchema:
    """
    Represents user information with Pydantic validation,
    leveraging the dataclass structure.
    """
    first_name: str
    last_name: str
    birth: date

    # Using Literal for stricter gender validation (optional but recommended)
    # If you prefer any string, use: gender: str
    gender: Literal['Male', 'Female', 'Other']

    nationality: str = "Vietnamese"

    # Example of a computed property using dataclass features
    age: int = field(init=False, repr=True) # repr=True ensures it shows in default repr
    full_name: str = field(init=False, repr=True)

    def __post_init__(self):
        today = date.today()
        birth_date = self.birth
        years_difference = today.year - birth_date.year
        calculated_age = years_difference - ((today.month, today.day) < (birth_date.month, birth_date.day))

        calculated_full_name = f"{self.last_name} {self.first_name}".strip()

        object.__setattr__(self, 'birth', self.birth.strftime('%Y-%m-%d'))
        object.__setattr__(self, 'age', calculated_age)
        object.__setattr__(self, 'full_name', calculated_full_name)