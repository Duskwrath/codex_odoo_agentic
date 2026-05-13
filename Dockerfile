FROM odoo:19.0
USER root

COPY ./addons /mnt/extra-addons
WORKDIR /opt/odoo

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*


# Install Python requirements
COPY ./requirements.txt /opt/odoo/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/odoo/requirements.txt --break-system-packages

USER odoo