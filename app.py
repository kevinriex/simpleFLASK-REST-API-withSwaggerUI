# Imports
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from jsonify import *
from marshmallow import Schema, fields


app = Flask(__name__, template_folder="swagger/templates") # Initilisation Flask App


@app.route("/") # Root Route
def home():
    return "<h1>Welcome, to my API</h1>"

spec = APISpec(
    title='FLASK-API-Swagger-Docs',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
) # Specifing th API Specifications

@app.route("/api/swagger.json") # Route to the auto generated "swagger.json"
def create_swagger_spec():
    return jsonify(spec.to_dict())

# Defining a Schema
class TodoResposeSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()

# Using the Schema
class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResposeSchema))


@app.route("/todo") # Route to GET the TodoList Item
def todo():
    '''Get List of Todo
        ---
        get:
            description: Get List of Todos
            responses:
                200:
                    description: Return a todo list
                    content: 
                        application/json:
                            schema: TodoListResponseSchema
    '''
    dummy = [{
        "id": 1,
        "title": "Finish it",
        "status": False
    },
    {
        "id": 1,
        "title": "Finish it",
        "status": False
    }]

    return TodoListResponseSchema().dump({"todo_list": dummy}) # Returns the Dummy Object as JSON within the Schema

with app.test_request_context(): # Adding the Todo Route to the swagger.json
    spec.path(view=todo)

@app.route("/docs") # Route to the Documentation
@app.route("/docs/<path:path>")
def swagger_docs(path=None):
    if not path or path == "index.html":
        return render_template("index.html", base_url="/docs") # Returning the index.html
    else:
        return send_from_directory("./swagger/static", path) # Serving static Content
        
if __name__ == "__maine__":
    app.run(debug=True) # Running the App in Debug Mode. If this dosen´t work use 'flask --debug run'