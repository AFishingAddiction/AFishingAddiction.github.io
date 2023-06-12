FROM jekyll/jekyll:pages

RUN apk add \
    gcc \
    make \
    musl-dev

COPY Gemfile* /srv/jekyll
RUN bundle install
VOLUME [ "/srv/jekyll" ]

COPY . /srv/jekyll
CMD jekyll serve \
  --host 0.0.0.0 \
  --destination ./_site \
  --strict_front_matter \
  --watch \
  --force_polling \
  --incremental \
  --drafts \
  --unpublished \
  --future \
  --verbose \
  --trace