from typing import Optional, TypedDict


class ODAReportRSA(TypedDict):
    name: str
    edrpou: str
    address: str


class ODAReport(TypedDict):
    id: int
    year: int
    quarter: int
    rsa: ODAReportRSA


class Locality(TypedDict):
    codifier: str
    name: str


class Address(TypedDict):
    address_full: str
    locality: Locality
    postal_code: str
    lat: Optional[float]
    lon: Optional[float]


class AscOrg(TypedDict):
    idf: str
    name: str
    address: Address


class TSNAPRegion(TypedDict):
    id: int
    asc_org: AscOrg


class GeneralData(TypedDict):
    asc_name: str
    asc_idf: str
    asc_type: int
    created_by: str
    edrpou: str
    is_diia: bool
    is_active: bool
    is_inactive: bool
    created_by_type: int
    is_close_transform: bool
    date_creation_decision_made: str
    date_created: str
    date_closing_decision_made: Optional[str]
    date_closed: Optional[str]
    is_permanent_working_unit: bool
    is_structural_unit: bool
    index: str
    region: str
    district: str
    local_community: str
    city: Optional[str]
    locality: Optional[str]
    village: Optional[str]
    street: Optional[str]
    building_number: Optional[str]
    consult_phone: Optional[str]
    consult_email: Optional[str]
    num_mobile_center: Optional[int]
    has_bus_stop_near: bool
    has_free_parking: bool
    has_free_parking_inv: bool
    has_asc_info_in_city: bool
    num_days_per_week: int
    num_days_per_week_bef_20: int
    has_break: bool
    works_in_saturday: bool
    work_time_mon: Optional[str]
    total_sq: Optional[float]
    open_reception_sq: Optional[float]
    open_info_sq: Optional[float]
    open_waiting_sq: Optional[float]
    open_service_sq: Optional[float]
    num_waiting_seats: Optional[int]
    num_served_people: Optional[int]
    has_otg_contract: bool
    contract_number: Optional[str]
    has_resolution: bool
    resolution_number: Optional[str]
    website: Optional[str]


class ActivityData(TypedDict):
    num_total_empl: int
    manager_name: Optional[str]
    num_managers: int
    num_business_reg: int
    num_realty_reg: int
    num_residence_reg: int
    num_other_empl: int
    num_other_total_empl: int
    num_other_business_reg: int
    num_other_realty_reg: int
    num_other_cadastral_reg: int
    num_other_residence_reg: Optional[int]
    num_other_mia_empl: int
    num_other_soc_protec_empl: int
    num_other_other_empl: int
    has_admin_service_consalt: bool
    has_info_department: Optional[bool]
    has_phone_consalt: bool
    has_online_consalt: bool
    has_sms_inform: bool
    has_online_inform: bool
    has_phone_inform: bool
    has_chat_bot_inform: bool
    has_personal_inform: bool
    has_mail_inform: bool
    has_other_inform: bool
    has_automatic_queue_handle: bool
    has_prev_appointment_personal: bool
    has_prev_appointment_online: bool
    avg_waiting: int
    has_free_access_doc_templ: bool
    has_separated_reception_delivery: bool
    has_bank_payment: bool
    has_pos_terminal_payment: bool
    has_self_service_payment: Optional[bool]
    has_other_payment_system: bool
    has_photocopy: Optional[bool]
    has_lamination: Optional[bool]
    has_photograpy: Optional[bool]
    has_free_wifi: bool
    has_stationery_sale: Optional[bool]
    has_corner_self_service: bool
    manager_self_esteem: Optional[int]
    num_trained_empl: Optional[int]
    has_feedback_box: bool
    has_feedback_book: bool
    has_google_map_feedback: Optional[bool]
    has_chat_bot_feedback: bool
    other_feedback: Optional[str]
    num_feedback_total: int
    num_feedback_positive: int
    num_feedback_negative: int
    has_technical_room: bool
    has_ramp: bool
    has_stairs_with_handrails: bool
    has_equiped_technical_room: bool
    has_braille_font: bool
    has_deaf_adaptation: bool
    has_temp_place_strollers: bool


class InfoSupportData(TypedDict):
    has_person_org_register: bool
    has_real_estate_rights_register: bool
    has_demography_register: bool
    has_land_cadastre: bool
    other_registers: Optional[str]
    has_e_sevices: Optional[bool]
    e_services_name: Optional[str]
    has_edm_system: bool
    edm_system_name: Optional[str]
    edm_system_developer: Optional[str]
    has_website_access: bool
    has_phone_access: bool
    has_info_terminal_access: bool
    has_info_stand_access: bool


class AdminServiceData(TypedDict):
    num_total_services: int
    num_e_services: Optional[int]
    num_rsa_services: int
    num_dsa_services: int
    num_city_services: int
    num_asc_services: int
    num_special_services: int
    is_all_asc_services_via_center: Optional[bool]
    num_all_asc_e_services: Optional[int]
    num_from_this_year_start: int
    num_services_residence: int
    num_services_passport: int
    num_services_vehicle: Optional[int]
    num_acts_services: int
    num_dzk_services: int


class RespPersonData(TypedDict):
    name: str
    phone: str
    email: str
    ceo_contact_pip: str
    ceo_contact_phone: str
    ceo_contact_mail: str


class TSNAPDetails(TypedDict):
    id: int
    asc_org: AscOrg
    general_data: GeneralData
    activity_data: ActivityData
    info_support_data: InfoSupportData
    admin_service_data: AdminServiceData
    resp_person_data: RespPersonData
