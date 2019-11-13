FROM phusion/baseimage:0.11

ENV DEBIAN_FRONTEND noninteractive
ENV LIBEV_FLAGS=4

RUN apt-get upgrade -y
RUN apt-get update --fix-missing
RUN apt-get install python3.7 -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN apt-get install libssl1.0.0 --force-yes -y

## postgres dev symbols

RUN apt-get install -y libpq-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev

RUN apt-get install -y nginx

RUN apt-get install python3-setuptools -y
RUN apt-get -y install python3-pip
RUN pip3 install --upgrade pip

RUN apt-get install -y build-essential freeglut3 freeglut3-dev binutils-gold
RUN apt-get install -y "^libxcb.*" libx11-xcb-dev libglu1-mesa-dev libxrender-dev
RUN apt-get install -y libglfw3-dev libgles2-mesa-dev

# custom

RUN apt-get update --fix-missing
RUN apt-get install -y sqlite3
RUN apt-get install -y libgl1-mesa-dev

ADD requirements.txt /src/project/requirements.txt
RUN cd /src/project; pip3 install -r requirements.txt --upgrade

RUN apt-get update --fix-missing

ADD . /src/project

RUN chmod -R +x /src/project/deploy/services/
RUN chmod -R +x /src/project/deploy/init/
RUN cp -R /src/project/deploy/services/* /etc/service/
RUN cp -R /src/project/deploy/init/* /etc/my_init.d/

RUN mkdir /var/www/static/
RUN mkdir /var/www/spooler/
RUN chown -R www-data /var/www

RUN cp /src/project/deploy/nginx.conf /etc/nginx/

RUN rm /etc/nginx/sites-enabled/default

RUN ln -s /src/project/deploy/django.conf /etc/nginx/sites-enabled/django.conf

EXPOSE 80

CMD ["/sbin/my_init"]
