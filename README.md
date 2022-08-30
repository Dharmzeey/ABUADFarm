# ABUAD Farm


I designed this web Application on the foundation of a Manufacturing Company.
It is a Django Project, which I also used djangorestframework for some serialization.
I used vanilla Js and Tailwind CSS(django-tailwind)
Django-Allauth was used for the authentication 

It has different Apps that handled different functionalities

You can check the mini documentation [Here](https://github.com/Dharmzeey/ABUADFarm/blob/master/code_docs.txt)


# ADMIN
##The Admin can:
-Can view all the Units.
-Can view all the customers on the Database, regardless of the unit they have made purchase from 
-Can see all messages sent to all customers 
-Untimately, can have access to all the features, models and everything of the Django Admin panel and also perform CRUD operations on everything in the Django Admin Panel 

#STAFFS
## These are the users that have been assigned to each units in the company 
###Their Staffs status was created by the superuser (Admin) in the Admin panel 
##Staffs Can:
-View all the customers that made purchase from their units 
-Send message to each customers who has made purchase from their units 
-Add customers product purchase for each customer who made purchase from their units 

#USERS
**All accounts created have user and  profiles model**
**But they are later given different statuses**
## Users are customers who created account and made purchase from any unit 
##Users can 
-Habe access to their Dashboard, Messages, Notifications and Profiles 
