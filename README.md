# kcsf-api
Kcsf Data Visualization platform API

### Inslallation
#### Environment
- Ubuntu 14.04 LTS 64 bit
- MongoDB 3.0.10
- Apache Virtual Hosts (httpd)

#### Initial Setup
Apache Virtual Host:
```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
```

Create project .wsgi
```
sudo cp app-template.wsgi app.wsgi
```

Open the new file in your editor with root privileges:
```
sudo nano app.wsgi
```

And configure the project's path:
```
app_dir_path = '/var/www/kcsf-api'
```

Create and edit project config file:
```
sudo config-template.cfg config.cfg
sudo nano config.cfg
```

#### Create New Virtual Host
**IMPORTANT:** In production we are deploying this app under opendatakosovo.org domain so we are just adding a new virtual host to the *opendatakosovo.org.conf* file. The following instructions do not apply in our case but we still include them for documentation purposes on how to set this up from scratch:

Copy default virtual host config file to create new file specific to the project:
```
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/kcsf-api.org.conf
```

Open the new file in your editor with root privileges:
```
sudo nano /etc/apache2/sites-available/kcsf-api.org.conf
```

And configure it to point to the project's app.wsgi file:
```
<VirtualHost *:80>
  ServerAdmin admin@localhost
  #ServerName opendatakosovo.org
  
  WSGIScriptAlias / /var/www/kcsf-api/app.wsgi
  <Directory /var/www/kcsf-api>
    Order allow,deny
    Allow from all
  </Directory>
    
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

#### Enable New Virtual Host
First disable the defaul one:
```
sudo a2dissite 000-default.conf
```

Then enable the new one we just created:
```
sudo a2ensite kcsf-api.org.conf
```

Restart the server for these changes to take effect:
```
sudo service apache2 restart
```

### Sample JSON structure for CSO Survey data entry.

```json
{
  "q2": {
    "answer": "Prishtina",
    "question": "Location (town/municipality)"
  },
  "q7": {
      "answer": ["Student Organization","Youth","Sport"],
      "question": "Scope of activity"
  },
  "q9": {
      "answer": "Specific municipality",
      "question": "Which level of governance is the main focus of the work of your organization?"
  }, 
  "q11": {
      "answer": "2010",
      "question": "In which year was your organization established"
  },
  "q14": {
      "answer": "Association (membership-based organization)",
      "question": "Which is the form of registration of your organization?"
  }, 
  "q15": {
      "answer": "Yes",
      "question": "Does your organization have a Public Beneficiary Status?"
  }, 
  "q18": {
      "answer": "Board",
      "question": "What is the highest governing body of your organization? "
  }
}
```
