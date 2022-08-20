# location_checker

1.  git clone my project from github => https://github.com/burmese-girl/location_checker
2.  create virtual enviroment with the below commands if you want to separate enviromnent for this project.

    export WORKON_HOME=$HOME/virtenvs

    export PROJECT_HOME=$HOME/Projects-Active

    source $HOME/.local/bin/virtualenvwrapper.sh

    mkvirtualenv dux

    After creating virtual environment, you should be on 'dux' environment. If 'dux' environment is not active, you can use 'workon dux' command in you terminal. Now you can install dependencies with this command => pip install -r requirements.txt

    After installing dependencies, please install the below python dependency in your local PC.

    sudo apt-get install gettext

3.  Create database with postgres, it is called 'dux_location' because this database name already setup in settings.py inside the project folder. After creating database, you need to restore database with my "dux_db.sql" then you don't need to create records in database for analysis.

Please do not use if you don't want to create data in database using "Search IP" button on Profile page.
Another options for new database but you need to search for almost all IP address in your excel because this new database will not have data for analysis.
After creating database, you need to migrate with the below command in your teminal.

        python manage.py makemigrations
        python mamage.py migrate

4.  run the server with the below command in your terminal
    python manage.py runserver

5.  You can create super user on terminal if you want.

        python manage.py createsuperuser

If you don't want to use super user for testing, please create normal user with this link => 'http://127.0.0.1:8000/user/register/'

In this step, you can give the username, email and password as you want.

6. All the above steps are finish, you can login now and search ip in profile page using with 'Search IP' button.

I call API 'http://ipwho.is/[IP]' when you click 'Search IP' button and save 7 fields(as described in your 'Test Location Review.pdf' into IPAddress table in postgresql database. Those data from IpAddress table will be used to show Pie Chart.

7. You can see your ip search history in profile page using 'Search History Dashboard' button, order by created date.

8. For the pie chart depend on the most searched country, click the 'Show Pie Chart' button in profile page too.

9. For the heap map, data will show with region and country depend on the users searched history, , click the 'Show Heap Map' button in profile page too.
