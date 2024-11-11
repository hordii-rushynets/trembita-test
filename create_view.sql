CREATE VIEW tsnap_full_view AS
SELECT 
    t.id AS tsnap_id,
    "asc".id AS asc_org_id,
    "asc".idf AS asc_org_idf,
    "asc".name AS asc_org_name,
    gen.asc_name AS asc_name,
    gen.asc_idf AS asc_idf,
    gen.asc_type AS asc_type,
    gen.created_by AS created_by,
    gen.is_active AS is_active,
    gen.date_created AS date_created,
    addr.address_full AS address_full,
    addr.postal_code AS postal_code,
    addr.lat AS latitude,
    addr.lon AS longitude,
    loc.name AS locality_name,
    loc.codifier AS locality_codifier,
    act.num_total_empl AS total_employees,
    act.manager_name AS manager_name,
    act.has_online_inform AS has_online_information,
    info.has_person_org_register AS has_person_org_register,
    info.has_land_cadastre AS has_land_cadastre,
    info.has_website_access AS has_website_access,
    admin.num_total_services AS total_services,
    admin.num_e_services AS e_services,
    admin.is_all_asc_services_via_center AS all_services_via_center,
    resp.name AS responsible_person_name,
    resp.phone AS responsible_person_phone,
    resp.email AS responsible_person_email
FROM 
    tsnap t
JOIN "asc_org" "asc" ON t.asc_org_id = "asc".id
JOIN general_data gen ON t.general_data_id = gen.id
JOIN address addr ON "asc".address_id = addr.id
JOIN locality loc ON addr.locality_id = loc.id
JOIN activity_data act ON t.activity_data_id = act.id
JOIN info_support_data info ON t.info_support_data_id = info.id
JOIN admin_service_data admin ON t.admin_service_data_id = admin.id
JOIN resp_person_data resp ON t.resp_person_data_id = resp.id;
