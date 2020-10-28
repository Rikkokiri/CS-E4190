#############################################################
#                                                           #
#   [X] Use python:3.8.5-alpine3.12 as the base image       #
#   [X] Set the working directory to /usr/app               #
#   [X] Copy the requirements.txt files in the route ./     #
#   [X] Install the dependencies (using pip install)        #
#   [X] Copy the app source code                            #
#   [X] Expose the port 5000                                # 
#   [X] Set the command to run flask run --host=0.0.0.0     #
#                                                           #
#############################################################

FROM python:3.8.5-alpine3.12
WORKDIR /usr/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Copy the current directory . in the project to the workdir . in the image.
COPY . .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]