from sqlalchemy import Column, Float, Integer, String, ForeignKey, Boolean, Date

from database import db
from sqlalchemy.orm import relationship


class RSA(db.Base):
    """Represents RSA (Regional State Administration) information in the 'rsa_info' table."""
    __tablename__ = 'rsa'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    edrpou = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)

    def __init__(self, **data):
        """Initializes an RSA object with the provided data."""
        for key, value in data.items(): setattr(self, key, value)


class ODAReport(db.Base):
    """Represents an ODA (Oblastna Derzhavna Administratsiya) report record in the 'oda_reports' table."""
    __tablename__ = 'oda_reports'
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)

    rsa_info_id = Column(Integer, ForeignKey('rsa.id'), nullable=False)

    def __init__(self, **data):
        """Initializes an ODAReport object with the provided data."""
        for key, value in data.items(): setattr(self, key, value)

    def __repr__(self):
        """Returns a string representation of the ODAReport instance."""
        return f"<ODAReport(id={self.id}, year={self.year}, quarter={self.quarter}, rsa_name={self.rsa_name})>"


class Locality(db.Base):
    """Represents locality information in the 'locality' table."""
    __tablename__ = 'locality'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    codifier = Column(String, nullable=True)

    def __init__(self, **data):
        """Initializes a Locality object."""
        for key, value in data.items():
            setattr(self, key, value)


class Address(db.Base):
    """Represents address information in the 'address' table."""
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True)
    address_full = Column(String, nullable=False)
    locality_id = Column(Integer, ForeignKey('locality.id'), nullable=True)
    postal_code = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    def __init__(self, **data):
        """Initializes a Address object."""
        for key, value in data.items():
            setattr(self, key, value)


class ASCOrg(db.Base):
    """Represents ASC organization information in the 'asc_org' table."""
    __tablename__ = 'asc_org'
    
    id = Column(Integer, primary_key=True)
    idf = Column(String, nullable=False, unique=True)  # Unique identifier
    name = Column(String, nullable=False)
    
    address_id = Column(Integer, ForeignKey('address.id'), nullable=True)

    def __init__(self, **data):
        """Initializes an ASCOrg object with the provided data."""
        for key, value in data.items():
            setattr(self, key, value)


class GeneralData(db.Base):
    """Represents general data related to ASC organization."""
    __tablename__ = 'general_data'

    id = Column(Integer, primary_key=True)
    asc_name = Column(String, nullable=False)
    asc_idf = Column(String, nullable=False)
    asc_type = Column(Integer, nullable=True)
    created_by = Column(String, nullable=True)
    edrpou = Column(String, nullable=True)
    is_diia = Column(Boolean, nullable=True)
    is_active = Column(Boolean, nullable=True)
    is_inactive = Column(Boolean, nullable=True)
    created_by_type = Column(Integer, nullable=True)
    is_close_transform = Column(Boolean, nullable=True)
    date_creation_decision_made = Column(Date, nullable=True)
    date_created = Column(Date, nullable=True)
    date_closing_decision_made = Column(Date, nullable=True)
    date_closed = Column(Date, nullable=True)
    is_permanent_working_unit = Column(Boolean, nullable=True)
    is_structural_unit = Column(Boolean, nullable=True)
    index = Column(String, nullable=True)
    region = Column(String, nullable=True)
    district = Column(String, nullable=True)
    local_community = Column(String, nullable=True)
    city = Column(String, nullable=True)
    locality = Column(String, nullable=True)
    village = Column(String, nullable=True)
    street = Column(String, nullable=True)
    building_number = Column(String, nullable=True)
    consult_phone = Column(String, nullable=True)
    consult_email = Column(String, nullable=True)
    num_mobile_center = Column(Integer, nullable=True)
    has_bus_stop_near = Column(Boolean, nullable=True)
    has_free_parking = Column(Boolean, nullable=True)
    has_free_parking_inv = Column(Boolean, nullable=True)
    has_asc_info_in_city = Column(Boolean, nullable=True)
    num_days_per_week = Column(Integer, nullable=True)
    num_days_per_week_bef_20 = Column(Integer, nullable=True)
    has_break = Column(Boolean, nullable=True)
    works_in_saturday = Column(Boolean, nullable=True)
    work_time_mon = Column(String, nullable=True)
    total_sq = Column(Integer, nullable=True)
    open_reception_sq = Column(Integer, nullable=True)
    open_info_sq = Column(Integer, nullable=True)
    open_waiting_sq = Column(Integer, nullable=True)
    open_service_sq = Column(Integer, nullable=True)
    num_waiting_seats = Column(Integer, nullable=True)
    num_served_people = Column(Integer, nullable=True)
    has_otg_contract = Column(Boolean, nullable=True)
    contract_number = Column(String, nullable=True)
    has_resolution = Column(Boolean, nullable=True)
    resolution_number = Column(String, nullable=True)
    website = Column(String, nullable=True)


