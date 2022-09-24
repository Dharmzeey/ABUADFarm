# ABUAD Farm


I designed this web Application on the foundation of a Manufacturing Company.
## About the company
- The Idea is as a result of where I was posted to do my IT, so the organization is a Farm and also a manufacturing company, they make different products from their farm produce. 
- They have different units and they produce different products at each units
I then decided to build something channeling my focus to the mode of operation 

It is a Django Project, which I also used djangorestframework for some serialization.
I used vanilla Js and Tailwind CSS(django-tailwind)
Django-Allauth was used for the authentication 

It has different Apps that handled different functionalities


![Homepage](https://github.com/Dharmzeey/dharmzeey/blob/master/public/images/abuadfarm/Home-page.png)
## **Home Page**


# ADMIN
**The Admin is a Django superuser who has full access to the Django Admin Panel and also to all the units and products and all customers both in the Django Admin Panel and the other Admin Page** 
## The Admin can:
- Can view all the Units.
- Can view all the customers on the Database, regardless of the unit they have made purchase from 
- Can see all messages sent to all customers 
- Untimately, can have access to all the features, models and everything of the Django Admin panel and also perform CRUD operations on everything in the Django Admin Panel 

# STAFFS
**The Staffs is also Django Staff, they only have restricted access to the models and customers concerning their units alone and has restricted access to the Django Admin panel.**
## These are the users that have been assigned to each units in the company 
### Their Staffs status was created by the superuser (Admin) in the Admin panel 
## Staffs Can:
- View all the customers that made purchase from their units 
- Send message to each customers who has made purchase from their units 
- Add customers product purchase for each customer who made purchase from their units 

# USERS
**Customers only have access to their accounts alone(which contains all the units they made purchases)**
**All accounts created have user and  profiles model**
**But they are later given different statuses**
## Users are customers who created account and made purchase from any unit 
## Users can:
- Have access to their Dashboard, Messages, Notifications and Profiles 

# OPERATIONS

## Frameworks
- Django-allauth was the framework used to handle user Registration, Authentication, Validations, Checks and restrictions concerning anything Username and Password.
- DjangorestFramwork was used to serialze the data from the Goods model of a customer to be dislayed a chart oh the dashboard.
- Django-Tailwind was used as the css framework throughout the whole project. It is contained in the app called theme.

## Lbraries
- amcharts js was the library used to render data as a grpah on user dashboard
- Tailwind was used for css
- Font awesome was used to load icons
- Google fonts was used to load font and style the Page

## MODELS
- The owner attribute (which is a ForeignKey to the User Model) of the Goods and Messages model class of the app named "user" refers to the customers and not the current logged in user when the logged in user is an Admin or a staff operating on the customers.
- If it is that the user (customer) is logged into his/her account, the owner attribute of the Profile, Goods and the Messages model will refer to the current logged in user
- The staffModel is used to carry staff detail and their units around the app for usage(which include filtering of units for customers when changes want to be made on the Models)
