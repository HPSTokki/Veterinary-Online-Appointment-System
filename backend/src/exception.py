from fastapi import HTTPException, status

class DomainException(Exception):
    def __init__(self, status_code: int, message: str, header: dict | None = None) -> None:
        self.message = message
        self.status_code = status_code
        self.header = header
    
class LoginInvalidCredentials(DomainException):
    def __init__(self, header: dict | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message="Invalid Login Credentials",
            header=header, 
        )
        
class DuplicateAccountCredentials(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            message="Account is already registered"
        )

class DuplicateAccountProfile(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            message="Profile associated with User Account already exists",
        )

class ClientProfileNotExist(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            message="Client Profile Not Found"
        )
        
class PetNotFound(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            message="Pet Not Found", 
        )
        
class AppointmentNotFound(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            message="Appointment Not Found"
        )

class ClinicIsClosed(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            message="Clinic is closed", 
        )

class SlotUnavailable(DomainException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Slot is Taken"
        )