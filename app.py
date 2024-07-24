# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
import random

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host,
        settings.mysql_user,
        settings.mysql_passwd,
        settings.mysql_schema)

    return con

def  findTrips(x,a,b):

    # Create a new connection
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    sql1= ("""SELECT tp.cost_per_person,tp.max_num_participants,count(r.Reservation_id),tp.max_num_participants - count(r.Reservation_id),tp.trip_start,tp.trip_end,tp.trip_package_id
from trip_package tp, reservation r,travel_agency_branch tab
WHERE tab.travel_agency_branch_id = %s and tab.travel_agency_branch_id = r.travel_agency_branch_id and r.offer_trip_package_id = tp.trip_package_id and tp.trip_start >=%s and tp.trip_start <=%s
group by tp.cost_per_person,tp.max_num_participants,tp.trip_start,tp.trip_end,tp.trip_package_id

""")
    tuple1 = (x, a, b)
    cur.execute(sql1,tuple1)
    data = cur.fetchall()
    a = list(data)


    k = 0
    for i in a:
        k=k+1
    q = []
    t = 0
    c = []

    for i in a:
            sql2=("""select distinct e.surname, e.name
            from trip_package tp,guided_tour gt,travel_guide tg, employees e
            where tp.trip_package_id = %s and tp.trip_package_id = gt.trip_package_id and gt.travel_guide_employee_AM = tg.travel_guide_employee_AM and tg.travel_guide_employee_AM = e.employees_AM""")
            cur.execute(sql2,i[6])
            data2 = cur.fetchall()
            b = tuple(data2)
            list_a1 = list(a[t])
            list_a1.remove(list_a1[6])
            first_package = list_a1




            q.append(b)

            print(q)
            first_package_with_guides = first_package + list(q)
            c.insert(t,first_package_with_guides)
            t = t + 1
            q.clear()

            # for m in range(l):
            #     if m == 0:
            #         a.insert(q,[a[t][0],a[t][1],a[t][2],a[t][3],a[t][4],a[t][5],b[m][0],b[m][1]])
            #         a.pop(q+1)
            #         q=q+1
            #         t=t+1
            #     else :
            #         a.insert(q,[" "," "," "," "," "," ",b[m][0],b[m][1]])
            #         q=q+1
            #         t=t+1
    print(c)
    c.insert(0, ["Cost per person", "Max num participants", "Reservation", "Empty seats", "Start date","End date", "Guides"])
    return c


def findRevenue(x):

   # Create a new connection
   con=connection()
   # Create a cursor on the connection
   cur = con.cursor()

   def sort_key(a_key):
       return a_key[2]

   if x == "DESC":
        sql=("""select distinct tab.travel_agency_branch_id,count(r.Reservation_id)
        from travel_agency_branch tab,reservation r,offer o
        where tab.travel_agency_branch_id = r.travel_agency_branch_id  and o.offer_id = r.offer_id
        group by tab.travel_agency_branch_id""")
        cur.execute(sql)
        data = cur.fetchall()
        a = list(data)
        print(a)
        sql2 = ("""select distinct tab.travel_agency_branch_id, sum(o.cost)
        from travel_agency_branch tab,reservation r,offer o
        where tab.travel_agency_branch_id = r.travel_agency_branch_id  and o.offer_id = r.offer_id
        group by tab.travel_agency_branch_id""")
        cur.execute(sql2)
        data1 = cur.fetchall()
        b = list(data1)
        sql3 = ("""select distinct tab.travel_agency_branch_id,count(e.employees_AM),sum(e.salary)
        from travel_agency_branch tab,employees e 
        where tab.travel_agency_branch_id = e.travel_agency_branch_travel_agency_branch_id 
        group by tab.travel_agency_branch_id""")
        cur.execute(sql3)
        data2 = cur.fetchall()
        c = list(data2)
        print(b)
        print(c)
        k=0
        for i in a:
            k=k+1


        for i in range(k):
            a.insert(i,[a[i][0],a[i][1],b[i][1],c[i][1],c[i][2]])
            a.pop(i+1)


        a.sort(key=sort_key, reverse=True)
        a.insert(0, ("TRAVEL_AGENCY_ID", "RESERVATIONS", "TOTAL_COST", "EMPLOYEES", "TOTAL_SALARY"))
        return (a)




   else:
       sql = ("""select distinct tab.travel_agency_branch_id,count(r.Reservation_id)
                from travel_agency_branch tab,reservation r,offer o
                where tab.travel_agency_branch_id = r.travel_agency_branch_id  and o.offer_id = r.offer_id
                group by tab.travel_agency_branch_id""")
       cur.execute(sql)
       data = cur.fetchall()
       a = list(data)
       print(a)
       sql2 = ("""select distinct tab.travel_agency_branch_id, sum(o.cost)
                from travel_agency_branch tab,reservation r,offer o
                where tab.travel_agency_branch_id = r.travel_agency_branch_id  and o.offer_id = r.offer_id
                group by tab.travel_agency_branch_id""")
       cur.execute(sql2)
       data1 = cur.fetchall()
       b = list(data1)
       sql3 = ("""select distinct tab.travel_agency_branch_id,count(e.employees_AM),sum(e.salary)
                from travel_agency_branch tab,employees e 
                where tab.travel_agency_branch_id = e.travel_agency_branch_travel_agency_branch_id 
                group by tab.travel_agency_branch_id""")
       cur.execute(sql3)
       data2 = cur.fetchall()
       c = list(data2)
       print(b)
       print(c)
       k = 0
       for i in a:
           k = k + 1

       for i in range(k):
           a.insert(i, [a[i][0], a[i][1], b[i][1], c[i][1], c[i][2]])
           a.pop(i + 1)


       a.sort(key=sort_key,reverse=False)
       a.insert(0, ("TRAVEL_AGENCY_ID", "RESERVATIONS", "TOTAL_COST", "EMPLOYEES", "TOTAL_SALARY"))
       return(a)

