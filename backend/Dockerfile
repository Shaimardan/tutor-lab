FROM nikolaik/python-nodejs:python3.12-nodejs20

COPY ./requirements.txt /backend/requirements.txt

RUN python -m pip install --extra-index-url https://pipupload:packages2018@pypi.polykod.com -r /backend/requirements.txt

COPY ./ /backend
