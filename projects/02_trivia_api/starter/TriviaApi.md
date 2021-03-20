## API Reference

### Getting Started
- Base URL: this app is hosted locally at `http://127.0.0.1:5000` 
- Authentication: no authentication required. 

### Error Handling
Errors are returned as JSON objects:
- Sample: `curl http://127.0.0.1:5000/`
    {
        "success": false, 
        "error": 404,
        "message": "Not Found"
    }

returned error codes:
- 405: Method not allowed
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error (rare)

### Endpoints 
### GET /questions 
- General:
    - Returns success value, available todos as the following format
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
- Parameter 
  -Url parameter of page number
- Returns :
```
 {
    "success":True,
    "questions":[],
    "categories":{},
    "current_category":"",
    "total_questions":5
    }

```

### GET /categories 
- General:
    - Returns success value, available todos as the following format
- Sample: `curl http://127.0.0.1:5000/categories`
- Returns :
``` 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

#### POST /questions/add
- General:
    - Creates a new question ,returns success value and an added questions object
    - expects input as :
    - 
- `curl http://127.0.0.1:5000/questions/add -X POST -H "Content-Type: application/json" -d '{"question":"new question" ,"answer":"","category":1,"difficulty":1}'`
-Returns :
```
{
  "success": true,
  "created_question": 1,
  "questions":[],
  "total_questions":10
}
```

#### DELETE /questions/1
- General:
    - Delete a question using question id ,returns success value and an added todo object
    - expects input as :
- `curl http://127.0.0.1:5000/questions/1 -X DELETE `
-Returns :
```
{
  "success": true,
  "deleted_question": 1,
  "questions":[],
  "total_questions":10
}
```