WITH raw_base AS (
    SELECT
      src.fiscal_year,
      src.fiscal_week,
      src.web_product,
      src.page,
      src.device,
      src.burberry_region,
      src.hostname,
      src.channel,
      src.transacted,
      src.logged_in,
      src.new_visit,
      src.guest_reg_checkout,
      src.cis_hd_checkout,

      src.true_visid,
      src.isentrance,
      src.isexit,
      src.pageviews_tot,
      src.engurl,
      src.eventcategory,
      src.eventlabel,
      src.eventaction,
      src.type,
      src.pagetype
    FROM digital_analytics.web_product_unaggregated src
    LEFT SEMI JOIN control.web_product_hostname_inclusions include
    ON src.hostname = include.hostname
    WHERE ((fiscal_year='2021' AND fiscal_week='06') 
       OR (fiscal_year='2021' AND fiscal_week='05'))
),
base AS (
    SELECT
      fiscal_year,
      fiscal_week,
      web_product,
      page,
      device,
      burberry_region,
      hostname,
      channel,
      transacted,
      logged_in,
      new_visit,
      guest_reg_checkout,
      cis_hd_checkout,
      
      true_visid,
      isentrance,
      isexit,
      pageviews_tot,
      engurl,
      eventcategory,
      eventlabel,
      eventaction,
      type,
      pagetype
    FROM raw_base
    -- without Sitewide and Parent page classes
    WHERE page IS NOT NULL
  UNION ALL
    SELECT
      fiscal_year,
      fiscal_week,
      'Sitewide' AS web_product,
      'Sitewide' AS page,
      device,
      burberry_region,
      hostname,
      channel,
      transacted,
      logged_in,
      new_visit,
      guest_reg_checkout,
      cis_hd_checkout,
      
      true_visid,
      isentrance,
      isexit,
      pageviews_tot,
      engurl,
      eventcategory,
      eventlabel,
      eventaction,
      type,
      pagetype
    FROM raw_base
  UNION ALL 
    SELECT
      fiscal_year,
      fiscal_week,
      web_product,
      web_product AS page,
      device,
      burberry_region,
      hostname,
      channel,
      transacted,
      logged_in,
      new_visit,
      guest_reg_checkout,
      cis_hd_checkout,
      
      true_visid,
      isentrance,
      isexit,
      pageviews_tot,
      engurl,
      eventcategory,
      eventlabel,
      eventaction,
      type,
      pagetype
    FROM raw_base
    WHERE web_product IN ('HP_LP', 'Bag_Checkout')
),
traffic AS (
    SELECT
      fiscal_year, fiscal_week, web_product, page, device, burberry_region, hostname, channel, transacted, logged_in, new_visit, guest_reg_checkout, cis_hd_checkout,
      count(DISTINCT true_visid) AS traffic,
      count(DISTINCT if(transacted = 'YES', true_visid, NULL)) AS transacting_traffic,
      count(DISTINCT if(pageviews_tot = 1, true_visid, NULL)) AS bounce_traffic,
      count(DISTINCT if(isentrance = true, true_visid, NULL)) AS entrance_traffic,
      count(DISTINCT if(isexit = true, true_visid, NULL)) AS exit_traffic,
      CASE WHEN page IN ('HP_LP', 'PLP', 'PDP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN sum(if(type='PAGE', 1, 0))
        ELSE NULL
      END AS specified_page_views,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory IN ('HP_navigation', 'Menu_navigation', 'L1_Menu_navigation') or (eventcategory='Navigation method' and eventaction='Navigation menu click'), true_visid, NULL))
        ELSE NULL
      END AS nav_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' or (eventcategory='Navigation method' and eventaction='Tap' and eventlabel not in ('right','left')), true_visid, NULL))
        ELSE NULL
      END AS asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B1$|B1[^\\d]' or (eventcategory='Navigation method' and eventaction='Tap' and eventlabel not in ('right','left')), true_visid, NULL))
        ELSE NULL
        END AS b1_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B2$|B2[^\\d]', true_visid, NULL))
        ELSE NULL
      END AS b2_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B3$|B3[^\\d]', true_visid, NULL))
        ELSE NULL
      END AS b3_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B4$|B4[^\\d]', true_visid, NULL))
        ELSE NULL
      END AS b4_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B5$|B5[^\\d]', true_visid, NULL))
        ELSE NULL
      END AS b5_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Internal ads' and eventlabel regexp 'B([5-9]|\\d{2,})', true_visid, NULL))
        ELSE NULL
      END AS other_asset_interaction_traffic,
      CASE WHEN page IN ('HP_LP', 'Homepage', 'Womens_LP', 'Mens_LP', 'Childrens_LP')
        THEN count(DISTINCT if(eventcategory='Bottom_navigation' or (eventcategory='Navigation method' and eventaction='Category page menu click'), true_visid, NULL))
        ELSE NULL
      END AS footer_interaction_traffic,
      CASE WHEN page IN ('PLP')
        THEN count(DISTINCT if(eventcategory='Faceted Search' or (eventcategory='Search Behaviour' and eventaction like '%Search filter:%'), true_visid, NULL))
        ELSE NULL
      END AS filter_traffic,
      CASE WHEN page IN ('Sitewide', 'PLP')
        THEN count(DISTINCT if(pagetype REGEXP 'Search' or engurl like '%search%', true_visid, NULL))
        ELSE NULL
      END AS search_traffic,
      CASE WHEN page IN ('PLP')
        THEN count(DISTINCT if((eventcategory='Listing page' and eventaction REGEXP 'Clicked product|Clicked availability link') or (eventcategory='Ecommerce' and eventaction='Select product'), true_visid, NULL))
        ELSE NULL
      END AS pdp_ct_traffic,
      CASE WHEN page IN ('PLP')
        THEN count(DISTINCT if(eventcategory='Add to favourite behaviour', true_visid, NULL))
        ELSE NULL
      END AS fav_traffic,
      CASE WHEN page IN ('Sitewide', 'PDP')
        THEN count(DISTINCT if(eventcategory REGEXP 'Product details|Ecommerce' and eventaction='Add to bag', true_visid, NULL))
        ELSE NULL
      END AS a2b_traffic,
      CASE WHEN page IN ('Sitewide', 'PDP')
        THEN count(DISTINCT if(eventcategory='Store stock look-up' and eventaction='PDP:Find in store', true_visid, NULL))
        ELSE NULL
      END AS sslu_traffic,
      CASE WHEN page IN ('PDP')
        THEN count(DISTINCT if(eventcategory='Complete the Look' and hostname!='cn.burberry.com', true_visid, NULL))
        ELSE NULL
      END AS ctl_traffic,
      CASE WHEN page IN ('PDP')
        THEN count(DISTINCT if(eventcategory='Product details' and eventaction='Recommended product', true_visid, NULL))
        ELSE NULL
      END AS rec_traffic,
      CASE WHEN page IN ('PDP')
        THEN count(DISTINCT if(eventcategory='Size Help' and eventaction='Size_Guide_Started' and hostname!='cn.burberry.com', true_visid, NULL))
        ELSE NULL
      END AS size_guide_traffic,
      CASE WHEN page IN ('PDP')
        THEN count(DISTINCT if((eventcategory='Size Help' and eventaction='Size_Guide_Started_FIT' and hostname!='cn.burberry.com') or (eventcategory='Product details' and eventaction='Size_Fit_Analytics' and hostname='cn.burberry.com'), true_visid, NULL))
        ELSE NULL
      END AS fit_analytics_traffic
    FROM base
    GROUP BY fiscal_year, fiscal_week, web_product, page, device, burberry_region, hostname, channel, transacted, logged_i
    n, new_visit, guest_reg_checkout, cis_hd_checkout
),
traffic_by_page AS (
    SELECT
         fiscal_year
        ,fiscal_week
        ,device            
        ,hostname          
        ,channel           
        ,transacted        
        ,logged_in         
        ,new_visit         
        ,guest_reg_checkout
        ,cis_hd_checkout
        ,max(if(web_product = 'HP_LP'        AND page = 'HP_LP'       , traffic, NULL)) as hp_lp_t
        ,max(if(web_product = 'HP_LP'        AND page = 'Homepage'    , traffic, NULL)) as hp_t
        ,max(if(web_product = 'HP_LP'        AND page = 'Womens_LP'   , traffic, NULL)) as womens_lp_t
        ,max(if(web_product = 'HP_LP'        AND page = 'Mens_LP'     , traffic, NULL)) as mens_lp_t
        ,max(if(web_product = 'HP_LP'        AND page = 'Childrens_LP', traffic, NULL)) as childrens_lp_t
        ,max(if(web_product = 'PDP'          AND page = 'PDP'         , traffic, NULL)) as pdp_t
        ,max(if(web_product = 'PLP'          AND page = 'PLP'         , traffic, NULL)) as plp_t
        ,max(if(web_product = 'Bag_Checkout' AND page = 'Bag_Checkout', traffic, NULL)) as bag_checkout_t
    FROM traffic t
    GROUP BY fiscal_year
            ,fiscal_week
            ,device            
            ,hostname          
            ,channel           
            ,transacted        
            ,logged_in         
            ,new_visit         
            ,guest_reg_checkout
            ,cis_hd_checkout
)

