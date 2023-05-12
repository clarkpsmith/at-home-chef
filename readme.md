**Description**

*At Home Chef* is a recipe/cooking website that allows users to look up recipes, add reviews/comments, save recipes to their user profile, and easily send ingredient lists to their email with the click of a button. It uses recipe data from the Spoonacular Recipe API. Recipe List Sending is done using the Sendgrid API. 

Recipe's can be searched by name with an optional filter for dietary restrictions or search by ingredients. There is also a seasonal dishes page that serves the user dish ideas based on the season or holiday that updates everytime the page is loaded. These feature can be used without the need for a user profile. 

Creating a user profile gives the user the ability to save favorite recipes and access a list of favorited recipes from their user page. (the user's favorite recipe list is ordered by favorited date with most recently favorited at the top)

Creating a user profile also allows the user to comment/review recipes that are visible to anyone using the site along with the ability to send an ingredient list to their email at the click of a button. 

User passwords are hashed using Bcrypt encryption and stored as encrypted data.

You can visit the site at [https://at-home-chef.herokuapp.com/
]()

**Front End Tech Stack**

(HTML, CSS, Javascript)
	 
**Back End Tech Stack**

(Python, Flask, PostgreSQL, SQlalchemy, WTF Forms)

**API's**

[https://spoonacular.com/food-api/ ]()

[https://sendgrid.com/]()
 

**IMPORTANT NOTES ON SETUP:**
 
 1. Setup PostgreSQL Database
	 (make sure psql is installed on your machine, then open psql)
	run the following in your shell
	
	createdb athomechef
	
2. In order to run this project you must get your own api key from the spoonacular api website along with the sendgrid api by creating an account for each and using those keys values for variable names API\_SECRET\_KEY for the Spoonacular API Key & SENDGRID\_API\_KEY for the sendgrid api key. Follow specific instructions below for setting up the SendGrid API Key and development enviroment

**Sendgrid API Key setup:**

1. Create a sengrid account
2. follow instructions for setting up an email api
3. Email API/Integration Guide/Web API/Python
4. follow instructions for creating an API KEY
5. Create an environment variable
	
 	- Update your development environment with your SENDGRID_API_KEY. (Run the following in your shell)
 	
	echo "export SENDGRID\_API\_KEY="'YOUR\_SENDGRID\_API\_KEY\_GOES\_HERE'" > 	sendgrid.env
	
	echo "sendgrid.env" >> .gitignore

6. **IMPORTANT** Run source ./sendgrid.env (every time you start up the application and before starting up your virtual environment)


