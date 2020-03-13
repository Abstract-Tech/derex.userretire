# syntax = docker/dockerfile:experimental
FROM python:3.6-alpine3.11 as sourceonly
# Version from Mar 2 2020
ARG TUBULAR_VERSION=aee0605aa25a7b39f70b661221ef0472d3757161
ARG TUBULAR_GITHUB_REPOSITORY=https://github.com/edx/tubular
ENV TUBULAR_URL=${TUBULAR_GITHUB_REPOSITORY}/tarball/${TUBULAR_VERSION}

# RUN --mount=type=cache,target=/var/cache/apk apk add git
# RUN git clone ${TUBULAR_GITHUB_REPOSITORY}.git --branch ${TUBULAR_VERSION} --depth 1 /tubular
RUN mkdir /tubular && \
    cd /tubular && \
    wget ${TUBULAR_URL} -O - |tar xzf - --strip-components 1

FROM sourceonly as wheels

RUN --mount=type=cache,target=/var/cache/apk apk add \
    alpine-sdk \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    python-dev

RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --wheel-dir=/wheelhouse -r /tubular/requirements.txt

FROM sourceonly

COPY retire_users.sh /usr/local/bin/

RUN --mount=type=cache,target=/root/.cache/pip --mount=type=bind,source=/wheelhouse,from=wheels,target=/wheelhouse \
    pip install --find-links /wheelhouse -r /tubular/requirements.txt && \
    ln -s /usr/local/bin/retire_users.sh /etc/periodic/hourly/retire_users
