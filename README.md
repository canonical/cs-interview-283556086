# AUDITOR

Event Submission Endpoint
Endpoint URL

```
POST /events
```

## Request Headers
|Header Name|	Required|	Description|
|-----------|---------|------------|
X-API-Key	|Yes|	The API key used to authenticate the request. This is a string value that must match the API key specified in the server.|


## Request Body

The request body must be a JSON object that contains the following properties:
|Property|	Type|	Required|	Description|
|----|----|----|----|
user_id	|string|	Yes|	The ID of the user who performed the action. This is a string value that uniquely identifies the user.|
event_type	|string|	Yes|	The type of the event. This is a string value that identifies the type of action that was performed.|
data|	object	|No|	Additional data about the event. This is an object value that can contain any number of properties specific to the event type.|


## Response Body

The response body will be a JSON object that contains the following properties:
|Property	|Type	|Description|
|-|-|-|
message	|string	|A message indicating the success or failure of the request. This is a string value that can contain any text.|
id	|string|	The ID of the event that was recorded. This is a string value that uniquely identifies the event.|

## Event Query Endpoint

### Endpoint URL

```
GET /events
```

### Request Headers
|Header Name|Required|	Description|
|-|-|-|
X-API-Key	|Yes|	The API key used to authenticate the request. This is a string value that must match the API key specified in the server.

### Query Parameters
The following query parameters can be used to filter the events:
Parameter Name	|Required	|Description
|-|-|-|
user_id	|Yes	|The ID of the user who performed the action. This is a string value that uniquely identifies the user.
event_type	|No|	The type of the event. This is a string value that identifies the type of action that was performed.
{field_name}	|No|	Additional fields to filter by. These are string values that match the property names in the data field of the event.

### Response Body

The response body will be a JSON array containing all the events that match the query parameters. Each event in the array will be a JSON object with the following properties:
Property|	Type	|Description
|-|-|-|
id	|string|	The ID of the event. This is a string value that uniquely identifies the event.
timestamp	|string	|The timestamp when the event was recorded. This is a string value in the ISO 8601 format.
user_id	|string	|The ID of the user who performed the action. This is a string value that uniquely identifies the user.
event_type	|string|	The type of the event. This is a string value that identifies the type of action that was performed.
data	|object	|Additional data about the event. This is an object value that can contain any number of properties specific to the event type.

### Authenticating the Request

To authenticate a request, the client must include the API key in the X-API-Key header of the HTTP request. The server will then check that the API key matches the one stored on the server. If the API key is valid, the request will be allowed to proceed. If the API key is invalid or missing, the server will return a 401 Unauthorized response.

## Design Notes

### Data Storage 
The reason SQLite was chosen as the data storage is because it is a file-based relational database that is optimized for write-intensive workloads. It provides high concurrency and low overhead, which makes it well-suited for handling a large volume of event data. The trade-off is that SQLite is not as scalable as some other databases, and may not be suitable for extremely large datasets or high-traffic.

### DB Schema
The database schema is designed to handle any type of event. All events are stored in the same database table, and the data field in each event record can store any additional data that is specific to the event type.
When a new event type is added, the only change that needs to be made is to include the new event type in the event_type property of the event object that is submitted to the microservice API. The microservice will store the event in the database with the same structure as any other event, and the data specific to the new event type will be stored in the data field of the event record.
This design allows the microservice to handle any number of event types without the need to modify the code or the database schema.

### HTTP Server
Python's built-in http.server module was chosen due the requirement restriction of minimise the use of frameworks.

### API Key Authentication.
The microservice uses API key authentication to secure the endpoints. This is achieved by requiring clients to include a valid API key in the X-API-Key header of the HTTP request. This provides a simple way to authenticate clients without requiring complex user authentication mechanisms. The trade-off is that API key authentication is less secure than other authentication mechanisms.
