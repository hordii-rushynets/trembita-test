import logging
from abc import abstractmethod
from typing import List

import requests
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session as SessionType

from apps.static_report.models import (RSA, ActivityData, Address,
                                       AdminServiceData, ASCOrg, GeneralData,
                                       InfoSupportData, Locality)
from apps.static_report.models import ODAReport as ODAReportModel
from apps.static_report.models import RespPersonData, TsNAP
from apps.static_report.types import ODAReport, ODAReportRSA, TSNAPDetails, TSNAPRegion
from database import db
from settings import DIIA_API_URL

logger = logging.getLogger(__name__)

class SRDiiaApiDaoService:
    """A DAO service for receiving data from the DIIA API."""
    base_url: str = f'{DIIA_API_URL}/v1/static_reports'

    def get_oda_reports(self, year: int, quarter: int) -> List[ODAReport]:
        """
        Fetches the list of ODA reports for a specified year and quarter.
        
        :param year: The year for which the reports are requested.
        :param quarter: The quarter (1 to 4) for which the reports are requested.

        :return List[ODAReport]: A list of ODA reports for the specified year and quarter.
        """
        logger.info(f'Get ODA Reports: year - {year}, quarter - {quarter}.')
        return self.make_get_request(f'list/{year}/{quarter}/?format=json').get('results')

    def get_tsnaps_in_region(self, report_id: int, collected_results: List[TSNAPRegion] = None, page: int=1) -> List[TSNAPRegion]:
        """
        Fetches the list of TsNAPs of the region:.
        
        :param report_id: The ID of the ODA report to retrieve TSNAP region data.
        :param collected_results: A list of TSNAPRegion objects to accumulate results across pages. Default is None, which initializes an empty list.
        :param page: The current page number for paginated requests. Default is 1.

        :return List[TSNAPRegion]: A list of TSNAP regions associated with the specified report ID.
        """
        logger.info(f'Get list of TSNAP region: report_id: {report_id}')

        if collected_results is None:
            collected_results = []

        entries = self.make_get_request(f'entries/{report_id}?page={page}')
        collected_results.extend(entries.get('results', []))

        next_url = entries.get('next')

        if next_url:
            query_params = self._get_query_params(next_url)
            return self.get_tsnaps_in_region(report_id, collected_results, query_params.get('page'))

        return collected_results

    def _get_query_params(self, url: str) -> dict:
        """
        Retrieve all query params from url.

        :param url: url to parse.

        :return dict: query params.
        """
        query_params = url.split('?')[1]
        return dict(param.split('=') for param in query_params.split('&') if '=' in param)


    def get_tsnap_details(self, report_entries_id: int) -> List[TSNAPDetails]:
        """
        Fetches detailed data for a specific TSNAP report entry.
        
        :param report_entries_id: The ID of the TSNAP report entry for which details are needed.

        :return List[TSNAPDetails]: Detailed data for the specified TSNAP report entry.
        """
        logger.info(f'Get list of TSNAP details: report_entries_id: {report_entries_id}.')
        return self.make_get_request(f'detail/{report_entries_id}').get('results')

    def make_get_request(self, url: str) -> list:
        """
        Makes an HTTP GET request to the specified URL and returns the results.
        
        :param url: The endpoint URL for the GET request.
        :return list: JSON response with the 'results' field, or an empty list on error.
        """
        try:
            response = requests.get(f'{self.base_url}/{url}')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else "No response"
            logger.error(f'Status code: {status_code}')
        except requests.exceptions.RequestException as req_err:
            logger.error(f'An error occurred: {req_err}')
        except ValueError as val_err:
            logger.error(f'JSON decode error: {val_err}')
        
        return []


class AbstractReportDaoService:
    """Base report DAO Service."""
    def __init__(self):
        self.session: SessionType = db.create_session()
        self.base_url: str = f'{DIIA_API_URL}/v1/static_reports'

    @abstractmethod
    def update_or_create(self, data: dict):
        """
        Abstract method that must be implemented by subclasses to either update an existing record 
        or create a new one based on the provided data.

        :param data: A dictionary containing the data to update or create a record with.
        """

    def update(self, obj, data: dict):
        """
        Updates an object's attributes with values from the provided dictionary.
        
        :param obj: The object to be updated.
        :param data: A dictionary containing key-value pairs where each key corresponds to an 
                         attribute name in `obj` and each value is the new value to set for that attribute.
        """
        for key, value in data.items():
            setattr(obj, key, value)

    def save(self, objs: list):
        """
        Adds a list of objects to the database session and commits the changes.

        :param objs: A list of objects to be added to the session and persisted in the database.
        """
        for obj in objs:
            self.session.add(obj)

        self.session.commit()


