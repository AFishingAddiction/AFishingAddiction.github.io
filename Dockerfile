FROM jekyll/jekyll:pages

WORKDIR /srv/jekyll
COPY Gemfile* /srv/jekyll
RUN bundle install
VOLUME [ "/srv/jekyll" ]

COPY . /srv/jekyll
CMD bundle exec jekyll serve --host 0.0.0.0 --watch --force_polling --incremental --drafts --unpublished --future --verbose --trace --strict_front_matter -d /tmp/_site