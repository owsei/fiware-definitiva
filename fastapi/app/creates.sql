CREATE OR REPLACE VIEW vista_union_uu AS
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_baja' AS origen FROM cata_pol_uu_baja
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_cuarta' FROM cata_pol_uu_cuarta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decima' FROM cata_pol_uu_decima
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimocuarta' FROM cata_pol_uu_decimocuarta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimonovena' FROM cata_pol_uu_decimonovena
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimooctava' FROM cata_pol_uu_decimooctava
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimoprimera' FROM cata_pol_uu_decimoprimera
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimoquinta' FROM cata_pol_uu_decimoquinta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimosegunda' FROM cata_pol_uu_decimosegunda
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimoseptima' FROM cata_pol_uu_decimoseptima
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimosexta' FROM cata_pol_uu_decimosexta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_decimotercera' FROM cata_pol_uu_decimotercera
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_entreplanta' FROM cata_pol_uu_entreplanta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_novena' FROM cata_pol_uu_novena
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_octava' FROM cata_pol_uu_octava
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_primera' FROM cata_pol_uu_primera
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_quinta' FROM cata_pol_uu_quinta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_segunda' FROM cata_pol_uu_segunda
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_semisotano' FROM cata_pol_uu_semisotano
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_septima' FROM cata_pol_uu_septima
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sexta' FROM cata_pol_uu_sexta
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotano' FROM cata_pol_uu_sotano
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanocuarto' FROM cata_pol_uu_sotanocuarto
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanoprimero' FROM cata_pol_uu_sotanoprimero
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanoquinto' FROM cata_pol_uu_sotanoquinto
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanosegundo' FROM cata_pol_uu_sotanosegundo
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanosexto' FROM cata_pol_uu_sotanosexto
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_sotanotercero' FROM cata_pol_uu_sotanotercero
UNION ALL
SELECT ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,  'cata_pol_uu_tercera' FROM cata_pol_uu_tercera;




select (planta_num * 3) as altura,planta_num,planta,* from 
(select  ogc_fid, geom, feature, municipio, poligono, parcela, subarea, uu, calle, num_portal, letra, planta, escalera, puerta, 
		super_graf, super_priv, super_cerr, super_abie, super_comu, cod_destin, uso, mslink, url, barrio, codbarrio, distrito, seccion, codpostal,
		
		case 
			when vuu.planta = 'Sótano-6' then -6
			when vuu.planta = 'Sótano-5' then -5
			when vuu.planta = 'Sótano-4' then -4
			when vuu.planta = 'Sótano-3' then -3
			when vuu.planta = 'Sótano-2' then -2
			when vuu.planta = 'Sótano-1' then -1
			when vuu.planta = 'Bajo' then 0
			when vuu.planta = 'Entresuelo' then 1
			when vuu.planta = 'Primero' then 2
			when vuu.planta = 'Segundo' then 3
			when vuu.planta = 'Tercero' then 4
			when vuu.planta = 'Cuarto' then 5
			when vuu.planta = 'Quinto' then 6
			when vuu.planta = 'Sexto' then 7
			when vuu.planta = 'Séptimo' then 8
			when vuu.planta = 'Octavo' then 9
			when vuu.planta = 'Noveno' then 10
			when vuu.planta = 'Décimo' then 11
			when vuu.planta = 'Undécimo' then 12
			when vuu.planta = 'Duodécimo' then 13
			when vuu.planta = 'Decimotercero' then 14
			when vuu.planta = 'Decimocuarto' then 15
			when vuu.planta = 'Decimoquinto' then 16
			when vuu.planta = 'Decimosexto' then 17
			when vuu.planta = 'Decimoséptimo' then 18
			when vuu.planta = 'Decimoctavo' then 19
			when vuu.planta = 'Decimoctavo' then 20
			when vuu.planta = 'Decimoctavo' then 21
			when vuu.planta = 'Decimoctavo' then 22
			when vuu.planta = 'Decimoctavo' then 23
			when vuu.planta = 'Decimonoveno' then 24
	end as planta_num
from vista_union_uu vuu ) as c
where c.municipio =201 and c.poligono =1 and c.parcela = 1
 and c.planta_num is not null
 order by planta_num