def bestClient(x):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()



    sql1=("""select sum(o.cost),t.traveler_id
    from traveler t,offer o,reservation r
    where  t.traveler_id = r.Customer_id and r.offer_id = o.offer_id 
    group by t.traveler_id
    order by sum(o.cost) DESC""")
    cur.execute(sql1)
    data = cur.fetchall()
    a = list(data)
    if a[0][0] != a[1][0]:
        sql2=("""select distinct  t.name,t.surname,count(distinct d.country),count(distinct d.destination_id)
        from  traveler t,reservation r,offer o,trip_package tp,trip_package_has_destination tphd,destination d,tourist_attraction ta,guided_tour gt 
        where t.traveler_id = %s and  t.traveler_id = r.Customer_id and r.offer_id = o.offer_id and o.trip_package_id = tp.trip_package_id and tp.trip_package_id = tphd.trip_package_trip_package_id and tphd.destination_destination_id = d.destination_id and tp.trip_package_id = gt.trip_package_id and ta.tourist_attraction_id = gt.tourist_attraction_id
        group by t.name,t.surname""")
        cur.execute(sql2,a[0][1])
        data1 = cur.fetchall()
        b = list(data1)
        print(a)
        sql3=("""select distinct  ta.name
        from  traveler t,reservation r,offer o,trip_package tp,trip_package_has_destination tphd,destination d,tourist_attraction ta,guided_tour gt 
        where t.traveler_id = %s and  t.traveler_id = r.Customer_id and r.offer_id = o.offer_id and o.trip_package_id = tp.trip_package_id and tp.trip_package_id = tphd.trip_package_trip_package_id and tphd.destination_destination_id = d.destination_id and tp.trip_package_id = gt.trip_package_id and ta.tourist_attraction_id = gt.tourist_attraction_id
        """)
        cur.execute(sql3,a[0][1])
        data2 = cur.fetchall()
        c = list(data2)
        a.insert(0, [b[0][0], b[0][1],b[0][2],b[0][3],c])
        k=[]
        k.insert(0,("NAME", "SURNAME", "COUNTRIES", "CITIES","ATTRACTIONS"))
        k.insert(1,a[0])
        return k
    else:
        b=[]
        c=[]
        m=0
        for i in a:
            m = m + 1
        for i in range(m):
            sql2 = ("""select distinct  t.name,t.surname,count(distinct d.country),count(distinct d.destination_id)
            from  traveler t,reservation r,offer o,trip_package tp,trip_package_has_destination tphd,destination d,tourist_attraction ta,guided_tour gt 
            where t.traveler_id = %s and  t.traveler_id = r.Customer_id and r.offer_id = o.offer_id and o.trip_package_id = tp.trip_package_id and tp.trip_package_id = tphd.trip_package_trip_package_id and tphd.destination_destination_id = d.destination_id and tp.trip_package_id = gt.trip_package_id and ta.tourist_attraction_id = gt.tourist_attraction_id
            group by t.name,t.surname""")
            cur.execute(sql2,a[i][1])
            data1 = cur.fetchall()
            sql3 = ("""select distinct  ta.name
            from  traveler t,reservation r,offer o,trip_package tp,trip_package_has_destination tphd,destination d,tourist_attraction ta,guided_tour gt
            where t.traveler_id = %s and  t.traveler_id = r.Customer_id and r.offer_id = o.offer_id and o.trip_package_id = tp.trip_package_id and tp.trip_package_id = tphd.trip_package_trip_package_id and tphd.destination_destination_id = d.destination_id and tp.trip_package_id = gt.trip_package_id and ta.tourist_attraction_id = gt.tourist_attraction_id
            """)
            cur.execute(sql3, a[i][1])
            data2 = cur.fetchall()
            b.insert(i,[data1,data2])

    return b


