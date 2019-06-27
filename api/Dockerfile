from python

RUN groupadd apigroup && useradd -m -g apigroup -s /bin/bash api
RUN echo "api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /home/api
WORKDIR /home/api
COPY requirements.txt /home/api
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R api:apigroup /home/api
USER api

ENTRYPOINT ["/usr/local/bin/gunicorn", "--bind", ":8001", "api:__hug_wsgi__", "--reload"]