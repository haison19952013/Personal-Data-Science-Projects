-- SEPARATE bhd, filmplus and film goi
WITH
	bhd_key AS (select lbm.CustomerID, lbm.date
				from log_bhd_movieid lbm 
				where lbm.MovieID in (SELECT id FROM mv_propertiesshowvn_narrow as mpn WHERE mpn.isDRM = 1)
				),
	fp_key AS (select lfpm.CustomerID, date_format(lfpm.date,'%Y-%m-%d') as date
				from log_fimplus_movieid lfpm 
				where lfpm.MovieID in (SELECT id FROM mv_propertiesshowvn_narrow as mpn WHERE mpn.isDRM = 1)
				)
select *
from
	(
	select bhd_key.date, count(distinct bhd_key.CustomerID) as total_key, 'bhd' as service
	from bhd_key
	group by bhd_key.date
	union
	select fp_key.date, count(distinct fp_key.CustomerID) as total_key, 'film_plus' as service
	from fp_key
	group by fp_key.date
	union
	select lgdl.date, count(distinct lgdl.CustomerID) as total_key, 'film_goi' as service
	from log_get_drm_list lgdl
	join customers c on c.customerid = lgdl.CustomerID -- and c.mac = lgdl.Mac 
	join customerservice cs on cs.CustomerID = c.customerid
	group by lgdl.date) as temp_tab
order by date desc;

-- Combine all
WITH
	bhd_key AS (select lbm.CustomerID, lbm.date
				from log_bhd_movieid lbm 
				where lbm.MovieID in (SELECT id FROM mv_propertiesshowvn_narrow as mpn WHERE mpn.isDRM = 1)
				),
	fp_key AS (select lfpm.CustomerID, date_format(lfpm.date,'%Y-%m-%d') as date
				from log_fimplus_movieid lfpm 
				where lfpm.MovieID in (SELECT id FROM mv_propertiesshowvn_narrow as mpn WHERE mpn.isDRM = 1)
				)
select date, count(distinct CustomerID) as total_key
from
	(
	select bhd_key.date, bhd_key.CustomerID, 'bhd' as service
	from bhd_key
	union
	select fp_key.date, fp_key.CustomerID, 'film_plus' as service
	from fp_key
	union
	select lgdl.date, lgdl.CustomerID, 'film_goi' as service
	from log_get_drm_list lgdl
	join customers c on c.customerid = lgdl.CustomerID -- and c.mac = lgdl.Mac 
	join customerservice cs on cs.CustomerID = c.customerid) as temp_tab
group by date
order by date desc;