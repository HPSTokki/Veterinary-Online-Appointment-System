from typing import cast

from sqlmodel import Session, col, select

from src.exception import ClientProfileNotExist, DomainException, DuplicateAccountProfile
from src.models.appointment_models import Client, UserAccount
from src.dtos.user_dtos import InsertClient, ReadClient, UpdateClient

class ClientService():
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def create_client(self, client_data: InsertClient, user_id: int) -> ReadClient:
        existing = self.session.exec(select(Client).where(col(Client.user_id) == user_id)).first()
        if existing:
            raise DuplicateAccountProfile()
        client = Client(**client_data.model_dump(), user_id=user_id)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return self._to_read(client)
    
    def get_client(self, user_id: int) -> ReadClient:
        client = self.session.exec(
            select(Client).where(col(Client.user_id) == user_id)
        ).first()
        if not client:
            raise ClientProfileNotExist()
        return self._to_read(cast(Client, client))
    
    def update_client(self, client_data: UpdateClient, user_id: int) -> ReadClient:
        client = self.session.exec(
            select(Client).where(col(Client.user_id) == user_id)
        ).first()
        if not client:
            raise ClientProfileNotExist()
        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(client, key, value)
        self.session.commit()
        self.session.refresh(client)
        return self._to_read(cast(Client, client))
    
    def _to_read(self, client: Client) -> ReadClient:
        user = self.session.get(UserAccount, client.user_id)
        result = ReadClient.model_validate(client, from_attributes=True)
        result.email = user.email if user else None
        return result