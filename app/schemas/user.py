import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic import validator


_PHONE_PATTERN = r'^' \
                 r'(\+|00)' \
                 r'(1|7|20|27|30|31|32|33|34|36|39|40|41|43|44|45|46|47' \
                 r'|48|49|51|52|53|54|55|56|57|58|60|61|62|63|64|65|66' \
                 r'|76|77|81|82|84|86|90|91|92|93|94|95|98|211|212|213' \
                 r'|216|218|220|221|222|223|224|225|226|227|228|229|230' \
                 r'|231|232|233|234|235|236|237|238|239|240|241|242|243' \
                 r'|244|245|246|248|249|250|251|252|253|254|255|256|257' \
                 r'|258|260|261|262|263|264|265|266|267|268|269|291|297' \
                 r'|298|299|350|351|352|353|354|355|356|357|358|359|370' \
                 r'|371|372|373|374|375|376|377|378|379|380|381|382|383' \
                 r'|385|386|387|389|420|421|423|500|501|502|503|504|505' \
                 r'|506|507|508|509|590|591|592|593|594|595|596|597|598' \
                 r'|670|672|673|674|675|676|677|678|679|680|681|682|683' \
                 r'|685|686|687|688|689|690|691|692|850|852|853|855|856' \
                 r'|880|886|960|961|962|963|964|965|966|967|968|970|971' \
                 r'|972|973|974|975|976|977|992|993|994|995|996|998|1242' \
                 r'|1246|1264|1268|1284|1340|1345|1441|1473|1649|1664|1670' \
                 r'|1671|1684|1721|1758|1767|1784|1787|1809|1829|1849|1868' \
                 r'|1869|1876|1939|4779|5999|3906698)' \
                 r'[0-9]{4,20}' \
                 r'$'
_PHONE_RE = re.compile(_PHONE_PATTERN, re.I)


class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)

    @validator('phone')
    def phone_validation(cls, v: str):
        v = v.strip()

        if v and not _PHONE_RE.search(v):
            raise ValueError('Invalid phone number')

        return v


class UserIn(UserBase):
    password: str = Field(...)


class UserData(UserBase):
    password_hash: str = Field(...)
    disabled: bool = Field(False)
    confirmed: bool = Field(False)

    class Config:
        orm_mode = True


class User(UserData):
    id: int = Field(...)
