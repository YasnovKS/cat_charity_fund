from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        None
    ]
):

    async def get_donations_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


crud = CRUDDonation(Donation)
