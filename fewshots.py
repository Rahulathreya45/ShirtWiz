fewshots = [

    {'Question': "How many white colour Levi t-shirts are available",
     'SQLQuery' : "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "There are 320 white colour Levi t-shirts are available right now"
    },
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "There are 88 t-shirts left for Nike in XS size and white color"},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "27325 is the total price of the inventory for all S-size t-shirts"},
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': "Revenue of our store will be 35593 if we sell all the Levi's T-shirts today with discounts applied"} ,
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "Revenue of our store will be 38425 if we sell all the Levi's T-shirts today without discounts applied"},
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "There are 320 white color Levi's shirt avaliable"
     },
    {'Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer' : "The Sales amount will be 290 if we sell all Large size t-shirts today in nike brand after discounts"
    },
    {'Question': "How many white colour Nike t-shirts are available",
     'SQLQuery' : "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "There are 366 white colour Nike t-shirts available"
    }
]