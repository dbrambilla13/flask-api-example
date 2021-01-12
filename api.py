from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort

# define flask app
app = Flask(__name__, template_folder="templates")

# wrap app in an Api
api = Api(app)


names = {}
@app.route("/")
def home():
    return render_template("home.html")

def abort_if_id_not_valid(id):
    if id not in names:
        abort(404, message="Id is not valid.")

def abort_if_id_already_exists(id):
    if id in names:
        abort(409, message="Id already exists.")


class Contacts(Resource):

    def __init__(self):
        
        self.names_put_args = reqparse.RequestParser()

        self.names_put_args.add_argument("name", type=str, help="Insert the person's firts name", required=True)
        self.names_put_args.add_argument("country", type=str, help="Insert the person's country of origin", required=False)
        self.names_put_args.add_argument("birth", type=str, help="Insert birth date.", required=False)

    def get(self, id):
        abort_if_id_not_valid(id)
        return names[id]

    def put(self, id):
        abort_if_id_already_exists(id)
        args = self.names_put_args.parse_args()
        names[id] = args
        return names[id], 201  # 201 created code


# register the class as a resource
api.add_resource(Contacts, "/Contacts/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)