class ActivityData(db.Base):
    """Represents activity data related to ASC organization."""
    __tablename__ = 'activity_data'

    id = Column(Integer, primary_key=True)
    num_total_empl = Column(Integer, nullable=True)
    manager_name = Column(String, nullable=True)
    num_managers = Column(Integer, nullable=True)
    has_admin_service_consalt = Column(Boolean, nullable=True)
    has_phone_consalt = Column(Boolean, nullable=True)
    has_online_consalt = Column(Boolean, nullable=True)
    has_sms_inform = Column(Boolean, nullable=True)
    has_online_inform = Column(Boolean, nullable=True)
    num_feedback_total = Column(Integer, nullable=True)
    other_feedback = Column(String, nullable=True)
    has_technical_room = Column(Boolean, nullable=True)

    def __init__(self, **data):
        """Initializes the TsNAPRegion with provided data."""
        for key, value in data.items(): setattr(self, key, value)


class InfoSupportData(db.Base):
    """Represents information support data for ASC organization."""
    __tablename__ = 'info_support_data'

    id = Column(Integer, primary_key=True)
    has_person_org_register = Column(Boolean, nullable=False, default=False)
    has_real_estate_rights_register = Column(Boolean, nullable=False, default=False)
    has_demography_register = Column(Boolean, nullable=False, default=False)
    has_land_cadastre = Column(Boolean, nullable=False, default=False)
    other_registers = Column(String, nullable=True)
    has_e_sevices = Column(Boolean, nullable=True)
    e_services_name = Column(String, nullable=True)
    has_edm_system = Column(Boolean, nullable=False, default=False)
    edm_system_name = Column(String, nullable=True)
    edm_system_developer = Column(String, nullable=True)
    has_website_access = Column(Boolean, nullable=False, default=True)
    has_phone_access = Column(Boolean, nullable=False, default=True)
    has_info_terminal_access = Column(Boolean, nullable=False, default=False)
    has_info_stand_access = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<InfoSupportData(id={self.id})>"


class AdminServiceData(db.Base):
    """Represents admin service data related to ASC organization."""
    __tablename__ = 'admin_service_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_total_services = Column(Integer, nullable=False)
    num_e_services = Column(Integer, nullable=True)
    num_rsa_services = Column(Integer, nullable=False, default=0)
    num_dsa_services = Column(Integer, nullable=False, default=0)
    num_city_services = Column(Integer, nullable=False, default=0)
    num_asc_services = Column(Integer, nullable=False, default=0)
    num_special_services = Column(Integer, nullable=False, default=0)
    is_all_asc_services_via_center = Column(Boolean, nullable=True)
    num_all_asc_e_services = Column(Integer, nullable=True)
    num_from_this_year_start = Column(Integer, nullable=False)
    num_services_residence = Column(Integer, nullable=False)
    num_services_passport = Column(Integer, nullable=False, default=0)
    num_services_vehicle = Column(Integer, nullable=True)
    num_acts_services = Column(Integer, nullable=False, default=0)
    num_dzk_services = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<AdminServiceData(id={self.id})>"

class RespPersonData(db.Base):
    """Represents responsible person data for ASC organization."""
    __tablename__ = 'resp_person_data'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ceo_contact_pip = Column(String, nullable=True)
    ceo_contact_phone = Column(String, nullable=True)
    ceo_contact_mail = Column(String, nullable=True)


class TsNAP(db.Base):
    """Represents a TsNAP region record in the 'tsnap' table."""
    __tablename__ = 'tsnap'
    
    id = Column(Integer, primary_key=True)
    asc_org_id = Column(Integer, ForeignKey('asc_org.id'), nullable=False)
    general_data_id = Column(Integer, ForeignKey('general_data.id'), nullable=False)
    activity_data_id = Column(Integer, ForeignKey('activity_data.id'), nullable=False)
    info_support_data_id = Column(Integer, ForeignKey('info_support_data.id'), nullable=False)
    admin_service_data_id = Column(Integer, ForeignKey('admin_service_data.id'), nullable=False)
    resp_person_data_id = Column(Integer, ForeignKey('resp_person_data.id'), nullable=False)

    def __init__(self, **data):
        """Initializes the TsNAPRegion with provided data."""
        for key, value in data.items(): setattr(self, key, value)
