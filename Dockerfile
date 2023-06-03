#      _                  _ _       _     _              _
#   __| | __ _  ___      | (_) __ _| |__ | |_      _   _(_)
#  / _` |/ _` |/ _ \_____| | |/ _` | '_ \| __|____| | | | |
# | (_| | (_| |  __/_____| | | (_| | | | | ||_____| |_| | |
#  \__,_|\__,_|\___|     |_|_|\__, |_| |_|\__|     \__,_|_|
#                             |___/
#
#  https://github.com/daeuniverse/dae-light-ui
#
#  Copyright (C) 2023 @daeuniverse
#
#  This is a self-hosted software, liscensed under the MIT License.
#  See /License for more information.

# === Build Stage === #
FROM python:3.10-bullseye as builder

WORKDIR /app

ADD requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ ./
RUN pyinstaller app.py

# === Prod Stage === #

FROM ubuntu:latest as prod

RUN apt update -y && \
  apt-get install -y --no-install-recommends \
  ca-certificates libcap-dev

RUN apt-get clean autoclean && \
  apt-get autoremove -y && \
  rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

COPY src/templates/ ./templates/
COPY src/static/ ./static/
COPY --from=builder /app/dist/app/ ./

RUN chmod +x ./app

CMD ["./app"]
