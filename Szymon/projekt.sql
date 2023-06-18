


select * from games_for_sale;


drop table competition_results;
drop table competition;
drop table games_for_sale;
drop table games_to_rent;
drop table staff;
drop table customers;
drop table sale;
drop table rental;

-------------------------------------------------


select staff_id, count(*)
from staff
left join sale
  on staff.staff_id = sale.staff_id
group by staff_id;

left join rental
  on staff.staff_id = rental.staff_id;