def giveAway(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    sql=("""select distinct t.traveler_id
from traveler t""")
    cur.execute(sql)
    data = cur.fetchall()
    a = list(data)
    b = []
    for i in range(int(N)):
        r = random.randint(1,2741)
        b.insert(i,[r,0,0,0,0,0,0,0,0,0,0])

    print(b)

    print("MMMMMMMMMMMMMMMMMM")
    c = []
    for i in range(int(N)):

        sql2= ("""select tp.trip_package_id
    from trip_package tp
    where not exists(select *
    from reservation r, traveler t
    where r.Reservation_id = t.traveler_id and tp.trip_package_id = r.offer_trip_package_id and t.traveler_id = %s)""")
        cur.execute(sql2,b[i][0])
        data1 = cur.fetchall()

        r = random.choice(data1)
        while r in c:
            r = random.choice(data1)
        c.insert(i,r[0])

    for i in range(int(N)):
        b[i][1] = c[i]

    print(b)

    for i in range(int(N)):
       sql3 = ("""select count(r.Reservation_id)
    from traveler t,reservation r
    where t.traveler_id = r.Customer_id and t.traveler_id = %s""")
       cur.execute(sql3,b[i][0])
       data2 = cur.fetchall()
       b[i][2] = data2[0][0]
    print(b)


    for i in range(int(N)):
        sql4=("""select tp.cost_per_person
     from trip_package tp
     where tp.trip_package_id = %s""")
        cur.execute(sql4,b[i][1])
        data3 = cur.fetchall()
        b[i][3] = data3[0][0]
    print(b)

    for i in range(int(N)):
        sql5 =("""select t.gender
     from traveler t
     where t.traveler_id =%s""")
        cur.execute(sql5,b[i][0])
        data4 = cur.fetchall()
        b[i][4] = data4[0][0]

    print(b)
    k = 100000
    for i in range(int(N)):
        if b[i][2] >= 2:
            sql6=("INSERT INTO `offer` VALUES (%s,'2022-12-27','2023-01-27',%s,'Happy traveler tour',%s,'group_discount')")
            res = b[i][3] - (25/100)*b[i][3]
            tuple2 = (k,res,b[i][1])
            cur.execute(sql6,tuple2)
            con.commit()
            b[i][8] = k
            b[i][9] = res
            k = k+1
        else:
            sql6=("INSERT INTO `offer` VALUES (%s,'2022-12-27','2023-01-27',%s,'Happy traveler tour',%s,'full_price')")
            tuple3 = (k,b[i][3], b[i][1])
            cur.execute(sql6,tuple3)
            con.commit()
            b[i][8] = k
            b[i][9] = b[i][3]
            k = k+1


    for i in range(int(N)):
        sql7=("""select t.name,t.surname
        from traveler t
        where t.traveler_id = %s""")
        cur.execute(sql7,b[i][0])
        data5 = cur.fetchall()
        b[i][5] = data5[0][0]
        b[i][6] = data5[0][1]
        sql8=("""select distinct d.name
        from destination d,trip_package tp,trip_package_has_destination tphd
        where tp.trip_package_id = %s and tp.trip_package_id = tphd.trip_package_trip_package_id and tphd.destination_destination_id = d.destination_id""")
        cur.execute(sql8,b[i][1])
        data6 = cur.fetchall()
        b[i][7] = (data6)
        sql9=("""select distinct o.offer_end
        from offer o,trip_package tp
        where tp.trip_package_id = %s and tp.trip_package_id = o.trip_package_id and o.offer_id = %s""")
        tuple4 = (b[i][1],b[i][8])
        cur.execute(sql9,tuple4)
        data7 = cur.fetchall()
        b[i][10] = data7[0][0]


    print(b)



    mes=[]
    for i in range(int(N)):
        if b[i][4]=='male':
            string1 = 'Congratulations Mr ' + str(b[i][5]) + ' ' + str(b[i][6])
            string1 = string1 +  """! Pack your bags and get ready to enjoy the Happy traveler! At ART TOUR travel we
            acknowledge you as a valued customer and we’ve selected the most incredible
            tailor-made travel package for you. We offer you the chance to travel to """ + str(b[i][7])
            string1 = string1 + """ at the incredible price of """ + str(b[i][9])
            string1 = string1 + """. Our offer ends on """ + str(b[i][10])
            string1 = string1 + """ . Use code OFFER""" + str(b[i][8])
            string1 = string1 + """ to book your trip. Enjoy these holidays that you deserve so much!"""
            mes.insert(i,[string1])
        else:
            string1 = 'Congratulations Ms ' + str(b[i][5]) + ' ' + str(b[i][6])
            string1 = string1 + """! Pack your bags and get ready to enjoy the Happy traveler! At ART TOUR travel we
            acknowledge you as a valued customer and we’ve selected the most incredible
            tailor-made travel package for you. We offer you the chance to travel to """ + str(b[i][7])
            string1 = string1 + """ at the incredible price of """ + str(b[i][9])
            string1 = string1 + """. Our offer ends on """ + str(b[i][10])
            string1 = string1 + """ . Use code OFFER""" + str(b[i][8])
            string1 = string1 + """ to book your trip. Enjoy these holidays that you deserve so much!"""
            mes.insert(i, [string1])





    mes.insert(0,["CONGRATULATIONS!"])

    return mes







