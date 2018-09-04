from app import create_app, mongo, bcrypt, secret_key

# instantiate app instance so that we can load mongo configurations
# and use them in the importer implementation
app = create_app()

def run_seed():

    # This is to expand the app's context(scope),
    # so that we can use mongo configurations for the importer too.
    with app.app_context():
        # First user
        firstName = 'KCSF'
        lastName = 'Admin'
        email = "admin@kcsf.com"
        password = "superkcsf"

        # Check if email is already used
        if mongo.db.user.find({'email': email}).count() > 0:
            print """Email is already used"""
            return

        # Hashing password
        hash_pwd = bcrypt.generate_password_hash(password)

        # Saving first user into db
        mongo.db.user.insert({
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'password': hash_pwd
        })

        print """User successfully saved!"""
        return

if __name__ == '__main__':
    run_seed()