class ODAReportDaoService(AbstractReportDaoService):
    """DAO service for managing ODA data."""
    def update_or_create(self, data: ODAReport) -> ODAReportModel:
        """
        Updates an existing ODA report record in the database if it exists; otherwise, creates a new record.
        
        :param data: The updated or newly created ODA report model instance.

        :return oda_report: Instance of ODARepor model. 
        """
        report_data = {
            "id": data.get("id"),
            "year": data.get("year"),
            "quarter": data.get("quarter")
        }

        rsa_record = self._update_or_create_rsa_record(data.get("rsa"))
        
        self.session.flush()

        oda_report = self.session.query(ODAReportModel).filter_by(id=report_data["id"]).one_or_none()
        if oda_report:
            oda_report.year = report_data["year"]
            oda_report.quarter = report_data["quarter"]
            oda_report.rsa_info_id = rsa_record.id
        else:
            oda_report = ODAReportModel(**report_data)
            oda_report.rsa_info_id = rsa_record.id
    
        self.save([oda_report])
        return oda_report

    def _update_or_create_rsa_record(self, data: ODAReportRSA) -> RSA:
        """
        Updates an existing ODA report record in the database if it exists; otherwise, creates a new record.
        
        :param data: The updated or newly created ODA report model instance.

        :return rsa_record: Instance of RSA model.
        """
        try:
            rsa_record = self.session.query(RSA).filter_by(edrpou=data["edrpou"]).one()
            rsa_record.name = data["name"]
            rsa_record.address = data["address"]
        except NoResultFound:
            rsa_record = RSA(**data)
        
        self.session.add(rsa_record)
        return rsa_record


class TsNAPReportDaoService(AbstractReportDaoService):
    """DAO service for managing TsNAP data."""
    def update_or_create(self, data: TSNAPDetails):
        asc_org_data = data.get('asc_org')

        asc_org = self._update_or_create_asc_org(asc_org_data)

        tsnap = self.session.query(TsNAP).filter(TsNAP.asc_org_id == asc_org.id).first()
        general_data = self._update_or_create_general_data(asc_org.idf, data.get('general_data'))

        if not tsnap:
            self._create_tsnap(data, asc_org.id, general_data.id)
            activity_data = ActivityData(**data.get('activity_data'))
            info_support_data = InfoSupportData(**data.get('info_support_data'))
            admin_service_data = AdminServiceData(**data.get('admin_service_data'))
            resp_person_data = RespPersonData(**data.get('resp_person_data'))
            self.save([activity_data, info_support_data, admin_service_data, resp_person_data])

            tsnap = TsNAP(asc_org_id=asc_org.id, general_data_id=general_data.id, activity_data_id=activity_data.id,
                          info_support_data_id=info_support_data.id, admin_service_data_id=admin_service_data.id, resp_person_data_id=resp_person_data.id)
            
            self.save([tsnap])
        else:
            self.update(self.session.query(ActivityData).filter(ActivityData.id == tsnap.activity_data_id).first(), data.get('activity_data', {}))
            self.update(self.session.query(InfoSupportData).filter(InfoSupportData.id == tsnap.info_support_data_id).first(), data.get('info_support_data', {}))
            self.update(self.session.query(AdminServiceData).filter(AdminServiceData.id == tsnap.admin_service_data_id).first(), data.get('admin_service_data', {}))
            self.update(self.session.query(RespPersonData).filter(RespPersonData.id == tsnap.resp_person_data_id).first(), data.get('resp_person_data', {}))
    
    def _create_tsnap(self, data: TSNAPDetails, asc_org_id: int, general_data_id: int):
        """
        Create TsNAP instance in the database.

        :param data: TsNAP data.
        :param asc_org_id: instance of asc_org.
        :param general_data_id: instance of general_data_id.
        """
        activity_data = ActivityData(**data.get('activity_data'))
        info_support_data = InfoSupportData(**data.get('info_support_data'))
        admin_service_data = AdminServiceData(**data.get('admin_service_data'))
        resp_person_data = RespPersonData(**data.get('resp_person_data'))
        self.save([activity_data, info_support_data, admin_service_data, resp_person_data])

        tsnap = TsNAP(asc_org_id=asc_org_id, general_data_id=general_data_id, activity_data_id=activity_data.id,
                        info_support_data_id=info_support_data.id, admin_service_data_id=admin_service_data.id, resp_person_data_id=resp_person_data.id)
        
        self.save([tsnap])

    def _update_or_create_general_data(self, asc_ord_idf: str, data) -> GeneralData:
        general_data = self.session.query(GeneralData).filter(GeneralData.asc_idf == asc_ord_idf).first()
        if not general_data:
            general_data = GeneralData(**data)
        else:
            self.update(general_data, data)

        self.save([general_data])
        return general_data

    def _update_or_create_asc_org(self, data: dict) -> ASCOrg:
        asc_org = self.session.query(ASCOrg).filter(ASCOrg.idf == data['idf']).first()
        address_data = data.pop('address')

        if not asc_org:
            asc_org = ASCOrg(idf=data['idf'], name=data['name'])
        else:
            self.update(asc_org, data)

        if address_data:
            address = self._update_or_create_address(asc_org, address_data)
            asc_org.address_id = address.id

        self.save([asc_org])
        return asc_org

    def _update_or_create_address(self, asc_org: ASCOrg, data) -> Address:
        address = self.session.query(Address).filter(Address.id == asc_org.address_id).first()

        locality_data = data.pop('locality')

        if not address:
            address = Address(**data)
        else:
            self.update(address, data)

        if locality_data:
            locality = self._update_or_create_locality(address, locality_data)
            address.locality_id = locality.id

        self.save([address])
        return address
    
    def _update_or_create_locality(self, address: Address, data) -> Locality:
        locality = self.session.query(Locality).filter(Locality.id == address.locality_id).first()

        if not locality and data:
            locality = Locality(**data)
        else:
            self.update(locality, data)

        self.save([locality])
        return locality
