FROM amazon/aws-lambda-python:3.9
# optional: ensure that pip is up to date
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#COPY app.py ./

#FROM base as debug
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#RUN apt-get update; apt-get install -y curl

RUN pip install debugpy

# Set the working directory in the container
WORKDIR /handler

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY env.env ${LAMBDA_TASK_ROOT}
COPY handler.py ${LAMBDA_TASK_ROOT}

# You can overwrite command in `serverless.yml` template
CMD ["handler.handler"]
