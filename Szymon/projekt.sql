


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




-- Zależność sprzedaży od ratingu gry

select s.game_id, g.name, g.avg_rating, count(*) as sale_count
from sale s
join games_for_sale g
  on s.game_id = g.game_id
where s.date > date_add(sysdate(), interval -12 month)
group by s.game_id, g.name, g.avg_rating
order by sale_count desc;


select max(avg_rating) from games_for_sale;