SELECT 
  t.web_product, 
  t.page, 
  t.device,
  t.burberry_region,
  t.hostname, 
  t.channel, 
  t.transacted, 
  t.logged_in, 
  t.new_visit, 
  if(t.guest_reg_checkout = '', NULL, t.guest_reg_checkout), 
  if(t.cis_hd_checkout = 'OTHER', NULL, t.cis_hd_checkout),
  t.traffic,
  t.transacting_traffic,
  t.bounce_traffic,
  t.entrance_traffic,
  t.exit_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.hp_lp_t       , 0), NULL) AS hp_lp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.hp_t          , 0), NULL) AS hp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.womens_lp_t   , 0), NULL) AS womens_lp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.mens_lp_t     , 0), NULL) AS mens_lp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.childrens_lp_t, 0), NULL) AS childrens_lp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.plp_t         , 0), NULL) AS plp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.pdp_t         , 0), NULL) AS pdp_traffic,
  if(t.web_product = 'Sitewide', nvl(tbp.bag_checkout_t, 0), NULL) AS bag_checkout_traffic,
  t.specified_page_views,
  t.nav_interaction_traffic,
  t.asset_interaction_traffic,
  t.b1_asset_interaction_traffic,
  t.b2_asset_interaction_traffic,
  t.b3_asset_interaction_traffic,
  t.b4_asset_interaction_traffic,
  t.b5_asset_interaction_traffic,
  t.other_asset_interaction_traffic,
  t.footer_interaction_traffic,
  t.filter_traffic,
  t.search_traffic,
  t.pdp_ct_traffic,
  t.fav_traffic,
  t.a2b_traffic,
  t.sslu_traffic,
  t.ctl_traffic,
  t.rec_traffic,
  t.size_guide_traffic,
  t.fit_analytics_traffic,
  t.fiscal_year, 
  t.fiscal_week
FROM traffic t
LEFT JOIN traffic_by_page tbp
ON  t.web_product = 'Sitewide'
AND t.page = 'Sitewide'
AND t.fiscal_year        = tbp.fiscal_year
AND t.fiscal_week        = tbp.fiscal_week
AND t.device             = tbp.device              
AND t.hostname           = tbp.hostname          
AND t.channel            = tbp.channel           
AND t.transacted         = tbp.transacted        
AND t.logged_in          = tbp.logged_in         
AND t.new_visit          = tbp.new_visit         
AND t.guest_reg_checkout = tbp.guest_reg_checkout
AND t.cis_hd_checkout    = tbp.cis_hd_checkout




-- INSERT OVERWRITE TABLE digital_analytics.web_product_bigquery PARTITION (fiscal_year, fiscal_week)
