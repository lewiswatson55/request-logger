# Code Documentation

This is a Python Flask application that logs incoming HTTP requests to files. It provides several routes for different purposes.

## Routes

### Index Route

```python
@app.route('/', methods=['GET', 'POST'])
@app.route('/log', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        save_request(request.data, subdirectory='request_logs')
        return "Logged request data successfully"
    else:
        return "Hello, World!", 200
```

- The index route ("/" or "/log") accepts both GET and POST requests.
- If a POST request is received, it calls the `save_request` function to save the request data to a file in the "request_logs" subdirectory.
- If a GET request is received, it returns the message "Hello, World!" with a status code 200.

### Log Route

```python
@app.route('/log/<log_name>', methods=['GET', 'POST'])
def log(log_name):
    if request.method == 'POST':
        save_request(request.data, subdirectory=str(log_name))
        return "Logged request data successfully into {}".format(log_name)
    else:
        return "womp womp, not a post request.", 418
```

- The log route ("/log/<log_name>") accepts both GET and POST requests.
- The `<log_name>` parameter in the route is a placeholder for the name of the log.
- If a POST request is received, it calls the `save_request` function to save the request data to a file in a subdirectory with the name of `<log_name>`.
- If a GET request is received, it returns the message "womp womp, not a post request." with a status code 418 (I'm a teapot).

### Dummy Route

```python
@app.route('/dummy', methods=['GET', 'POST'])
def dummy():
    if request.method == 'POST':
        save_request(request.data, subdirectory='dummy')
        return "ko", 200
    else:
        return render_template('dummy.html')
```

- The dummy route ("/dummy") accepts both GET and POST requests.
- If a POST request is received, it calls the `save_request` function to save the request data to a file in the "dummy" subdirectory.
- If a GET request is received, it renders a template called "dummy.html".

### Complete Route

```python
@app.route('/complete')
def complete():
    return render_template('complete.html')
```

- The complete route ("/complete") only accepts GET requests.
- It renders a template called "complete.html".

## Helper Function

### save_request

```python
def save_request(request_data, subdirectory='request_logs'):
    print("Received request data:", request_data)

    # Generate a unique ID for the file name
    id = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

    # Get current month and year
    current_month = datetime.datetime.now().strftime("%B")
    current_year = datetime.datetime.now().strftime("%Y")

    # Create subdirectory if it doesn't exist under the base directory
    base_directory = 'requests'
    subdirectory_path = os.path.join(base_directory, subdirectory)
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)

    # Create year directory if it doesn't exist under the subdirectory
    year_directory = os.path.join(subdirectory_path, current_year)
    if not os.path.exists(year_directory):
        os.makedirs(year_directory)

    # Create month directory if it doesn't exist under the year directory
    month_directory = os.path.join(year_directory, current_month)
    if not os.path.exists(month_directory):
        os.makedirs(month_directory)

    # Save the request data to a file
    file_path = os.path.join(month_directory, "{}.txt".format(id))
    with open(file_path, 'w') as f:
        f.write(str(request_data))

    return 0
```

- The `save_request` function is responsible for saving the incoming request data to a file in a specified subdirectory.
- It takes the request data as input and an optional `subdirectory` parameter (default value is 'request_logs').
- It generates a unique ID for the file name using the current timestamp.
- It gets the current month and year.
- It creates the subdirectory, year directory, and month directory if they don't exist under the base directory.
- It saves the request data to a file in the month directory with the generated ID as the file name.
- It returns 0 as a placeholder value.

## Running the Application

```python
if __name__ == '__main__':
    app.run(debug=True)
```

- This block of code is the entry point for running the Flask application.
- It runs the application in debug mode if the script is executed directly and not imported as a module.