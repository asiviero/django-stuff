# Django Stuff, with TDD

Hi! In this repo I intend to keep track of my learning of Django using
TDD as an approach for development. It will consistly mostly of doing
usual Django tutorials but forcing myself to use TDD as much as
possible. As I'm still a novice in both of those subjects, I greatly
appreciate criticism if you can share your own experience.

I will use a branch for each tutorial/test, and link them all here in
an index so it's easy to find them.

# The tutorials

1. `poll` - This is Django's [first tutorial](https://docs.djangoproject.com/en/1.8/intro/tutorial03/), which aims to create a polling website with an admin interface so the admin can enter new polls. Still haven't done the last parts that deal with optimization but rough main functionality there and covered by tests.
1. `social` - Although I'm not exactly following any tutorial for this one, my aim is to create a micro social network in which users will be able to add themselves and join groups and eventually grow that to a gaming network, starting with single player games and at last multiplayer with websockets.

  - [x] Users creation, friend request and group joining
  - [ ] Some front-end and UI creation
  - [ ] Annotators to prevent weird situations
  - [ ] Layouting a little bit
  - [ ] Code a singleplayer game (Word search maybe?)
  - [ ] Stats tracking for games
  - [ ] Simple chat system running on websockets
  - [ ] More complex messages via websockets
  - [ ] Simple multiplayer game (tic-tac-toe would be a good fit)
  - [ ] Intermediate multiplayer game (checkers would be fine, I guess)
  - [ ] Some board game emulation (e.g. Risk/War)
  - [ ] Who knows?

# Running the tests

All tests are run from `manage.py`. As the [Testing Goat](http://www.obeythetestinggoat.com) commands us, I
have divided the tests in functional and unit tests, although I might
get a little confused in the early steps.

Functional tests are on a directory which is in the same level as the
main app, which effectively makes Django acts as if it were a different app. So in order to run *functional tests*, run:

```
  $ python3 manage.py test functional_tests
```

Similarly, unit tests are run like this:
```
  $ python3 manage.py test [app]
```

To run them all at once, just omit the last parameter:
```
  $ python3 manage.py test
```
# Requirements

  * [Python 3](https://www.python.org/downloads/)
  * [Django](https://www.djangoproject.com/download/) (I'm currently using v1.8 but I guess earlier versions will be fine)
  * Selenium

Notice: It's advisable to always use the latest version from Selenium, and install it via `pip`. As quoted in [Test-Driven Development with Python](http://chimera.labs.oreilly.com/books/1234000000754/pr02.html#_required_python_packages):

> Make sure you have the absolute latest version [of Selenium]
> installed. Selenium is engaged in a permanent arms race with the
> major browsers, trying to keep up with the latest features. If you
> ever find Selenium misbehaving for some reason, the answer is often
> that it’s a new version of Firefox and you need to upgrade to the
> latest Selenium …


# Contributing

Help me! Know any interesting Django tutorials and challenges? I'd
be eager to know! Open issues as you will with them and I'll do my
best to answer in the minimun possible time.

# License

Do we really need to? Well, code in this repo is mostly aimed at
learning purposes, as such I believe [MIT](http://opensource.org/licenses/MIT) license will be the best
choice.
