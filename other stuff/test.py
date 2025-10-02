import mysql.connector as mysql

watched_list = [
    "All Of Us Are Dead",            
    "My Demon",
    "Backstreet Rookie" ,     
    "Nevertheless",           
    "Love Alarm",                  
    "Descendants Of The Sun",        
    "Angel’s Last Mission: Love",   
    "Tale Of The Nine Tailed",   
    "It’s Okay to Not Be Okay",       
    "Crash Landing On You",       
    "Vincenzo",          
    "My Roommate Is A Gumiho",      
    "Destined With You",       
    "Goblin",              
    "The Judge From Hell",           
    "Business Proposal",             
    "The Beauty Inside",             
    "I’m Not a Robot",               
    "King The Land",                  
    "What’s Wrong With Secretary Kim",
    "Start-Up",
    "Suspicious Partner",            
    "True Beauty"  
]

connection = mysql.connect(host="localhost", user="root", password="system")
cursor = connection.cursor()
cursor.execute("USE dramas;")
for drama in watched_list:
    cursor.execute("select drama_name from drama_table where drama_name like %s;",(f"%{drama}%",))
    drama_name = cursor.fetchall()[0][0]
    print(drama_name)
    values = (drama_name,'watched')
    cursor.execute("INSERT IGNORE INTO user_table (drama_name,category) values(%s,%s)",values)
connection.commit()
cursor.close()
connection.close()