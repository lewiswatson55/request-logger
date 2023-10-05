from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/log', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        save_request(request.data, subdirectory='request_logs')
        return "Logged request data successfully"
    else:
        return "Hello, World!", 200


# Path for specific logging i.e log/<log_name> will save the request data to a file with the name <log_name>
@app.route('/log/<log_name>', methods=['GET', 'POST'])
def log(log_name):
    if request.method == 'POST':
        save_request(request.data, subdirectory=str(log_name))
        return "Logged request data successfully into {}".format(log_name)
    else:
        #save_request(request.data, subdirectory=str(log_name)) # testinf get requests
        return "womp womp, not a post request.", 418


# Render dummy form for testing
@app.route('/dummy', methods=['GET', 'POST'])
def dummy():
    if request.method == 'POST':
        # dump
        save_request(request.data, subdirectory='dummy')
        return "ko", 200 # redirect to complete page
    else:
        return render_template('dummy.html')

# Completion page after dummy form submission
@app.route('/complete')
def complete():
    return render_template('complete.html')

# Function to save incoming request data to a file for logs
def save_request(request_data, subdirectory='request_logs'):
    print("Received request data:", request_data)

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


if __name__ == '__main__':
    app.run(debug=True)

