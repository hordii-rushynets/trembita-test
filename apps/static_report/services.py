from apps.static_report.dao_services import SRDiiaApiDaoService, ODAReportDaoService, TsNAPReportDaoService


class TsNAPStaticReportService:
    """Service to manage ODA and TsNAP data."""
    oda_report_dao_service = ODAReportDaoService()
    tsnap_report_dao_service = TsNAPReportDaoService()
    sr_dia_api_dao_service = SRDiiaApiDaoService()

    def create_or_update(self, year: int, quarter: int):
        oda_reports = self.sr_dia_api_dao_service.get_oda_reports(year, quarter)

        for report in oda_reports:
            self.oda_report_dao_service.update_or_create(report)

            self.create_or_update_tsnaps(report['id'])

    def create_or_update_tsnaps(self, report_id):
        tsnaps_in_region = self.sr_dia_api_dao_service.get_tsnaps_in_region(report_id)

        for tsnap in tsnaps_in_region:
            tsnap_detail = self.sr_dia_api_dao_service.get_tsnap_details(tsnap['id'])

            if tsnap_detail:
                self.tsnap_report_dao_service.update_or_create(tsnap_detail[0])
