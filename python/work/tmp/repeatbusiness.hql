select
    n.store_country, 
    n.store_no, 
    n.store_name, 
    concat(2020, tc.fin_month) as fin_month, 
    concat(2020, 'W', tc.fin_week) as fin_week, 
    case 
        when tc.trans_channel = 'MAINLINE Direct' 
            then 'MAINLINE' 
        when tc.store_type = 'BURBERRY.COM' 
                or tc.trans_channel in ('MAINLINE Device', 'OUTLET Device') 
            then 'BURBERRY.COM' 
        else '' 
    end store_type,
    tc.cust_country_code, 
    tc.cust_country, 
    case 
        when nr.new_repeat = 'NB' 
            then 'New' 
        when nr.new_repeat = 'RB' 
            then 'Repeat' 
        else 'Unknown' 
    end repeat_business_flag,
    sum(case 
            when tc.fin_year = 2020
                then tc.revenue_extax_central_constant 
            else 0 
        end) as sales_ty, 
    sum(case 
            when tc.fin_year = 2019 
                then tc.revenue_extax_central_constant 
            else 0 
        end) as sales_ly,
    sum(case 
            when tc.fin_year = 2020
                then tc.trans_count 
            else 0 
        end) as trans_ty, 
    sum(case 
            when tc.fin_year = 2019 
                then tc.trans_count 
            else 0 
        end) as trans_ly,    
    sum(case 
            when tc.fin_year = 2020
                then tc.quantity 
            else 0 
        end) as units_ty, 
    sum(case 
            when tc.fin_year = 2019 
                then tc.quantity 
            else 0 
        end) as units_ly,
    tc.comp_2019, 
    sif.inc_status
from commercial.transaction_customer as tc
    inner join azaparozhtsa.n on concat(tc.fin_year, "W", tc.fin_week, tc.store_no) = concat(n.fin_week, n.store_no)
    inner join azaparozhtsa.sif on concat(tc.fin_year, "W", tc.fin_week ,tc.store_no) = sif.year_week_store
    left join commercial.transaction_new_repeat as nr on tc.trans_id = nr.trans_id
where tc.record_type = 'HEADER'
    and tc.fin_year in (2020, 2019)
    and n.store_region in ('EMEIA')
    and tc.trans_channel in ('MAINLINE Direct')
    and tc.fin_week <= '5'
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17

union all

select
    n.store_country, 
    n.store_no, 
    n.store_name, 
    concat(2019, tc.fin_month) as fin_month, 
    concat(2019, 'W', tc.fin_week) as fin_week, 
    case 
        when tc.trans_channel = 'MAINLINE Direct' 
            then 'MAINLINE' 
        when tc.store_type = 'BURBERRY.COM' or tc.trans_channel in ('MAINLINE Device', 'OUTLET Device') 
            then 'BURBERRY.COM' 
        else '' 
    end store_type,
    tc.cust_country_code, 
    tc.cust_country, 
    case 
        when nr.new_repeat = 'NB' 
            then 'New' 
        when nr.new_repeat = 'RB' 
            then 'Repeat' 
        else 'Unknown' 
    end repeat_business_flag,
    sum(case 
            when tc.fin_year = 2019
                then tc.revenue_extax_central_constant 
            else 0 
        end) as sales_ty, 
    sum(case 
            when tc.fin_year = 2018
                then tc.revenue_extax_central_constant 
            else 0 
        end) as sales_ly,
    sum(case 
            when tc.fin_year = 2019
                then tc.trans_count 
            else 0 
        end) as trans_ty, 
    sum(case 
            when tc.fin_year = 2018
                then tc.trans_count 
            else 0 
        end) as trans_ly,    
    sum(case 
            when tc.fin_year = 2019
                then tc.quantity 
            else 0 
        end) as units_ty, 
    sum(case 
            when tc.fin_year = 2018
                then tc.quantity 
            else 0 
        end) as units_ly,
    tc.comp_2019, 
    sif.inc_status
from commercial.transaction_customer as tc
    inner join azaparozhtsa.n on concat(tc.fin_year, "W", tc.fin_week, tc.store_no) = concat(n.fin_week,n.store_no)
    inner join azaparozhtsa.sif on concat(tc.fin_year, "W", tc.fin_week, tc.store_no) = sif.year_week_store
    left join commercial.transaction_new_repeat as nr on tc.trans_id = nr.trans_id
where tc.record_type = 'HEADER'
    and tc.fin_year in (2019, 2018)
    and n.store_region in ('EMEIA')
    and tc.trans_channel in ('MAINLINE Direct')
    and tc.fin_week <= '5'
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17